from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QTextEdit, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
import pandas as pd
import os
import random

class RensheModule(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # 保存主窗口的引用
        self.init_ui()

    def init_ui(self):
        # 创建布局
        layout = QVBoxLayout()

        # 文件选择下拉菜单
        self.file_label = QLabel("选择文件:")
        self.file_combobox = QComboBox()
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_combobox)

        # 随机生成按钮
        self.generate_button = QPushButton("随机生成")
        layout.addWidget(self.generate_button)

        # 结果文本框
        self.result_label = QLabel("生成结果:")
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_text)

        # 增加人设
        self.character_label = QLabel("增加人设:")
        self.character_entry = QLineEdit()
        self.add_character_button = QPushButton("增加人设")
        layout.addWidget(self.character_label)
        layout.addWidget(self.character_entry)
        layout.addWidget(self.add_character_button)

        # 增加属性
        self.attribute_label = QLabel("增加属性:")
        self.attribute_combobox = QComboBox()
        self.attribute_entry = QLineEdit()
        self.add_attribute_button = QPushButton("增加属性")
        layout.addWidget(self.attribute_label)
        layout.addWidget(self.attribute_combobox)
        layout.addWidget(self.attribute_entry)
        layout.addWidget(self.add_attribute_button)

        # 返回主菜单按钮
        self.return_button = QPushButton("返回主菜单")
        layout.addWidget(self.return_button)

        # 设置布局
        self.setLayout(layout)

        # 初始化数据
        self.load_data()

        # 连接信号和槽
        self.generate_button.clicked.connect(self.generate_random)
        self.add_character_button.clicked.connect(self.add_character)
        self.add_attribute_button.clicked.connect(self.add_attribute)
        self.file_combobox.currentIndexChanged.connect(self.refresh_data)
        self.return_button.clicked.connect(self.return_to_main_menu)

    def load_data(self):
        """加载人物设定文件夹中的 Excel 文件"""
        # 获取脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.characters_folder = os.path.join(script_dir, '人物设定')

        # 检查文件夹是否存在
        if not os.path.exists(self.characters_folder):
            QMessageBox.critical(self, "Error", f"文件夹未找到: {self.characters_folder}")
            return

        # 获取文件夹中的所有 Excel 文件
        self.excel_files = [f for f in os.listdir(self.characters_folder) if f.endswith('.xlsx')]
        if not self.excel_files:
            QMessageBox.critical(self, "Error", "文件夹中没有 Excel 文件。")
            return

        # 更新文件下拉菜单
        self.file_combobox.clear()
        self.file_combobox.addItems(self.excel_files)

        # 默认选择第一个文件
        self.refresh_data()

    def refresh_data(self):
        """刷新数据：读取当前选择的 Excel 文件"""
        selected_file = self.file_combobox.currentText()
        self.file_path = os.path.join(self.characters_folder, selected_file)

        try:
            # 读取 Excel 文件
            self.df = pd.read_excel(self.file_path)
            self.update_dropdown()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"刷新数据时出错: {e}")

    def update_dropdown(self):
        """更新属性下拉菜单"""
        columns = self.df.columns.tolist()
        self.attribute_combobox.clear()
        self.attribute_combobox.addItems(columns)

    def generate_random(self):
        """随机生成人设"""
        self.result_text.clear()
        try:
            selected_data = {}
            for column in self.df.columns:
                non_empty_values = self.df[column].dropna().tolist()
                if non_empty_values:
                    selected_value = random.choice(non_empty_values)
                else:
                    selected_value = "N/A"
                selected_data[column] = selected_value

            self.result_text.setText("\n".join([f"{col}: {val}" for col, val in selected_data.items()]))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def add_character(self):
        """增加人设"""
        new_column_name = self.character_entry.text().strip()
        if not new_column_name:
            QMessageBox.warning(self, "Warning", "请输入有效的列名。")
            return

        if new_column_name in self.df.columns:
            QMessageBox.warning(self, "Warning", "该列名已存在，请选择另一个列名。")
            return

        self.df[new_column_name] = ""
        self.save_to_excel()
        self.update_dropdown()
        self.character_entry.clear()

    def add_attribute(self):
        """增加属性"""
        selected_column = self.attribute_combobox.currentText()
        new_value = self.attribute_entry.text().strip()

        if not selected_column or not new_value:
            QMessageBox.warning(self, "Warning", "请选择列并输入有效的内容。")
            return

        self.df.loc[len(self.df)] = [new_value if col == selected_column else "" for col in self.df.columns]
        self.save_to_excel()
        self.attribute_entry.clear()

    def save_to_excel(self):
        """保存数据到 Excel 文件"""
        try:
            self.df.to_excel(self.file_path, index=False)
            QMessageBox.information(self, "Success", "数据已保存到 Excel 文件。")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"保存文件时出错: {e}")

    def return_to_main_menu(self):
        """返回主菜单"""
        self.main_window.stacked_widget.setCurrentIndex(5)  # 切换到主菜单