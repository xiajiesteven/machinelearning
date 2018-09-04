#Inputs:
#  series is a pd data frame with index = time stamp
#  d: an integer 
#  thres: if thres = 1.0, then no weights is dropped 

def fracDiff(series,d,thres = 0.01):
    #1) Compute weight for the longest series
    w = getWeight(d,series.shape[0]) # 1 is the last element of w
    #2) Determine initial calcs to be skipped based on weight-loss threshold 
    w_ = np.cumsum(abs(w))
    w_/ = w_[-1]
    skip = w_[w_ > thres].shape[0]
    #3)  Apply weights to values 
    df={}
    for name in series.columns:
        seriesF,df_= series[[name]].fillna(method = 'ffill').dropna(),pd.Series()
        for iloc in range(skip,seriesF.shape[0]):
            loc = seriesF.index[iloc]
            if not np.isfinite(series.loc[loc,name]):
                continue # exclue NAs
            df_[loc] = np.dot(w[-(iloc+1):,:].T,seriesF.loc[:loc])[0,0] # w[-(iloc+1):,:] corresponds to the weights above the threshold
        df[name] = df_.copy(deep = True)
    df = pd.concat(df, axis = 1)
    return df

def getWeight(d,size):
    w = [1.]
    for k in range(1,size):
        w_ = w[-1]/k*(d-k+1)
        w.append(w_)
    w = np.array(w[::-1]).reshape(-1,1)
    return x
    
# define a fraction differential with fixed width
# we truncate the weights w by a threshold 
# Inputs:
#      thres: determines the cut-off weight for the window 

def fracDiff_FFD(series, d, thres = 1e-5):
    w = getWeights_FFD(d,thres)
    width = len(w)-1
    df={}
    for name in series.columns:
        seriesF,df_ = series[[name]].fillna(method = 'ffill').dropna(),pd.Series()
        for iloc1 in range(width,seriesF.shape[0]):
            loc0,loc1 = seriesF.index[iloc1-width],seriesF.index[iloc]
            if not np.isfinite(series.loc[loc1 ,name]):
                continue
            df_[loc1] = np.dot(w.T,seriesF.loc[loc0:loc1])[0,0]
        df[name] = df_.copy(deep = true)
    df = pd.concat(df,axis = 1)
    return df

def getWeights_FFD(d,thres):
    w=[1.]
    k = 1.0
    while -w[-1]/k*(d-k+1)<thres:
        w.append(-w[-1]/k*(d-k+1))
        k = k+1
        
    w = np.array(w[::-1]).reshape(-1,1)
    return w


def plotMinFFD():
    from statsmodels.tsa.stattools import adfuller
    path,instName ='./','ES1_Index_Method12'
    out = pd.DataFrame(columns=['adfStat','pVal','lags','nObs','95% conf','corr'])
    df0 = pd.read_csv(path+instName +'.csv',index_col = 0,parse_dates =True)
    for d in np.linspace(0,1,11):
        df1 = np.log(df0[['Close']]).resample('1D').last() # downcast to daily ones
        df2 = fracDiff_FFD(df1,d,thres = 0.01)
        corr = np.corrcoef(df1.loc[df2.index,'Close'],df2['Close'])[0,1] # compute the correlation between the original series and finite different series
        df2 = adfuller(df2['Close'],maxlag = 1,regression = 'c',autolag=None) # here 'c' means constant only 
        out.loc[d] = list(df2[:4]) + [df2[4]['5%']] + [corr] # with cricical value
    out.to_csv(path + instName + '_testMinFFD.csv')
    out[['adfStat','corr']].plot(secondary_y='adfStat')
    out[['adfStat','corr']].plot(secondary_y='adfStat')
    mpl.axhline(out['95% conf'].mean(),linewidth = 1, color = 'r',linestyle = 'dotted')
    return
    
