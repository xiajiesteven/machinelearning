# Inputs:
# close: A pandas series of prices
# tEvents: A pandas timeindex of starting timestamps for each sample. It could be the time of structural break or some events. 
# ptSl: A non-negative float that sets the width of the two barriers. A 0 value means that the repective horizontal barrier (profit taking or stop loss) will be disabled.
# t1: A pandas series with timestamps of the vertical barriers. We pass a False when we want to disable vertical barriers
# trgt: A pandas series of targets, expressed in terms of absolute returns. 
# minRet: The minimum target return required for running a triple barrier search.
# numThreads: The number of threads concurrently used by the function. 
# side: the side of bet , 1 or -1. 

#Output: events -- a pandas dataframe with column = t1 ( the termination time), 
                                                # = trgt ( absolute return target that is used to generate the horizontal barriers)
#                                     with index = events' starting time
# This function takes in side as an argument. When side is not None, then it is a multi-labelling and argument ptsl is a list of two 
# non-negative float numbers -- we discriminate between profit taking and stop loss. 

def getEvents(close,tEvents,ptSl,trgt,minRet,numThreads,t1=False,side = None):
    #1) get target
    trgt = trgt.loc[tEvents]
    trgt = trgt[trgt>minRet] # the minimal return
    #2) get t1 (max holding period)
    if t1 is False:
        t1 = pd.Series(pd.NaT, index = tEvents)
    #3) form events object, apply stop loss on t1
    if side is None: 
        side_,ptSl_ = pd.Series(1.,index = trgt.index),[ptSl[0],ptSl[1]] # if no side is provided, then by default side_ is set to be 1
    else:
        side_,ptSl_ = side.loc[trgt.index],ptSl[:2] 
    events = pd.concat({'t1':t1, 'trgt':trgt,'side':side},axis = 1).dropna(subset=['trgt'])
    df0 = mpPandasObj(func = applyPtSlOnT1, pdObj = ('molecule',events.index),numThreads = numThreads,close = close, events = events,ptSl = ptSl_)
    events['t1'] = df0.dropna(how = 'all').min(axis = 1) #pd.min ignores nan
    if side is None:
        events = events.drop('side',axis = 1)
    return events


#Inputs:
# close: A pandas series of prices
# events: A pd dataframe , with columns
    # t1: the vertical barrier 
    # trgt: unit width of the horizontal barrier, expressed in terms of absolute returns
    # side: 1 or -1
# ptSl: a list of two non-negative float values
    # ptSl[0] the factor that multiplies trgt to set the width of the upper barrier 
    # ptSl[1] the factor that multiplies trgt to set the width of the lower barrier 

# Outputs:
    # out is a Pandas DataFrame with columns: t1, sl and pt
    
def applyPtSlOnT1(close, events,ptSl,molecule):
    # apply stop lose/profit taking, if it takes place before t1 (end of event)
    events_ = events.loc[molecule]
    out = events_[['t1']].copy(deep = true)
    if ptSl[0] >0:
        pt = ptSl[0] * events_['trgt'] # upper bound
    else:
        pt = pd.Series(index = events.index) #NaNs
    if ptSl[1] > 0:
        sl = -ptSl[1] * events_['trgt'] # lower bound
    else:
        sl = pd.Series(index = events.index) #NaNs
    for loc,t1 in events_['t1'].fillna(close.index[-1]).iteritems(): # loc is the starting time, t1 is the end time
        df0 = close[loc:t1] #path prices 
        df0 = (df0/close[loc]-1) * events_.at[loc,'side'] # path returns
        out.loc[loc,'sl'] = df0[df0 < sl[loc]].index.min()
        out.loc[loc,'pt'] = df0[df0 > pt[loc]].index.min()
    return out

  # Adding a vertical barrier = a certain number of days after the starting time 

t1 = close.index.searchsorted(tEvents + pd.Timedelta(days = numDays)) # tEvents is the series of the starting time , close.index is also a series of time
t1 = t1[t1 < close.shape[0]] # truncated by the length of closed price series 
t1 = pd.Series(close.index[t1],index = tEvents[:t1.shape[0]])

# getBins: 
# Inputs: 
#   events: dataframe as the output from getEvents 
#   close: a pandas series of close prices 
# Outputs:
#   a dataframe with columns:
#      ret: the return realized at the time of the first touched barrier
#      bin: The label, {-1,0,1}, as the function of the sign of the outcomes.

def getBins(events,close):
    #1) prices aligned with events 
    events_ = events.dropna(subset=['t1'])
    px = events_.index.union(events_['t1'].values).drop_duplicates()
    px = close.reindex(px, method = 'bfill') #use the next valid observation to fill gap
    #2) create out object 
    out = pd.DataFrame(index = events_.index)
    out['ret'] = px.loc[events_['t1'].values].values/px.loc[events_.index]-1
    if 'side' in events_:
        out['ret'] *= events_['side']
    out['bin'] = np.sign(out['ret'])
    if 'side' in events_:
        out.loc[out['ret']<=0,'bin'] =0 
    return out
