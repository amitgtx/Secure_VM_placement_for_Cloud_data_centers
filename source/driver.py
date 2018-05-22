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
Ngp = float(sys.argv[6]) / 100.0	

DatasetFilePath = "azure-trace.txt"

sumCU = 0.0
sumCLR = 0.0

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

	CU = metrics.coreUtilization(vmList, pmList, timeStamp)
	CLR  = metrics.CoLocRes(vmList)


	sumCU += CU
	sumCLR += CLR

	print "CU = ",round((CU*100), 2)
	print "CLR = ", round((CLR*100), 2)
	print "\n"


print "------------FINAL----------------"

print "\n\n\n"
print "CU = ", round((sumCU*100)/trials, 2)
print "CLR = ", round((sumCLR*100)/trials, 2)

print "---------------------------------"
