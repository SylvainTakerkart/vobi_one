# Author: Philippe Katz <philippe.katz@gmail.com>,
#         Sylvain Takerkart <Sylvain.Takerkart@incm.cnrs-mrs.fr>
# License: BSD Style.

# Qt widget for condition file visualisation

userLevel = 3 # Never visible

import sys
from PyQt4 import QtGui, QtCore
import numpy as np

# Programme attributes
progname = 'oi-brainvisa-tbx'
progversion = "1.0a1"


class ShowTxt(QtGui.QWidget):
    """Creation of text visualisation

    Attributes
    ----------
    conditions : numpy array
        Contains informations on datas :
            1. Filename
            2. Experience
            3. Trial
            4. Condition
            5. Selected (if file is selected or not)
    grid : QtGrid
        Grid used for text structuration
    label : array
        Text on each grid's square

    Methods
    -------
    __init__( ... )
        Class initialization
    create_grid( ... )
        Grid creation
    update_label( ... )
        Updating grid's labels names
    sort_file( ... )
        Sorts files by name
    sort_exp( ... )
        Sorts files by experience
    sort_trial( ... )
        Sorts files by trial
    sort_cond( ... )
        Sorts files by condition
    sort_select( ... )
        Sorts files by selection
    """
    def __init__(self,conditions,parent=None):
        """Class initialization

        Parameters
        ----------
        conditions : numpy array
            Contains informations on datas :
                1. Filename
                2. Experience
                3. Trial
                4. Condition
                5. Selected (if file is selected or not)
        parent : QtClass
            Parent Widget
        """
        QtGui.QWidget.__init__(self, parent) # QtWidget initialization

        self.conditions=conditions
        self.parent=parent

        self.grid = QtGui.QGridLayout() # Grid instance initialization

        file_button = QtGui.QPushButton('Filenames') # "Sort by filename" button
        self.grid.addWidget(file_button,0,0) # Position on grid
        self.connect(file_button,QtCore.SIGNAL("clicked()"),self.sort_file) # Waiting for action

        exp_button = QtGui.QPushButton('Experiences') # "Sort by experience" button
        self.grid.addWidget(exp_button,0,1) # Position on grid
        self.connect(exp_button,QtCore.SIGNAL("clicked()"),self.sort_exp) # Waiting for action

        trial_button = QtGui.QPushButton('Trials') # "Sort by trial" button
        self.grid.addWidget(trial_button,0,2) # Position on grid
        self.connect(trial_button,QtCore.SIGNAL("clicked()"),self.sort_trial) # Waiting for action

        cond_button = QtGui.QPushButton('Conditions') # "Sort by condition" button
        self.grid.addWidget(cond_button,0,3) # Position on grid
        self.connect(cond_button,QtCore.SIGNAL("clicked()"),self.sort_cond) # Waiting for action

        select_button = QtGui.QPushButton('Selected') # "Sort by selected" button
        self.grid.addWidget(select_button,0,4) # Position on grid
        self.connect(select_button,QtCore.SIGNAL("clicked()"),self.sort_select) # Waiting for action


        self.create_grid() # Grid creation

    def create_grid(self):
        """Grid creation
        """
        self.label=[] # label initialisation
        i=0
        while i<self.conditions.shape[1]:
            j=0
            tmp_label=[]
            while j<self.conditions.shape[0]:
                tmp_label.append(QtGui.QLabel(self.conditions[j,i])) # Association between labal's text and conditions
                self.grid.addWidget(tmp_label[j],i+1,j) # Creation of label
                j=j+1
            self.label.append(tmp_label)
            i=i+1
 
        self.setLayout(self.grid) # Displaying on grid

    def update_label(self):
        """Updating grid's labels names
        """
        i=0
        while i<self.conditions.shape[1]:
            j=0
            while j<(self.conditions.shape[0]):
                self.label[i][j].setText(self.conditions[j,i]) # Association between labal's text and conditions
                j=j+1
            i=i+1
            
    def sort_file(self):
        """Sorts by name
        """
        self.conditions=self.conditions[:,self.conditions[0].argsort(),] # Sorting conditions
        self.update_label() # Updating grid's labels names

    def sort_exp(self):
        """Sorts by experience
        """
        self.conditions=self.conditions[:,self.conditions[1].argsort(),] # Sorting conditions
        self.update_label() # Updating grid's labels names

    def sort_trial(self):
        """Sorts by trial
        """
        self.conditions=self.conditions[:,self.conditions[2].argsort(),] # Sorting conditions
        self.update_label() # Updating grid's labels names

    def sort_cond(self):
        """Sorts by condition
        """
        self.conditions=self.conditions[:,self.conditions[3].argsort(),] # Sorting conditions
        self.update_label() # Updating grid's labels names

    def sort_select(self):
        """Sorts by selection
        """
        self.conditions=self.conditions[:,self.conditions[4].argsort(),] # Sorting conditions
        self.update_label() # Updating grid's labels names

class WidgetModel(QtGui.QMainWindow):
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
    def __init__(self,conditions):
        """Class initialization
        """
        QtGui.QMainWindow.__init__(self) # Qt window initialization
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose) # Destruction when closed
        self.setWindowTitle(progname) # Window title

        scrollBar=QtGui.QScrollArea() # Scroll bar initialization
        scrollBar.setWidget(ShowTxt(conditions)) # Scroll bar on file list

        self.setCentralWidget(scrollBar) # Displaying scroll bar

        self.file_menu = QtGui.QMenu('&File', self) # File menu initialization
        self.file_menu.addAction('&Quit', self.fileQuit, # Add a quit button in file menu
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu) # Displaying file menu
        self.help_menu = QtGui.QMenu('&Help', self)  # Help menu initialization
        self.menuBar().addSeparator() # Add separator in menu bar
        self.menuBar().addMenu(self.help_menu) # Displaying help menu

        self.help_menu.addAction('&About', self.about) # Add an about button in file menu
    
        self.statusBar().showMessage("BrainMonkey - INCM CNRS", 200000) # Displaying a text bar in the window bottom
        self.setWindowIcon(QtGui.QIcon('../icon.png')) # Icon
        self.resize(500, 700) # Size

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
