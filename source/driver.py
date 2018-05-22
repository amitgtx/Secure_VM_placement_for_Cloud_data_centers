import sys
import constants
import azureParser
import algorithms
import metrics
import classes

#python driver2.py <P-m> <algorithm> <trial> <Ng-p>


P_m = float(sys.argv[1])
algoCode = sys.argv[2]
dataset = "azure"
trials = int(sys.argv[3])
Ngp = float(sys.argv[4]) / 100.0	

DatasetFilePath = "azure-trace.txt"

sumCU = 0.0
sumCLR = 0.0

for seedVal in xrange(1, trials+1):

	vmDict, userDict, jobList = azureParser.parse(traceFile = DatasetFilePath,
							P_m = P_m,
							seedVal = seedVal
							)

	
	if(algoCode == "pssf"):
		algorithm = algorithms.algorithmDict[algoCode](int(Ngp * constants.MAX_PMS))
	elif(algoCode == "azar"):
		algorithm = algorithms.algorithmDict[algoCode](int(Ngp * constants.MAX_PMS))
	else:
		algorithm = algorithms.algorithmDict[algoCode]()


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
