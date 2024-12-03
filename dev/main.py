import os
from PySide6.QtCore import QFile, QIODevice, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene
from PySide6.QtGui import QPixmap, QGuiApplication
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
import cv2

from utils import crop_text_bands5, crop_text_bands3, mock_process_image, save_image, detect_and_deskew_object


class ImageUpscalerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the .ui file
        ui_file_name = "main_window.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            return

        # Load the UI dynamically
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        if not self.ui:
            print(f"Error loading UI: {loader.errorString()}")
            return

        # Set the loaded UI as the central widget
        self.setCentralWidget(self.ui)

        # Dynamically resize based on screen size
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Set window size to 70% of screen size
        self.resize(int(screen_width * 0.7), int(screen_height * 0.7))

        # Apply the stylesheet
        stylesheet = """
        QMainWindow {
            background-color: #1e1e1e;
            color: #dcdcdc;
            font-family: "Roboto", Arial, sans-serif;
            font-size: 12pt;
        }
        QPushButton {
            background-color: #2b2b2b;
            color: #f0f0f0;
            border: 1px solid #4CAF50;
            padding: 8px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #3e3e3e;
            border-color: #45a049;
        }
        QComboBox {
            background-color: #2b2b2b;
            color: #f0f0f0;
            border: 1px solid #4CAF50;
            padding: 5px;
            border-radius: 3px;
        }
        QGraphicsView {
            border: 2px solid #3e3e3e;
            background-color: #292929;
        }
        QLabel {
            color: #dcdcdc;
            font-weight: bold;
        }
        """
        self.setStyleSheet(stylesheet)

        # Initialize attributes
        self.directory = None
        self.image_files = []
        self.current_index = 0
        self.upscaled_dir = "../upscaled_images"

        # Ensure the upscaled directory exists
        if not os.path.exists(self.upscaled_dir):
            os.makedirs(self.upscaled_dir)

        # Populate processing method dropdown
        self.ui.processingMethodComboBox.addItems([
            "Mock Process",
            "Real-ESRGAN Upscaling",
            "Crop Text Bands",
            "Crop Text Bands 3",
            "Detect and Deskew Object"
        ])

        # Connect UI elements
        self.ui.selectDirButton.clicked.connect(self.select_directory)
        self.ui.nextButton.clicked.connect(self.next_image)
        self.ui.prevButton.clicked.connect(self.prev_image)

        # Disable navigation buttons initially
        self.ui.nextButton.setEnabled(False)
        self.ui.prevButton.setEnabled(False)

    def select_directory(self):
        """Allow the user to select a directory with images."""
        self.directory = QFileDialog.getExistingDirectory(self, "Select Image Directory")
        if self.directory:
            print(f"Selected directory: {self.directory}")
            self.image_files = [f for f in os.listdir(self.directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if self.image_files:
                self.current_index = 0
                self.process_images()
                self.update_images()
                self.ui.nextButton.setEnabled(len(self.image_files) > 1)
                self.ui.prevButton.setEnabled(False)
            else:
                self.ui.originalImageView.scene().clear()
                self.ui.upscaledImageView.scene().clear()

    def process_images(self):
        """Process images based on the selected method."""
        selected_method = self.ui.processingMethodComboBox.currentText()
        if selected_method == "Mock Process":
            for image_file in self.image_files:
                input_path = os.path.join(self.directory, image_file)
                output_path = os.path.join(self.upscaled_dir, image_file)
                mock_process_image(input_path, output_path)
        elif selected_method == "Real-ESRGAN Upscaling":
            self.esrgan_process_images()
        elif selected_method == "Crop Text Bands":
            for image_file in self.image_files:
                input_path = os.path.join(self.directory, image_file)
                output_path = os.path.join(self.upscaled_dir, image_file)
                image = cv2.imread(input_path)
                if image is not None:
                    cropped_image = crop_text_bands5(image)
                    save_image(output_path, cropped_image)
        elif selected_method == "Crop Text Bands 3":
            for image_file in self.image_files:
                input_path = os.path.join(self.directory, image_file)
                output_path = os.path.join(self.upscaled_dir, image_file)
                image = cv2.imread(input_path)
                if image is not None:
                    cropped_image = crop_text_bands3(image)
                    save_image(output_path, cropped_image)
        elif selected_method == "Detect and Deskew Object":
            for image_file in self.image_files:
                input_path = os.path.join(self.directory, image_file)
                output_path = os.path.join(self.upscaled_dir, image_file)
                image = cv2.imread(input_path)
                if image is not None:
                    deskewed_image = detect_and_deskew_object(image)
                    save_image(output_path, deskewed_image)
    def esrgan_process_images(self):
        """Perform Real-ESRGAN upscaling on all images."""
        model_path = "RealESRGAN_x4plus.pth"
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        upscaler = RealESRGANer(
            scale=4,
            model_path=model_path,
            model=model,
            tile=256,
            tile_pad=10,
            pre_pad=10,
            half=False
        )

        for image_file in self.image_files:
            input_path = os.path.join(self.directory, image_file)
            output_path = os.path.join(self.upscaled_dir, image_file)
            input_image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
            output_image, _ = upscaler.enhance(input_image)
            save_image(output_path, output_image)

    def update_images(self):
        """Update the display to show the current original and processed images."""
        if self.image_files:
            original_path = os.path.join(self.directory, self.image_files[self.current_index])
            upscaled_path = os.path.join(self.upscaled_dir, self.image_files[self.current_index])

            original_scene = QGraphicsScene()
            original_scene.addPixmap(QPixmap(original_path))
            self.ui.originalImageView.setScene(original_scene)
            self.ui.originalImageView.fitInView(original_scene.itemsBoundingRect(), Qt.KeepAspectRatio)

            upscaled_scene = QGraphicsScene()
            upscaled_scene.addPixmap(QPixmap(upscaled_path))
            self.ui.upscaledImageView.setScene(upscaled_scene)
            self.ui.upscaledImageView.fitInView(upscaled_scene.itemsBoundingRect(), Qt.KeepAspectRatio)

    def next_image(self):
        """Display the next image."""
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.update_images()
            self.ui.prevButton.setEnabled(True)
            if self.current_index == len(self.image_files) - 1:
                self.ui.nextButton.setEnabled(False)

    def prev_image(self):
        """Display the previous image."""
        if self.current_index > 0:
            self.current_index -= 1
            self.update_images()
            self.ui.nextButton.setEnabled(True)
            if self.current_index == 0:
                self.ui.prevButton.setEnabled(False)

    def resizeEvent(self, event):
        """Handle window resize events to dynamically adjust image sizes."""
        super().resizeEvent(event)
        if self.image_files:
            self.ui.originalImageView.fitInView(self.ui.originalImageView.scene().itemsBoundingRect(), Qt.KeepAspectRatio)
            self.ui.upscaledImageView.fitInView(self.ui.upscaledImageView.scene().itemsBoundingRect(), Qt.KeepAspectRatio)


if __name__ == "__main__":
    app = QApplication([])
    window = ImageUpscalerApp()
    window.show()
    app.exec()