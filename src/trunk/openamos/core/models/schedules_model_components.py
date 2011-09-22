

class ReconcileSchedulesSpecification(object):
    def __init__(self, activityAttribs):
        self.activityAttribs = activityAttribs

        self.choices = None
        self.coefficients = None

class HouseholdSpecification(object):
    def __init__(self, activityAttribs, dailyStatusAttribs=None,
                 dependencyAttribs=None, arrivalInfoAttribs=None,
		 terminalEpisodesAllocation=False, 
		 childDepProcessingType="Allocation",
		 occupancyInfoAttribs=False):
	self.childDepProcessingType = childDepProcessingType
	self.activityAttribs = activityAttribs
	self.dailyStatusAttribs = dailyStatusAttribs
	self.dependencyAttribs = dependencyAttribs
	self.arrivalInfoAttribs = arrivalInfoAttribs
	self.occupancyInfoAttribs = occupancyInfoAttribs

	self.terminalEpisodesAllocation = terminalEpisodesAllocation

	if self.arrivalInfoAttribs == None:
	    self.schedAdjType = "Occupancy Adjustment"


	if self.occupancyInfoAttribs == None:
	    self.schedAdjType = "Arrival Adjustment"

	self.choices = None
	self.coefficients = None
	
class ActivityAttribsSpecification(object):
    def __init__(self, hidName, pidName, scheduleidName,
                 activitytypeName, starttimeName,
                 endtimeName, locationidName, 
                 durationName, dependentPersonName):
	self.hidName = hidName
        self.pidName = pidName
        self.scheduleidName = scheduleidName
        self.activitytypeName = activitytypeName
        self.locationidName = locationidName
        self.starttimeName = starttimeName
        self.endtimeName = endtimeName
        self.durationName = durationName
        self.dependentPersonName = dependentPersonName

class ArrivalInfoSpecification(object):
    def __init__(self, dependentPersonName,
		 actualArrivalName, expectedArrivalName):
	self.dependentPersonName = dependentPersonName
	self.actualArrivalName = actualArrivalName
	self.expectedArrivalName = expectedArrivalName

class OccupancyInfoSpecification(object):
    def __init__(self, tripIndicatorName, startTimeName):
	self.tripIndicatorName = tripIndicatorName
	self.startTimeName = startTimeName


class DailyStatusAttribsSpecification(object):
    def __init__(self, workStatusName, schoolStatusName):
	self.workStatusName = workStatusName
	self.schoolStatusName = schoolStatusName


class DependencyAttribsSpecification(object):
    def __init__(self, childDependencyName, elderlyDependencyName=None):
	self.childDependencyName = childDependencyName
	self.elderlyDependencyName = elderlyDependencyName

class TripOccupantSpecification(object):
    def __init__(self,
		 idSpec,
		 tripDepAttribSpec):
	self.idSpec = idSpec	
	self.tripDepAttribSpec = tripDepAttribSpec
		 
        self.choices = None
        self.coefficients = None

class PersonsArrivedSpecification(object):
    def __init__(self,
		 idSpec,
		 persArrivedAttribSpec):
	self.idSpec = idSpec
	self.persArrivedAttribSpec = persArrivedAttribSpec

        self.choices = None
        self.coefficients = None



class PersonsArrivedAttributes(object):
    def __init__(self, tripDepName):
	self.tripDepName = tripDepName

class TripDependentPersonAttributes(object):
    def __init__(self, 
		 tripPurposeFromName,
		 tripDepName,
		 lastTripDepName,
		 stActDepName,
		 enActDepName,
		 personOnNetworkName=None):
	self.tripPpurposeFromName = tripPurposeFromName
	self.tripDepName = tripDepName
	self.lastTripDepName = lastTripDepName
	self.stActDepName = stActDepName
	self.enActDepName = enActDepName
	self.personOnNetworkName = personOnNetworkName

class UniqueRecordsSpecification(object):
    def __init__(self, uniqueRecordsColName):
	self.uniqueRecordsColName = uniqueRecordsColName

        self.choices = None
        self.coefficients = None

