from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from cihui_module import CihuiModule
from renshe_module import RensheModule
from wenduan_module import WenduanModule
from xp_module import XpModule
from waimao_py import WaimaoModule  # 导入新模块

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("岁九的思路快递")
        self.setGeometry(100, 100, 800, 600)

        # 创建堆叠窗口
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 创建功能模块
        self.cihui_module = CihuiModule(self)  # 传递 self（主窗口）作为参数
        self.renshe_module = RensheModule(self)  # 如果需要，其他模块也可以传递 self
        self.wenduan_module = WenduanModule(self)
        self.xp_module = XpModule(self)
        self.waimao_module = WaimaoModule(self)  # 新增角色外貌模块

        # 将模块添加到堆叠窗口
        self.stacked_widget.addWidget(self.cihui_module)  # 索引 0
        self.stacked_widget.addWidget(self.renshe_module)  # 索引 1
        self.stacked_widget.addWidget(self.wenduan_module)  # 索引 2
        self.stacked_widget.addWidget(self.xp_module)  # 索引 3
        self.stacked_widget.addWidget(self.waimao_module)  # 索引 4

        # 创建主菜单
        self.create_main_menu()

    def create_main_menu(self):
        # 创建主菜单布局
        main_menu_layout = QGridLayout()

        # 标题
        title_label = QLabel("岁九的思路快递")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_menu_layout.addWidget(title_label, 0, 0, 1, 2, alignment=Qt.AlignCenter)

        # 创建按钮
        cihui_button = QPushButton("词汇汇总")
        renshe_button = QPushButton("人物设定")
        wenduan_button = QPushButton("随机文段")
        xp_button = QPushButton("xp速看")
        waimao_button = QPushButton("角色外貌")  # 新增按钮
        exit_button = QPushButton("退出软件")

        # 连接按钮点击事件
        cihui_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))  # 切换到词汇汇总模块
        renshe_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))  # 切换到人物设定模块
        wenduan_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))  # 切换到随机文段模块
        xp_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))  # 切换到xp速看模块
        waimao_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))  # 切换到角色外貌模块
        exit_button.clicked.connect(self.close)  # 退出程序

        # 添加按钮到布局
        main_menu_layout.addWidget(cihui_button, 1, 0)
        main_menu_layout.addWidget(renshe_button, 1, 1)
        main_menu_layout.addWidget(wenduan_button, 2, 0)
        main_menu_layout.addWidget(xp_button, 2, 1)
        main_menu_layout.addWidget(waimao_button, 3, 0)  # 新增按钮位置
        main_menu_layout.addWidget(exit_button, 4, 0)  # 退出按钮放在左下角

        # 创建主菜单容器
        main_menu_container = QWidget()
        main_menu_container.setLayout(main_menu_layout)

        # 将主菜单添加到堆叠窗口
        self.stacked_widget.addWidget(main_menu_container)  # 主菜单的索引为 5

        # 默认显示主菜单
        self.stacked_widget.setCurrentIndex(5)  # 切换到主菜单