from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QTextEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
import pandas as pd
import os

class CihuiModule(QWidget):
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

        # 详细信息文本框
        self.detail_label = QLabel("详细信息:")
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)  # 设置为只读
        layout.addWidget(self.detail_label)
        layout.addWidget(self.detail_text)

        # 按钮布局（刷新按钮和返回主菜单按钮）
        button_layout = QHBoxLayout()
        self.refresh_button = QPushButton("数据刷新")
        self.return_button = QPushButton("返回主菜单")
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.return_button)
        layout.addLayout(button_layout)

        # 设置布局
        self.setLayout(layout)

        # 初始化数据
        self.load_data()

        # 连接信号和槽
        self.file_combobox.currentIndexChanged.connect(self.refresh_data)  # 文件切换时刷新数据
        self.column_combobox.currentIndexChanged.connect(
            lambda index: self.display_column_content(self.column_combobox.itemText(index))
        )  # 列切换时显示内容
        self.refresh_button.clicked.connect(self.refresh_data)  # 点击刷新按钮时刷新数据
        self.return_button.clicked.connect(self.return_to_main_menu)  # 返回主菜单

    def load_data(self):
        """加载词汇汇总文件夹中的 Excel 文件"""
        # 获取脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.vocab_folder = os.path.join(script_dir, 'cihui')

        # 检查文件夹是否存在
        if not os.path.exists(self.vocab_folder):
            QMessageBox.critical(self, "Error", f"文件夹未找到: {self.vocab_folder}")
            return

        # 获取文件夹中的所有 Excel 文件
        self.excel_files = [f for f in os.listdir(self.vocab_folder) if f.endswith('.xlsx')]
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
        self.file_path = os.path.join(self.vocab_folder, selected_file)

        try:
            # 使用 pandas 读取 Excel 文件，指定引擎为 openpyxl
            self.df = pd.read_excel(self.file_path, engine='openpyxl')
            print(f"Loaded data from {self.file_path}")  # 调试信息
            print(f"DataFrame columns: {self.df.columns.tolist()}")  # 调试信息
            self.update_column_dropdowns()  # 更新列下拉菜单
        except Exception as e:
            QMessageBox.critical(self, "Error", f"刷新数据时出错: {e}")

    def update_column_dropdowns(self):
        """更新列下拉菜单：读取第一行中有内容的列"""
        self.column_combobox.clear()

        # 获取第一行中有内容的列
        first_row = self.df.iloc[0]  # 第一行数据
        for column_name, value in first_row.items():
            if pd.notna(value):  # 如果单元格有内容
                self.column_combobox.addItem(str(column_name))  # 将内容添加到下拉菜单

        # 默认选择第一列
        if self.column_combobox.count() > 0:
            self.display_column_content(self.column_combobox.itemText(0))  # 传递第一列的列名

    def display_column_content(self, column_name):
        """显示当前列的内容"""
        print(f"Displaying content for column: {column_name} (type: {type(column_name)})")  # 调试信息
        self.detail_text.clear()  # 清空文本框

        try:
            # 找到列名对应的列索引
            if column_name not in self.df.columns:
                QMessageBox.warning(self, "Warning", f"选择的列不存在: {column_name}")
                return

            # 获取该列的所有非空值（从第二行开始）
            column_data = self.df[column_name].iloc[1:].dropna().tolist()

            if not column_data:
                self.detail_text.setText("无")  # 如果列内容为空，显示“无”
                return

            # 将列内容用逗号隔开并显示
            content = ', '.join(map(str, column_data))
            self.detail_text.setText(content)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"显示列内容时出错: {e}")

    def return_to_main_menu(self):
        """返回主菜单"""
        self.main_window.stacked_widget.setCurrentIndex(5)  # 切换到主菜单