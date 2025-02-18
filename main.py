import sys
import os
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from dotenv import load_dotenv

server_address = 'https://static-maps.yandex.ru/v1?'

path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(path):
    load_dotenv()
    API_KEY = os.environ.get('API_KEY')


class MapApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Карта")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Метка для отображения карты
        self.map_label = QLabel(self)
        self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.map_label)

        central_widget.setLayout(layout)

        # Начальные координаты и масштаб
        self.lat = 55.751244
        self.lon = 37.618423
        self.zoom = 10

        # Предельные значения масштаба
        self.min_zoom = 0
        self.max_zoom = 21

        # Обновляем карту при запуске
        self.update_map()

    def update_map(self):
        # Формируем URL для запроса к API Яндекс.Карт
        url = f"{server_address}ll={self.lon},{self.lat}&z={self.zoom}&size=600,400&l=map&apikey={API_KEY}"

        response = requests.get(url)
        if response.status_code == 200:
            # Сохраняем изображение во временный файл
            with open("map.png", "wb") as f:
                f.write(response.content)

            # Загружаем изображение в QLabel
            pixmap = QPixmap("map.png")
            self.map_label.setPixmap(pixmap)
        else:
            self.map_label.setText("Ошибка при загрузке карты")

    def keyPressEvent(self, event):
        # Обработка нажатия клавиш PgUp и PgDown
        if event.key() == Qt.Key.Key_PageUp:
            self.zoom += 1
            if self.zoom > self.max_zoom:
                self.zoom = self.max_zoom
            self.update_map()
        elif event.key() == Qt.Key.Key_PageDown:
            self.zoom -= 1
            if self.zoom < self.min_zoom:
                self.zoom = self.min_zoom
            self.update_map()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapApp()
    window.show()
    sys.exit(app.exec())
