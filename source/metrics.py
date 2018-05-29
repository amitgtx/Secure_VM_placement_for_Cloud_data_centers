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
	BenignUsers = dict() #dict of (Bengin User, [vms colocated, total vms])

	for vm in vmList:
		user = vm.user

		if(user.ACL == 1):
			continue

		if(user not in BenignUsers):
			BenignUsers[user] = [0, 0]
		
		BenignUsers[user][1] += 1
		if(vm.colocated == 1):
			BenignUsers[user][0] += 1

	num = 0.0
	den = 0.0

	for user in BenignUsers:
		num += user.repScore * float(BenignUsers[user][0]) / float(BenignUsers[user][1])
		den += user.repScore

	CLR = 1 - num / den

	return CLR
