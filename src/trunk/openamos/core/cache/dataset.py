import tables as t
import time

from numpy import unique
from numpy.ma import zeros, masked_equal, ones
from openamos.core.cache.dataset_table_layouts import *

class DB(object):
    def __init__(self, fileLoc, mode='w'):
        self.fileh = t.openFile("%s/amosdb.h5" %(fileLoc), mode=mode)

    """
        self.groupDict = {'households_r':'households',
                          'vehicles_r':'households',
                          'person_r':'persons',
                          'tsp_r':'persons',
                          'scehulde_r':'persons',
                          'trips_r':'persons'}

        # TODO: where do we get the table definitions and relationships from
        # for now this is static
        self.tableDefDict = {'households_r':['houseid, numvehs'],
                             'vehicles_r':['houseid', 'vehid', 'vehtype'],
                             'person_r':['persons'],
                             'tsp_r':'persons',
                             'scehulde_r':'persons',
                             'trips_r':'persons'}
    """    
    def create(self, tableName=None):
        # TODO: create output/input tables everytime?

        # Output Tables - Creating groups
        output_grp = self.fileh.createGroup(self.fileh.root, "output_grp")
        # Input Tables - Creating groups
        input_grp = self.fileh.createGroup(self.fileh.root, "input_grp")

        # Output Tables - Creating the table
        self.fileh.createTable(output_grp, "vehicles_r", Vehicles_R)
        self.fileh.createTable(output_grp, "households_r", Households_R)
        self.fileh.createTable(output_grp, "tsp_r", Tsp_R)
        self.fileh.createTable(output_grp, "schedule_r", Schedule_R)
        self.fileh.createTable(output_grp, "schedule_ltrec_r", Schedule_R)
        self.fileh.createTable(output_grp, "workers_r", Workers_R)

        #Input Tables - Creatign the table
        self.fileh.createTable(input_grp, "travel_skims1", Travel_Skims)
        self.fileh.createTable(input_grp, "travel_skims2", Travel_Skims)


    def close(self):
        self.fileh.close()
        
    def returnGroup(self, tableName):
        if tableName[-2:] == "_r":
            return 'output'
        else:
            return 'input'


    def returnTableReference(self, tableName):
        tableName = tableName.lower()
        grp = self.returnGroup(tableName)
        loc = '/%s_grp' %(grp)
        return self.fileh.getNode(loc, name=tableName)


    def returnTypeConversion(self, tableName):
        tableRef = self.returnTableReference(tableName)
        colDtypes = tableRef.coldtypes

        uniqColDtypes = list(set(colDtypes.values()))

        convType = ""
        for i in uniqColDtypes:
            if i.kind in "iu":
                convType = "int"
            if i.kind in "f":
                convType = "float"
                return convType
        return convType

        

    def createSkimsTableFromDatabase(self, tableInfo, queryBrowser):
        t = time.time()

	tableName = tableInfo.tableName

	colsList = []
	colsList.append(tableInfo.origin_var)
	colsList.append(tableInfo.destination_var)
	colsList.append(tableInfo.skims_var)

        data = queryBrowser.select_all_from_table(tableName, colsList)
        print '\tTotal time taken to retrieve records from the database %.4f' %(time.time()-t)

        cols = data.varnames
        colIndices = range(data.cols)
        
        tableRef = self.returnTableReference(tableName)
        tableRow = tableRef.row


        for i in data.data:
            for j in colIndices:
                #if i[j] is not None:
                #    tableRow[cols[j]] = i[j]
                tableRow[cols[j]] = i[j]
            tableRow.append()
        tableRef.flush()
        print '\tTime taken to write to hdf5 format %.4f' %(time.time()-t)
        

    def returnTableAsMatrix(self, tableName, originColName, destinationColName, skimColName, fillValue=9999):
        tableRef = self.returnTableReference(tableName)
        
        origin = tableRef.col(originColName)
        destination = tableRef.col(destinationColName)
        skims = tableRef.col(skimColName)

        # Initialize matrix
        skimsMatrix = ones((max(origin)+1, max(destination)+1)) * fillValue

        # Populate matrix
        skimsMatrix[origin, destination] = skims
	#skimsMatrix = masked_equal(skimsMatrix, 9999)
        
        return masked_equal(skimsMatrix, 9999), unique(origin)


    
if __name__ == '__main__':
    db = DB('w')
    db.create()
    table = db.returnTableReference('households_r')
