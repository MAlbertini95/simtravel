import sys
import multiprocessing
import argparse

from openamos.core.run.simulation_manager_cursor import SimulationManager
from openamos.core.errors import ArgumentsError

parser = argparse.ArgumentParser(description="OpenAMOS Run Module")
parser.add_argument('-file', help='specifies the location of the configuration file', 
			default='../configs/mag_zone/config_before_malta.xml', type=str)
parser.add_argument('-it', help='this attribute specifies the iteration count; a integer value', 
			default=1, type=int)
parser.add_argument('-crca', help="""this attribute specifies whether cache needs to be """\
				     """created; default is 1 to create a cache """\
				     """and any other integer value does not create a new cache""", 
			default=1, type=int)
parser.add_argument('-bkup', help="""this attribute specifies whether the cache and the skim tables as """\
				     """specified in the config file need to be backed up """\
				     """; default is 0 to not backup """\
				     """and a value of 1 creates a backup""", 
			default=0, type=int)


argsG = vars(parser.parse_args(sys.argv[1:]))
print argsG


def run(fileLoc=None):
    """
    Runs the OpenAMOS program to simulate the activity-travel choices as 
    indicated by the models and their specifications in the config file.

    Please refer to OpenAMOS documentation on www.simtravel.wikispaces.asu.edu
    for guidance on setting up the configuration file.
    """
    print 'File location is %s'%fileLoc, sys.argv
    
    if fileLoc is None:
	fileLoc = argsG['file']	
	

    iteration = argsG['it']
    create_cache = argsG['crca']
    backup_results = argsG['bkup']

    print ("""Project attributes:\n\tFile location - %s \n\tIteration count - %s """\
		"""\n\tCreate cache - %s \n\tBackup results - %s""" 
		%(fileLoc, iteration, create_cache, backup_results))

    simulationManagerObject = SimulationManager(fileLoc = fileLoc, iteration=iteration)

    queryBrowser = simulationManagerObject.setup_databaseConnection()
    if create_cache == 1:
	#raw_input('creating new cache')
        simulationManagerObject.setup_cacheDatabase()
	simulationManagerObject.setup_inputCacheTables()
	simulationManagerObject.setup_outputCacheTables()
    else:
	#raw_input('reading old cache')
	simulationManagerObject.read_cacheDatabase()
    simulationManagerObject.setup_tod_skims()	
    simulationManagerObject.setup_location_information(queryBrowser)
    simulationManagerObject.close_database_connection(queryBrowser)

    simulationManagerObject.parse_config()
    simulationManagerObject.clean_database_tables()
    simulationManagerObject.run_components()
    simulationManagerObject.close_cache_connection()
    if backup_results == 1:
	simulationManagerObject.setup_resultsBackup()


"""
    else:
        numParts = int(args[2])
        simulationManagerObject = SimulationManager(fileLoc = fileLoc)
        simulationManagerObject.divide_database(numParts)
        simulationManagerObject.parse_config()
        simulationManagerObject.clean_database_tables()
	
	
	simulationManagerObject.setup_cacheDatabase()
	simulationManagerObject.setup_inputCacheTables()
    	queryBrowser = simulationManagerObject.setup_databaseConnection()
	simulationManagerObject.setup_tod_skims()
    	simulationManagerObject.setup_location_information(queryBrowser)
    	simulationManagerObject.close_database_connection(queryBrowser)    
	

	# Everything related to parts from here on ....
        partsList = range(numParts)

	# Creating the output cache branches
	for partId in partsList:
            simulationManagerObject.setup_outputCacheTables(partId+1)
	    simulationManagerObject.clean_database_tables(partId+1)

       
        #Multiprocessing
        pool = multiprocessing.Pool()
        print partsList
        argsParallel = [(fileLoc, i+1) for i in partsList]
        print argsParallel

        pool.map(run_components_in_parallel, argsParallel)
        
        simulationManagerObject.collate_results(numParts)
        

def run_components_in_parallel(args):
    print args
    
    fileLoc = args[0]
    partId = args[1]
    simulationManagerObject = SimulationManager(fileLoc = fileLoc)
    simulationManagerObject.read_cacheDatabase()
    simulationManagerObject.parse_config()
    simulationManagerObject.run_components(partId)
    simulationManagerObject.close_cache_connection()
    
"""

if __name__ == "__main__":
    sys.exit(run())
