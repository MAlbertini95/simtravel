#main class. this class will be used to define the database connection.
#it will create/drop database, schema and tables
 

#include all the import 
import sys
import os
import exceptions
import time
import sqlalchemy
import psycopg2 as dbapi2
import numpy as na
import time
from cursor_database_connection import DataBaseConnection
from psycopg2 import extensions
from sqlalchemy.types import Integer, SmallInteger, \
			                 Numeric, Float, \
            			     VARCHAR, String, CLOB, Text,\
			                 Boolean, DateTime
from numpy import array, ma
from database_configuration import DataBaseConfiguration
#from data_array import DataArray

class DivideData(object):
    #initialize the class 

    def __init__(self,dbconfig):
        
        if not isinstance(dbconfig, DataBaseConfiguration):
            raise DatabaseConfigurationError, """The dbconfig input is not a valid """\
                """DataBaseConfiguration object."""

        self.protocol = dbconfig.protocol
        self.user_name = dbconfig.user_name
        self.password = dbconfig.password
        self.host_name = dbconfig.host_name
        self.database_name = dbconfig.database_name
        self.database_config_object = dbconfig
        self.dbcon_obj = DataBaseConnection(dbconfig)
        print self.dbcon_obj
        
        #input table names
        self.house_tab = 'households'
        self.persons_tab = 'persons'

        #output tables names
        self.child_tab = 'child_dependency_r'
        self.school_tab = 'daily_school_status_r'
        self.work_tab = 'daily_work_status_r'
        self.veh_count_tab = 'households_vehicles_count_r'
        self.ltrec_tab = 'schedule_ltrec_r'
        self.schedule_tab = 'schedule_r'
        self.trips_tab = 'trips_r'
        self.veh_tab = 'vehicles_r'
        self.workers_tab = 'workers_r'


    #create dummy databases
    def dummy_db(self, dbname, number):
        """
        This method is used to create the dummy databases.
        This method is called before any other method in this class
        
        Input:
        Number of dummy databases
        
        Output:
        Dummy databases created
        """
        #database name
        db_name = dbname
        db_str = ''
        t1 = time.time()
       
        for each in range(number):
            db_str = db_name + '_' + str(each)
            self.dbcon_obj.database_name = db_str
            result = self.dbcon_obj.create_database(db_str)
            result = result * result
        
        self.dbcon_obj.database_name = dbname

        t2 = time.time()
        print 'Total time taken to create new databases %s'%(t2-t1)

        if result:
            return 'true'
        else:
            return 'false'


    #get the datatypes and primary keys
    def get_tab_structure(self, table_name):
        """
        This method is used to get the data types and the primary keys
        
        Input:
        Database configuration object and table name
        
        Output:
        List of datatypes and primary keys
        """
        #get the columns
        cols = self.dbcon_obj.get_column_list(table_name)
        
        #get the data types of the columns
        data_type = self.dbcon_obj.get_column_types(table_name)
        
        #get the keys of the table
        keys = self.dbcon_obj.get_table_keys(table_name)
        
        #generate the list for the keys
        key_list = []
        for column in cols:
            key_list.append(0)
            
        for key in keys:
            index = cols.index(key)
            key_list[index] = 1
        
        #key list created. return the required
        return cols, data_type, key_list
        

    #get the columns and then create the list of datatypes and keys
    def get_table_info(self):
        """
        This method is used to get the table information
        
        Input:
        
        Output:
        
        """     
        #get info for all tables and store them in variable
        #input tables
        self.house_cols, self.house_dt, self.house_keys = self.get_tab_structure(self.house_tab)
        self.persons_cols, self.persons_dt, self.persons_keys = self.get_tab_structure(self.persons_tab)
        
        #output tables
        self.child_cols, self.child_dt, self.child_keys = self.get_tab_structure(self.child_tab)
        self.school_cols, self.school_dt, self.school_keys = self.get_tab_structure(self.school_tab)
        self.work_cols, self.work_dt, self.work_keys = self.get_tab_structure(self.work_tab)
        self.veh_count_cols, self.veh_count_dt, self.veh_count_keys = self.get_tab_structure(self.veh_count_tab)
        self.ltrec_cols, self.ltrec_dt, self.ltrec_keys = self.get_tab_structure(self.ltrec_tab)
        self.schedule_cols, self.schedule_dt, self.schedule_keys = self.get_tab_structure(self.schedule_tab)
        self.trips_cols, self.trips_dt, self.trips_keys = self.get_tab_structure(self.trips_tab)
        self.veh_cols, self.veh_dt, self.veh_keys = self.get_tab_structure(self.veh_tab)
        self.workers_cols, self.workers_dt, self.workers_keys = self.get_tab_structure(self.workers_tab)


    #create db and tables based on the parts
    def create_partitions(self, databasename, chunks):
        """
        This method is used to create db's and tables based on the 
        the number of chunks.
        
        Input:
        Database configuration object and chunks
        
        Output:
        Databases and tables created
        """
        #database name
        db_name = databasename
        
        #databases are created. add tables to each
        #run a loop the create the new table names
        t1 = time.time()
        for each in range(chunks):
            db_str = db_name + '_' + str(each)
            self.dbcon_obj.database_name = db_str

            #create a new database connection
            self.dbcon_obj.new_connection()
            
            #create the tables
            self.dbcon_obj.create_table(self.house_tab, self.house_cols, self.house_dt, self.house_keys)
            self.dbcon_obj.create_table(self.persons_tab, self.persons_cols, self.persons_dt, self.persons_keys)
            self.dbcon_obj.create_table(self.child_tab, self.child_cols, self.child_dt, self.child_keys)
            self.dbcon_obj.create_table(self.school_tab, self.school_cols, self.school_dt, self.school_keys)
            self.dbcon_obj.create_table(self.work_tab, self.work_cols, self.work_dt, self.work_keys)
            self.dbcon_obj.create_table(self.veh_count_tab, self.veh_count_cols, self.veh_count_dt, self.veh_count_keys)
            self.dbcon_obj.create_table(self.ltrec_tab, self.ltrec_cols, self.ltrec_dt, self.ltrec_keys)
            self.dbcon_obj.create_table(self.schedule_tab, self.schedule_cols, self.schedule_dt, self.schedule_keys)
            self.dbcon_obj.create_table(self.trips_tab, self.trips_cols, self.trips_dt, self.trips_keys)
            self.dbcon_obj.create_table(self.veh_tab, self.veh_cols, self.veh_dt, self.veh_keys)
            self.dbcon_obj.create_table(self.workers_tab, self.workers_cols, self.workers_dt, self.workers_keys)
            
            #close the database connection
            self.dbcon_obj.close_connection()
        
        #assign the old database name to the config obj
        self.dbcon_obj.database_name = databasename
        
        t2 = time.time()
        print 'Total time taken to create new tables in the databases %s'%(t2-t1)

    
    #get row count of the table
    def get_count(self, table_name, column_name):
        """
        This method is used to get the max of houseid from the table specified.

        Input:
        Class name corresponding to the table and column name

        Output:
        Returns all the rows in the table
        """
        #check if table exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        
        sql_string = "SELECT max(%s) FROM %s"%(column_name, table_name)

        if tab_flag:
            try:    
                self.dbcon_obj.cursor.execute(sql_string)
                result = self.dbcon_obj.cursor.fetchall()
                res = []
                for each in result:
                    res.append(each[0])
                return res[0]
            except Exception, e:
                print 'Error while retreiving the data from the table'
                print e
        else:
            print 'Table %s does not exist.'%table_name
            

    #divide the rows
    def divide_rows(self, parts):
        """
        This method divides the rows in the households tables
        
        Input:
        Number of parts
        
        Output:
        Intervals
        """
        tab = 'households'
        col = 'houseid'
        total = self.get_count(tab, col)

        interval_list = []
        interval = total/parts
        for each in range(parts-1):
            next_val = interval * (each+1)
            interval_list.append(next_val)
        interval_list.append(total)

        return interval_list
           
  
    #select rows based on a selection criteria
    def get_interval_rows(self, databasename, table1, table2, column_name, interval_list, index):
        """
        This method is used to get selected rows between the interval 
        from the table in the database.

        Input:
        Database configuration object, class name and selection criteria.

        Output:
        Returns the rows that satisfy the selection criteria
        """
        #create a new database connection
        self.dbcon_obj.new_connection()
        
        fin_flag = None
        #check if table exists and then if columns exists
        tab_flag1 = self.dbcon_obj.check_if_table_exists(table1)
        tab_flag2 = self.dbcon_obj.check_if_table_exists(table2)
        if tab_flag1 == tab_flag2:
            fin_flag = True
        else:
            fin_flag = False

        #declare the interval
        if index == 0:
            low = 1
            high = interval_list[index]
        else:
            low = interval_list[index-1] + 1
            high = interval_list[index]
            
        t1 = time.time()
        #get the rows from households table
        sql_string1 = "SELECT * FROM %s WHERE %s BETWEEN %s AND %s"%(table1, column_name, low, high)
        sql_string2 = "SELECT * FROM %s WHERE %s BETWEEN %s AND %s"%(table2, column_name, low, high)
        
        if fin_flag:
            try:
                self.dbcon_obj.cursor.execute(sql_string1)
                house_data = self.dbcon_obj.cursor.fetchall()
    
                self.dbcon_obj.cursor.execute(sql_string2)
                person_data = self.dbcon_obj.cursor.fetchall()
                
                house_rows = []
                person_rows = []
                count1 = 0
                count2 = 0
                
                for each in house_data:
                    count1 = count1 + 1
                    house_rows.append(each)
                for each in person_data:
                    count2 = count2 + 1
                    person_rows.append(each)
                    
                #close the new database connection
                self.dbcon_obj.close_connection()
                
                if count1 == 0 or count2 == 0:
                    print 'No rows selected.\n'           
                print 'Select query successful.\n'
                return house_rows, person_rows
            except Exception, e:
                print 'Error retrieving the information. Query failed.\n'
                print e
        else:
            print 'Table(s) do not belong to the database.'
            #close the new database connection
            self.dbcon_obj.close_connection()
            
            t2 = time.time()
            print 'Total time taken to select the required rows %s'%(t2-t1)
            return None    
        
    
    #trial insert query
    def insert_data(self, databasename, arr, table_name, index):
        """
        This method is used to insert data into the table
        
        Input:
        Array of the values and the table name
        
        Output:
        Data inserted into the table
        """
        db_name = databasename
        #open a new connection to the required database
        db_str = db_name + '_' + str(index)
        self.dbcon_obj.database_name = db_str
        
        t1 = time.time()
        
        #create a new database connection
        self.dbcon_obj.new_connection()
        
        #table = 'temp_households'
        cols = self.dbcon_obj.get_column_list(table_name)
        col_str = ''
        col_count = 0
        for i in cols:
            if col_count < (len(cols)-1):
                col_str = col_str + i + ', '
                col_count = col_count + 1
            else:
                col_str = col_str + i

        arr_str = [tuple(each) for each in arr]
        arr_str = str(arr_str)[1:-1]
        arr_str = arr_str.replace('L', '')
        
        sql_string = 'insert into %s (%s) values %s'%(table_name, col_str, arr_str)

        t1 = time.time()
        try:
            self.dbcon_obj.cursor.execute(sql_string)
            self.dbcon_obj.connection.commit()
        except Exception, e:
            print e
        
        t2 = time.time()
        print 'total taken to insert %s'%(t2-t1)
        
        #close the new database connection
        self.dbcon_obj.close_connection()
        
        #assign old database name
        self.dbcon_obj.database_name = databasename
        
        t2 = time.time()
        print 'Total time taken to insert records %s'%(t2-t1)
        
        
    #copy the data from a csv file
    def copy_data(self, databasename, table_name1, table_name2, index, location):
        """
        This method copies the data from a csv file into the 
        persons and households table
        
        Input:
        
        Output:
        """
        db_name = databasename
        #open a new connection to the required database
        db_str = db_name + '_' + str(index)
        self.dbcon_obj.database_name = db_str

        #create a new database connection
        self.dbcon_obj.new_connection()
        
        #check if the table exists
        tab_flag1 = self.dbcon_obj.check_if_table_exists(table_name1)
        tab_flag2 = self.dbcon_obj.check_if_table_exists(table_name2)
        if tab_flag1 == tab_flag2:
            try:
                #for the first table
                t1 = time.time()
                insert_stmt = ("""copy %s from '%s/households.csv' """
                               """ delimiters ',' csv header""" %(table_name1, location))
                result = self.dbcon_obj.cursor.execute(insert_stmt)
                self.dbcon_obj.connection.commit()
                t2 = time.time()
                print 'Time taken to copy %s -- %s'%(table_name1, (t2-t1))
                
                #for the second table
                t1 = time.time()
                insert_stmt = ("""copy %s from '%s/persons.csv' """
                               """delimiters ',' csv header"""%(table_name2, location))
                result = self.dbcon_obj.cursor.execute(insert_stmt)
                self.dbcon_obj.connection.commit()
                t2 = time.time()
                print 'Time taken to copy %s -- %s'%(table_name2, (t2-t1))
                
            except Exception, e:
                print e
        else:
           print 'Table(s) do not exist.'

        #close the new database connection
        self.dbcon_obj.close_connection()
        
        #assign old database name
        self.dbcon_obj.database_name = databasename

        
    #delete unwanted records
    def delete_records(self, databasename, table1, table2, column_name, index, interval_list):
        """
        This method is used to delete selected rows between the interval 
        from the table in the database.

        Input:
        Database configuration object, class name and selection criteria.

        Output:
        Returns the rows that satisfy the selection criteria
        """
        fin_flag = None
        db_name = databasename
        
        #open a new connection to the required database
        db_str = db_name + '_' + str(index)
        #print db_str
        self.dbcon_obj.database_name = db_str

        #create a new database connection
        self.dbcon_obj.new_connection()
        
        #check if table exists and then if columns exists
        tab_flag1 = self.dbcon_obj.check_if_table_exists(table1)
        tab_flag2 = self.dbcon_obj.check_if_table_exists(table2)
        
        if tab_flag1 == tab_flag2:
            fin_flag = True
        else:
            fin_flag = False

        #declare the interval
        if index == 0:
            low = 1
            high = interval_list[index]
        else:
            low = interval_list[index-1] + 1
            high = interval_list[index]
        #get the rows from households table
        sql_string1 = "DELETE FROM %s WHERE %s NOT BETWEEN %s AND %s"%(table1, column_name, low, high)
        sql_string2 = "DELETE FROM %s WHERE %s NOT BETWEEN %s AND %s"%(table2, column_name, low, high)
        
        if fin_flag:
            try:
                t1 = time.time()
                self.dbcon_obj.cursor.execute(sql_string1)
                self.dbcon_obj.connection.commit()
    
                self.dbcon_obj.cursor.execute(sql_string2)
                self.dbcon_obj.connection.commit()
                t2 = time.time()
                print 'Total time taken to delete the unwanted rows %s'%(t2-t1)
            except Exception, e:
                print e
        else:
            print 'Table(s) do not exist.'
            
        #close the new database connection
        self.dbcon_obj.close_connection()
        
        #assign old database name
        self.dbcon_obj.database_name = databasename
        
        
    #partition the data in the newly created tables
    def partition_data(self, parts, location, table1, table2, column_name):
        """
        This method runs a loop and divides all the data
        
        Input:
        Number of partitions
        
        Output:
        
        """
        #declare the lists
        house_rows = []
        person_rows = []
        
        #create the dummy databases
        res = self.dummy_db(self.dbcon_obj.database_name, parts)
        print '---> dummy databases created'
        
        #open a connection to current database and get the table information
        self.dbcon_obj.new_connection()
        print '----> new connection created'
        
        #call the get table info to fetch all data and save it
        self.get_table_info()
        print '---> table info fetched'
        
        #get the interval data
        interval_list = self.divide_rows(parts)
        print '---> divide rows complete'
        
        #close the connection to the database
        self.dbcon_obj.close_connection()
        print '---> connection closed'

        #create new tables in the databases
        self.create_partitions(self.database_name, parts)
        print '---> partitions created'
        
        """
        To divide the data into chunks and distribute it in the new databases, 
        use the functions in the pairs as mentioned
        
        1) get_interval_rows() and insert_data()
                            OR
        2) copy_data() and delete_records()
        for the copy_data() method the households and persons table have to be 
        exported as a csv file and the location should be assigned where the 
        file is located
        """
        #run a loop to copy data and delete the rows
        print 'Loop starts.'
        t1 = time.time()
        for index in range(parts):
            #select the required data
            house_rows, person_rows = self.get_interval_rows(self.database_name, table1, table2, column_name, interval_list, index)
            
            #insert the selected data into the required tables
            self.insert_data(self.database_name, house_rows, table1, index)
            self.insert_data(self.database_name, person_rows, table2, index)
            
            #copy all the data into the new data
            #self.copy_data(self.database_name, table1, table2, index, location)
        
            #delete the unwanted rows
            #self.delete_records(self.database_name, table1, table2, column_name, index, interval_list)
            
        print 'Loop ended'
        t2 = time.time()
        print 'Total time taken by main function %s'%(t2-t1)
        
        #return interval_list
        print 'Done'
        
                        
#unit test to test the code
import unittest

#define a class for testing
class TestDivideData(unittest.TestCase):
    #only initialize objects here
    def setUp(self):
        self.protocol = 'postgres'		
        self.user_name = 'postgres'
        self.password = '1234'
        self.host_name = 'localhost'
        self.database_name = 'mag_zone'

    
    def testdividedata(self):
        """ definitions for config class and create objects """
        dbconf = DataBaseConfiguration(self.protocol, self.user_name, self.password, self.host_name, self.database_name)
        newobject = DivideData(dbconf)
        
        print 'Start program'
        
        """ Call main function """
        parts = 4
        location = '/home/namrata/Documents/threads'
        table1 = 'households'
        table2 = 'persons'
        column_name = 'houseid'
        index = 0
        count = 0
        print '\t Parts are %s and Database name is %s'%(parts, self.database_name)
        print '\t Location is %s'%location
        print '\t Table 1 is %s, Table 2 is %s and Column name is %s'%(table1, table2,column_name)
        
        #main function to divide and distribute the data
        newobject.partition_data(parts, location, table1, table2, column_name)

        print 'End of program'
        

if __name__ == '__main__':
    unittest.main()
