import sys, os, requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QFileDialog,
    QVBoxLayout, QHBoxLayout, QProgressBar, QComboBox, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap, QPalette, QColor, QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from pytube import YouTube

class FearLinkDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.yt = None
        self.streams = []
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("FearLink YouTube Downloader 🎬")
        self.setGeometry(400, 150, 650, 550)
        self.setStyleSheet("""
            QWidget { background-color: #0A0F1E; color: #FFFFFF; font-family: 'Segoe UI'; }
            QLineEdit, QComboBox {
                background-color: #1B1B2F; border: 2px solid #00F7FF; border-radius: 6px;
                padding: 10px; color: #00F7FF; font-size: 14px;
            }
            QPushButton {
                background-color: #FF2E63; color: white; border: none; padding: 10px;
                font-weight: bold; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #FF4D7E;
                box-shadow: 0 0 10px #FF2E63;
            }
            QLabel { font-size: 14px; }
        """)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.title = QLabel("🎥 FearLink Downloader")
        self.title.setFont(QFont('Segoe UI', 20, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste YouTube video URL...")
        self.url_input.returnPressed.connect(self.auto_fetch)
        layout.addWidget(self.url_input)

        self.thumb_label = QLabel()
        self.thumb_label.setFixedSize(480, 270)
        self.thumb_label.setStyleSheet("border: 2px solid #00F7FF;")
        self.thumb_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.thumb_label)

        self.video_title = QLabel("")
        self.video_title.setWordWrap(True)
        self.video_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.video_title)

        self.res_dropdown = QComboBox()
        self.res_dropdown.setEnabled(False)
        layout.addWidget(self.res_dropdown)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #00F7FF;
                border-radius: 6px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #00F7FF;
                width: 20px;
            }
        """)
        layout.addWidget(self.progress)

        btn_layout = QHBoxLayout()
        self.fetch_btn = QPushButton("🔍 Fetch Info")
        self.fetch_btn.clicked.connect(self.auto_fetch)
        self.download_btn = QPushButton("⬇️ Download")
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.download_video)
        btn_layout.addWidget(self.fetch_btn)
        btn_layout.addWidget(self.download_btn)
        layout.addLayout(btn_layout)

        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status)

        self.fade_in()

    def fade_in(self):
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(1500)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.start()

    def auto_fetch(self):
        url = self.url_input.text().strip()
        if not url:
            self.toast("Paste a valid YouTube URL!", error=True)
            return
        try:
            self.status.setText("⏳ Getting video info...")
            self.yt = YouTube(url, on_progress_callback=self.on_progress)
            self.video_title.setText(f"🎬 {self.yt.title}\n📏 Duration: {round(self.yt.length / 60)} mins")
            self.thumb_label.setPixmap(self.get_thumbnail(self.yt.thumbnail_url))
            self.streams = self.yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            self.res_dropdown.clear()
            for s in self.streams:
                self.res_dropdown.addItem(s.resolution)
            self.res_dropdown.setCurrentIndex(0)
            self.res_dropdown.setEnabled(True)
            self.download_btn.setEnabled(True)
            self.toast("✅ Video info loaded!")
        except Exception as e:
            self.toast(f"Failed: {str(e)}", error=True)

    def get_thumbnail(self, url):
        response = requests.get(url)
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        return pixmap.scaled(480, 270, Qt.KeepAspectRatio)

    def on_progress(self, stream, chunk, bytes_remaining):
        total = stream.filesize
        downloaded = total - bytes_remaining
        percent = int((downloaded / total) * 100)
        self.progress.setValue(percent)

    def download_video(self):
        default_path = os.path.join(os.path.expanduser("~"), "Downloads")
        save_path = QFileDialog.getExistingDirectory(self, "Choose Download Folder", default_path)
        if not save_path:
            self.toast("Download cancelled.")
            return
        selected_res = self.res_dropdown.currentText()
        stream = next((s for s in self.streams if s.resolution == selected_res), None)
        if stream:
            self.status.setText("⬇️ Downloading...")
            self.progress.setValue(0)
            stream.download(output_path=save_path)
            self.toast("🎉 Download completed successfully!")
        else:
            self.toast("❌ Resolution not found", error=True)

    def toast(self, msg, error=False):
        box = QMessageBox()
        box.setText(msg)
        box.setWindowTitle("FearLink Status")
        box.setIcon(QMessageBox.Critical if error else QMessageBox.Information)
        box.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))  # Optional custom icon
    window = FearLinkDownloader()
    window.show()
    sys.exit(app.exec_())
