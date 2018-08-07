

def getTrainTimes(t1,testTimes):
    # given testTimes, find the times of the training observations. 
    # t1.index: Time when the observation started
    # t1.value: Time when the observation ended
    # testTimes: Times of testing observations 
    trn = t1.copy(deep = True )
    for i,j in testTimes.iteritems():
        df0 = trn[(i<=trn.index)&(trn.index <= j)].index # train starts within test
        df1 = trn[(i<=trn)&(trn<=j)].index # train ends within test
        df2 = trn[(trn.index <= i)&(j<=trn)].index # train envelop test
        trn = trn.drop(df0.union(df1).union(df2))
    return trn

def getEmbargoTimes(times,pctEmbargo):
    # Get embargo time for each bar
    step = int(times.shape[0] * pctEmbargo)
    if step == 0:
        mbrg = pd.Series(times,index = times)
    else:
        mbrg = pd.Series(times[step:],index = times[:-step])
        mbrg = mbrg.append(pd.Series(times[-1],index = times[-step:]))
    return mbrg
            

class PurgedKFold(_BaseKFold):
    # Extend KFold class to work with labels that span intervals 
    # The train is purged of obervation overlapping test-label intervals
    # Test set is assumed continous without training sample 
    
    def _init_(self,n_splits = 3, t1=None, pctEmbargo = 0.):
        if not isinstance(t1,pd.Series):
            raise ValueError('Label Through Dates must be a pd.Series')
        super(PurgedKFold,self)._init_(n_splits, shuffle = False, random_state = None)
        self.t1 = t1
        self.pctEmbargo = pctEmbargo
        
def split(self,X,y=None, groups = None):
    if (X.index == self.t1.index).sum() != len(self.t1):
        raise ValueError('X and ThruDateValues must have the same index')
    indices = np.arrange(X.shape[0])
    mbrg = int(X.shape[0] * self.pctEmbargo)
    test_starts = [(i[0],i[-1]+1) for i in np.array_split(np.arrange(X.shape[0]),self.n_splits)]
     # separate the array (not necessarily evenly) into n_splits parts 
    for i,j in test_starts:
        t0 = self.t1.index[i] # start of test set 
        test_indices = indices[i:j]
        maxT1Idx = self.t1.index.searchsorted(self.t1[test_indices].max())
        train_indices = self.t1.index.searchsorted(self.t1[self.t1 <= t0].index)
        if maxT1Idx < X.shape[0]: # the right to the test data 
            train_indices = np.concatenate((train_indices, indices[maxT1Idx+mbrg:]))
        yield train_indices,test_indices
