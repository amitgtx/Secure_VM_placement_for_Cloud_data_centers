# Secure_VM_placement_for_Cloud_data_centers

The use of virtualization and resource multiplexing enable commercial cloud providers (e.g., Amazon EC2) to maximize utilization but at the same time introduce new security vulnerabilities. It has been demonstrated that malicious users could launch virtual machines (VM) which are placed co-resident (on the same physical machine) with the target VM. Such placement in turn may lead to cross-VM side-channel attacks to extract sensitive information from the target VM. In this project, we investigate solutions including but not limited to VM placement algorithms to ensure security and privacy for IaaS cloud data centers.

The source/ folder contains all the code organized into 6 separate files. Below is a short description of what the code in each file is resposible for :

metrics.py : This file contains methods for calculation of performance metrics such as Core Utilization and Co-Location Resistance (Refer to the paper for more detailed description of the metric).

constants.py : This file contains some static constants used in the experimental setting such as MAX_CORES (the maximum number of cores on each PM), MAX_MEM (the maximum memory in GB associated with each PM), MAX_PMS (the maximum number of PMs in the datacenter), MAX_VM_CORES (the maximum core capacity of a VM), MAX_VM_MEM (the maximum memory capacity in GB of a VM)

classes.py : This file contains some of the basic entities related to a cloud infrastructure such as PM (Physical Machine), User (a cloud user), VM (Virtual Machine), Datacenter (the Cloud Datacenter). Each entity has been represented in the form of a distinct Class and has properties (in the form of instance variables) and functionality (in the form of instance method) associated with it.

azureParser.py : This file provides a single a method called parse() which takes traceFile (the path location of cloud trace dataset), P_m (the percentage of malicious cloud users), seedVal (for initializing the Random Number Generator) as input and returns jobList (a list of VM job events sorted by the timestamp). It also instantiates VMs and Users while parsing the dataset and randomly marks P_m % of the instantiated users as malicious.

algorithms.py : This file contains the code of 7 different VM placement algorithms - BestFit, WorstFit, RandomPlacement, PreviousCoLocatedUsersFirst, DedicatedInstance, Azar, PreviousSelectedServersFirst. Each algorithm can been represented as a separate class consiting of 3 methods : init(), placeVM(), removeVM(). The purpose of init() is to initialize the datacenter and PMs within it, placeVM() handles the task of mapping a VM to a PM, removeVM() handles the task of deallocating a VM from the PM.

driver.py : This can be considered as the main file as it is the starting point of execution. It automatically calls all other files in appropriate sequence and finally displays the results. The correct syntax for executing this file from the command line is as follows :
python driver.py P-m algorithm trial \<k\>

In the above syntax :

-P-m : Indicates the % of malicious cloud users. It can be any value from 0 and 100.

-algorithm : Indicates which Placement Algorithm to use for mapping VMs to PMs. Can be any one of the following 7 values :
	bf : BestFit
	wf : WorstFit
	rp : RandomPlacement
	pcuf : PreviousCoLocatedUsersFirst
	di : DedicatedInstance
	azar : Azar
	pssf : PreviousSelectedServersFirst
  
-trial : Indicates how many times do you want to repeat the experiment. Different trials would allow you to experiment with different set of malicious users.

-k : This parameter is relevant only when the algorithm selected is either pssf or azar. It can be any value from 0 and 100. It represents the parametric values of Ng and λ for pssf and azar respectively. Refer to the paper for more details.

Sample command :
python driver.py 30 bf 10 0 

The above command would execute Best Fit placement algorithm using 30% of the users as malicious. The algorithm would be executed 10 times. For each run the CU (Core Utilization) and CLR (Co-Lcoation Resistance) would be reported on the standard output. Additionally, in the end, the avg CU and CLR would also be reported.
