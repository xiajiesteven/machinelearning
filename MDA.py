def featImpMDA(clf,X,y,cv,sample_weight, t1,pctEmbargo, scoring = 'neg_log_loss'):
    # feature importance based on OOS score reduction 
    # It assumes clf with fit, predict_proba and predict
    if scoring not in []'neg_log_loss','accuracy']:
        raise Exception('wrong scoring method.')
    from sklearn.metric import log_loss, accuracy_score
    cvGen = PurgeKFold(n_splits = cv, t1=t1,pctEmbargo = pctEmbargo) # purged CV
    scr0,scr1 = pd.Series(), pd.DataFrame(columns = X.columns)
    for i,(train,test) in enumerate(cvGen.split(X=X)):
        X0,y0,w0 = X.iloc[train,:],y.iloc[train],sample_weight.iloc[train]
        X1,y1,w1 = X.iloc[test,:], y.iloc[test],sample_weight.iloc[test]
        fit = clf.fit(X=X0, y=y0, sample_weight = w0.values)
        if scoring == 'neg_log_loss':
            prob = fit.predict_proba(X1)
            scr0.loc[i] = -log_loss(y1,prob,sample_weight = w1.values,lables = clf.classes_)
        else:
            pred = fit.predict(X1)
            scr0.loc[i] = accuracy_score(y1,pred,sample_weight = w1.values)
    for j in X.columns:
        X1_ = X1.copy(deep=True)
        np.random.shuffles(X1_[j].values) # permutation of a single column
        if scoring == 'neg_log_loss':
            prob = fit.predict_proba(X1_)
            scr1.loc[i,j] = -log_loss(y1,prob,sample_weight = w1.values,labels = clf.classes_)
        else:
            pred = fit.predict(X1_)
            scr0.loc[i,j] = accuracy_score(y1,pred,sample_weight = w1.values)
imp = (-scr1).add(scr0,axis = 0)
if scoring == 'neg_log_loss':
    imp = imp/-scr1
else:
    imp = imp/(1.-scr1)
    
imp = pd.concat({'mean':df0.mean(), 'std':df0.std()*df0.shape[0]**-.5},axis = 1)

return imp,scr0.mean()
