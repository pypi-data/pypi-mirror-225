import numpy as np
from gastimator import gastimator
import matplotlib.pyplot as plt
#from time import sleep
from gastimator import corner_plot

# from astropy.modeling.models import ExponentialCutoffPowerLaw1D
# def mod4pdf(values,x):
#     return ExponentialCutoffPowerLaw1D(amplitude=values[0], x_0=values[1], alpha=values[2], x_cutoff=values[3])(x)

def gaussian(values,x):
    mu=values[0]
    sigma=values[1]
    #sleep(0.05)
    x = (x - mu) / sigma
    return np.exp(-x*x/2.0) #/ np.sqrt(2.0*np.pi) / sigma
    
def myfunc(values,x):
    norm=values[0]
    x0=values[1]
    width=values[2]
    out=x.copy()*0
    out[x<x0]=1
    out[x>=x0]=gaussian([x0,width],x[x>=x0])
    return out*norm    
    

def fitmyfunc(samples):
    hi,b=np.histogram(samples,bins=100,density=True)
    err=np.sqrt(hi*len(samples))/len(samples)
    mcmc2 = gastimator(myfunc,b[1:])
    mcmc2.labels=np.array(['norm','x0','width'])
    mcmc2.guesses=np.array([0.5,7,0.3]) # these are purposefully way off
    mcmc2.min=np.array([0.01,np.min(outputvalue[2,:]),0.01]) # allow the fit to guess values between these minimum values
    mcmc2.max=np.array([1,np.max(outputvalue[2,:]),10]) # ... and these maximum values
    mcmc2.fixed=np.array([False, False,False]) #if you would like to fix a varts value to True here.
    mcmc2.precision=np.array([100.,0.1,0.1]) #here we assume and gradient within ±1.0 - very conservative
    mcmc2.prior_func=(None,None,None)
    nsamples=300000
    mcmc2.silent=True

    #mcmc.input_checks()
    #print(mcmc.prior_func)
    #mcmc.nprocesses=1
    outputvaluez, outputllz= mcmc2.run(hi,err,nsamples,nchains=1,plot=False)
    bestz=np.median(outputvaluez,1)
    #breakpoint()
    print(bestz[1:])
    # plt.plot(b[1:],hi)
    # plt.plot(b[1:],myfunc(bestz,b[1:]))
    # plt.show()
    
    return bestz[1],bestz[2]
    
    
def model(values,x):
    vmax=values[0]
    rturn=values[1]
    mbh=values[2]
    return np.sqrt((vmax*np.arctan(x/rturn))**2 + (4.301e-3*(10**mbh))/(x*4.84*16.5))
    
truth=np.array([300,1,6])
x=np.arange(0.15,10.,0.05)
error=50

data=model(truth,x)
data+=np.random.normal(size=x.size)*error

bottomrange=[1,2,3,4,5]
val=[]
val2=[]
val3=[]
for btm in bottomrange:
    mcmc = gastimator(model,x)
    mcmc.labels=np.array(['vmax','rturn','logmbh'])
    mcmc.guesses=np.array([250,2,7]) # these are purposefully way off
    mcmc.min=np.array([10.,0.,btm]) # allow the fit to guess values between these minimum values
    mcmc.max=np.array([500.,5,10]) # ... and these maximum values
    mcmc.fixed=np.array([False, False,False]) #if you would like to fix a varts value to True here.
    mcmc.precision=np.array([10.,0.1,0.3]) #here we assume and gradient within ±1.0 - very conservative
    mcmc.prior_func=(None,None,None)
    nsamples=1000000
    mcmc.silent=True

    #mcmc.input_checks()
    #print(mcmc.prior_func)
    #mcmc.nprocesses=1
    outputvalue, outputll= mcmc.run(data,error,nsamples,nchains=3,plot=False)    
    val.append(np.percentile(outputvalue[2,:],99.))
    v2,v3=fitmyfunc(outputvalue[2,:])
    val2.append(v2)
    val3.append(v3)
    
    #fitmyfunc(outputvalue[2,:])
    #breakpoint()
#breakpoint()
plt.plot(bottomrange,val,'o-',label=r'Percentile 99%')
plt.plot(bottomrange,np.array(val2)+1.5*np.array(val3),'o-',label='Functional Form')
plt.legend(frameon=False)
plt.xlabel("Lower Prior Bound Mass")
plt.ylabel("M(BH) limit")
plt.savefig("ULtest.pdf")
#
plt.show()
breakpoint()
#figure = corner_plot.corner_plot(outputvalue.T,like=outputll,labels=mcmc.labels,quantiles=[0.16, 0.5, 0.84], truths=truth)
#plt.show()

#best=np.median(outputvalue,1)

#breakpoint()
# plt.plot(x,data)
# plt.plot(x,model(best,x))
# plt.show()
