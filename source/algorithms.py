import classes
import constants
from time import clock
import random

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


class PreviousCoLocatedUsersFirst:

	def __init__(self):
		self.datacenter = classes.Datacenter("d")
		self.totalUsersDuringFirstAllotment = 0.0
		self.users = set()
		for i in xrange(constants.MAX_PMS):
			pmId = self.datacenter.id+"-"+str(i)
			pm_new = classes.Pm(pmId, constants.MAX_CORES, constants.MAX_MEM)
			self.datacenter.emptyPms.append(pm_new)

	def placeVM(self, vm, timeStamp):
		start = clock()
		datacenter = self.datacenter
		U_curr = vm.user

		if(U_curr in self.users):
			eligible_pms = [pm for pm in datacenter.livePms if(pm.check(vm) == True and set(pm.userFreq.keys()).issubset(U_curr.colocatedUsers) == True)]
			if(len(eligible_pms) != 0):
				p_k = sorted(eligible_pms, key = lambda pm : pm.freeCores)[0]
				stop = clock()
				p_k.allocate(vm, timeStamp + float(stop - start))
			else:
				pm_k = datacenter.emptyPms[0]
				datacenter.emptyPms.remove(pm_k)
				datacenter.livePms.append(pm_k)
				stop = clock()
				pm_k.allocate(vm, timeStamp + float(stop - start))

		else:
			self.users.add(U_curr)
			eligible_pms = [pm for pm in datacenter.livePms if(pm.check(vm) == True)]
			if(len(eligible_pms) != 0):
				p_k = random.sample(eligible_pms, 1)[0]
				self.totalUsersDuringFirstAllotment += len(p_k.userFreq.keys())
				stop = clock()
				p_k.allocate(vm, timeStamp+0.0 * float(stop - start))
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



class DedicatedHosting:

	def __init__(self):
		self.datacenter = classes.Datacenter("d")
		self.users = set()
		for i in xrange(constants.MAX_PMS):
			pmId = self.datacenter.id+"-"+str(i)
			pm_new = classes.Pm(pmId, constants.MAX_CORES, constants.MAX_MEM)
			self.datacenter.emptyPms.append(pm_new)


	def placeVM(self, vm, timeStamp):
		start = clock()
		datacenter = self.datacenter
		U_curr = vm.user

		if(U_curr in self.users):
			eligible_pms = [pm for pm in datacenter.livePms if(pm.check(vm) == True and set(pm.userFreq.keys()).issubset(U_curr.colocatedUsers) == True)]
			if(len(eligible_pms) != 0):
				p_k = sorted(eligible_pms, key = lambda pm : pm.freeCores)[0]
				stop = clock()
				p_k.allocate(vm, timeStamp + float(stop - start))
			else:
				pm_k = datacenter.emptyPms[0]
				datacenter.emptyPms.remove(pm_k)
				datacenter.livePms.append(pm_k)
				stop = clock()
				pm_k.allocate(vm, timeStamp + float(stop - start))

		else:
			self.users.add(U_curr)			
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


class Azar:

	def __init__(self, lmbda):
		self.lmbda = lmbda
		self.OPN = set()
		self.EMP = set()
		self.CL = set()
		self.datacenter = classes.Datacenter("d")
		for i in xrange(constants.MAX_PMS):
			pmId = self.datacenter.id+"-"+str(i)
			pm_new = classes.Pm(pmId, constants.MAX_CORES, constants.MAX_MEM)
			self.datacenter.emptyPms.append(pm_new)

		self.OPN = set(random.sample(self.datacenter.emptyPms, self.lmbda))
		for pm in self.datacenter.emptyPms:
			if (pm not in self.OPN):
				self.EMP.add(pm)



	def placeVM(self, vm, timeStamp):
		start = clock()

		Srv = random.sample(self.OPN, 1)[0]
		current_coreLoad = Srv.cores - Srv.freeCores
		current_memLoad = Srv.mem - Srv.freeMem

		stop = clock()
		Srv.allocate(vm, timeStamp+ float(stop - start))

		if(((current_coreLoad/constants.MAX_VM_CORES + vm.cores/constants.MAX_VM_CORES) > (Srv.cores/constants.MAX_VM_CORES - 1)) or
		 ((current_memLoad/constants.MAX_VM_MEM + vm.mem/constants.MAX_VM_MEM) > (Srv.mem/constants.MAX_VM_MEM - 1))):
			self.OPN.remove(Srv)
			self.CL.add(Srv)
			if(len(self.OPN) < self.lmbda):
				pEmpty = self.EMP.pop()
				self.OPN.add(pEmpty)	

	
	def removeVM(self, vm, timeStamp):
		start = clock()
		pm = vm.pm
		stop = clock()
		pm.deallocate(vm, timeStamp+float(stop-start))
		if(pm in self.CL):
			self.CL.remove(pm)
			self.OPN.add(pm)

		elif(pm in self.OPN):
			if(len(pm.currentVms) == 0):
				self.OPN.remove(pm)
				self.EMP.add(pm)



class PreviousSelectedServersFirst:

	def __init__(self, Ng):
		self.Ng = Ng
		self.datacenter = classes.Datacenter("d")
		self.pmGroups = dict() #Dictionary of (group index, list of PMs in this group)

		for i in xrange(constants.MAX_PMS):
			pmId = self.datacenter.id+"-"+str(i)
			pm_new = classes.Pm(pmId, constants.MAX_CORES, constants.MAX_MEM)
			pm_new.groupIndex = i/self.Ng
			self.datacenter.livePms.append(pm_new)


	def placeVM(self, vm, timeStamp):
		start = clock()
		datacenter = self.datacenter

		PSSList = list()
		NPSSList = list()
		U_curr = vm.user

		PSSList = [si for si in U_curr.residentPms if(si.check(vm) == True)]
		

		if(len(PSSList) != 0):
			p_k = random.sample(PSSList, 1)[0]
			stop = clock()
			p_k.allocate(vm, timeStamp + float(stop - start))
		
		else:
			NPSSList = [si for si in datacenter.livePms if((si.check(vm) == True) and (si not in U_curr.residentPms))]
			NPSSList = sorted(NPSSList, key = lambda pm : (pm.groupIndex, -pm.freeCores))
			i = 0
			for pm in NPSSList:
				if(pm.groupIndex == NPSSList[0].groupIndex and pm.freeCores == NPSSList[0].freeCores):
					i += 1
			p_k = NPSSList[random.randint(0, i-1)]
			stop = clock()
			p_k.allocate(vm, timeStamp + float(stop - start))


	def removeVM(self, vm, timeStamp):
		start = clock()
		datacenter = self.datacenter

		pm = vm.pm
		stop = clock()
		pm.deallocate(vm, timeStamp+float(stop-start))


algorithmDict = {
	"bf" : BestFit,
	"wf" : WorstFit,
	"rp" : RandomPlacement,
	"pcuf" : PreviousCoLocatedUsersFirst,
	"dh" : DedicatedHosting,
	"azar" : Azar,
	"pssf" : PreviousSelectedServersFirst
}
