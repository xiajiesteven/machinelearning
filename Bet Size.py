def getSignal(events, stepSize,prob,pred,numClasses,numThreads,**kargs):
    if prob.shape[0] == 0:
        return pd.Series()
    #1) generate signals from one-vs-rest classification 
    signal0 = (prob - 1./numClasses)/(prob*(1.-prob))**.5 # t-value of OvR
    signal0 = pred *(2*norm.cdf(singal0)-1)
    if 'side' in events:
        singal0*=events.loc[singal0.index,'side'] # meta-labelling
    #2) compute average signal among those concurrently open
    df0 = singal0.to_frame('signal').join(event[['t1']],how = 'left')
    df0 = avgActiveSignals(df0,numThreads)
    signal1 = discreteSignal(signal0 = df0, stepSize = stepSize )
    return signal1
    
    def avgActiveSignals(signals,numThreads):
    # compute the average signal among those active 
    # 1) time points where signals change (either one starts or one ends)
    tPnts = set(signals['t1'].dropna().values)
    tPnts = tPnts.union(signals.index.values)
    tPnts = list(tPnts)
    tPnts.sort()
    out = mpPandasObj(mpAvgActiveSignals,('molecule',tPnts),numThreads,signals = signals)
    return out
