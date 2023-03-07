
import setproctitle
import time
import ui
import sys

from multiprocessing import Pipe, Process
from backend import backend_run

__auth__ = "yinbing"
__DEBUG__ = False
__auth_key__ = '3a66eca2c941'
__yike_appid__ = '75246564'
__yike_appsecret__ = 'Ga0ty4WS'
__local_city__ = '五寨'

def background(conn_recv, conn_send):
    # 设置本进程名为 smart-dapeng-backend，可在bash用 [ps aux] 命令查看 
    setproctitle.setproctitle("smart-dapeng-backend")
    time.sleep(3)
    backend_run(auth_key       = __auth_key__, 
                yike_appid     = __yike_appid__, 
                yike_appsecret = __yike_appsecret__, 
                city           = __local_city__,
                debug          = __DEBUG__,
                send_pipe_conn = conn_send,
                recv_pipe_conn = conn_recv)

def frontstage(conn_recv, conn_send):
    # while 1:
    #     pass
    app = ui.QApplication(sys.argv)
    app.setStyleSheet(ui.Stylesheet)
    w = ui.LeftTabWidget(pipe_conn_recv=conn_recv, pipe_conn_send=conn_send)
    w.showFullScreen()
    app.exec_()
    
def func(conn_recv, conn_send):
    while True:
        args = conn_recv.recv()
        print(args)

if __name__ == "__main__":
    # 设置本进程名为 smart-dapeng，可在bash用 [ps aux] 命令查看 
    setproctitle.setproctitle("smart-dapeng-frontstage")
    parent_conn1, child_conn1 = Pipe()
    parent_conn2, child_conn2 = Pipe()
    p = Process(target=background, args=(child_conn1, child_conn2,), daemon=True)
    p.start()
    frontstage(parent_conn2, parent_conn1)
    # func(parent_conn2, parent_conn1)
    # p.join()

# import multiprocessing
# from multiprocessing import Process, Pipe
# from setproctitle import setproctitle
# import time
# from ui import LeftTabWidget, Stylesheet
# from PyQt5 import QtWidgets
# import sys

# def gui(conn_send, conn_recv):
#     # setproctitle("sub_proc")
#     app = QtWidgets.QApplication(sys.argv)
#     app.setStyleSheet(Stylesheet)

#     widget = LeftTabWidget(conn_recv, conn_send)
#     # widget.resize(800, 480)

#     # arg = conn.recv()
#     # widget.text.setText(arg[0])
#     widget.showFullScreen()

#     app.exec_()

# def func(conn_recv, conn_send):
#     while True:
#         args = conn_recv.recv()
#         print(args)

# if __name__ == "__main__":
#     conn1_parent, conn1_child = Pipe()
#     conn2_parent, conn2_child = Pipe()
#     p = Process(target=func, args=(conn1_child, conn2_child,), daemon=True, name="sub")
#     p.start()
#     gui(conn1_parent, conn2_parent)
