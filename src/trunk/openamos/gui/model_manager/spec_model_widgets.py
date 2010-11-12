'''
Created on Apr 19, 2010

@author: bsana
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import copy

from openamos.gui.misc.basic_widgets import *
from openamos.gui.env import *

class AbstractModWidget(QGroupBox):
    '''
    classdocs
    '''
    def __init__(self, parent=None):
        super(AbstractModWidget, self).__init__(parent)
        self.setTitle("Specification")
        self.mainlayout = QGridLayout()
        self.setLayout(self.mainlayout)

    def makeProbChoiceWidget(self):
        self.choicewidget = QWidget(self)
        self.choicelayout = QVBoxLayout()
        self.choicewidget.setLayout(self.choicelayout)
        
        self.choicebuttonwidget = QWidget(self)
        choicebuttonlayout = QHBoxLayout()
        self.choicebuttonwidget.setLayout(choicebuttonlayout)
        self.choiceaddbutton = QPushButton('Add Alternative')
        choicebuttonlayout.addWidget(self.choiceaddbutton)
        self.choicedelbutton = QPushButton('Delete Alternative')
        choicebuttonlayout.addWidget(self.choicedelbutton)
        self.choicelayout.addWidget(self.choicebuttonwidget)
        
        self.choicetable = QTableWidget(0,2,self) #3,self)
        self.choicetable.setHorizontalHeaderLabels(['Alternative', 'Value']) #, 'Probability'])
        self.choicetable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.choicetable.horizontalHeader().setResizeMode(0,1)
        self.choicetable.horizontalHeader().setResizeMode(1,1)
        
        #self.choicetable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.choicelayout.addWidget(self.choicetable)
    
        self.mainlayout.addWidget(self.choicewidget,0,0,1,1)
        
        self.connect(self.choiceaddbutton, SIGNAL("clicked(bool)"), self.addChoice) 
        self.connect(self.choicedelbutton, SIGNAL("clicked(bool)"), self.delChoice)

    def addChoice(self):
        self.choicetable.insertRow(self.choicetable.rowCount())
        
    def delChoice(self):
        self.choicetable.removeRow(self.choicetable.currentRow())
    
    def makeChoiceWidget(self,x=0,y=0):
        self.choicewidget = QWidget(self)
        self.choicelayout = QVBoxLayout()
        self.choicewidget.setLayout(self.choicelayout)
        
        self.choicebuttonwidget = QWidget(self)
        choicebuttonlayout = QHBoxLayout()
        self.choicebuttonwidget.setLayout(choicebuttonlayout)
        self.choiceaddbutton = QPushButton('Add Alternative')
        choicebuttonlayout.addWidget(self.choiceaddbutton)
        self.choicedelbutton = QPushButton('Delete Alternative')
        choicebuttonlayout.addWidget(self.choicedelbutton)
        self.choicelayout.addWidget(self.choicebuttonwidget)
        
        self.choicetable = QTableWidget(self)
        self.choicetable.setRowCount(0)
        self.choicetable.setColumnCount(2)
        self.choicetable.setHorizontalHeaderLabels(['Alternative', 'Value'])
        #self.choicetable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.choicetable.setSelectionMode(QAbstractItemView.SingleSelection)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        self.choicetable.setSizePolicy(sizePolicy)
        self.choicetable.horizontalHeader().setResizeMode(0,1)
        self.choicelayout.addWidget(self.choicetable)
        
        self.mainlayout.addWidget(self.choicewidget,x,y,1,1)
        
        self.connect(self.choiceaddbutton, SIGNAL("clicked(bool)"), self.addChoice)
        self.connect(self.choicedelbutton, SIGNAL("clicked(bool)"), self.delChoice)


    def makeVarsWidget(self,x=0,y=1):
        self.varswidget = QWidget(self)
        self.varslayout = QGridLayout()
        self.varswidget.setLayout(self.varslayout)
        
        tableslabel = QLabel('Tables')
        self.varslayout.addWidget(tableslabel,0,0)
        
        self.tableswidget = QListWidget()
        self.tableswidget.setSelectionMode(QAbstractItemView.SingleSelection)
        parentdialog = self.parent()
        self.tableswidget.addItems(parentdialog.tablelist)
        self.tableswidget.setMaximumWidth(180)
        self.varslayout.addWidget(self.tableswidget,1,0)
        
        varslabel = QLabel('Columns')
        self.varslayout.addWidget(varslabel,0,1)
        
        self.colswidget = QListWidget()
        self.colswidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.colswidget.setMaximumWidth(180)
        self.varslayout.addWidget(self.colswidget,1,1)        
        
        self.varsbutton = QPushButton('>>')
        self.varslayout.addWidget(self.varsbutton,1,2)

        self.buttonwidget = QWidget(self)
        buttonlayout = QHBoxLayout()
        self.buttonwidget.setLayout(buttonlayout)
        self.intbutton = QPushButton('Add Interaction')
        buttonlayout.addWidget(self.intbutton)
        self.delbutton = QPushButton('Delete Row')
        buttonlayout.addWidget(self.delbutton)
        
        
        self.varslayout.addWidget(self.buttonwidget,0,3)
        
        self.varstable = QTableWidget(0,3,self)
        self.varstable.setHorizontalHeaderLabels(['Table', 'Column', 'Coefficient'])
        self.varstable.setSelectionBehavior(QAbstractItemView.SelectRows)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        self.varstable.setSizePolicy(sizePolicy)
        self.varstable.horizontalHeader().setResizeMode(0,1)
        self.varstable.horizontalHeader().setResizeMode(1,1)
        self.varstable.horizontalHeader().setResizeMode(2,1)
        self.varslayout.addWidget(self.varstable,1,3)
        
        self.mainlayout.addWidget(self.varswidget,x,y,1,10)
        self.mainlayout.setColumnStretch(y,5)
        
        self.connect(self.tableswidget, SIGNAL("itemClicked (QListWidgetItem *)"), self.populateColumns)
        self.connect(self.varsbutton, SIGNAL("clicked(bool)"), self.addVariable)
        self.connect(self.delbutton, SIGNAL("clicked(bool)"), self.delVariable)
        self.connect(self.intbutton, SIGNAL("clicked(bool)"), self.makeIntVar) 

    def populateColumns(self, item):
        self.colswidget.clear()
        seltab = str(item.text())
        parentdialog = self.parent()
        self.colswidget.addItems(parentdialog.coldict[seltab])          

    def addVariable(self):     
        if (self.tableswidget.currentItem() != None) & (self.colswidget.currentItem() != None):
            self.varstable.insertRow(self.varstable.rowCount())
            currtable = (self.tableswidget.currentItem()).text()
            tableitem = QTableWidgetItem()
            tableitem.setText(currtable)
            tableitem.setFlags(tableitem.flags() & ~Qt.ItemIsEditable)
            self.varstable.setItem(self.varstable.rowCount()-1, 0, tableitem)
            
            currvar = (self.colswidget.currentItem()).text()
            varitem = QTableWidgetItem()
            varitem.setText(currvar)
            varitem.setFlags(varitem.flags() & ~Qt.ItemIsEditable)
            self.varstable.setItem(self.varstable.rowCount()-1, 1, varitem)
        else:
            msg = "Please select a Table and a Column"
            QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)            

    def delVariable(self):
        self.varstable.removeRow(self.varstable.currentRow())

    def makeNestWidget(self):
        self.nestwidget = QWidget(self)
        self.nestlayout = QVBoxLayout()
        self.nestwidget.setLayout(self.nestlayout)
        
        self.nestbuttonwidget = QWidget(self)
        nestbuttonlayout = QHBoxLayout()
        self.nestbuttonwidget.setLayout(nestbuttonlayout)
        self.nesteaddbutton = QPushButton('Add Nest')
        nestbuttonlayout.addWidget(self.nesteaddbutton)
        self.nestdelbutton = QPushButton('Delete Nest')
        nestbuttonlayout.addWidget(self.nestdelbutton)
        self.nestlayout.addWidget(self.nestbuttonwidget)
        
        self.nesttable = QTableWidget(0,2,self)
        self.nesttable.setHorizontalHeaderLabels(['Nest', 'IV Parameter'])
        self.nesttable.horizontalHeader().setResizeMode(0,1)
        self.nesttable.horizontalHeader().setResizeMode(1,1)
        self.nestlayout.addWidget(self.nesttable)
        
        self.mainlayout.addWidget(self.nestwidget,0,0,1,1)
        
        self.connect(self.nesteaddbutton, SIGNAL("clicked(bool)"), self.addNest) 
        self.connect(self.nestdelbutton, SIGNAL("clicked(bool)"), self.delNest)

    def addNest(self):
        self.nesttable.insertRow(self.nesttable.rowCount())

    def delNest(self):
        self.nesttable.removeRow(self.nesttable.currentRow())
    
    def makeVarianceWidget(self):
        self.variancevwidget = QWidget(self)
        self.variancevlayout = QHBoxLayout()
        self.variancevwidget.setLayout(self.variancevlayout)

        self.variancevlabel = QLabel('Variance')
        self.variancevlayout.addWidget(self.variancevlabel)

        self.variancevline = LineEdit()
        self.variancevline.setFixedWidth(100)
        self.variancevlayout.addWidget(self.variancevline)

        self.mainlayout.addWidget(self.variancevwidget,0,0,1,1,Qt.AlignLeft)
 
        
    def makeSFVarianceWidget(self):
        self.variancevwidget = QWidget(self)
        self.varianceuwidget = QWidget(self)
        self.variancevlayout = QHBoxLayout()
        self.varianceulayout = QHBoxLayout()
        self.variancevwidget.setLayout(self.variancevlayout)
        self.varianceuwidget.setLayout(self.varianceulayout)
        
        self.variancevlabel = QLabel('Variance (v) - Normal')
        self.varianceulabel = QLabel('Variance (u) - Half Normal')
        self.variancevlayout.addWidget(self.variancevlabel)
        self.varianceulayout.addWidget(self.varianceulabel)
        
        self.variancevline = LineEdit()
        self.variancevline.setFixedWidth(100)
        self.varianceuline = LineEdit()
        self.varianceuline.setFixedWidth(100)
        self.variancevlayout.addWidget(self.variancevline)
        self.varianceulayout.addWidget(self.varianceuline)
        
        self.mainlayout.addWidget(self.variancevwidget,0,0,1,1,Qt.AlignLeft)
        self.mainlayout.addWidget(self.varianceuwidget,0,1,1,1,Qt.AlignLeft)

   
    def makeIntVar(self):
        selectedrows = []
        for modindex in self.varstable.selectedIndexes():
            row = modindex.row()
            col = modindex.column()
            if col == 0:
                selectedrows.append(row) 

        if len(selectedrows) == 2:
            table1 = str((self.varstable.item(selectedrows[0],0)).text())
            col1 = str((self.varstable.item(selectedrows[0],1)).text())
            table2 = str((self.varstable.item(selectedrows[1],0)).text())
            col2 = str((self.varstable.item(selectedrows[1],1)).text())
            
            if len(table1.split(',')) > 1 or len(table2.split(',')) > 1:
                msg = "Please select only non-interacted variables"
                QMessageBox.information(self, "Warning",
                                        msg,
                                        QMessageBox.Ok) 
            else:  
                selectedrows.sort()
                self.varstable.removeRow(selectedrows[0])
                self.varstable.removeRow(selectedrows[1]-1)
                self.varstable.insertRow(self.varstable.rowCount())
    
                tableitem = QTableWidgetItem()
                tableitem.setText(table1 + ',' + table2)
                tableitem.setFlags(tableitem.flags() & ~Qt.ItemIsEditable)
                self.varstable.setItem(self.varstable.rowCount()-1, 0, tableitem)
                
                varitem = QTableWidgetItem()
                varitem.setText(col1 + ',' + col2)
                varitem.setFlags(varitem.flags() & ~Qt.ItemIsEditable)
                self.varstable.setItem(self.varstable.rowCount()-1, 1, varitem)
        else:
            msg = "Please select only two variables"
            QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)            

    def genChecks(self):
        res = True
        return res
        

class ProbModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(ProbModWidget, self).__init__(parent)
        self.makeProbChoiceWidget()
        self.makeVarsWidget(0,1)
        self.intbutton.setVisible(False)
        #self.delbutton.setVisible(False)
    
    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res

class CountModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(CountModWidget, self).__init__(parent) 
        self.makeCountTypeWidget()
        self.makeChoiceWidget(1,0) 
        self.makeVarsWidget(1,1) 

    def makeCountTypeWidget(self):
        self.poiradio = QRadioButton(POI_MODEL)
        self.nbradio = QRadioButton(NEGBIN_MODEL)
        self.nbradio.setChecked(True)
        buttonlayout = QHBoxLayout()
        buttonlayout.addWidget(self.poiradio)
        buttonlayout.addWidget(self.nbradio)
        self.counttypewidget = QWidget(self)
        self.counttypewidget.setLayout(buttonlayout)
        
        self.odwidget = QWidget(self)
        odlayout = QHBoxLayout()
        self.odwidget.setLayout(odlayout)
        self.odlabel = QLabel("Overdispersion")
        odlayout.addWidget(self.odlabel)
        self.odline = LineEdit()
        self.odline.setFixedWidth(100) 
        odlayout.addWidget(self.odline)
               
        self.mainlayout.addWidget(self.counttypewidget,0,0,1,1,Qt.AlignLeft)
        self.mainlayout.addWidget(self.odwidget,0,1,1,1,Qt.AlignLeft)
        
        self.connect(self.nbradio, SIGNAL("toggled(bool)"), self.ctypeAction)
         
    def ctypeAction(self, checked):
        if checked:
            self.odline.setEnabled(True) 
        else:
            self.odline.setEnabled(False)
        self.emit(SIGNAL("completeChanged()"))  

    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res

class OrderedModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(OrderedModWidget, self).__init__(parent) 
        self.makeOrdTypeWidget()
        self.makeOrdChoiceWidget(1,0)
        self.makeVarsWidget(1,1) 

    def makeOrdTypeWidget(self):
        self.logradio = QRadioButton(LOGIT)
        self.probradio = QRadioButton(PROBIT)
        self.logradio.setChecked(True)
        buttonlayout = QHBoxLayout()
        buttonlayout.addWidget(self.logradio)
        buttonlayout.addWidget(self.probradio)
        self.ordtypewidget = QWidget(self)
        self.ordtypewidget.setLayout(buttonlayout)
               
        self.mainlayout.addWidget(self.ordtypewidget,0,0,1,1,Qt.AlignLeft)

    def makeOrdChoiceWidget(self,x=0,y=0):
        self.choicewidget = QWidget(self)
        self.choicelayout = QVBoxLayout()
        self.choicewidget.setLayout(self.choicelayout)
        
        self.choicebuttonwidget = QWidget(self)
        choicebuttonlayout = QHBoxLayout()
        self.choicebuttonwidget.setLayout(choicebuttonlayout)
        self.choiceaddbutton = QPushButton('Add Alternative')
        choicebuttonlayout.addWidget(self.choiceaddbutton)
        self.choicedelbutton = QPushButton('Delete Alternative')
        choicebuttonlayout.addWidget(self.choicedelbutton)
        self.choicelayout.addWidget(self.choicebuttonwidget)
        
        self.choicetable = QTableWidget(0,3,self)
        self.choicetable.setHorizontalHeaderLabels(['Alternative', 'Value', 'Threshold'])
        self.choicelayout.addWidget(self.choicetable)
        
        self.mainlayout.addWidget(self.choicewidget,x,y,1,1)
        
        self.connect(self.choiceaddbutton, SIGNAL("clicked(bool)"), self.addOrdChoice) 
        self.connect(self.choicedelbutton, SIGNAL("clicked(bool)"), self.delOrdChoice) 

    def addOrdChoice(self):
        self.choicetable.insertRow(self.choicetable.rowCount())
        self.choicetable.setItem(0,2,QTableWidgetItem())
        disableitem = self.choicetable.item(0, 2)
        disableitem.setFlags(disableitem.flags() & ~Qt.ItemIsEnabled)
        disableitem.setBackgroundColor(Qt.darkGray)

    def delOrdChoice(self):
        self.choicetable.removeRow(self.choicetable.currentRow())
        self.choicetable.setItem(0,2,QTableWidgetItem())
        disableitem = self.choicetable.item(0, 2)
        if disableitem != None:
            disableitem.setFlags(disableitem.flags() & ~Qt.ItemIsEnabled)
            disableitem.setBackgroundColor(Qt.darkGray)

    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res
        
class SFModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(SFModWidget, self).__init__(parent) 
        self.makeSFVarianceWidget()
        self.makeVarsWidget(1,0)  

    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res    

class MNLogitModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(MNLogitModWidget, self).__init__(parent)
        self.alternatives = []
        self.specs = {}
        self.curralt = None
        self.makeChoiceWidget() 
        self.makeVarsWidget() 
        #self.connect(self.choicetable, SIGNAL("currentItemChanged (QTableWidgetItem *,QTableWidgetItem *)"), self.showVarsTable)
        self.connect(self.choicetable, SIGNAL("currentCellChanged (int,int,int,int)"), self.showVarsTable)
        #self.connect(self.varstable, SIGNAL("cellChanged (int,int)"), self.storeVarsTable)
        
    def addVariable(self):
        sellist = self.choicetable.selectedIndexes() 
        if(len(sellist)!=1):
            msg = "Please select ONE alternative"
            QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)
        else:
            selaltitem = self.choicetable.itemFromIndex(sellist[0])
            if selaltitem == None:
                msg = "Please specify the selected alternative"
                QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)
            else:
                selalt = selaltitem.text()
                if selalt not in self.alternatives:
                    self.alternatives.append(selalt)
                super(MNLogitModWidget,self).addVariable()

    def showVarsTable(self,currrow,currcol,prevrow,prevcol):
        self.storeVarsTable(prevrow)
        #print 'change var table'
        self.varstable.clearContents()
        self.varstable.setRowCount(0)
        curritem = self.choicetable.item(currrow, 0)
        if curritem != None:
            selalt = str(curritem.text())
            self.curralt = selalt
            altspecs = self.specs[selalt]
            self.varstable.setRowCount(len(altspecs))
            i = 0
            while i < self.varstable.rowCount():
                altspecrow = altspecs[i]
                tableitem = QTableWidgetItem()
                tableitem.setText(altspecrow[0])
                self.varstable.setItem(i,0,tableitem)
                varitem = QTableWidgetItem()
                varitem.setText(altspecrow[1])
                self.varstable.setItem(i,1,varitem)
                coeffitem = QTableWidgetItem()
                coeffitem.setText(altspecrow[2])
                self.varstable.setItem(i,2,coeffitem)
                i = i + 1
        else:
            pass  

    def storeVarsTable(self,prevrow):
        #print 'store var table'
        storeitem = self.choicetable.item(prevrow, 0)
        if storeitem != None:
            selalt = str(storeitem.text())
            altspecs = []
            i = 0
            while i < self.varstable.rowCount():
                if self.varstable.item(i, 2) != None:
                    var = []
                    tab = (self.varstable.item(i, 0)).text()
                    col = (self.varstable.item(i, 1)).text()
                    coeff = (self.varstable.item(i, 2)).text()
                    var.append(tab)
                    var.append(col)
                    var.append(coeff)
                    altspecs.append(var)
                i = i + 1
            self.specs[selalt] = altspecs
        else:
            print 'storeitem is None'

#    def showVarsTable(self,curritem,previtem):
#        self.storeVarsTable(previtem)
#        print 'change var table'
#        self.varstable.clearContents()
#        self.varstable.setRowCount(0)
#        if curritem != None:
#            selalt = str(curritem.text())
#            self.curralt = selalt
#            altspecs = self.specs[selalt]
#            self.varstable.setRowCount(len(altspecs))
#            i = 0
#            while i < self.varstable.rowCount():
#                altspecrow = altspecs[i]
#                tableitem = QTableWidgetItem()
#                tableitem.setText(altspecrow[0])
#                self.varstable.setItem(i,0,tableitem)
#                varitem = QTableWidgetItem()
#                varitem.setText(altspecrow[1])
#                self.varstable.setItem(i,1,varitem)
#                coeffitem = QTableWidgetItem()
#                coeffitem.setText(altspecrow[2])
#                self.varstable.setItem(i,2,coeffitem)
#                i = i + 1
#        else:
#            pass    

#    def storeVarsTable(self,storeitem):
#        print 'store var table'
#        if storeitem != None:
#            selalt = str(storeitem.text())
#            print selalt
#            altspecs = []
#            i = 0
#            while i < self.varstable.rowCount():
#                if self.varstable.item(i, 2) != None:
#                    var = []
#                    tab = (self.varstable.item(i, 0)).text()
#                    col = (self.varstable.item(i, 1)).text()
#                    coeff = (self.varstable.item(i, 2)).text()
#                    var.append(tab)
#                    var.append(col)
#                    var.append(coeff)
#                    altspecs.append(var)
#                i = i + 1
#            self.specs[selalt] = altspecs
#        else:
#            print 'storeitem is None'


    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res

class GCMNLogitModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(GCMNLogitModWidget, self).__init__(parent) 
        #self.makeChoiceWidget()
        self.makeVarsWidget() 
        
    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res

class LogRegModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(LogRegModWidget, self).__init__(parent) 
        self.makeVarianceWidget()
        self.makeVarsWidget(1,0) 

    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        return res

class NLogitModWidget(AbstractModWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(NLogitModWidget, self).__init__(parent) 
        self.alternatives = []
        self.specs = {}
        self.curralt = None
        self.makeNestWidget()
        self.makeChoiceWidget(0, 1)
        self.makeVarsWidget(0, 2) 
        self.connect(self.choicetable, SIGNAL("currentItemChanged (QTableWidgetItem *,QTableWidgetItem *)"), self.showVarsTable) 
        #self.connect(self.varstable, SIGNAL("itemSelectionChanged()"), self.printSelection) 

    def addVariable(self):
        sellist = self.choicetable.selectedIndexes() 
        if(len(sellist)!=1):
            msg = "Please select ONE alternative"
            QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)
        else:
            selaltitem = self.choicetable.itemFromIndex(sellist[0])
            if selaltitem == None:
                msg = "Please specify the selected alternative"
                QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok)
            else:
                selalt = selaltitem.text()
                if selalt not in self.alternatives:
                    self.alternatives.append(selalt)
                super(NLogitModWidget,self).addVariable()

    def showVarsTable(self,curritem,previtem):
        self.storeVarsTable(previtem)
        print 'change var table'
        self.varstable.clearContents()
        self.varstable.setRowCount(0)
        if curritem != None:
            selalt = str(curritem.text())
            self.curralt = selalt
            altspecs = self.specs[selalt]
            self.varstable.setRowCount(len(altspecs))
            i = 0
            while i < self.varstable.rowCount():
                altspecrow = altspecs[i]
                tableitem = QTableWidgetItem()
                tableitem.setText(altspecrow[0])
                self.varstable.setItem(i,0,tableitem)
                varitem = QTableWidgetItem()
                varitem.setText(altspecrow[1])
                self.varstable.setItem(i,1,varitem)
                coeffitem = QTableWidgetItem()
                coeffitem.setText(altspecrow[2])
                self.varstable.setItem(i,2,coeffitem)
                i = i + 1
        else:
            pass    

    def storeVarsTable(self,storeitem):
        print 'store var table'
        if storeitem != None:
            selalt = str(storeitem.text())
            altspecs = []
            i = 0
            while i < self.varstable.rowCount():
                if self.varstable.item(i, 2) != None:
                    var = []
                    tab = (self.varstable.item(i, 0)).text()
                    col = (self.varstable.item(i, 1)).text()
                    coeff = (self.varstable.item(i, 2)).text()
                    var.append(tab)
                    var.append(col)
                    var.append(coeff)
                    altspecs.append(var)
                i = i + 1
            self.specs[selalt] = altspecs


    def checkInputs(self):
        res = True
        res = res and self.genChecks()
        
        ivnests = []
        cnests = []
        i = 0
        while i < self.nesttable.rowCount():
            ivnests.append(str((self.nesttable.item(i, 0)).text()))
            i = i + 1         
        print ivnests
        i = 0
        while i < self.choicetable.rowCount():
            ch = (self.choicetable.item(i, 0)).text()
            chdet = ch.split('/')
            if len(chdet)>1:
                for j in range(len(chdet)-1):
                    cnests.append(str(chdet[j]))
            i = i + 1
        print cnests
        
        if len(cnests) == 0:
            self.errmsg = 'The choices do not have a nested structure\n'
            return False   
                
        badn = []
        for cn in cnests:
            if cn not in ivnests:
                badn.append(cn)
        if len(badn) > 0:
            self.errmsg = 'Please specify the IV parameters for the following nests:\n' + str(badn) + '\n'
            return False

        badn = []
        for ivn in ivnests:
            if ivn not in cnests:
                badn.append(ivn)
        if len(badn) > 0:
            self.errmsg = 'Please specify the following nests in the alternatives table:\n' + str(badn) + '\n'
            return False

        return res    

                
    
   