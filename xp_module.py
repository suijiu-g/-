from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import pandas as pd
import os
import random

class XpModule(QWidget):
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

        # 随机XP按钮
        self.random_xp_button = QPushButton("随机XP")
        layout.addWidget(self.random_xp_button)

        # 对应文段按钮
        self.corresponding_segment_button = QPushButton("对应文段")
        layout.addWidget(self.corresponding_segment_button)

        # 随机XP结果文本框
        self.result_label = QLabel("随机XP:")
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_text)

        # 对应文段文本框
        self.detail_label = QLabel("对应文段:")
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        layout.addWidget(self.detail_label)
        layout.addWidget(self.detail_text)

        # 返回主菜单按钮
        self.return_button = QPushButton("返回主菜单")
        layout.addWidget(self.return_button)

        # 设置布局
        self.setLayout(layout)

        # 初始化数据
        self.load_data()

        # 连接信号和槽
        self.random_xp_button.clicked.connect(self.select_random_xp)
        self.corresponding_segment_button.clicked.connect(self.show_corresponding_segment)
        self.file_combobox.currentIndexChanged.connect(self.refresh_data)
        self.return_button.clicked.connect(self.return_to_main_menu)

    def load_data(self):
        """加载xp速看文件夹中的 Excel 文件"""
        # 获取脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.xp_folder = os.path.join(script_dir, 'xp速看')

        # 检查文件夹是否存在
        if not os.path.exists(self.xp_folder):
            QMessageBox.critical(self, "Error", f"文件夹未找到: {self.xp_folder}")
            return

        # 获取文件夹中的所有 Excel 文件
        self.excel_files = [f for f in os.listdir(self.xp_folder) if f.endswith('.xlsx')]
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
        self.file_path = os.path.join(self.xp_folder, selected_file)

        try:
            # 读取 Excel 文件
            self.df = pd.read_excel(self.file_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"刷新数据时出错: {e}")

    def select_random_xp(self):
        """随机选择XP"""
        self.result_text.clear()
        self.detail_text.clear()
        try:
            if self.df.empty:
                QMessageBox.warning(self, "Warning", "Excel文件为空。")
                return

            first_column = self.df.iloc[:, 0].dropna().tolist()

            if not first_column:
                QMessageBox.warning(self, "Warning", "第一列没有有效内容。")
                return

            selected_value = random.choice(first_column)
            self.result_text.setText(str(selected_value))

            # 存储当前选中的值
            self.current_selected_value = selected_value
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def show_corresponding_segment(self):
        """显示对应文段"""
        self.detail_text.clear()
        try:
            if not hasattr(self, 'current_selected_value') or self.current_selected_value is None:
                QMessageBox.warning(self, "Warning", "请先选择一个XP。")
                return

            # 找到当前选中的值所在的行
            matching_rows = self.df[self.df.iloc[:, 0] == self.current_selected_value]

            if matching_rows.empty:
                self.detail_text.setText("无")
                return

            # 随机选择该行中的一个非空单元格
            row = matching_rows.iloc[0]
            non_empty_values = row[row.notna()].tolist()

            if not non_empty_values:
                self.detail_text.setText("无")
                return

            selected_value = random.choice(non_empty_values)
            self.detail_text.setText(str(selected_value))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def return_to_main_menu(self):
        """返回主菜单"""
        self.main_window.stacked_widget.setCurrentIndex(5)  # 切换到主菜单