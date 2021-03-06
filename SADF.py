# We implement the Supreme ADF test 
# Inputs:
#    logP: a pd Series containing log prices
#    minSL: the minimal sample length used by the final regression 
#    constant: the regression's time trden component : 'nc' (no time trend),'ct'(first degree),'ctt' (constant + second-degree polynomial)
#    lags: the number of lags used in ADF specification

# Output: the supreme of ADF t-stats. It follows DF distribution. The null hypothesis is t=0 (random walk), the alternative is t<0 (statioinary) or t>0(momentum).

def get_bsadf(logP, minSL, constant, lags):
    y,x = getYX(logP, constant = constant, lags = lags)
    startPoints, bsadf, allADF = range(0,y.shape[0] + lags - minSL+1),None,[]
    for start in startPoints
        y_,x_ = y[start:],x[start:]
        bMean_,bStd_ = getBetas(y_,x_)
        bMean_,bStd_ = bMean_[0,0],bStd_[0,0]**.5
        allADF.append(bMean_/bStd_)  # look at the t-stats of ADF regression
        if allADF[-1] > bsadf: 
            bsadf = allADF[-1]
    out = {'Time':logP.index[-1],'gsadf':bsadf}
    return out

# reform the series as ADF model 

def getYX(series,constant,lags):
    series_ = series.diff().dropna()
    x = lagDF(series_,lags).dropna()
    x.iloc[:,0] = series.values[-x.shape[0]-1:-1,0] # the y_{t-1} term
    y = series_.iloc[-x.shape[0]:].values
    if constant != 'nc':
        x = np.append(x,np.ones((x.shape[0],1)),axis = 1)
        if constant[:2] == 'ct':
            trend = np.arange(x.shape[0]).reshape(-1,1)
            x = np.append(x,trend,axis = 1)
        if constant == 'cct':
            trend = np.arange(x.shape[0]).reshape(-1,1)
            x = np.append(x,trend**2,axis = 1)
    return y,x
    
 def lagDF(df0,lags):
    df1 = pd.DataFrame()
    if isinstance(lags,int):
        lags = range(lags+1)
    else: 
        lags = [int(lag) for lag in lags]
    for lag in lags:
        df_ = df0.shift(lag).copy(deep=True)
        df_.columns = [str(i)+'_'+str(lag) for i in df_.columns]
        df1 = df1.join(df_,how = 'outer')
    return df1
    
# perform the ADF test     
def getBetas(y,x):
    xy = np.dot(x.T,y)
    xx = np.dot(x.T,x)
    xxinv = np.linalg.inv(xx)
    bMean = np.dot(xxinv,xy)
    err = y - np.dot(x,bMean)
    bVar = np.dot(err.T,err)/(x.shape[0]-x.shape[1])*xxinv # x.shape[0]-x.shape[1] gives the freedom degree
    return bMean,bVar
