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
    
