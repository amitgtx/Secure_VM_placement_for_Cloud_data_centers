import sys
import constants
from math import sqrt

class Pm:


	def __init__(self, pmId, cores, mem):
		self.pmId = pmId
		self.cores = cores
		self.mem = mem
		self.freeCores = cores
		self.freeMem = mem
		self.totalUptime = 0
		
		self.currentVms = set() #currentVms is a set of Vm references which have been placed in this Pm
		self.lastBootTime = int()
		self.attackersVmCount = 0 #Number of attackers VM

		self.userFreq = dict() #Dict of (user, number of vms of the user on this pm)
		self.groupIndex = None
		self.hostedUsers = set()


	def allocate(self, vm, timeStamp):
		if (len(self.currentVms) == 0):
			self.lastBootTime = timeStamp

		U_curr = vm.user
		U_curr.residentPms.add(self)
		self.hostedUsers.add(U_curr)

		for user in self.userFreq.keys():
			user.colocatedUsers.add(U_curr)
			U_curr.colocatedUsers.add(user)



		self.freeCores -= vm.cores
		self.freeMem -= vm.mem

		self.currentVms.add(vm)
		if(vm.user not in self.userFreq):
			self.userFreq[vm.user] = 1
		else:
			self.userFreq[vm.user] += 1

		if(vm.user.ACL == 1):
			if(self.attackersVmCount == 0):
				for vm2 in self.currentVms:
					vm2.colocated = 1
			self.attackersVmCount += 1

	
			
		if(self.attackersVmCount > 0):
			vm.colocated = 1
		else:
			vm.colocated = 0


		vm.pm = self
		vm.allocated = timeStamp

		# print vm.vmId[0:7]," belonging to ", vm.user.userID[0:7], "(", vm.user.ACL, ")", " allocated to ", self.pmId, " at ", timeStamp, "seconds"


	def check(self, vm1):
		if(vm1.cores > self.freeCores or vm1.mem > self.freeMem): 
			return False
		return True


	def deallocate(self, vm, timeStamp):
		self.freeCores += vm.cores
		self.freeMem += vm.mem

		if(vm.user.ACL == 1):
			self.attackersVmCount -= 1

		self.currentVms.remove(vm)

		self.userFreq[vm.user] -= 1
		if(self.userFreq[vm.user] == 0):
			del self.userFreq[vm.user]


		vm.deallocated = timeStamp
		vm.hasDeallocated = 1
		if(len(self.currentVms) == 0):
			self.totalUptime += (timeStamp - self.lastBootTime)
		# print vm.vmId[0:7], " deallocated from ", self.pmId[0:7], " at ", timeStamp, "seconds"


class User:

	def __init__(self, userID, ACL = None):
		self.userID = userID
		self.ACL = ACL
		self.colocatedUsers = set([self])
		self.residentPms = set()


class Vm:
		
	def __init__(self, vmId, cores, mem, user, startReq):
		self.vmId = vmId
		self.cores = cores
		self.mem = mem
		self.user = user 	#User who requested this PM
		self.startReq = startReq	#Time when the request to start the VM was made my user

		self.pm = None 		#PM which this VM got allocated
		self.stopReq = float()	#Time when the request to stop the VM was made my user
		self.allocated = float()	#Time when the VM got allocated 
		self.deallocated = float()	#Time when the VM got deallocated
		self.colocated = 0	# 1 if colocated with attacker's VM else 0
		self.hasDeallocated = 0	#True if the VM has been deallocated

class Datacenter:

	def __init__(self, id):
		self.id = id
		self.livePms = list()
		self.emptyPms = list()
