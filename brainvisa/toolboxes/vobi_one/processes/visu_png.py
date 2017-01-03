# Author: Flavien Garcia <flavien.garcia@free.fr>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Qt widget for plot visualisation
# Integration with matplotlib

# Imports
try:
    from PyQt4 import QtGui, QtCore
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
except ImportError:
    print('Impossible to import packages')
    
# Header
userLevel = 3 # Never visible

# Programme attributes
progname = 'Vobi One'
progversion = "1.0a1"


class FigureConstruct(FigureCanvas):
    """Plot construction

    Attributes
    ----------
    fig : matplotlib Figure
        Create active figure
    axes : matplotlib Figure
        Set the current axis limits 
    parent : QtClass
        Parent Widget
    X : numpy array
        Data displayed
    period: float
        Period between two samples (in ms)

    Methods
    -------
    __init__( ... )
        Class initialization
    setdata( ... )
        Sets X
    plotDataGraph( ... )
        Plots the current data graph
    """
    def __init__(self, parent=None, width=5, height=4, dpi=100,path_data_graph=''):
        """Class initialization
        """
        self.fig = plt.figure()
        img = mpimg.imread(path_data_graph)              
        self.axes = self.fig.add_subplot(111)
        self.axes.imshow(img)
        self.parent=parent

        # Widget
        FigureCanvas.__init__(self, self.fig) # Figure Canvas initialization
        self.setParent(self.parent) # Sets parent Qt Class
        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self) # Class updating


class DataGraphModel(QtGui.QMainWindow):
    """Creation of Qt main window

    Attributes
    ----------
    file_menu : Qt menu
        File menu
    help_menu : Qt menu
        Help menu


    Methods
    -------
    __init__( ... )
        Class initialization
    fileQuit( ... )
        Window quit function in file menu
    closeEvent( ... )
        Window quit function
    about( ... )
        Informations about program menu
    """
    def __init__(self,path_data_graph):
        """Class initialization
        """
        # Qt window
        QtGui.QMainWindow.__init__(self) # Qt window initialization
        self.resize(1000,1000) # Increases data graph size
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose) # Destruction when closed

        # Qt window menu
        self.file_menu = QtGui.QMenu('&File', self) # File menu initialization
        self.file_menu.addAction('&Quit', self.fileQuit, # Add a quit button in file menu
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu) # Displaying file menu
        self.help_menu = QtGui.QMenu('&Help', self)  # Help menu initialization
        self.menuBar().addSeparator() # Add separator in menu bar
        self.menuBar().addMenu(self.help_menu) # Displaying help menu

        self.help_menu.addAction('&About', self.about) # Add an about button in file menu

        # Qt widget
        self.main_widget = QtGui.QWidget(self) # Widget initialization
        box = QtGui.QVBoxLayout(self.main_widget)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        plot = FigureConstruct(self.main_widget, width=5, height=4, dpi=100,path_data_graph=path_data_graph) # Widget initialization
        box.addWidget(plot) # Attach plot
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.statusBar().showMessage("Vobi One - INCM CNRS", 200000) # Displaying a text bar in the window bottom
        self.setWindowIcon(QtGui.QIcon('../icon.png')) # Icon

    def fileQuit(self):
        """Window quit function in file menu
        """
        self.close()

    def closeEvent(self, ce):
        """Window quit function
        """
        self.fileQuit()

    def about(self):
        """Informations about program menu
        """
        QtGui.QMessageBox.about(self, "About %s" % progname,
u"""%(prog)s version %(version)s
Authors: Flavien Garcia <flavien.garcia@free.fr>,
         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
License: BSD Style.
"""
                                % {"prog": progname, "version": progversion})