# mdock.py

import matplotlib.pyplot as plt
from matplotlib.backends.qt_compat import QtWidgets, QtCore
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backend_bases import FigureManagerBase
import PyQtAds

def drawnow():
    cls = MDock
    if cls.manager is not None:
        for canvas in cls.manager.findChildren(FigureCanvasQTAgg):
            canvas.draw()
            canvas.flush_events()
    
def title(t):
    cls = MDock
    cls.title(t)

def restore_state():
    cls = MDock
    cls.restore_state()

def store_state():
    cls = MDock
    cls.store_state()
    
def show():
    cls = MDock
    cls.show()

class MDock(FigureManagerBase):
    dock_title = 'Matplotlib Dock'
    window = None

    def __init__(self, canvas, num):
        cls = MDock
        if cls.window is None:
            cls.window = QtWidgets.QMainWindow()
            cls.window.setWindowTitle(cls.dock_title)
            cls.manager = PyQtAds.ads.CDockManager()
            cls.window.setCentralWidget(cls.manager)
            
            cls.settings = QtCore.QSettings("MikkelNSchmidt", "MDock")
            cls.manager.loadPerspectives(cls.settings)
            
            cls.toolbar = QtWidgets.QToolBar()
            cls.toolbar.setIconSize(QtCore.QSize(16, 16))
            cls.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
            cls.window.addToolBar(cls.toolbar)
            
            cls.action_save = QtWidgets.QAction('Store state')
            cls.action_save.setIcon(cls.window.style().standardIcon(QtWidgets.QStyle.SP_DialogNoButton))            
            cls.action_save.triggered.connect(cls.store_state)
            
            cls.action_restore = QtWidgets.QAction('Restore state')
            cls.action_restore.setIcon(cls.window.style().standardIcon(QtWidgets.QStyle.SP_DialogYesButton))
            cls.action_restore.triggered.connect(cls.restore_state)

            cls.toolbar.addAction(cls.action_save)
            cls.toolbar.addAction(cls.action_restore)
        
        self.dock_widget = PyQtAds.ads.CDockWidget(f'Figure {num}')
        self.dock_widget.setFeature(self.dock_widget.DockWidgetClosable, True)
        self.dock_widget.setWidget(canvas)
        cls.manager.addDockWidget(PyQtAds.ads.BottomDockWidgetArea, self.dock_widget)
        cls.window.adjustSize()
        #cls.restore_geometry()
        
        cls.window.show()
        super().__init__(canvas=canvas, num=num)
        
    def store_state():
        cls = MDock
        cls.manager.addPerspective(cls.dock_title)
        cls.manager.savePerspectives(cls.settings)
        cls.store_geometry()
        
    def store_geometry():
        cls = MDock
        geometry = cls.window.saveGeometry()
        cls.settings.setValue(cls.dock_title + ":geometry", geometry)        

    def restore_state():
        cls = MDock
        if cls.window is not None:
            cls.manager.openPerspective(cls.dock_title)    
            cls.restore_geometry()

    def restore_geometry():
        cls = MDock
        geometry = cls.settings.value(cls.dock_title + ":geometry")
        if geometry is not None:
            cls.window.restoreGeometry(geometry)
    
    def title(t):
        cls = MDock
        cls.dock_title = t
        if cls.window is not None:
            cls.window.setWindowTitle(t)

    def destroy(self, *args):
        try:
            self.dock_widget.closeDockWidget()
            self.window.destroy()
        except:
            pass

    def get_window_title(self):
        return self.dock_widget.windowTitle()

    def set_window_title(self, title):
        self.dock_widget.setWindowTitle(title)

    def show(self=None):
        cls = MDock
        if cls.window is not None:
#            cls.restore_state()
            cls.window.show()



class FigureCanvas(FigureCanvasQTAgg):
    manager_class = MDock  
    
FigureManager = MDock
    
