from PyQt4.QtCore import *
from PyQt4.QtGui import *
from spec_abstract_dialog import *
from openamos.gui.env import *



class LongTermModels(QWidget):
    def __init__(self, parent=None, co=None):
        super(LongTermModels, self).__init__(parent)
        self.setWindowTitle('Long_Term_Choices')
        self.setAutoFillBackground(True)
        size =  parent.geometry()
     
        # These two global variables are used in paintevent.
        global widgetwidth, widgetheight
        widgetwidth = size.width()
        widgetheight = size.height()
        
        generate_synthetic_population_button = QPushButton('Generate Synthetic \nPopulation', self)
        generate_synthetic_population_button.setGeometry((size.width())/2 - 100, size.height() / 2 - 400,200, 50)
        self.connect(generate_synthetic_population_button, SIGNAL('clicked()'), self.synthetic_population)
#        self.connect(generate_synthetic_population_button, SIGNAL('clicked()'),
#                     qApp, SLOT('deleteLater()'))

        
        labor_force_participation_model_button = QPushButton('If worker status was not \n generated then run a Labor \n Force Participation Model to \n simulate the worker status \n individuals', self)
        labor_force_participation_model_button.setGeometry((size.width())/2 - 100, size.height() / 2 - 320, 200, 110)
        self.connect(labor_force_participation_model_button, SIGNAL('clicked()'), self.labor_force)

        
        number_of_jobs_button = QPushButton('For each worker identify \n the number of jobs', self)
        number_of_jobs_button.setGeometry((size.width())/2 - 100, size.height() / 2 - 180, 200, 50)
        self.connect(number_of_jobs_button, SIGNAL('clicked()'), self.number_jobs)


        primary_worker_button = QPushButton('Primary worker in the \nhousehold \n\nIn the absence of data \nidentified based on personal \nincome', self)
        primary_worker_button.setGeometry((size.width())/2 - 100, size.height() / 2 - 100, 200, 130)
        self.connect(primary_worker_button, SIGNAL('clicked()'), self.primary_worker)


        school_status_button  = QPushButton('School status of everyone \nincluding those individuals \nthat are workers', self)
        school_status_button.setGeometry((size.width())/2 - 100, size.height() / 2 + 60, 200, 70)
        self.connect(school_status_button, SIGNAL('clicked()'), self.school_status)


        residential_location_choice_button  = QPushButton('Residential Location Choice', self)
        residential_location_choice_button.setGeometry((size.width())/2 - 100, size.height() / 2 + 160, 200, 50)
        self.connect(residential_location_choice_button, SIGNAL('clicked()'), self.residential_location)
        
        self.configob = co
        
        
    def synthetic_population(self):
        diagtitle = COMPMODEL_SYNTHPOP
        modelkey = MODELKEY_SYNTHPOP
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def labor_force(self):
        diagtitle = COMPMODEL_WORKSTAT
        modelkey = MODELKEY_WORKSTAT
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def number_jobs(self):
        diagtitle = COMPMODEL_NUMJOBS
        modelkey = MODELKEY_NUMJOBS
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def primary_worker(self):
        diagtitle = COMPMODEL_PRIMWORK
        modelkey = MODELKEY_PRIMWORK
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def school_status(self):
        diagtitle = COMPMODEL_SCHSTAT
        modelkey = MODELKEY_SCHSTAT
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        
        
    def residential_location(self):
        diagtitle = COMPMODEL_RESLOC
        modelkey = MODELKEY_RESLOC
        
        diag = AbtractSpecDialog(self.configob,modelkey,diagtitle)
        diag.exec_()
        

    def paintEvent(self, parent = None):
        # Drawing line
        line = QPainter()
        line.begin(self)
        pen = QPen(Qt.black,2,Qt.SolidLine)
        line.setPen(pen)
        line.drawLine((widgetwidth) / 2, widgetheight / 2 - 350, (widgetwidth) / 2, widgetheight / 2 + 160)
        line.end()
        # Drawing arrow
        arrow = QPainter()
        arrow.begin(self)
        point = QPoint()

        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 - 320)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 - 180)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 - 100)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 + 60)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))

        point.setX(widgetwidth / 2)  
        point.setY(widgetheight / 2 + 160)
        arrow.setBrush(QColor("black"))
        arrow.drawPolygon(QPoint(point.x(),point.y()),QPoint(point.x() - 4,point.y() - 13), QPoint(point.x() + 4,point.y() - 13))


        arrow.end()



 


