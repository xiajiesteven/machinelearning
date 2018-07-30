def featImportance(trnsX,cont,n_estimator = 1000, cv = 10, max_samples = 1., numThreads = 24, pctEmbargo = 0,scoring = 'accuracy',method = 'SFI',minWLeaf =0.,**kargs):
    #feature importance from a random forest 
    from sklearn.tree import DecisionTreeClassifier 
    from sklearn.ensemble import BaggingClassifier
    from mpEngine import mpPandasObj
    n_jobs = (-1 if numTreads > 1 else 1)
    
    clf = DecisionTreeClassifier(criterion = 'entropy', max_feature = 1, class_weight = 'balanced', min_weight_fraction_leaf = minWLeaf) 
    # class_weight automatically adjust weights inversely proportional to class frequencies in the input data
    
    clf = BaggingClassifier(base_estimator = clf, n_estimators = n_estimators, max_features = 1., max_samples = max_samples, oob_scores = True, n_jobs = n_jobs)
    # max_feature and max_samples are double 1.0, which mean that we will use all of samples and features to train each individual base estimator
    
    fit = clf.fit(X=trnsX, y = cont['bin'],sample_weight = cont['w'].values)
    oob = fit.oob_score_
    
    if method == 'MDI':
        imp = featImpMDI(fit, featnames =trnsX.columns)
        oos = cvScore(clf,X=trnsX, y = cont['bin'], cv = cv, sample_weight = cont['w'],t1 = cont['t1'], pctEmbargo = pctEmbargo, scoring = scoring).mean()
        
    elif method == 'MDA':
        imp,oos = featImpMDA(clf, X=trnsX, y = cont['bin'], cv = cv , sample_weight = cont['w'], t1=cont['t1'], pctEmbargo = pctEmbargo, scoring = scoring)
    
    elif method == 'SFI':
        cvGen = PurgedKFold(n_splits = cv, t1 = cont['t1'], pctEmbargo = pctEmbargo)
        oos = cvScore(clf, X = trnsX, y = cont['bin'], sample_weight = cont['w'], scoring = scoring, cvGen = cvGen).mean()
        clf.n_jobs = 1
        imp = mpPandasObj(auxFeatImpSFI,('featNames',trnsX.columns),numThreads, clf = clf, trnsX = trnsX, cont = cont, scoring = scoring, cvGen = cvGen)
        
    return imp,oob,oos
