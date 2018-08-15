#
# close: A pandas series of prices
# events: A pd dataframe , with columns
    # t1: the vertical barrier 
    # trgt: unit width of the horizontal barrier
    # side: 1 or -1
# ptSl: a list of two non-negative float values
    # ptSl[0] the factor that multiplies trgt to set the width of the upper barrier 
    # ptSl[1] the factor that multiplies trgt to set the width of the lower barrier 

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
