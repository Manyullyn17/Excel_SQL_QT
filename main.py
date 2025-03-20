import sys
import os.path
import subprocess
import time
import sqlite3

import PyQt6
from PyQt6 import QtGui
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, QSize, QSettings, QCoreApplication, QAbstractTableModel, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QPushButton, QDialog
from PyQt6.uic.Compiler.qtproxies import QtWidgets
import pandas as pd
import openpyxl
from openpyxl.worksheet.table import Table, TableStyleInfo

from GUI import Ui_MainWindow
from settings import Ui_SettingsWindow

class OutputTableModel(QAbstractTableModel):
    def __init__(self, data: pd.DataFrame):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            return str(self._data.columns[section]) # Column headers
        elif orientation == Qt.Orientation.Vertical:
            return str(self._data.index[section]+1) # Row headers

        return None

    def sort(self, column: int, order: Qt.SortOrder=Qt.SortOrder.AscendingOrder):
        """
        Sort the data in the model by a given column and order.
        This method is triggered when the user clicks on the column header.
        """
        # Sort the DataFrame based on the column
        self.beginResetModel()  # Tell the model that it will be reset
        self._data = self._data.sort_values(self._data.columns[column], ascending=(order != Qt.SortOrder.AscendingOrder))
        self.endResetModel()  # Notify the model that the reset is complete

class SettingsWindow(QDialog, Ui_SettingsWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle('Settings')
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(icon_path)))
        self.infoLabel.setText(QCoreApplication.translate("SettingsWindow",
                                                          f"""<html><head/><body><p><span style=\" font-weight:700;\">SQL Query Tool for Excel</span></p>
                                                          <p>Version: 2.0.0</p><p>Developed by Manyullyn17<br/></p>
                                                          <p>A lightweight tool for running SQL queries on Excel files.<br/></p>
                                                          <p><a href=\"https://github.com/Manyullyn17/Excel_SQL_GUI\">
                                                          <span style=\" text-decoration: underline; color:#007af4;\">GitHub Repository</span></a><br/></p>
                                                          <p><span style=\" font-style:italic;\">Powered by Python, PyQt6, Pandas, openpyxl, and SQLite.</span></p><br/>
                                                          <img src="{icon_png_path}" width="160"></body></html>"""))

        # Load settings
        self.settings = QSettings('Manyullyn17', 'Excel_SQL')

        # Settings
        self.experimentalFeaturesCheckBox.setChecked(self.settings.value('experimentalFeatures', False, type=bool))
        self.showOutputTableCheckBox.setChecked(self.settings.value('showOutputTable', False, type=bool))
        self.hideSuccessCheckBox.setChecked(self.settings.value('hideSuccess', False, type=bool))

        self.applyButton.clicked.connect(self.apply_settings)

    def apply_settings(self):
        self.settings.setValue('experimentalFeatures', self.experimentalFeaturesCheckBox.isChecked())
        self.settings.setValue('showOutputTable', self.showOutputTableCheckBox.isChecked())
        self.settings.setValue('hideSuccess', self.hideSuccessCheckBox.isChecked())
        self.accept()

class LoadFileThread(QThread):
    """Loads the file in a separate thread to avoid freezing the UI"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, input_file):
        super().__init__()
        self.input_file = input_file

    def run(self):
        try:
            xls = pd.ExcelFile(self.input_file)
            loaded_data = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}
            self.finished.emit(loaded_data)
        except Exception as e:
            self.error.emit(str(e))

class ExecuteQueryThread(QThread):
    """Executes the SQL Query in a background thread to keep UI responsive"""
    finished = pyqtSignal(pd.DataFrame)
    error = pyqtSignal(str)
    cancel = pyqtSignal()
    update_timer = pyqtSignal(str, int)

    def __init__(self, loaded_data, query, output_file):
        super().__init__()
        self.loaded_data = loaded_data
        self.query = query
        self.output_file = output_file
        self.stop = False
        self.start_time = time.time()

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer_func)

    def run(self):
        try:
            conn = sqlite3.connect(":memory:")

            # Load all sheets into SQLite
            for sheet, df in self.loaded_data.items():
                if self.stop:
                    self.cancel_query()
                    return
                df.to_sql(sheet, conn, if_exists="replace", index=False)

            if self.stop:
                self.cancel_query()
                return

            # Execute the query
            result_df = pd.read_sql_query(self.query, conn)

            result_df.to_excel(self.output_file, index=False, sheet_name="SQLResults")

            if self.stop:
                self.cancel_query()
                return

            # Open and adjust the workbook
            wb = openpyxl.load_workbook(self.output_file)
            ws = wb["SQLResults"]
            table_ref = f"A1:{chr(64 + len(result_df.columns))}{len(result_df) + 1}"
            table = Table(displayName="SQLTable", ref=table_ref)
            style = TableStyleInfo(name="TableStyleMedium2", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=False)
            table.tableStyleInfo = style
            ws.add_table(table)

            # Adjust column widths
            for column in ws.columns:
                if self.stop:
                    wb.save(self.output_file) # save before stopping
                    self.cancel_query()
                    return
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except (AttributeError, TypeError):
                        pass
                ws.column_dimensions[column_letter].width = max_length + 2

            wb.save(self.output_file)
            wb.close()

            elapsed_time = time.time() - self.start_time
            self.update_timer.emit(f"Done! Took: {int(elapsed_time)}s", int(elapsed_time))
            self.timer.stop()
            self.finished.emit(result_df)

        except Exception as e:
            self.timer.stop()
            self.error.emit(str(e))

    def update_timer_func(self):
        """Updates the timer every second"""
        elapsed_time = time.time() - self.start_time
        self.update_timer.emit(f"Running: {int(elapsed_time)}s", int(elapsed_time))

    def cancel_query(self):
        """Handles cancelling the query"""
        self.cancel.emit()
        elapsed_time = time.time() - self.start_time
        self.update_timer.emit(f"Query cancelled after: {int(elapsed_time)}s", int(elapsed_time))
        self.timer.stop()

    def stop_query(self):
        """Set flag to stop the thread"""
        self.stop = True

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Excel SQL Query Tool')
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(icon_path)))

        # Load Settings
        self.settings = QSettings('Manyullyn17', 'Excel_SQL')

        # Variables
        self.input_file = None
        self.output_file = None
        self.xls = None
        self.loaded_data = None
        self.skip_load_dialog = False
        self.done_loading = False
        self.elapsed = 0
        self.load_thread = None
        self.query_thread = None
        self.tableVisible = False
        self.fullscreen = False
        self.oldHeight = None
        self.table_model = OutputTableModel(pd.DataFrame())

        # Settings
        self.enableExperimentalFeatures = False
        self.hideSuccess = False
        self.showOutputTable = False

        self.update_settings()

        self.success_msg_box = None
        self.cancel_msg_box = None

        # Set Widget Visibility
        self.outputTable.setVisible(False)
        self.fullscreenTableButton.setVisible(False)

        self.outputTable.setModel(self.table_model)

        self.inputButton.clicked.connect(self.load_file)
        self.outputButton.clicked.connect(self.save_file)
        self.loadQueryButton.clicked.connect(self.load_sql_query)
        self.saveQueryButton.clicked.connect(self.save_sql_query)
        self.executeButton.clicked.connect(self.execute_query)
        self.cancelButton.clicked.connect(self.cancel_query)
        self.sheetList.clicked.connect(self.on_sheet_select)
        self.inputInput.returnPressed.connect(self.load_file_quiet)
        self.showTableButton.clicked.connect(self.toggle_output_table)
        self.fullscreenTableButton.clicked.connect(self.table_fullscreen)
        self.actionSettings.triggered.connect(self.open_settings)

    def open_settings(self):
        """Opens settings window"""
        settings_window = SettingsWindow()
        settings_window.exec()

        self.update_settings()

    def update_settings(self):
        """Loads settings and updates variables"""
        self.enableExperimentalFeatures = self.settings.value('experimentalFeatures', type=bool)
        self.hideSuccess = self.settings.value('hideSuccess', type=bool)
        self.showOutputTable = self.settings.value('showOutputTable', type=bool)

        if self.tableVisible is True:
            self.fullscreenTableButton.setVisible(self.enableExperimentalFeatures)
        else:
            self.fullscreenTableButton.setVisible(False)

    def hide_widgets(self, layout):
        """Hides all widgets except output table"""
        for i in range(layout.count()):
            item = layout.itemAt(i)

            if item is None:
                continue

            widget = item.widget()
            if widget:
                if not isinstance(widget, (PyQt6.QtWidgets.QToolButton, PyQt6.QtWidgets.QTableWidget)):
                    widget.setVisible(False)

            # Handle nested layouts
            elif item.layout():
                self.hide_widgets(item.layout())  # Recursively check sub-layouts

    def show_widgets(self, layout):
        """Shows all widgets except output table"""
        for i in range(layout.count()):
            item = layout.itemAt(i)

            if item is None:
                continue

            widget = item.widget()
            if widget:
                if not isinstance(widget, (PyQt6.QtWidgets.QToolButton, PyQt6.QtWidgets.QTableWidget)):
                    widget.setVisible(True)

            # Handle nested layouts
            elif item.layout():
                self.show_widgets(item.layout())  # Recursively check sub-layouts

    def toggle_output_table(self):
        """Toggles the visibility of the output table"""
        if not self.tableVisible:
            self.outputTable.setVisible(True)
            self.showTableButton.setText(' ^ ')
            self.fullscreenTableButton.setVisible(self.enableExperimentalFeatures)
            self.resize(QSize(self.width(), self.height() + 180))
            self.tableVisible = True
        else:
            self.outputTable.setVisible(False)
            self.showTableButton.setText(' v ')
            self.fullscreenTableButton.setVisible(False)
            self.resize(QSize(self.width(), self.height() - 180))
            self.tableVisible = False

    def table_fullscreen(self): # not quite working atm
        """Shows output table in fullscreen mode"""
        if not self.fullscreen:
            self.oldHeight = self.outputTable.height()
            self.fullscreen = True
            self.showTableButton.setVisible(False)
            self.fullscreenTableButton.setText(' Exit ')
            self.hide_widgets(self.verticalLayout)
            self.sheetList.setVisible(False)
            self.columnList.setVisible(False)
            self.outputTable.setMinimumSize(self.width(), self.height() - 100)
        else:
            self.fullscreen = False
            self.showTableButton.setVisible(True)
            self.fullscreenTableButton.setText(' Fullscreen ')
            self.show_widgets(self.verticalLayout)
            self.sheetList.setVisible(True)
            self.columnList.setVisible(True)
            self.outputTable.setMinimumSize(self.width(), self.oldHeight)

    def load_file(self):
        """Start file loading in a separate thread to prevent UI freeze"""
        if not self.skip_load_dialog:
            file, _ = QFileDialog.getOpenFileName(self, "Select Input Excel File", "", "Excel Files (*.xlsx;*.xls)")
        else:
            file = self.inputInput.text()

        self.skip_load_dialog = False

        if file:
            # Show "Loading sheets..." before starting the process
            self.sheetList.clear()
            self.sheetList.addItem("Loading sheets...")

            self.input_file = file
            self.inputInput.clear()
            self.inputInput.setText(self.input_file)

            if not self.output_file:
                input_dir = os.path.dirname(self.input_file)
                input_name = os.path.splitext(os.path.basename(self.input_file))[0]
                self.output_file = os.path.join(input_dir, f"{input_name}_output.xlsx")
                self.outputIInput.clear()
                self.outputIInput.setText(self.output_file)

            try:
                self.xls = pd.ExcelFile(self.input_file)
                sheet_names = self.xls.sheet_names

                # Show the sheet count **immediately**
                self.sheetNumLabel.setText(f"Sheets: {len(sheet_names)}")

                self.load_thread = LoadFileThread(self.input_file)
                self.load_thread.finished.connect(self.on_file_loaded)
                self.load_thread.error.connect(self.on_file_load_error)
                self.load_thread.start()

            except Exception as e:
                QMessageBox.critical(self,"Error", f"Failed to load file: {e}")
                self.sheetList.clear()
                self.sheetList.addItem(f"Failed to load file")

    def load_file_quiet(self):
        """Loads a file without showing a dialog window"""
        self.skip_load_dialog = True
        self.load_file()

    def on_file_loaded(self, loaded_data):
        """Populates sheetlist when file loading is finished"""
        self.loaded_data = loaded_data
        self.sheetList.clear()
        for sheet in self.xls.sheet_names:
            self.sheetList.addItem(sheet)
        self.columnList.addItem("Select sheet to see columns")
        self.done_loading = True

    def on_file_load_error(self, e):
        """Shows error when file loading encounteres an error"""
        QMessageBox.critical(self, "Error", f"Failed to load file: {e}")
        self.sheetList.clear()
        self.sheetList.addItem(f"Failed to load file")
        self.done_loading = True

    def on_sheet_select(self):
        """Handle sheet selection and display columns in the second listbox"""
        if self.done_loading:
            try:
                selected_sheet = self.xls.sheet_names[self.sheetList.currentIndex().row()]  # Get selected sheet name

                # Clear the columns listbox first
                self.columnList.clear()

                # Fetch columns of the selected sheet
                if selected_sheet in self.loaded_data:
                    columns = self.loaded_data[selected_sheet].columns
                    for column in columns:
                        self.columnList.addItem(column)  # Insert each column into the column listbox
            except (IndexError, KeyError, AttributeError):
                return

    def save_file(self):
        """Opens a dialog to select an output Excel file"""
        self.output_file, _ = QFileDialog.getSaveFileName(self, "Select Output Excel File", "", "Excel Files (*.xlsx)")
        if self.output_file:
            self.outputIInput.clear()
            self.outputIInput.setText(self.output_file)

    def load_sql_query(self):
        """Load an SQL query from a file into the text widget"""
        query_file, _ = QFileDialog.getOpenFileName(self, "Select Query File", "", "Text Files (*.txt)")
        if query_file:
            with open(query_file, 'r') as file:
                self.queryInput.clear()
                self.queryInput.setPlainText(file.read())

    def save_sql_query(self):
        """Save the current query to a file"""
        query_text = self.queryInput.toPlainText()  # Get the text from the query box
        if not query_text:
            QMessageBox.critical(self, "No Query", "Please write a query before saving.")
            return

        # Open a file dialog to choose the save location
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Query as", "", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(query_text)  # Save the query to the file
                QMessageBox.information(self, "Saved", f"Query saved successfully to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save query: {e}")

    def execute_query(self):
        """Execute the SQL query on the selected input file and save the result to the output file"""
        self.output_file = self.outputIInput.text()

        if not self.input_file or not self.output_file or not self.queryInput.toPlainText():
            QMessageBox.critical(self, "Error", "Please fill in all fields.")
            return

        if not self.done_loading:
            QMessageBox.critical(self, "Error", "Please wait for data to load.")
            return

        self.statusbar.showMessage("Running: 0s")  # Reset timer display

        self.query_thread = ExecuteQueryThread(self.loaded_data, self.queryInput.toPlainText(), self.output_file)
        self.query_thread.finished.connect(self.query_finished)
        self.query_thread.error.connect(self.query_error)
        self.query_thread.cancel.connect(self.query_cancelled)
        self.query_thread.update_timer.connect(self.update_timer)
        self.query_thread.start()

    def update_timer(self, msg, elapsed):
        """Updates the timer in the statusbar"""
        self.statusbar.showMessage(msg)
        self.elapsed = elapsed

    def query_finished(self, result_df):
        """Populates output table after query is finished and shows success message"""
        # self.outputTable.blockSignals(True)  # Prevent UI from processing signals during update
        # self.outputTable.setUpdatesEnabled(False)  # Stop rendering updates temporarily
        #
        # # Ready Table
        # rows, cols = result_df.shape
        # self.outputTable.setRowCount(rows)
        # self.outputTable.setColumnCount(cols)
        # self.outputTable.clear()
        # self.outputTable.setHorizontalHeaderLabels(result_df.columns)
        #
        # for row in range(rows):
        #     for col in range(cols):
        #         value = str(result_df.iat[row, col])
        #         self.outputTable.setItem(row, col, QTableWidgetItem(value))
        #
        # self.outputTable.setUpdatesEnabled(True)  # Re-enable updates
        # self.outputTable.blockSignals(False)  # Allow UI to process updates
        # self.outputTable.viewport().update()  # Force a repaint

        self.table_model.beginResetModel() # Notify the view that a big update is happening
        self.table_model._data = result_df # Refresh the view
        self.table_model.endResetModel() # Refresh the view

        if not self.hideSuccess:
            self.show_success_dialog()
        elif self.showOutputTable and not self.tableVisible:
            self.toggle_output_table()

    def query_error(self, e):
        """Displays an error message if the query fails"""
        QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def cancel_query(self):
        """Cancels the Query"""
        try:
            self.query_thread.stop_query()
        except AttributeError:
            return

    def query_cancelled(self):
        """Displays message that query has been cancelled"""
        self.query_thread.quit()
        QMessageBox.information(self, "Query cancelled", "Query has been cancelled.")

    def show_success_dialog(self):
        """Shows a success dialog with a button to open the output file"""
        self.success_msg_box = QMessageBox(self)
        self.success_msg_box.setWindowTitle("Execution Complete")
        self.success_msg_box.setText(f"Query executed successfully!\nTook {self.elapsed} seconds")
        self.success_msg_box.setIcon(QMessageBox.Icon.Information)

        # Add custom buttons
        open_button = QPushButton("Open Output File")
        close_button = QPushButton("Close")

        open_button.clicked.connect(self.open_output_file)
        close_button.clicked.connect(self.success_msg_box.close)

        self.success_msg_box.addButton(open_button, QMessageBox.ButtonRole.AcceptRole)
        self.success_msg_box.addButton(close_button, QMessageBox.ButtonRole.RejectRole)

        self.success_msg_box.exec()

        if self.showOutputTable and not self.tableVisible:
            self.toggle_output_table()

    def show_cancel_dialog(self):
        """Shows a cancel dialog with a button to retry the query"""
        self.cancel_msg_box = QMessageBox(self)
        self.cancel_msg_box.setWindowTitle("Execution Cancelled")
        self.cancel_msg_box.setText(f"Query cancelled!")
        self.cancel_msg_box.setIcon(QMessageBox.Icon.Information)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.cancel_msg_box.close)
        self.cancel_msg_box.addButton(close_button, QMessageBox.ButtonRole.RejectRole)

        self.cancel_msg_box.exec()

    def open_output_file(self):
        """Opens the output file with the default program"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(self.output_file)
            elif os.name == 'posix':  # Mac/Linux
                subprocess.run(['open', self.output_file])
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Could not open the file: {e}")
        self.success_msg_box.close()

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        # Running as a bundled PyInstaller executable
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    else:
        # Running as a normal Python script
        base_path = os.path.dirname(os.path.abspath(__file__))

    icon_path = os.path.join(base_path, "Excel_SQL_Icon.ico")
    icon_png_path = os.path.join(base_path, "Excel_SQL_Icon.png")

    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(icon_path)))
    window = MainWindow()
    window.show()  # Show the window
    sys.exit(app.exec())
