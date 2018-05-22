def coreOccupancy(vmList, timestamp):
	V = 0

	for vm in vmList:
		V += vm.cores * (vm.deallocated - vm.allocated)

	return V

def coreAvailability(pmList, timestamp):
	S = 0

	for pm in pmList:
		S += pm.cores * pm.totalUptime

	return S

def coreUtilization(vmList, pmList, timestamp):
	V = coreOccupancy(vmList, timestamp)
	S = coreAvailability(pmList, timestamp)
	return V / (float(S))


def CoLocRes(vmList):
	BenignUsers = dict() #dict of (Bengin User, Malicious Co-Location)

	for vm in vmList:
		user = vm.user

		if(user.ACL == 1):
			continue

		if(user not in BenignUsers):
			BenignUsers[user] = 0
			
		if(vm.colocated == 1):
			BenignUsers[user] = 1

	num = 0.0
	den = 0.0

	for user in BenignUsers:
		if(BenignUsers[user] != 1):
			num += 1
		den += 1

	CLR = num / den

	return CLR
