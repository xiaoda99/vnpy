# encoding: UTF-8

import sys
import os
import ctypes
import platform

import vtPath
from vtEngine import MainEngine
from uiMainWindow import *

# XD
from datetime import datetime
from utils import data_dir, date2str
from gm_utils import is_trading_day

# 文件路径名
path = os.path.abspath(os.path.dirname(__file__))
ICON_FILENAME = 'vnpy.ico'
ICON_FILENAME = os.path.join(path, ICON_FILENAME)

SETTING_FILENAME = 'VT_setting.json'
SETTING_FILENAME = os.path.join(path, SETTING_FILENAME)

#----------------------------------------------------------------------
def main():
    """主程序入口"""
    # 重载sys模块，设置默认字符串编码方式为utf8
    reload(sys)
    sys.setdefaultencoding('utf8')

    # 设置Windows底部任务栏图标
    if 'Windows' in platform.uname() :
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('vn.trader')

    # 初始化Qt应用对象
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(ICON_FILENAME))
    app.setFont(BASIC_FONT)

    # 设置Qt的皮肤
    try:
        f = file(SETTING_FILENAME)
        setting = json.load(f)
        if setting['darkStyle']:
            import qdarkstyle
            app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    except:
        pass

    # 初始化主引擎和主窗口对象
    mainEngine = MainEngine()
    mainWindow = MainWindow(mainEngine, mainEngine.eventEngine)
    mainWindow.showMaximized()
    mainWindow.autorun()  # XD

    # 在主线程中启动Qt事件循环
    sys.exit(app.exec_())


# XD
def check_error():
    dirname = '/home/xd/production/pivotrader'
    return os.path.getsize(os.path.join(dirname, 'download' + '_error.out')) + \
        sum([os.path.getsize(os.path.join(data_dir, name + '_error.out'))
            for name in ['sc', 'youse', 'dc', 'zc']])


def link(source, link_name):
    if os.path.isfile(link_name):
        assert os.path.islink(link_name)
        os.unlink(link_name)
    os.symlink(os.path.basename(source), link_name)


if __name__ == '__main__':
    # XD
    if not is_trading_day(datetime.now()):
        print 'vtMain exit: not trading day.'
        exit(0)
    if check_error() > 0:
        print 'vtMain exit: step error.'
        exit(-1)

    main()
