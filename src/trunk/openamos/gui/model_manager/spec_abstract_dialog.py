'''
Created on Apr 19, 2010

@author: bsana
'''

import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from lxml import etree

from openamos.gui.env import *
from spec_model_widgets import *

from openamos.core.database_management.database_connection import *
from openamos.core.database_management.database_configuration import *

class AbtractSpecDialog(QDialog):
    '''
    classdocs
    '''

    def __init__(self, configobject, key, title = '', parent=None):
        super(AbtractSpecDialog, self).__init__(parent)
        
        self.setWindowTitle(title)
        
        self.glayout = QGridLayout()
        self.setLayout(self.glayout)
        
        self.modeltypegb = QGroupBox("Model Type")
        modeltypegblayout = QVBoxLayout()
        self.modeltypegb.setLayout(modeltypegblayout)
        self.modeltypecb = QComboBox()
        self.modeltypecb.addItems([QString(PROB_MODEL), QString(COUNT_MODEL),
                                   QString(SF_MODEL), QString(LOGREG_MODEL),
                                   QString(GC_MNL_MODEL), QString(MNL_MODEL),
                                   QString(ORD_MODEL),QString(NL_MODEL)])
        modeltypegblayout.addWidget(self.modeltypecb)
        self.glayout.addWidget(self.modeltypegb,0,0)
        
        self.configobject = configobject
        self.modelkey = key
        self.populateFromDatabase()
        print key
        
        
        self.subpopgb = QGroupBox("Sub-Population")
        self.subpopgb.setCheckable(True)
        subpoplayout = QGridLayout()
        self.subpopgb.setLayout(subpoplayout)
        tablelabel = QLabel("Table")
        subpoplayout.addWidget(tablelabel,0,0)
        self.subpoptab = QComboBox()
        self.subpoptab.addItems(self.tablelist)
        subpoplayout.addWidget(self.subpoptab,1,0)
        varlabel = QLabel("Column")
        subpoplayout.addWidget(varlabel,0,1)
        self.subpopvar = QComboBox()
        subpoplayout.addWidget(self.subpopvar,1,1)
        oplabel = QLabel("Operator")
        subpoplayout.addWidget(oplabel,0,2)          
        self.subpopop = QComboBox()
        self.subpopop.addItems([QString(OP_EQUAL), QString(OP_NOTEQUAL),
                                QString(OP_GT), QString(OP_LT),
                                QString(OP_GTE), QString(OP_LTE)])
        subpoplayout.addWidget(self.subpopop,1,2)
        vallabel = QLabel("Value")  
        subpoplayout.addWidget(vallabel,0,3)          
        self.subpopval = LineEdit()
        subpoplayout.addWidget(self.subpopval,1,3)
        subpoplayout.setColumnStretch(0,1)
        subpoplayout.setColumnStretch(1,1)
        subpoplayout.setColumnStretch(2,1)
        subpoplayout.setColumnStretch(3,1)
        self.glayout.addWidget(self.subpopgb,1,0)
    
        

        self.modwidget = QWidget()
        self.glayout.addWidget(self.modwidget,2,0)
        
        self.dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.glayout.addWidget(self.dialogButtonBox,3,0)
        
        self.connect(self.modeltypecb, SIGNAL("currentIndexChanged(int)"), self.changeModelWidget)
        self.connect(self.subpoptab, SIGNAL("currentIndexChanged(int)"), self.populateColumns)
        self.connect(self.dialogButtonBox, SIGNAL("accepted()"), self.storeSpec)
        self.connect(self.dialogButtonBox, SIGNAL("rejected()"), SLOT("reject()"))
        
        self.loadFromConfigObject()


    
    def loadFromConfigObject(self):
        modelspecified = self.configobject.modelSpecInConfig(self.modelkey)
        if modelspecified is not None:
            form = modelspecified.get(FORMULATION)
            if form == MODELFORM_REG:
                type = modelspecified.get(MODELTYPE)
                if type == SF_MODEL:
                    modtxt = SF_MODEL
                elif type == LOGREG_MODEL:
                    modtxt = LOGREG_MODEL
            elif form == MODELFORM_CNT:
                modtxt = MODELFORM_CNT
                type = modelspecified.get(MODELTYPE)
            elif form == MODELFORM_ORD:
                modtxt = ORD_MODEL
                type = modelspecified.get(MODELTYPE)
            elif form == MODELFORM_MNL:
                type = modelspecified.get(MODELTYPE)
                if type == ALTSPEC:
                    modtxt = MNL_MODEL
                else:
                    modtxt = GC_MNL_MODEL
            elif form == MODELFORM_NL:
                modtxt = NL_MODEL
                            
            ind = self.modeltypecb.findText(modtxt)
            self.modeltypecb.setCurrentIndex(ind)
            
        self.changeModelWidget()
        self.populateColumns()
        
        
        if modelspecified is not None:
            self.populateRununtilWidget(modelspecified)
            self.populateFilterWidget(modelspecified)
            
            if self.modeltypecb.currentText() == SF_MODEL:
                self.populateVarsWidget(modelspecified)
                for varianceelt in modelspecified.getiterator(VARIANCE):
                    if MODELTYPE in varianceelt.keys():
                        self.modwidget.varianceuline.setText(varianceelt.get(VALUE))
                    else:
                        self.modwidget.variancevline.setText(varianceelt.get(VALUE)) 
            if self.modeltypecb.currentText() == COUNT_MODEL:
                self.populateVarsWidget(modelspecified)
                self.populateAltsWidget(modelspecified)
                if type == NEGBIN_MODEL:
                    varianceelt = modelspecified.find(VARIANCE)
                    self.modwidget.odline.setText(varianceelt.get(VALUE))
                else:
                    self.modwidget.poiradio.setChecked(True)
            if self.modeltypecb.currentText() == ORD_MODEL:
                self.populateVarsWidget(modelspecified)
                self.populateOrdAltsWidget(modelspecified)
                if type == PROBIT:
                    self.modwidget.probradio.setChecked(True)
            if self.modeltypecb.currentText() == GC_MNL_MODEL:
                self.populateVarsWidget(modelspecified)
                self.populateAltsWidget(modelspecified)
            if self.modeltypecb.currentText() == MNL_MODEL:
                self.populateAltsWidget(modelspecified)
                self.modwidget.specs = {}
                for altelt in modelspecified.getiterator(ALTERNATIVE):
                    altspecs = []
                    for varelt in altelt.getiterator(VARIABLE):
                        varspec = []
                        varspec.append(varelt.get(TABLE))
                        varspec.append(varelt.get(COLUMN))
                        varspec.append(varelt.get(COEFF))
                        altspecs.append(varspec)
                    self.modwidget.specs[altelt.get(ID)] = altspecs
            if self.modeltypecb.currentText() == NL_MODEL:
                self.modwidget.specs = {}
                for altelt in modelspecified.getiterator(ALTERNATIVE):
                    altstable = self.modwidget.choicetable
                    altstable.insertRow(altstable.rowCount())
            
                    altitem = QTableWidgetItem()
                    alt = altelt.get(ID)
                    altbranch = altelt.get(BRANCH)
                    if altbranch != 'root':
                        alt = (altbranch.split('/',1))[1] + '/' + alt
                    altitem.setText(alt)
                    altstable.setItem(altstable.rowCount()-1, 0, altitem)
                    
                    altspecs = []
                    for varelt in altelt.getiterator(VARIABLE):
                        varspec = []
                        varspec.append(varelt.get(TABLE))
                        varspec.append(varelt.get(COLUMN))
                        varspec.append(varelt.get(COEFF))
                        altspecs.append(varspec)
                    self.modwidget.specs[alt] = altspecs
                for neselt in modelspecified.getiterator(BRANCH):
                    nestable = self.modwidget.nesttable
                    nestable.insertRow(nestable.rowCount())
                    nesname = QTableWidgetItem()
                    nesname.setText(neselt.get(NAME))
                    nestable.setItem(nestable.rowCount()-1, 0, nesname) 
                    nescoeff = QTableWidgetItem()
                    nescoeff.setText(neselt.get(COEFF))
                    nestable.setItem(nestable.rowCount()-1, 1, nescoeff)
                    
    def populateRununtilWidget(self,modelelt):
        temp = modelelt.find(RUNUNTIL)
        if temp <> None:
            for rununtil in modelelt.getiterator(RUNUNTIL):
                self.runtable = rununtil.get(TABLE)
                self.runvar = rununtil.get(COLUMN)
                self.runcond = rununtil.get(COND)
                self.runtablev = rununtil.get(VTABLE)
                self.runvarv = rununtil.get(VCOLUMN)
            
    def populateFilterWidget(self,modelelt):
        temp = modelelt.find(FILTER)
        if temp <> None:
            for filt in modelelt.getiterator(FILTER):
                ind = self.subpoptab.findText(filt.get(TABLE))
                self.subpoptab.setCurrentIndex(ind)
                ind = self.subpopvar.findText(filt.get(COLUMN))
                self.subpopvar.setCurrentIndex(ind)
                ind = self.subpopop.findText(filt.get(COND))
                self.subpopop.setCurrentIndex(ind)                
                self.subpopval.setText(filt.get(VALUE))
        else:
            self.subpopgb.setChecked(False)
            
#        for filt in modelelt.getiterator(FILTER):
#            ind = self.subpoptab.findText(filt.get(TABLE))
#            self.subpoptab.setCurrentIndex(ind)
#            ind = self.subpopvar.findText(filt.get(COLUMN))
#            self.subpopvar.setCurrentIndex(ind)
#            ind = self.subpopop.findText(filt.get(COND))
#            self.subpopop.setCurrentIndex(ind)                
#            self.subpopval.setText(filt.get(VALUE))
    
    def populateVarsWidget(self,modelelt):
        for varelt in modelelt.getiterator(VARIABLE):
            varstable = self.modwidget.varstable
            varstable.insertRow(varstable.rowCount())
            
            tableitem = QTableWidgetItem()
            tableitem.setText(varelt.get(TABLE))
            tableitem.setFlags(tableitem.flags() & ~Qt.ItemIsEditable)
            varstable.setItem(varstable.rowCount()-1, 0, tableitem)

            varitem = QTableWidgetItem()
            varitem.setText(varelt.get(COLUMN))
            varitem.setFlags(varitem.flags() & ~Qt.ItemIsEditable)
            varstable.setItem(varstable.rowCount()-1, 1, varitem)

            coeffitem = QTableWidgetItem()
            coeffitem.setText(varelt.get(COEFF))
            varstable.setItem(varstable.rowCount()-1, 2, coeffitem)

    def populateAltsWidget(self,modelelt):
        for altelt in modelelt.getiterator(ALTERNATIVE):
            altstable = self.modwidget.choicetable
            altstable.insertRow(altstable.rowCount())
            
            altitem = QTableWidgetItem()
            altitem.setText(altelt.get(ID))
            altstable.setItem(altstable.rowCount()-1, 0, altitem)

            altvalue = QTableWidgetItem()
            altvalue.setText(altelt.get(VALUE))
            altstable.setItem(altstable.rowCount()-1, 1, altvalue)

    def populateOrdAltsWidget(self,modelelt):
        i = 0
        for altelt in modelelt.getiterator(ALTERNATIVE):
            altstable = self.modwidget.choicetable
            altstable.insertRow(altstable.rowCount())
            
            altitem1 = QTableWidgetItem()
            altitem1.setText(altelt.get(ID))
            altstable.setItem(altstable.rowCount()-1, 0, altitem1)
            altitem2 = QTableWidgetItem()
            altitem2.setText(altelt.get(VALUE))
            altstable.setItem(altstable.rowCount()-1, 1, altitem2)
            if i > 0:
                thitem = QTableWidgetItem()
                thitem.setText(altelt.get(THRESHOLD))
                altstable.setItem(altstable.rowCount()-1, 2, thitem)
            else:
                altstable.setItem(0,2,QTableWidgetItem())
                disableitem = altstable.item(0, 2)
                disableitem.setFlags(disableitem.flags() & ~Qt.ItemIsEnabled)
                disableitem.setBackgroundColor(Qt.darkGray)
            i = i+1
            
    
    def changeModelWidget(self, idx=0):
        self.subpoptab.setCurrentIndex(0)
        self.subpopop.setCurrentIndex(0)
        self.subpopval.clear()  
          
        self.modwidget.setParent(None)
        if self.modeltypecb.currentText() == PROB_MODEL:
            self.modwidget = ProbModWidget(self)
        elif self.modeltypecb.currentText() == COUNT_MODEL:
            self.modwidget = CountModWidget(self)
        elif self.modeltypecb.currentText() == MNL_MODEL:
            self.modwidget = MNLogitModWidget(self)
        elif self.modeltypecb.currentText() == GC_MNL_MODEL:
            self.modwidget = GCMNLogitModWidget(self)
        elif self.modeltypecb.currentText() == SF_MODEL:
            self.modwidget = SFModWidget(self)
        elif self.modeltypecb.currentText() == LOGREG_MODEL:
            self.modwidget = LogRegModWidget(self)
        elif self.modeltypecb.currentText() == ORD_MODEL:
            self.modwidget = OrderedModWidget(self)
        elif self.modeltypecb.currentText() == NL_MODEL:
            self.modwidget = NLogitModWidget(self)
        
        self.glayout.addWidget(self.modwidget,2,0)
        self.update()


    def populateColumns(self, idx=0):
        self.subpopvar.clear()
        seltab = str(self.subpoptab.currentText())
        self.subpopvar.addItems(self.coldict[seltab])
        
        
    
    def storeSpec(self):
        if self.checkInputs():
            modelkey = self.modelkey
    
            modelelt = None
    
            if self.modeltypecb.currentText() == SF_MODEL:
                modelform = MODELFORM_REG
                otherattr = None
                if modelkey == MODELKEY_DAYSTART:
                    otherattr = VERTEX,START
                if modelkey == MODELKEY_DAYEND:
                    otherattr = VERTEX,END
                modelelt = self.createModelElement(modelkey,modelform,SF_MODEL,otherattr)
                self.addDepVarToElt(modelelt, modelkey)
                self.addFiltToElt(modelelt)
                variancevelt = etree.SubElement(modelelt, VARIANCE)
                variancevelt.set(VALUE,str(self.modwidget.variancevline.text()))
                varianceuelt = etree.SubElement(modelelt, VARIANCE)
                varianceuelt.set(VALUE,str(self.modwidget.varianceuline.text()))
                varianceuelt.set(MODELTYPE,'Half Normal')
                self.addVariables(modelelt)
                
            elif self.modeltypecb.currentText() == COUNT_MODEL:
                modelform = MODELFORM_CNT
                type = ""
                if self.modwidget.nbradio.isChecked():
                    type = NEGBIN_MODEL
                else:
                    type = POI_MODEL
                modelelt = self.createModelElement(modelkey,modelform,type)
                self.addDepVarToElt(modelelt, modelkey)
                self.addFiltToElt(modelelt)
                if type == NEGBIN_MODEL:
                    varianceelt = etree.SubElement(modelelt, VARIANCE)
                    varianceelt.set(VALUE,str(self.modwidget.odline.text()))
                    varianceelt.set(MODELTYPE,'Overdispersion') 
                self.addAlternatives(modelelt)
                self.addVariables(modelelt) 
    
            elif self.modeltypecb.currentText() == ORD_MODEL:
                modelform = MODELFORM_ORD
                type = ""
                if self.modwidget.logradio.isChecked():
                    type = LOGIT
                else:
                    type = PROBIT
                modelelt = self.createModelElement(modelkey,modelform,type)
                self.addDepVarToElt(modelelt,modelkey)
                self.addFiltToElt(modelelt)
                #Add ordered choice alternatives with thresholds
                numrows = self.modwidget.choicetable.rowCount()
                for i in range(numrows):
                    altname = (self.modwidget.choicetable.item(i,0)).text()
                    altelt = etree.SubElement(modelelt,ALTERNATIVE)
                    altelt.set(ID,str(altname))
                    altvalue = (self.modwidget.choicetable.item(i,1)).text()
                    altelt.set(VALUE,str(altvalue))
                    if i > 0:
                        threshval = (self.modwidget.choicetable.item(i,2)).text()
                        altelt.set(THRESHOLD,str(threshval))
                
                self.addVariables(modelelt) 
    
            elif self.modeltypecb.currentText() == GC_MNL_MODEL:
                modelform = MODELFORM_MNL
                modelelt = self.createModelElement(modelkey,modelform,'')
                self.addDepVarToElt(modelelt,modelkey)
                self.addFiltToElt(modelelt)
                
                #self.addAlternatives(modelelt)
                self.addVariables(modelelt)
            
            elif self.modeltypecb.currentText() == MNL_MODEL:
                self.modwidget.storeVarsTable(self.modwidget.choicetable.currentRow()) #self.modwidget.choicetable.currentItem())
                modelform = MODELFORM_MNL
                type = ALTSPEC
                modelelt = self.createModelElement(modelkey,modelform,type)
                self.addDepVarToElt(modelelt,modelkey)
                self.addRununtilToElt(modelelt)
                self.addFiltToElt(modelelt)
                
                numrows = self.modwidget.choicetable.rowCount()
                specs = self.modwidget.specs
                for i in range(numrows):
                    altname = str((self.modwidget.choicetable.item(i,0)).text())
                    altvalue = str((self.modwidget.choicetable.item(i,1)).text())
                    altelt = etree.SubElement(modelelt,ALTERNATIVE)
                    altelt.set(ID,altname)
                    altelt.set(VALUE,altvalue)
                    altspecs = specs[altname]
                    numvars = len(altspecs)
                    for i in range(numvars):
                        specrow = altspecs[i]
                        self.addVariabletoElt(altelt,specrow[0],specrow[1],specrow[2])
                    modelelt.append(altelt)   
                
            
            elif self.modeltypecb.currentText() == NL_MODEL:
                self.modwidget.storeVarsTable(self.modwidget.choicetable.currentItem())
                modelform = MODELFORM_NL
                modelelt = self.createModelElement(modelkey,modelform,'')
                self.addDepVarToElt(modelelt,modelkey)
                self.addFiltToElt(modelelt)
                
                numrows = self.modwidget.choicetable.rowCount()
                specs = self.modwidget.specs
                for i in range(numrows):
                    altname = str((self.modwidget.choicetable.item(i,0)).text())
                    altdet = altname.rsplit('/',1)
                    l = len(altdet)
                    if l==1:
                        altid = altdet[0]
                        altbr = 'root'
                    if l>1:
                        altid = altdet[1]
                        altbr = 'root/' + altdet[0]
                    altelt = etree.SubElement(modelelt,ALTERNATIVE)
                    altelt.set(ID,altid)
                    altelt.set(BRANCH,altbr)
                    altspecs = specs[altname]
                    numvars = len(altspecs)
                    for i in range(numvars):
                        specrow = altspecs[i]
                        self.addVariabletoElt(altelt,specrow[0],specrow[1],specrow[2])
                    modelelt.append(altelt)  
                numnests = self.modwidget.nesttable.rowCount()
                for i in range(numnests):
                    nestname = str((self.modwidget.nesttable.item(i,0)).text())
                    nestiv = str((self.modwidget.nesttable.item(i,1)).text())
                    neselt = etree.SubElement(modelelt,BRANCH)
                    neselt.set(NAME,nestname)
                    neselt.set(COEFF,nestiv)
                    modelelt.append(neselt)
                                      
            elif self.modeltypecb.currentText() == LOGREG_MODEL:
                modelform = MODELFORM_REG
                modelelt = self.createModelElement(modelkey,modelform,'')
                self.addDepVarToElt(modelelt,modelkey)
                self.addFiltToElt(modelelt)
                self.addVariables(modelelt)
                #pass
    
            
            self.configobject.addModelElement(modelelt)
            
            QDialog.accept(self)
        #else:
            #msg = self.modwidget.errmsg
            #QMessageBox.information(self, "Warning", msg, QMessageBox.Ok)
            #QMessageBox.warning(self, "Warning", "The value must be numeric, or greater than or equal to zero in the Sub-Population.")            

    
    def createModelElement(self,name,formulation,type,otherattr=None):
        elt = etree.Element(MODEL)
        elt.set(NAME,name)
        elt.set(FORMULATION,formulation)
        elt.set(MODELTYPE,type)
        if otherattr != None:
            elt.set(otherattr[0],otherattr[1])
        return elt

    def addDepVarToElt(self,elt,col):
        depvarelt = etree.SubElement(elt,DEPVARIABLE)
#        if col in PERSON_TABLE_MODELS:
#            tab = TABLE_PER
#        elif col in HH_TABLE_MODELS:
#            tab = TABLE_HH
#        depvarelt.set(TABLE,tab)
        depvarelt.set(COLUMN,col.lower())
        
    def addRununtilToElt(self,elt):
        if self.runtable <> "" and self.runtable <> None:
            runelt = etree.SubElement(elt,RUNUNTIL)
            runelt.set(TABLE,str(self.runtable))
            runelt.set(COLUMN,str(self.runvar))
            runelt.set(COND,str(self.runcond))
            runelt.set(VTABLE,str(self.runtablev))
            runelt.set(VCOLUMN,str(self.runvarv))
    
    def addFiltToElt(self,elt):
        if self.subpopgb.isChecked():
            if (str(self.subpopval.text()) != ''):
                filterelt = etree.SubElement(elt,FILTER)
                filterelt.set(TABLE,str(self.subpoptab.currentText()))
                filterelt.set(COLUMN,str(self.subpopvar.currentText()))
                filterelt.set(COND,str(self.subpopop.currentText()))
                filterelt.set(VALUE,str(self.subpopval.text()))

    def addAlternatives(self,elt):
        numrows = self.modwidget.choicetable.rowCount()
        for i in range(numrows):
            altname = (self.modwidget.choicetable.item(i,0)).text()
            altvalue = (self.modwidget.choicetable.item(i,1)).text()
            altelt = etree.SubElement(elt,ALTERNATIVE)
            altelt.set(ID,str(altname))
            altelt.set(VALUE,str(altvalue))

    def addVariables(self,elt):
        numrows = self.modwidget.varstable.rowCount()
        for i in range(numrows):
            tablename = (self.modwidget.varstable.item(i,0)).text()
            colname = (self.modwidget.varstable.item(i,1)).text()
            coeff = (self.modwidget.varstable.item(i,2)).text()
            self.addVariabletoElt(elt,tablename,colname,coeff)
        
    def addVariabletoElt(self,elt,tablename,colname,coeff):
        variableelt = etree.SubElement(elt, VARIABLE)
        variableelt.set(TABLE,str(tablename))
        variableelt.set(COLUMN,str(colname))
        variableelt.set(COEFF,str(coeff))
    
    def populateFromDatabase(self):
        self.protocol = self.configobject.getConfigElement(DB_CONFIG,DB_PROTOCOL)        
        self.user_name = self.configobject.getConfigElement(DB_CONFIG,DB_USER)
        self.password = self.configobject.getConfigElement(DB_CONFIG,DB_PASS)
        self.host_name = self.configobject.getConfigElement(DB_CONFIG,DB_HOST)
        self.database_name = self.configobject.getConfigElement(DB_CONFIG,DB_NAME)
        self.database_config_object = DataBaseConfiguration(self.protocol, self.user_name, self.password, self.host_name, self.database_name)
        
        new_obj = DataBaseConnection(self.database_config_object)
        new_obj.new_connection()
        tables = new_obj.get_table_list()
        
        self.tablelist = []
        self.coldict = {}
        for table in tables:
            self.tablelist.append(QString(table))
            cols = new_obj.get_column_list(table)
            varlist = []
            for col in cols:
                varlist.append(QString(col))
            self.coldict[table] = varlist
            
    def checkFloat(self,num):
        res = False
        try:
            temp = float(num)
            res = True
        except:
            res = False
        
        return res
    
    
    def checkInput_table1(self):
        numrows = self.modwidget.choicetable.rowCount()
        for i in range(numrows):
            
            if self.modwidget.choicetable.item(i,1) == None:
                    QMessageBox.warning(self, "Warning", "The value of an alternative must be numeric.")
                    return False
                
            coeff = unicode((self.modwidget.choicetable.item(i,1)).text())
            if not self.checkFloat(coeff):
                QMessageBox.warning(self, "Warning", "The value of an alternative must be numeric.")
                return False
#            else:
#                if float(coeff) < 0.0:
#                    QMessageBox.warning(self, "Warning", "The value of an alternative must be greater than or equal to zero.")
#                    return False
                
        return True
    
    
    def checkInput_table2(self):
        numrows = self.modwidget.varstable.rowCount()
        for i in range(numrows):
            
            if self.modwidget.varstable.item(i,2) == None:
                    QMessageBox.warning(self, "Warning", "Coefficient must be numeric.")
                    return False
                
            coeff = unicode((self.modwidget.varstable.item(i,2)).text())
            if not self.checkFloat(coeff):
                QMessageBox.warning(self, "Warning", "Coefficient must be numeric.")
                return False
#            else:
#                if float(coeff) < 0.0:
#                    QMessageBox.warning(self, "Warning", "Coefficient must be greater than or equal to zero.")
#                    return False
                
        return True
    
    
    def checkInputs(self):
        
        res = True
        
        if self.subpopgb.isChecked():
            subvalue = unicode(self.subpopval.text())
            if not self.checkFloat(subvalue):
                QMessageBox.warning(self, "Warning", "The value must be numeric in the Sub-Population.")
                return False
            else:
                if float(subvalue) < 0.0:
                    QMessageBox.warning(self, "Warning", "The value must be positive in the Sub-Population.")
                    return False

                
        if self.modeltypecb.currentText() == PROB_MODEL:
            numrows = self.modwidget.choicetable.rowCount()
            for i in range(numrows):
                
                if self.modwidget.choicetable.item(i,1) == None:
                    QMessageBox.warning(self, "Warning", "The value of an alternative must be entered as a number.")
                    return False
                    
                colname = unicode((self.modwidget.choicetable.item(i,1)).text())
                if not self.checkFloat(colname):
                    QMessageBox.warning(self, "Warning", "The value of an alternative must be numeric.")
                    return False
                else:
                    if float(colname) < 0.0:
                        QMessageBox.warning(self, "Warning", "The value of an alternative must be greater than or equal to zero.")
                        return False
                
                if self.modwidget.choicetable.item(i,2) == None:
                    QMessageBox.warning(self, "Warning", "Probability must be entered between 0.0 and 1.0.")
                    return False
                
                coeff = unicode((self.modwidget.choicetable.item(i,2)).text())
                if self.checkFloat(coeff):
                    coeff1 = float(coeff)
                    if coeff1 < 0.0 or coeff1 > 1.0:
                        QMessageBox.warning(self, "Warning", "Probability must be between 0.0 and 1.0.")
                        return False
                else:
                    QMessageBox.warning(self, "Warning", "Probability must be numeric.")
                    return False
                                   
        elif self.modeltypecb.currentText() == COUNT_MODEL:
            
            dispersion = unicode(self.modwidget.odline.text())
            if self.modwidget.odline.isEnabled():
                if not self.checkFloat(dispersion):
                    QMessageBox.warning(self, "Warning", "Overdispersion must be numeric.")
                    return False
                else:
                    if float(dispersion) < 0.0:
                        QMessageBox.warning(self, "Warning", "Overdispersion must be greater than or equal to zero.")
                        return False
            
            if not self.checkInput_table1():
                return False
            
            if not self.checkInput_table2():
                return False
            
        elif self.modeltypecb.currentText() == SF_MODEL:
            
            variancev = unicode(self.modwidget.variancevline.text())
            if not self.checkFloat(variancev):
                QMessageBox.warning(self, "Warning", "Variance (v) - Normal must be numeric.")
                return False
            else:
                if float(variancev) < 0.0:
                    QMessageBox.warning(self, "Warning", "Variance (v) - Normal must be greater than or equal to zero.")
                    return False
                
            varianceu = unicode(self.modwidget.varianceuline.text())
            if not self.checkFloat(varianceu):
                QMessageBox.warning(self, "Warning", "Variance (u) - Half Normal must be numeric.")
                return False
            else:
                if float(varianceu) < 0.0:
                    QMessageBox.warning(self, "Warning", "Variance (u) - Half Normal must be greater than or equal to zero.")
                    return False
                
            if not self.checkInput_table2():
                return False
            
        elif self.modeltypecb.currentText() == GC_MNL_MODEL:
            
            if not self.checkInput_table2():
                return False
            
        elif self.modeltypecb.currentText() == MNL_MODEL:
            
            if not self.checkInput_table1():
                return False
            
#            if not self.checkInput_table2():
#                return False
            
            numrows = self.modwidget.choicetable.rowCount()
            specs = self.modwidget.specs
            for i in range(numrows):
                altname = str((self.modwidget.choicetable.item(i,0)).text())
                altspecs = specs[altname]
                numvars = len(altspecs)
                for i in range(numvars):
                    specrow = altspecs[i]
                    print specrow[2]
                    if not self.checkFloat(specrow[2]):
                        QMessageBox.warning(self, "Warning", "The value of a coefficient must be numeric.")
                        return False
                    
            
        elif self.modeltypecb.currentText() == ORD_MODEL:
            
            numrows = self.modwidget.choicetable.rowCount()
            for i in range(numrows):
                
                if self.modwidget.choicetable.item(i,1) == None:
                    QMessageBox.warning(self, "Warning", "The value of an alternative must be entered as a number.")
                    return False
                
                value = unicode((self.modwidget.choicetable.item(i,1)).text())
                if not self.checkFloat(value):
                    QMessageBox.warning(self, "Warning", "The value of an alternative must be numeric.")
                    return False
                else:
                    if float(value) < 0.0:
                        QMessageBox.warning(self, "Warning", "The value of an alternative must be greater than or equal to zero.")
                        return False
                
#                if self.modwidget.choicetable.item(i,2) == None:
#                    QMessageBox.warning(self, "Warning", "Threshold must be entered as a number greater than 0.0.")
#                    return False
                
                if i > 0:
                    thresh = unicode((self.modwidget.choicetable.item(i,2)).text())
                    if self.checkFloat(thresh):
                        if float(thresh) < 0.0:
                            QMessageBox.warning(self, "Warning", "Threshold must be greater than or equal to 0.0.")
                            return False
#                        else:
#                            QMessageBox.warning(self, "Warning", "Threshold must be numeric.")
#                            return False
                    else:
                        QMessageBox.warning(self, "Warning", "Threshold must be numeric.")
                        return False
                            
                
            if not self.checkInput_table2():
                return False
            
        elif self.modeltypecb.currentText() == NL_MODEL:
            
            if not self.checkInput_table1():
                return False
            
            if not self.checkInput_table2():
                return False
            
        elif self.modeltypecb.currentText() == LOGREG_MODEL:
            
            if not self.checkInput_table2():
                return False           
        
        
        return res
#        res = False
#        if self.modwidget.checkInputs():
#            res = True
#        return res

    


def main():
    app = QApplication(sys.argv)
    config = None
    diag = AbtractSpecDialog(config)
    diag.show()
    app.exec_()

if __name__=="__main__":
    main()        
        