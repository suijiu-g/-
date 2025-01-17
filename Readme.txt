PyQt5==5.15.11
PyQt5-Qt5==5.15.2
PyQt5_sip==12.16.1
pandas==2.2.3

pyinstaller --onefile --add-data "xp速看;xp速看" --add-data "人物设定;人物设定" --add-data "随机文段;随机文段" --add-data "外貌;外貌" --add-data "cihui;cihui" --add-data "suijiu.ico;." --icon=suijiu.ico main_app.py