import classes
import constants
from time import clock
import random
import overlap

class BestFit:

	def __init__(self):
		self.datacenter = classes.Datacenter("d")
		for i in xrange(constants.MAX_PMS):
			pmId = self.datacenter.id+"-"+str(i)
			pm_new = classes.Pm(pmId, constants.MAX_CORES, constants.MAX_MEM)
			self.datacenter.emptyPms.append(pm_new)


	def placeVM(self, vm, timeStamp):
		start = clock()
		datacenter = self.datacenter

		eligible_pms = [pm for pm in datacenter.livePms if(pm.check(vm) == True)]

		if(len(eligible_pms) != 0):
			eligible_pms = sorted(eligible_pms, key = lambda pm : pm.freeCores)
			bestPm = eligible_pms[0]
			stop = clock()
			bestPm.allocate(vm, timeStamp+ float(stop - start))
		else:
			pm_k = datacenter.emptyPms[0]
			datacenter.emptyPms.remove(pm_k)
			datacenter.livePms.append(pm_k)
			stop = clock()
			pm_k.allocate(vm, timeStamp + float(stop - start))				


	def removeVM(self, vm, timeStamp):
		start = clock()
		datacenter = self.datacenter
		pm = vm.pm
		stop = clock()
		pm.deallocate(vm, timeStamp+float(stop-start))
		if(len(pm.currentVms) == 0):
			datacenter.livePms.remove(pm)
			datacenter.emptyPms.append(pm)


class WorstFit:

	def __init__(self):
		self.datacenter = classes.Datacenter("d")
		for i in xrange(constants.MAX_PMS):
			pmId = self.datacenter.id+"-"+str(i)
			pm_new = classes.Pm(pmId, constants.MAX_CORES, constants.MAX_MEM)
			self.datacenter.emptyPms.append(pm_new)

	def placeVM(self, vm, timeStamp):
		start = clock()
		datacenter = self.datacenter

		eligible_pms = [pm for pm in datacenter.livePms if(pm.check(vm) == True)]

		if(len(eligible_pms) != 0):
			eligible_pms = sorted(eligible_pms, key = lambda pm : pm.freeCores, reverse = True)
			bestPm = eligible_pms[0]
			stop = clock()
			bestPm.allocate(vm, timeStamp+ float(stop - start))
		else:
			pm_k = datacenter.emptyPms[0]
			datacenter.emptyPms.remove(pm_k)
			datacenter.livePms.append(pm_k)
			stop = clock()
			pm_k.allocate(vm, timeStamp + float(stop - start))
		


	def removeVM(self, vm, timeStamp):
		start = clock()
		datacenter = self.datacenter
		pm = vm.pm
		stop = clock()
		pm.deallocate(vm, timeStamp+float(stop-start))
		if(len(pm.currentVms) == 0):
			datacenter.livePms.remove(pm)
			datacenter.emptyPms.append(pm)


class RandomPlacement:

	def __init__(self):
		self.datacenter = classes.Datacenter("d")
		for i in xrange(constants.MAX_PMS):
			pmId = self.datacenter.id+"-"+str(i)
			pm_new = classes.Pm(pmId, constants.MAX_CORES, constants.MAX_MEM)
			self.datacenter.emptyPms.append(pm_new)

	def placeVM(self, vm, timeStamp):
		start = clock()
		datacenter = self.datacenter

		eligible_pms = [pm for pm in datacenter.livePms if(pm.check(vm) == True)]

		if(len(eligible_pms) != 0):
			eligible_pms = sorted(eligible_pms, key = lambda pm : pm.freeCores, reverse = True)
			bestPm = random.sample(eligible_pms, 1)[0]
			stop = clock()
			bestPm.allocate(vm, timeStamp+ float(stop - start))
		else:
			pm_k = datacenter.emptyPms[0]
			datacenter.emptyPms.remove(pm_k)
			datacenter.livePms.append(pm_k)
			stop = clock()
			pm_k.allocate(vm, timeStamp + float(stop - start))		


	def removeVM(self, vm, timeStamp):
		start = clock()
		datacenter = self.datacenter
		pm = vm.pm
		stop = clock()
		pm.deallocate(vm, timeStamp+float(stop-start))
		if(len(pm.currentVms) == 0):
			datacenter.livePms.remove(pm)
			datacenter.emptyPms.append(pm)

class SecurePlacement:

	def __init__(self):
		self.datacenter = classes.Datacenter("d")
		for i in xrange(constants.MAX_PMS):
			pmId = self.datacenter.id+"-"+str(i)
			pm_new = classes.Pm(pmId, constants.MAX_CORES, constants.MAX_MEM)
			self.datacenter.emptyPms.append(pm_new)

	def placeVM(self, vm, timeStamp):
		start = clock()
		datacenter = self.datacenter

		for pm in datacenter.livePms:
			pmr = 0.0
			pms = 0.0
			userFreq = dict()
			
			for vm2 in pm.currentVms:
				pmr += vm2.user.repScore
				if(vm2.user in userFreq):
					userFreq[vm2.user] += 1
				else:
					userFreq[vm2.user] = 1

			for user in userFreq:
				pms += (userFreq[user] ** 2 ) * (user.spread ** 2)

			N = len(pm.currentVms)
			pmr = pmr / N
			pms = sqrt(pms/(N*N))

			area = overlap.findOverlap(vm.user.repScore, vm.user.spread, pmr, pms)
			
			if((pm.check(vm) == True) and (random.uniform(0, 1) <= area)):
				eligible_pms.append(pm)

		if(len(eligible_pms) != 0):
			eligible_pms = sorted(eligible_pms, key = lambda pm : pm.freeCores, reverse = True)
			bestPm = random.sample(eligible_pms, 1)[0]
			stop = clock()
			bestPm.allocate(vm, timeStamp+ float(stop - start))
		else:
			pm_k = datacenter.emptyPms[0]
			datacenter.emptyPms.remove(pm_k)
			datacenter.livePms.append(pm_k)
			stop = clock()
			pm_k.allocate(vm, timeStamp + float(stop - start))		


	def removeVM(self, vm, timeStamp):
		start = clock()
		datacenter = self.datacenter
		pm = vm.pm
		stop = clock()
		pm.deallocate(vm, timeStamp+float(stop-start))
		if(len(pm.currentVms) == 0):
			datacenter.livePms.remove(pm)
			datacenter.emptyPms.append(pm)



algorithmDict = {
	"bf" : BestFit,
	"wf" : WorstFit,
	"rp" : RandomPlacement,
	"pcuf" : PreviousCoLocatedUsersFirst,
	"di" : DedicatedInstance,
	"azar" : Azar,
	"pssf" : PreviousSelectedServersFirst
}
