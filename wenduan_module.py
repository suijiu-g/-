from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import pandas as pd
import os
import random

class WenduanModule(QWidget):
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

        # 列选择下拉菜单
        self.column_label = QLabel("选择列:")
        self.column_combobox = QComboBox()
        layout.addWidget(self.column_label)
        layout.addWidget(self.column_combobox)

        # 随机选择按钮
        self.generate_button = QPushButton("随机选择")
        layout.addWidget(self.generate_button)

        # 删除按钮
        self.delete_button = QPushButton("删除")
        layout.addWidget(self.delete_button)

        # 结果文本框
        self.result_label = QLabel("生成结果:")
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_text)

        # 返回主菜单按钮
        self.return_button = QPushButton("返回主菜单")
        layout.addWidget(self.return_button)

        # 设置布局
        self.setLayout(layout)

        # 初始化数据
        self.load_data()

        # 连接信号和槽
        self.generate_button.clicked.connect(self.generate_random)
        self.file_combobox.currentIndexChanged.connect(self.refresh_data)
        self.return_button.clicked.connect(self.return_to_main_menu)
        self.delete_button.clicked.connect(self.delete_row)  # 新增删除按钮的信号连接

    def load_data(self):
        """加载随机文段文件夹中的 Excel 文件"""
        # 获取脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.random_text_folder = os.path.join(script_dir, '随机文段')

        # 检查文件夹是否存在
        if not os.path.exists(self.random_text_folder):
            QMessageBox.critical(self, "Error", f"文件夹未找到: {self.random_text_folder}")
            return

        # 获取文件夹中的所有 Excel 文件
        self.excel_files = [f for f in os.listdir(self.random_text_folder) if f.endswith('.xlsx')]
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
        self.file_path = os.path.join(self.random_text_folder, selected_file)

        try:
            # 读取 Excel 文件
            self.df = pd.read_excel(self.file_path)
            self.update_column_dropdowns()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"刷新数据时出错: {e}")

    def update_column_dropdowns(self):
        """更新列下拉菜单"""
        columns = self.df.columns.tolist()
        self.column_combobox.clear()
        self.column_combobox.addItems(columns)

    def generate_random(self):
        """随机生成文段"""
        self.result_text.clear()
        try:
            selected_column = self.column_combobox.currentText()
            non_empty_values = self.df[selected_column].dropna().tolist()
            if non_empty_values:
                selected_value = random.choice(non_empty_values)
            else:
                selected_value = "N/A"

            self.result_text.setText(selected_value)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def delete_row(self):
        """删除当前选中的单元格，并将下方的单元格往上移动一格"""
        try:
            selected_file = self.file_combobox.currentText()
            self.file_path = os.path.join(self.random_text_folder, selected_file)
            selected_column = self.column_combobox.currentText()
            selected_value = self.result_text.toPlainText()

            # 找到要删除的行索引
            row_index = self.df[self.df[selected_column] == selected_value].index[0]

            # 删除该行
            self.df.drop(index=row_index, inplace=True)

            # 保存修改后的数据到 Excel 文件
            self.df.to_excel(self.file_path, index=False)

            # 刷新数据
            self.refresh_data()

            # 清空结果文本框
            self.result_text.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"删除行时出错: {e}")

    def return_to_main_menu(self):
        """返回主菜单"""
        self.main_window.stacked_widget.setCurrentIndex(5)  # 切换到主菜单
