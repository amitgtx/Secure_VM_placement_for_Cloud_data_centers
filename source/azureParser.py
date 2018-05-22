import random
import constants
import classes


def parse(traceFile, P_m, seedVal):

	random.seed(seedVal)

	#Dict of (key = vmId, value = Vm Object)
	vmDict = dict()

	#Dict of (key = userId, value = User object)
	userDict = dict()

	
	jobList = list() #list of (jobType, timeStamp, vm)
	f = open(traceFile,'r')
	

	for line in f:
		tmp = line.split(',')
		vmId = tmp[0]
		userID = tmp[1]
		tStart = float(tmp[3])
		tEnd = float(tmp[4])
		cores = float(tmp[9])
		mem = float(tmp[10])

		if((tStart < (86400.0 * 10)) or (tEnd > (86400.0 * 20))): continue

		if(userID in userDict):
			user = userDict[userID]
		else:
			user = classes.User(userID = userID)
			userDict[userID] = user

		vm = classes.Vm(vmId, cores, mem, user, tStart)
		vm.stopReq = tEnd
		vmDict[vmId] = vm

		jobList.append(("START", tStart, vm))
		jobList.append(("STOP", tEnd, vm))

	jobList  = sorted(jobList, key = lambda job : job[1])

	userList = userDict.values()


	N = len(userList)
	N_m = int((P_m / 100.0) * N)
	N_b = N - N_m
	
	# User_List = set(userDict.values())
	User_List = userDict.values()
	Actual_Malicious = random.sample(User_List, N_m)
	Actual_Benign = set()

	for user in User_List:
		if(user in Actual_Malicious):
			user.ACL = 1
		else:
			Actual_Benign.add(user)
			user.ACL = 0

	return vmDict, userDict, jobList
