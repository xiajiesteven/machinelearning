import scipy.cluster.hierarchy as sch
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as mpl

def getIVP(cov,**kargs): #Compute the inverse-variance portfolio
    ivp = 1./np.diag(cov)
    ivp/= ivp.sum()
    return ivp
def getClusterVar(cov,cItems):
    cov_ = cov.loc[cItems,cItems]
    w_ = getIVP(cov_).reshape(-1,1)
    cVar = np.dot(np.dot(w_.T,cov_),w_)[0,0]
    return cVar

# link is a (N-1)*4 matrix Z. The first two columns contain the two elements in the clusters. The thrid column is the correlation between the two elements. The fourth is the number of original elements in the cluster.
def getQuasiDiag(link):
    link = link.astype(int)
    sortIx = pd.Series([link[-1,0],link[-1,1]])
    numItems = link[-1,3]
    while sortIx.max()>=numItems:
        sortIx.index = range(0,sortIx.shape[0]*2,2)
        df0 = sortIx[sortIx >= numItems]
        i = df0.index
        j = df0.values - numItems # the cluster of Z[i,0] and Z[i,1] is labelled as N+i
        sortIx[i] = link[j,0]  # replace the i-th position by the first element in Cluster i
        df0 = pd.Series(link[j,1],index = i+1) # replace the (i+1)-th position by the second element in Cluster i
        sortIx = sortIx.append(df0) 
        sortIx = sortIx.sort_Ix()
        sortIx.index = range(sortIx.shape[0]) 
    return sortIx.tolist()


def getRecBipart(cov,sortIx):
    w = pd.Series(1,index = sortIx)
    cItems = [sortIx]
    while len(cItems) > 0:
        cItems = [i[j:k] for i in cItems for j,k in ((0,len(i)/2),(len(i)/2,len(i))) if len(i)>1] # for each item i in cItems , we bisect the item i.
        for i in xrange(0,len(cItems),2):  # step size = 2 . In one iteration, we deal with two indices i and i+1
            cItems0 = cItems[i] 
            cItems1 = cItems[i+1] 
            cVar0 = getClusterVar(cov,cItems0)
            cVar1 = getClusterVar(cov, cItems1)
            alpha = 1- cVar0/(cVar0+cVar1)
            w[cItem0] *= alpha
            w[cItem1] *= 1 - alpha
    return w

def correlDist(corr):
    dist = ((1-corr)/2.)**.5 #distance matrix
    return dist

def generateData(nObs, size0,size1,sigma1):
    np.random.seed(seed = 12345)
    random.seed(12345)
    x = np.random.normal(0,1,size=(nObs,size0))
    
    cols = [random.randint(0,size0-1) for i in xrange(size1)]
    y = x[:,cols] + np.random.normal(0,sigma1,size=(nObs,len(cols)))
    x = np.append(x,y,axis=1)
    
    x = pd.DataFrame(x, columns = range(1,x.shape[1]+1))
    return x,cols
