import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox

# Default input and output paths
image_path = r"C:\Users\aisha\OneDrive\Pictures\Saved_Pictures\Allah.jpg"
output_path = r"C:\Users\aisha\OneDrive\Desktop\Stenography-main\encryptedImage.png"

class EncryptGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Encryption")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Enter secret message:")
        layout.addWidget(self.label)

        self.message_input = QLineEdit(self)
        layout.addWidget(self.message_input)

        self.label2 = QLabel("Enter passcode:")
        layout.addWidget(self.label2)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.encrypt_button = QPushButton("Encrypt Image", self)
        self.encrypt_button.clicked.connect(self.encrypt_image)
        layout.addWidget(self.encrypt_button)

        self.setLayout(layout)

    def encrypt_image(self):
        message = self.message_input.text()
        password = self.password_input.text()
        if not message or not password:
            QMessageBox.warning(self, "Error", "Message and password cannot be empty!")
            return
        img = cv2.imread(image_path)
        if img is None:
            QMessageBox.warning(self, "Error", "Image not found or cannot be read.")
            return

        n, m, z = 0, 0, 0

        # Store password and message length in the image
        img[n, m, z] = np.uint8(len(password))
        img[n + 1, m + 1, (z + 1) % 3] = np.uint8(len(message))
        n += 2
        m += 2
        z = (z + 2) % 3
        # Encrypt password and message into the image
        for char in password + message:
            img[n, m, z] = np.uint8(ord(char))
            n += 1
            m += 1
            z = (z + 1) % 3

        cv2.imwrite(output_path, img)  # Save as PNG to avoid compression
        QMessageBox.information(self, "Success", f"Message encrypted successfully!\nSaved at: {output_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EncryptGUI()
    window.show()
    sys.exit(app.exec())