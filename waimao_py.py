import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class WaimaoModule(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # 保存主窗口的引用
        self.current_pixmap = None  # 用于存储当前图片
        self.init_ui()

    def init_ui(self):
        # 创建布局
        layout = QVBoxLayout()

        # 文件夹选择下拉菜单
        self.folder_label = QLabel("选择文件夹:")
        self.folder_combobox = QComboBox()
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.folder_combobox)
        layout.addLayout(folder_layout)

        # 文件选择下拉菜单
        self.file_label = QLabel("选择文件:")
        self.file_combobox = QComboBox()
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_combobox)
        layout.addLayout(file_layout)

        # 文字和图片显示区域
        self.text_label = QLabel("文字内容:")
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.image_label = QLabel("图片:")
        self.image_display = QLabel()
        self.image_display.setAlignment(Qt.AlignCenter)
        self.image_display.setStyleSheet("border: 1px solid black;")

        # 左右布局
        content_layout = QHBoxLayout()
        content_layout.addWidget(self.text_display, stretch=1)  # 文字框占一半
        content_layout.addWidget(self.image_display, stretch=1)  # 图片框占一半
        layout.addWidget(self.text_label)
        layout.addWidget(self.image_label)
        layout.addLayout(content_layout)

        # 返回主菜单按钮
        self.return_button = QPushButton("返回主菜单")
        layout.addWidget(self.return_button)

        # 设置布局
        self.setLayout(layout)

        # 初始化数据
        self.load_folders()

        # 连接信号和槽
        self.folder_combobox.currentIndexChanged.connect(self.on_folder_changed)
        self.file_combobox.currentIndexChanged.connect(self.display_content)
        self.return_button.clicked.connect(self.return_to_main_menu)

    def load_folders(self):
        """加载外貌文件夹中的子文件夹"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.waimao_folder = os.path.join(script_dir, '外貌')

        # 检查文件夹是否存在
        if not os.path.exists(self.waimao_folder):
            QMessageBox.critical(self, "Error", f"文件夹未找到: {self.waimao_folder}")
            return

        # 获取文件夹中的所有子文件夹
        self.sub_folders = [f for f in os.listdir(self.waimao_folder) if os.path.isdir(os.path.join(self.waimao_folder, f))]
        if not self.sub_folders:
            QMessageBox.critical(self, "Error", "文件夹中没有子文件夹。")
            return

        # 更新文件夹下拉菜单
        self.folder_combobox.clear()
        self.folder_combobox.addItems(self.sub_folders)

        # 默认选择第一个文件夹
        if self.sub_folders:
            self.folder_combobox.setCurrentIndex(0)
            self.on_folder_changed()  # 手动触发文件夹切换事件

    def on_folder_changed(self):
        """文件夹切换时更新文件列表，但不加载内容"""
        selected_folder = self.folder_combobox.currentText()
        folder_path = os.path.join(self.waimao_folder, selected_folder)

        # 检查文件夹是否存在
        if not os.path.exists(folder_path):
            QMessageBox.critical(self, "Error", f"文件夹未找到: {folder_path}")
            return

        # 获取文件夹中的所有txt文件
        self.txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        if not self.txt_files:
            QMessageBox.warning(self, "Warning", "文件夹中没有txt文件。")
            return

        # 更新文件下拉菜单
        self.file_combobox.clear()
        self.file_combobox.addItems(self.txt_files)

        # 清空显示内容
        self.text_display.clear()
        self.image_display.clear()

        # 默认选择第一个文件
        if self.txt_files:
            self.file_combobox.setCurrentIndex(0)
            self.display_content()  # 显示第一个文件的内容

    def display_content(self):
        """显示选中的txt文件和对应的图片"""
        selected_folder = self.folder_combobox.currentText()
        selected_file = self.file_combobox.currentText()
        folder_path = os.path.join(self.waimao_folder, selected_folder)
        file_path = os.path.join(folder_path, selected_file)

        # 检查文件是否存在
        if not os.path.exists(file_path):
            QMessageBox.critical(self, "Error", f"文件未找到: {file_path}")
            return

        # 读取txt文件内容
        self.load_text_file(file_path)

        # 加载同名图片（支持 .png, .jpg, .jpeg 格式）
        self.load_image_file(folder_path, selected_file)

    def load_text_file(self, file_path):
        """读取txt文件内容"""
        try:
            # 尝试使用 utf-8 编码读取
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
                self.text_display.setText(text_content)
        except UnicodeDecodeError:
            # 如果 utf-8 失败，尝试使用 gbk 编码
            try:
                with open(file_path, 'r', encoding='gbk') as file:
                    text_content = file.read()
                    self.text_display.setText(text_content)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"读取txt文件时出错: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"读取txt文件时出错: {e}")

    def load_image_file(self, folder_path, selected_file):
        """加载同名图片"""
        image_base_name = os.path.splitext(selected_file)[0]  # 去掉 .txt 后缀
        image_extensions = ['.png', '.jpg', '.jpeg']  # 支持的图片格式
        image_path = None

        # 遍历支持的图片格式，查找对应的图片文件
        for ext in image_extensions:
            possible_image_path = os.path.join(folder_path, image_base_name + ext)
            if os.path.exists(possible_image_path):
                image_path = possible_image_path
                break

        # 如果找到图片文件，则加载并显示
        if image_path:
            print("Loading image:", image_path)
            self.current_pixmap = QPixmap(image_path)
            if self.current_pixmap.isNull():
                QMessageBox.warning(self, "Warning", "图片文件损坏或格式不受支持。")
                self.image_display.clear()  # 清空图片显示区域
                return

            # 设置图片固定大小（例如 300x300）
            self.image_display.setFixedSize(300, 300)
            self.image_display.setPixmap(self.current_pixmap.scaled(
                300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))

    def return_to_main_menu(self):
        """返回主菜单"""
        # 切换到主菜单（假设主菜单的索引是 5）
        self.main_window.stacked_widget.setCurrentIndex(5)