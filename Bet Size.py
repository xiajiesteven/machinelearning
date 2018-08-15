#getSignal:
# inputs:
#    events: a matrix of data, with column = meta-labelling estimator, or a standard labeling estimator.
#    stepSize: a double
#    prob: a matrix with size = events.index  * 1. Each entry = max(output from ML classification algorithm, a numClass * 1 vector)
#    numClasses: the number of classes out of the ML algorithm, an int
# Outputs:
#   signal1 is the average bet size of the asset/portfolio. Mathematically it's 2* norm.cdf(signal0) - 1

def getSignal(events, stepSize,prob,pred,numClasses,numThreads,**kargs):
    if prob.shape[0] == 0:
        return pd.Series()
    #1) generate signals from one-vs-rest classification 
    signal0 = (prob - 1./numClasses)/(prob*(1.-prob))**.5 # t-value of OvR, a vector operation 
    signal0 = pred *(2*norm.cdf(singal0)-1)  # compute the bet size 
    # signal0.index = events.index
    if 'side' in events:
        singal0*=events.loc[singal0.index,'side'] # meta-labelling
    #2) compute average signal among those concurrently open
    # t1 is the termination time of the event/time series
    df0 = singal0.to_frame('signal').join(event[['t1']],how = 'left') # df0 is a data frame with index = events.index, column = ['signal','t1']
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

def mpAvgActiveSignals(signals,molecule):
    out = pd.Series()
    for loc in molecule:
        df0 = (signals.index.values <= loc) &((loc < signals['t1'])|pd.isnull(signals['t1'])) # A singal is active if 1) started before or at loc AND 2) end after loc
        act = signals[df0].index
        if len(act) >0:
            out[loc] = signals.loc[act,'signal'].mean()
        else:
            out[loc] = 0 # no signals active at this time
    return out

def discreteSignal(signal0, stepSize):
    # discretize signal
    signal1 = (signal0/stepSize).round() * stepSize # discretize 
    signal1[signal1 > 1] = 1
    signal1[signal1 < -1] = -1
    return signal1
