# implement PCA to obtain the othogonal feature
# We can compare the eigenvalue associated to an eigenvector (ignore the labelling information) with the MDI score of the feature associated to the eigenvector (using labelling information). 

def get_eVec(dot,varThres):
    # compute eVec from dot prod matrix, reduce dimension 
    eVal,eVec = np.linalg.eigh(dot)
    idx = eVal.argsor()[::-1] # arguments for sorting eVal desc
    eVal,eVec = eVal[idx],eVec[:,idx]
    
    eVal = pd.Series(eVal, index=['PC_'+str(i+1) for i in range(eVal.shape[0])])
    eVec = pd.DataFrame(eVec, index = dot.index, columns = eVal.index)
    eVec = eVec.loc[:,eVal.index]
    
    cumVar = eVal.cumsum()/eVal.sum()
    dim = cumVar.values.searchsorted(varThres)
    eVal,eVec = eVal.iloc[:dim+1],eVec.iloc[:,:dim+1]
    return eVal,eVec

def orthoFeats(dfX,varThres = .95):
    # Given a dataframe dfX of features, compute orthofeatures dfP
    dfZ = dfX.sub(dfX.mean()).div(dfX.std(),axis = 1)
    dot = pd.DataFrame(np.dot(dfZ.T,dfZ),index = dfX.columns,columns = dfX.columns)
    eVal,eVec = get_eVec(dot, varThres)
    dfP = np.dot(dfZ,eVec)
    return dfP
