import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def solve(m1,m2,std1,std2):
    a = 1./(2.*std1**2) - 1./(2.*std2**2)
    b = m2/(std2**2) - m1/(std1**2)
    c = m1**2 /(2*std1**2) - m2**2 / (2*std2**2) - np.log(std2/std1)
    return np.roots([a,b,c])

# m1 = 0.2
# std1 = 0.1
# m2 = 1
# std2 = 0.5

def findOverlap(m1, std1, m2, std2):
    
    if(m1 == m2 and std1 == std2):
        return 1.0
    result = solve(m1,m2,std1,std2)
    # 'lower' and 'upper' represent the lower and upper bounds of the space within which we are computing the overlap
    # lower = -100000000.0
    lower = -10000.0
    # upper = 100000000.0
    upper = 10000.0
    overlap = 0.0

    if(len(result)==0): # Completely non-overlapping 
        overlap = 0.0

    elif(len(result)==1): # One point of contact
        r = result[0]
        if(m1>m2):
            tm,ts=m2,std2
            m2,std2=m1,std1
            m1,std1=tm,ts
        if(r<lower): # point of contact is less than the lower boundary. order: r-l-u
            overlap = (norm.cdf(upper,m1,std1)-norm.cdf(lower,m1,std1))
        elif(r<upper): # point of contact is more than the upper boundary. order: l-u-r
            overlap = (norm.cdf(r,m2,std2)-norm.cdf(lower,m2,std2))+(norm.cdf(upper,m1,std1)-norm.cdf(r,m1,std1))
        else: # point of contact is within the upper and lower boundaries. order: l-r-u
            overlap = (norm.cdf(upper,m2,std2)-norm.cdf(lower,m2,std2))

    elif(len(result)==2): # Two points of contact
        r1 = result[0]
        r2 = result[1]
        if(r1>r2):
            temp=r2
            r2=r1
            r1=temp
        if(std1>std2):
            tm,ts=m2,std2
            m2,std2=m1,std1
            m1,std1=tm,ts
        if(r1<lower):
            if(r2<lower):           # order: r1-r2-l-u
                overlap = (norm.cdf(upper,m1,std1)-norm.cdf(lower,m1,std1))
            elif(r2<upper):         # order: r1-l-r2-u
                overlap = (norm.cdf(r2,m2,std2)-norm.cdf(lower,m2,std2))+(norm.cdf(upper,m1,std1)-norm.cdf(r2,m1,std1))
            else:                   # order: r1-l-u-r2
                overlap = (norm.cdf(upper,m2,std2)-norm.cdf(lower,m2,std2))
        elif(r1<upper): 
            if(r2<upper):         # order: l-r1-r2-u
                # print norm.cdf(r1,m1,std1), "-", norm.cdf(lower,m1,std1), "+", norm.cdf(r2,m2,std2), "-", norm.cdf(r1,m2,std2), "+", norm.cdf(upper,m1,std1), "-", norm.cdf(r2,m1,std1)
                overlap = (norm.cdf(r1,m1,std1)-norm.cdf(lower,m1,std1))+(norm.cdf(r2,m2,std2)-norm.cdf(r1,m2,std2))+(norm.cdf(upper,m1,std1)-norm.cdf(r2,m1,std1))
            else:                   # order: l-r1-u-r2
                overlap = (norm.cdf(r1,m1,std1)-norm.cdf(lower,m1,std1))+(norm.cdf(upper,m2,std2)-norm.cdf(r1,m2,std2))
        else:                       # l-u-r1-r2
            overlap = (norm.cdf(upper,m1,std1)-norm.cdf(lower,m1,std1))
   

    # print overlap
    # # print ""

    # x = np.linspace(-5,9,10000)
    # plot1=plt.plot(x,norm.pdf(x,m1,std1))
    # plot2=plt.plot(x,norm.pdf(x,m2,std2))
    # plot3=plt.plot(result,norm.pdf(result,m1,std1),'o')
    # plt.show()

    return overlap