import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

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
        self.label.setStyleSheet("QLabel { background-color: #444444; border: 1px solid gray; padding: 10px; color: white; }")  # set the label's background color to light gray and its text color to white

        # Create a layout to hold the label
        layout = QVBoxLayout()
        layout.addWidget(self.label)

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

        # Convert the PNG file to an ICO file using the command line tool "magick"
        output_path = os.path.join(os.path.dirname(file_path), os.path.splitext(os.path.basename(file_path))[0] + ".ico")
        os.system("magick convert {} {}".format(file_path, output_path))

        # Update the label to show the conversion was successful
        pixmap = QPixmap(output_path)
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.width(), pixmap.height())
        self.label.setText("PNG file converted to ICO file:\n{}".format(output_path))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
