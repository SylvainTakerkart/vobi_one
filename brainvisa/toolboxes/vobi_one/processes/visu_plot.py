# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Flavien Garcia <flavien.garcia@free.fr>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Qt widget for plot visualisation
# Integration with matplotlib

# Imports
try:
    from PyQt4 import QtGui, QtCore
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    import matplotlib.pyplot as plt
    import numpy as np
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
    plotfigure( ... )
        Plots the current figure
    """
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """Class initialization
        """
        self.fig = plt.figure() # Creates a figure
        self.axes = self.fig.add_subplot(111) # Add a new graphic display
        self.axes.hold(False) # Sets the axes hold state to false
        self.parent=parent
        
        # Parameters recuperation
        self.period=0.009090909*1000 # Period in ms
        frame0_window=[0,10] # Window chosen for frame0 division
        self.start=frame0_window[1]-frame0_window[0] # Samples lag at the beginning
        
    def setdata(self,X):
        """Sets X
        """
        self.X=X # Sets signals to plot list

    def settimevector(self,time_vector):
        """Sets time_vector (used for the abscissa of the plot)
        """
        self.time_vector=time_vector # Sets signals to plot list

    def plotfigure(self,title):
        """Plots the current figure
        """
        """
        nb_samples=110 # Number of samples
        x=np.linspace(-self.start*self.period\
                    ,(nb_samples-self.start)*self.period\
                    ,nb_samples) 
        """
        self.axes.plot(self.time_vector,self.X) # Sets data in current figure
        
        mini=np.array(self.X).min() # Min value of all signals of X
        maxi=np.array(self.X).max() # Max value of all signals of X
        
        if mini<0: # Defines min vertical limit
            mini=mini*1.1
        else:
            mini=mini*0.9
        if maxi<0: # Defines max vertical limit
            maxi=maxi*0.9
        else:
            maxi=maxi*1.1    
            
        self.axes.set_ylim([mini,maxi]) # Sets the vertical limits
         
        self.axes.grid(True) # Sets the grid state
        self.axes.set_xlabel('Time') # Sets horizontal title
        # The following line will be uncommented with BrainVISA 4.4 with a more recent version of matplotlib
        #self.axes.set_ylabel(r'$\Delta$'+'F/F') # Sets vertical title
        self.axes.set_ylabel('Normalized signal') # Sets vertical title
        self.axes.set_title(title) # Sets figure title
        
        # Widget
        FigureCanvas.__init__(self, self.fig) # Figure Canvas initialization
        self.setParent(self.parent) # Sets parent Qt Class
        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self) # Class updating


class PlotModel(QtGui.QMainWindow):
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
    def __init__(self,series,titles,time_vector):
        """Class initialization
        """
        # Qt window
        QtGui.QMainWindow.__init__(self) # Qt window initialization
        self.resize(1000,1000) # Increases figure size
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

        t=0 # Current title
        for serie in series: # Plots each serie (numpy vector)
            plot = FigureConstruct(self.main_widget, width=5, height=4, dpi=100) # Widget initialization
            plot.setdata(serie) # Sets figure serie
            plot.settimevector(time_vector) # Set timevector used for the abscissa of the plot
            plot.plotfigure(titles[t]) # Plots figure
            box.addWidget(plot) # Attach plot
            t+=1 # Next title

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
Authors: Philippe Katz <philippe.katz@gmail.com>,
         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
License: BSD Style.
"""
                                % {"prog": progname, "version": progversion})

