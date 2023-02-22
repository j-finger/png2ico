import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget, QProgressBar
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class ConverterThread(QThread):
    progress_update = pyqtSignal(int)
    finished_conversion = pyqtSignal(str)

    def __init__(self, file_path, output_path):
        super().__init__()
        self.file_path = file_path
        self.output_path = output_path

    def run(self):
        # Convert the PNG file to an ICO file using the command line tool "magick"
        os.system("magick convert {} {}".format(self.file_path, self.output_path))

        # Signal the completion of the conversion process
        self.finished_conversion.emit(self.output_path)

    def update_progress(self, value):
        self.progress_update.emit(value)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("PNG to ICO Converter")
        self.setAcceptDrops(True)
        self.setStyleSheet("QMainWindow { background-color: #333333; }")  # set the background color to dark gray

        # Create a label to display the dropped file names
        self.label = QLabel("Drag and drop a PNG file here")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("QLabel { background-color: #444444; border: 1px solid gray; padding: 10px; color: "
                                 "white; }")  # set the label's background color to light gray and its text color to
        # white

        # Create a progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("QProgressBar { background-color: #444444; border: 1px solid gray; padding: 1px; }"
                                         "QProgressBar::chunk { background-color: #77aaff; }")

        # Create a layout to hold the label and progress bar
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)

        # Set the layout as the central widget of the main window
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def dragEnterEvent(self, event):
        # Accept the drag event if a file is being dragged
        if event.mimeData().hasUrls() and event.mimeData().urls()[0].toString().endswith(".png"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # Get the file path of the dropped file
        file_path = event.mimeData().urls()[0].toLocalFile()

        # Create the output path
        output_path = os.path.join(os.path.dirname(file_path), os.path.splitext(os.path.basename(file_path))[0] + ".ico")

        # Create a converter thread to convert the file
        converter_thread = ConverterThread(file_path, output_path)
        converter_thread.finished_conversion.connect(self.conversion_finished)
        converter_thread.progress_update.connect(self.update_progress_bar)
        converter_thread.start()

        # Update the label to show that the conversion is in progress
        self.label.setText("Converting PNG file to ICO file...\n\nThis may take some time.")

    def conversion_finished(self, output_path):
        # Update the label to show the conversion was successful
        pixmap = QPixmap(output_path)
        self.label
