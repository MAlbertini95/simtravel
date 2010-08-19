CONFIG_XML = 'config.xml'
PROJECT_CONFIG = 'ProjectConfig'
PROJECT_NAME = 'ProjectName'
PROJECT_HOME = 'ProjectHome'
DB_CONFIG = 'DBConfig'
DB_PROTOCOL = 'protocol'
DB_HOST = 'dbhost'
DB_USER = 'dbusername'
DB_PASS = 'dbpassword'
DB_NAME = 'DBName'
POSTGRES = 'postgres'

MODELCONFIG = 'ModelConfig'
COMP = 'Component'
MODEL = 'Model'
NAME = 'name'
FORMULATION = 'formulation'
MODELTYPE = 'type'
FILTER = 'Filter'
VERTEX = 'vertex'
START = 'start'
END = 'end'
VARIANCE = 'Variance'
VARIABLE = 'Variable'
ALTERNATIVE = 'Alternative'
DEPVARIABLE = 'DependentVariable'
VALUE = 'value'
TABLE = 'table'
COLUMN = 'var'
COND = 'condition'
COEFF = 'coeff'
ID = 'id'
THRESHOLD = 'threshold'
ALTSPEC = 'Alternative Specific'
BRANCH = 'Branch'

PROB_MODEL = 'Probability Distribution'
COUNT_MODEL = 'Count'
MNL_MODEL = 'Multinomial Logit'
GC_MNL_MODEL = 'Multinomial Logit (Generic Choices)'
ORD_MODEL = 'Ordered Choice'
NL_MODEL = 'Nested Logit'
SF_MODEL = 'Stochastic Frontier'
LOGREG_MODEL = 'Logistic Regression'
NEGBIN_MODEL = 'Negative Binomial'
POI_MODEL = 'Poisson'
LOGIT = 'Logit'
PROBIT = 'Probit'

MODELFORM_REG = 'Regression'
MODELFORM_ORD = 'Ordered'
MODELFORM_MNL = 'Multinomial Logit'
MODELFORM_CNT = 'Count'
MODELFORM_NL = 'Nested Logit'

OP_EQUAL = 'equals'
OP_NOTEQUAL = 'not equals'
OP_GT = 'greater than'
OP_GTE = 'greater than equals'
OP_LT = 'less than'
OP_LTE = 'less than equals'

TABLE_HH = 'households'
TABLE_PER = 'persons'

COMP_LONGTERM = 'Long Term Choices'
COMP_FIXEDACTLOCATION = 'Fixed Activity Location Choices'
COMP_VEHOWN = 'Vehicle Ownership Model'
COMP_FIXEDACTPRISM = 'Fixed Activity Prism Generator'
COMP_CHILDSTATUS = 'Child Daily Status and Allocation Model'
COMP_ADULTSTATUS = 'Adult Daily Status Model'
COMP_ACTSKELRECONCILIATION = 'Activity Skeleton Reconciliation System'
COMP_ACTTRAVSIMULATOR = 'Activity Travel Pattern Simulator'
COMP_ACTTRAVRECONCILIATION = 'Activity Travel Reconciliation System'

COMPKEY_LONGTERM = 'LongTermModels'
COMPKEY_VEHOWN = 'VehicleOwnershipModels'
COMPKEY_FIXEDACTPRISM = 'FixedActivityPrismModels'
COMPKEY_CHILDSTATUS = 'ChildStatusAllocationModels'


COMPMODEL_WORKSTAT = 'Worker Status'
COMPMODEL_NUMJOBS = 'Number of Jobs'
COMPMODEL_PRESCHSTAT = 'School Status: Ages 0 - 4'
COMPMODEL_SCHSTAT1 = 'School Status: Ages 5 - 14'
COMPMODEL_SCHSTAT2 = 'School Status: Ages 15 and over'
COMPMODEL_RESLOC = 'Residential Location Choice'
COMPMODEL_WORKLOC = 'Work Location Choice'
COMPMODEL_PRESCHLOC = 'PreSchool Location: Ages 0 - 4'
COMPMODEL_SCHLOC1 = 'School Location: Ages 5 - 14'
COMPMODEL_SCHLOC2 = 'School Location: Ages 15 and over'
COMPMODEL_NUMVEHS = 'Household Vehicle Counts'
COMPMODEL_NUMTYPES = 'Household Vehicle Types'
COMPMODEL_DAYSTART = 'Daily Prism Start'
COMPMODEL_DAYEND = 'Daily Prism End'
COMPMODEL_NUMWRKEPISODES = 'Number of Work Episodes'
COMPMODEL_WORKSTART1 = 'Work Prism 1 Start'
COMPMODEL_WORKEND1 = 'Work Prism 1 End'
COMPMODEL_WORKSTART2 = 'Work Prism 2 Start'
COMPMODEL_WORKEND2 = 'Work Prism 2 End'
COMPMODEL_NUMSCHEPISODES = 'Number of School Episodes'
COMPMODEL_SCHSTART1 = 'School Prism 1 Start'
COMPMODEL_SCHEND1 = 'School Prism 1 End'
COMPMODEL_SCHSTART2 = 'School Prism 2 Start'
COMPMODEL_SCHEND2 = 'School Prism 2 End'
COMPMODEL_PRESCHSTART = 'PreSchool Prism Start'
COMPMODEL_PRESCHEND = 'PreSchool Prism End'
COMPMODEL_PRESCHDAILYSTAT = 'PreSchool Daily Status'
COMPMODEL_SCHDAILYSTAT = 'School Daily Status: Ages 5 - 17'
COMPMODEL_SCHDAILYINDEP = 'School Daily Independence: Ages 5 - 17'
COMPMODEL_AFTSCHDAILYINDEP = 'After School Daily Independence: Ages 5 - 17'
COMPMODEL_AFTSCHACTSTAT = 'After School Activity Status: Ages 5 - 17'
COMPMODEL_AFTSCHACTTYPE = 'After School Activity Type: Ages 0 - 17'
COMPMODEL_AFTSCHACTDEST = 'After School Activity Destination: Ages 0 - 17'
COMPMODEL_AFTSCHACTDUR = 'After School Activity Duration: Ages 0 - 17'
COMPMODEL_WRKDAILYSTAT = 'Work Daily Status'
COMPMODEL_AFTSCHACTMODE = 'After School Activity Mode for Dependent Children'
COMPMODEL_ACTTYPE = 'Activity Type'
COMPMODEL_ACTDEST = 'Activity Destination'
COMPMODEL_ACTDUR = 'Activity Duration'
COMPMODEL_FIXEDACTMODE = 'Fixed Activity Mode'
COMPMODEL_JOINTACT = 'Joint Activity'
COMPMODEL_TRIPVEH = 'Trip Vehicle'
#Child Daily Status and Allocation Model
COMPMODEL_CSCHILD017 = 'Children (0-17 years old)'
COMPMODEL_CSCHILDSCH1 = 'Children (Status \55 School)'
COMPMODEL_CSCHILDPRE1 = 'Children (Status \55 Pre-school)'
COMPMODEL_CSCHILDSTA = 'Children (Status \55 Stay home)'
COMPMODEL_CSSCHPRE = 'Is the child going to School or Pre-school today?'
COMPMODEL_CSINDCHILD = 'Can the child engage in activities independently?'
COMPMODEL_CSCHILDIND = 'Child can engage in activities independently like adults'
COMPMODEL_CSASSIGN = 'Assign the child to household'
COMPMODEL_CSCHILDSCH2 = 'Children (Status \55 School)'
COMPMODEL_CSCHILDPRE2 = 'Children (Status \55 Pre-school)'
COMPMODEL_CSINSCHTO = 'Does the child travel independently to school?'
COMPMODEL_CSMODETOSCH = 'Travel Mode to School'
COMPMODEL_CSDROPOFF = 'Assign a drop-off event to household'
COMPMODEL_CSINSCHFROM = 'Does the child travel independently from school?'
COMPMODEL_CSMODEFROMSCH = 'Travel Mode from School'
COMPMODEL_CSPICKUP = 'Assign a pick-up event to household'
COMPMODEL_CSINAFTER = 'Activity pursued independently after school?'
COMPMODEL_CSTREAT = 'Treat the child like an adult and generate activity-travel patterns'
COMPMODEL_CSISTHERE = 'Is there time to engage in an after school CHILD activity?'
COMPMODEL_CSACTTYPE = 'Activity Type\Choice Destination Choice\Activity Duration Choice'
COMPMODEL_CSWORKSTAT = 'Flag the child as a dependent and the child engages in activity with an adult'
COMPMODEL_CSMOREACT = 'More activities'
COMPMODEL_CSRETURNH = 'Return Home'
COMPMODEL_CSMOVEADULT = 'Move to Adult Daily Status'
#Adult Daily Status Model
COMPMODEL_ASISDEPEND = 'Is a dependent child/children assigned to household including stay home and chauffeuring activities?'
COMPMODEL_ASHOUSEWORKER = 'Households with all working adults'
COMPMODEL_ASDEPENDWORKER = 'Assign all dependent children to a working adult'
COMPMODEL_ASADULTHOME = 'This adult works from home'
COMPMODEL_ASONENWORKER = 'Households with at least one non-working adult'
COMPMODEL_ASDEPENDNONWORK = 'Assign all dependent children to one non-working adult'
COMPMODEL_ASASSIGNHOUSE = 'Assign each dependent child to a household adult subject to the fixed activity schedule of the adult'
COMPMODEL_ASISWORKER = 'For all other adults, check to see if the adult is worker?'
COMPMODEL_ASEMPLOYWORK = 'Is an employed adult going to work today?'
COMPMODEL_ASWORKHOME = 'Work from home'
COMPMODEL_ASGOTOWORK = 'Go to Work'
COMPMODEL_ASNWORKEPISO = 'No Work Episodes'


MODELKEY_WORKSTAT = 'WorkStat'
MODELKEY_NUMJOBS = 'NumJobs'
MODELKEY_PRESCHSTAT = 'PreSchStat'
MODELKEY_SCHSTAT1 = 'SchStat1'
MODELKEY_SCHSTAT2 = 'SchStat2'
MODELKEY_RESLOC = 'ResLoc'
MODELKEY_WORKLOC = 'WorkLoc'
MODELKEY_PRESCHLOC = 'PreSchLoc'
MODELKEY_SCHLOC1 = 'SchLoc1'
MODELKEY_SCHLOC2 = 'SchLoc2'
MODELKEY_NUMVEHS = 'NumVehs'
MODELKEY_NUMVEHTYPES = 'VehTypes'
MODELKEY_DAYSTART = 'DayStart'
MODELKEY_DAYEND = 'DayEnd'
MODELKEY_NUMWRKEPISODES = 'NumWorkEpisodes'
MODELKEY_WORKSTART1 = 'WorkStart1'
MODELKEY_WORKEND1 = 'WorkEnd1'
MODELKEY_WORKSTART2 = 'WorkStart2'
MODELKEY_WORKEND2 = 'WorkEnd2'
MODELKEY_NUMSCHEPISODES = 'NumSchEpisodes'
MODELKEY_SCHSTART1 = 'SchStart1'
MODELKEY_SCHEND1 = 'SchEnd1'
MODELKEY_SCHSTART2 = 'SchStart2'
MODELKEY_SCHEND2 = 'SchEnd2'
MODELKEY_PRESCHDAILYSTAT = 'PreSchDailyStatus'
MODELKEY_SCHDAILYSTAT = 'SchDailyStatus'
MODELKEY_SCHDAILYINDEP = 'SchDailyIndependence'
MODELKEY_AFTSCHDAILYINDEP = 'AfterSchDailyIndependence'
MODELKEY_AFTSCHACTSTAT = 'AfterSchActStatus'
MODELKEY_AFTSCHACTTYPE = 'AftSchActivityType'
MODELKEY_AFTSCHACTDEST = 'AftSchActDestination'
MODELKEY_AFTSCHACTDUR = 'AftSchActDuration'
MODELKEY_WRKDAILYSTAT = 'WorkDailyStatus'
MODELKEY_AFTSCHACTMODE = 'AftSchActivityMode'
MODELKEY_ACTTYPE = 'ActivityType'
MODELKEY_ACTDEST = 'ActDestinationMode'
MODELKEY_ACTDUR = 'ActivityDuration'
MODELKEY_FIXEDACTMODE = 'FixedActivityMode'
MODELKEY_JOINTACT = 'JointActivity'
MODELKEY_TRIPVEH = 'TripVehicle'
#Child Daily Status and Allocation Model
MODELKEY_CSCHILD017 = 'Child0-17'
MODELKEY_CSCHILDSCH1 = 'ChildSch1'
MODELKEY_CSCHILDPRE1 = 'ChildPreSch1'
MODELKEY_CSCHILDSTA = 'ChildStayHome'
MODELKEY_CSSCHPRE = 'SchOrPresch'
MODELKEY_CSINDCHILD = 'ActiveIndepend'
MODELKEY_CSCHILDIND = 'ActiveIndependAdult'
MODELKEY_CSASSIGN = 'AssignChildHouse'
MODELKEY_CSCHILDSCH2 = 'ChildSch2)'
MODELKEY_CSCHILDPRE2 = 'ChildPreSch2'
MODELKEY_CSINSCHTO = 'TravelIndepToSchool?'
MODELKEY_CSMODETOSCH = 'TravelModeTo'
MODELKEY_CSDROPOFF = 'AssignDrop-off'
MODELKEY_CSINSCHFROM = 'TravelIndepFromSch'
MODELKEY_CSMODEFROMSCH = 'TravelModeFrom'
MODELKEY_CSPICKUP = 'AssignPick-up'
MODELKEY_CSINAFTER = 'ActiveIndepAfterSch'
MODELKEY_CSTREAT = 'ActiveTravelPatterns'
MODELKEY_CSISTHERE = 'IsAfterSchoolActive'
MODELKEY_CSACTTYPE = 'ChildActiveType'
MODELKEY_CSWORKSTAT = 'ActiveWithAdult'
MODELKEY_CSMOREACT = 'MoreActive'
MODELKEY_CSRETURNH = 'RetHome'
MODELKEY_CSMOVEADULT = 'Move to Adult Daily Status'
#Adult Daily Status Model
MODELKEY_ASISDEPEND = 'DependentAssignedtoHouse'
MODELKEY_ASHOUSEWORKER = 'HouseWorkAdults'
MODELKEY_ASDEPENDWORKER = 'AssignDependentWorkAdult'
MODELKEY_ASADULTHOME = 'WorkfromHome'
MODELKEY_ASONENWORKER = 'HouseNonWorkAdult'
MODELKEY_ASDEPENDNONWORK = 'AssignDependentNonWorker'
MODELKEY_ASASSIGNHOUSE = 'AssignDependentHouse'
MODELKEY_ASISWORKER = 'AdultisWorker'
MODELKEY_ASEMPLOYWORK = 'EmployedToworkToday'
MODELKEY_ASWORKHOME = 'WorkfromHome'
MODELKEY_ASGOTOWORK = 'GoWork'
MODELKEY_ASNWORKEPISO = 'NoWorkEpisodes'



COMPMODELMAP = {}
COMPMODELMAP[COMPKEY_FIXEDACTPRISM] = [MODELKEY_DAYSTART,MODELKEY_DAYEND,MODELKEY_NUMWRKEPISODES,
                                       MODELKEY_WORKSTART1,MODELKEY_WORKEND1,MODELKEY_WORKSTART2,MODELKEY_WORKEND2,
                                       MODELKEY_NUMSCHEPISODES,MODELKEY_SCHSTART1,MODELKEY_SCHEND1,MODELKEY_SCHSTART2,
                                       MODELKEY_SCHEND2]

PERSON_TABLE_MODELS = [MODELKEY_DAYSTART,MODELKEY_DAYEND,MODELKEY_NUMWRKEPISODES,
                                       MODELKEY_WORKSTART1,MODELKEY_WORKEND1,MODELKEY_WORKSTART2,MODELKEY_WORKEND2,
                                       MODELKEY_NUMSCHEPISODES,MODELKEY_SCHSTART1,MODELKEY_SCHEND1,MODELKEY_SCHSTART2,
                                       MODELKEY_SCHEND2]

HH_TABLE_MODELS = [MODELKEY_NUMVEHS]

MODELKEYSMAP = {}
MODELKEYSMAP[MODELKEY_WORKSTAT] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_NUMJOBS] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_PRESCHSTAT] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHSTAT1] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHSTAT2] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_RESLOC] = ['Household_ID','']
MODELKEYSMAP[MODELKEY_WORKLOC] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_PRESCHLOC] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHLOC1] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHLOC2] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHLOC2] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_NUMVEHS] = ['Household_ID','']
MODELKEYSMAP[MODELKEY_NUMVEHTYPES] = ['Household_ID_fk','Vehicle_ID']
MODELKEYSMAP[MODELKEY_DAYSTART] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_DAYEND] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_NUMWRKEPISODES] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_WORKSTART1] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_WORKEND1] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_WORKSTART2] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_WORKEND2] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_NUMSCHEPISODES] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHSTART1] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHEND1] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHSTART2] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHEND2] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_PRESCHDAILYSTAT] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHDAILYSTAT] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_SCHDAILYINDEP] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_AFTSCHDAILYINDEP] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_AFTSCHACTSTAT] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_AFTSCHACTTYPE] = ['Person_ID_fk','Schedule_ID']
MODELKEYSMAP[MODELKEY_AFTSCHACTDEST] = ['Person_ID_fk','Schedule_ID']
MODELKEYSMAP[MODELKEY_AFTSCHACTDUR] = ['Person_ID_fk','Schedule_ID']
MODELKEYSMAP[MODELKEY_WRKDAILYSTAT] = ['Person_ID','']
MODELKEYSMAP[MODELKEY_AFTSCHACTMODE] = ['PT_ID_fk','Trip_ID']
MODELKEYSMAP[MODELKEY_ACTTYPE] = ['Person_ID','Schedule_ID']
MODELKEYSMAP[MODELKEY_ACTDEST] = ['Person_ID','Schedule_ID']
MODELKEYSMAP[MODELKEY_ACTDUR] = ['Person_ID','Schedule_ID']
MODELKEYSMAP[MODELKEY_FIXEDACTMODE] = ['PT_ID_fk,Trip_ID','']
MODELKEYSMAP[MODELKEY_JOINTACT] = ['PT_ID_fk,Trip_ID','']
MODELKEYSMAP[MODELKEY_TRIPVEH] = ['Vehicle_ID_fk','Trip_ID']



