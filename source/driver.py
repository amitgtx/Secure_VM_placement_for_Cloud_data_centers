import sys
import constants
from azureParser import parseEucalyptus
import algorithmsNew
import metrics
from classes import Datacenter



#python driver2.py <P-m> <p> <q> <algorithm> <trial> <Ng-p>


P_m = float(sys.argv[1])
p = float(sys.argv[2])
q = float(sys.argv[3])
algoCode = sys.argv[4]
dataset = "azure"
trials = int(sys.argv[5])
userCoLocDict = dict() # Dict of (Users, No. of other users this user has co-located with)
Ngp = float(sys.argv[6]) / 100.0	

DatasetFilePath = "azure-trace.txt"

sumCU = 0.0
sumCLR = 0.0
sumk1 = 0.0
sumk2 = 0.0
sumk3 = 0.0

for seedVal in xrange(1, trials+1):

	vmDict, userDict, jobList = parseEucalyptus(traceFile = DatasetFilePath,
												P_m = P_m,
												p = p,
												q = q,
												seedVal = seedVal
												)

	
	if(algoCode == "pssf"):
		algorithm = algorithmsNew.algorithmDict[algoCode](int(Ngp * constants.MAX_PMS))
	elif(algoCode == "azar"):
		algorithm = algorithmsNew.algorithmDict[algoCode](int(Ngp * constants.MAX_PMS))
	else:
		algorithm = algorithmsNew.algorithmDict[algoCode]()


	for jobType, timeStamp, vm in jobList:

		if(jobType == "START"):

			algorithm.placeVM(vm, timeStamp)

		else:

			algorithm.removeVM(vm, timeStamp)

		# print timeStamp

	vmList = vmDict.values()
	datacenter = algorithm.datacenter
	pmList = datacenter.livePms + datacenter.emptyPms

	V, S, CU = metrics.coreUtilization(vmList, pmList, timeStamp)
	CLR, k1, k2, k1_T, k2_T = metrics.CoLocRes(vmList)


	for userId in userDict.keys():
		if(userId not in userCoLocDict):
			userCoLocDict[userId] = 0
		userCoLocDict[userId] += (len(userDict[userId].colocatedUsers)-1)

	sumCU += CU
	sumCLR += CLR
	sumk1 += k1
	sumk2 += k2
	if(algoCode == "pcuf") : sumk3 += algorithm.totalUsersDuringFirstAllotment / len(userDict.keys())

	print "CU = ",round((CU*100), 2)
	print "CLR = ", round((CLR*100), 2)
	print "SAFE B/B users = ", int(k1)
	print "TOTAL B/B users = ", int(k1_T)
	print "SAFE M/B users = ", int(k2)
	print "TOTAL M/B users = ", int(k2_T)
	print "TOTAL USERS = ", int(len(userDict.keys()))
	if(algoCode == "pcuf") : print "AVG USERS DURING 1st ALLOTMENT = ", algorithm.totalUsersDuringFirstAllotment / len(userDict.keys())
	print "TOTAL VMS = ", len(vmList)
	print "\n"


print "------------FINAL----------------"

for userId in userCoLocDict:
	print userId[0:7],"\t",round(float(userCoLocDict[userId]) / trials, 2)
print "\n\n\n"
print "CU = ", round((sumCU*100)/trials, 2)
print "CLR = ", round((sumCLR*100)/trials, 2)

print "SAFE B/B users = ", round(sumk1/trials, 2)
print "SAFE M/B users = ", round(sumk2/trials, 2)
print "TOTAL users = ", len(userDict.keys())
print "AVG CO-LOCATED USERS = ", round(float(sum(userCoLocDict.values())) / (trials * len(userDict.keys())) , 2)
if(algoCode == "pcuf") : print "AVG USERS DURING 1st ALLOTMENT = ", round(sumk3/trials, 2)


print "---------------------------------"
