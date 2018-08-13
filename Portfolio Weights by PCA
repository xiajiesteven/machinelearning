def pcaWeights(cov,riskDist = None, riskTarget = 1.):
    # Following the riskAlloc distribution , match riskTarget
    eVal,eVec = np.linalg.eigh(cov)
    indices = eVal.argsort()[::-1] # arguments for sorting eVal desc
    eVal, eVec = eVal[indices],eVec[:,indices]
    if riskDist is None:
        riskDist = np.zeros(cov.shape[0])
        riskDist[-1] = 1.  # if risk distribution is not defined, then all risk is on the smalles eigenvalue
    loads = riskTarget*(riskDist/eVal)**.5
    wghts = np.dot(eVec,np.reshape(loads,(-1,1))) # the allocation in the old basis 
    return wghts
