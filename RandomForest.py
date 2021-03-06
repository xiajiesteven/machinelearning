# RF trains independently individual estimators over bootstrapped subsets of the data. 
# When optimizing each node split, only a random subsample of the attributes will be evaluated.

clf0 = RandomForestClassifier(n_estimator = 1000, class_weight = 'balanced_subsample',criterion = 'entropy' )
# balanced_subsample class weight means weights inversely proportional to the class frequency in the bootstrap sample for every tree grown.

clf1 = DecisionTreeClassifier(criterion = 'entropy', max_feature = 'auto',class_weights = 'balanced')
# auto max_feature means the number of feature for the tree is sqrt(number of feature)

clf1 = BaggingClassifier(base_estimator = clf1, n_estimators = 1000, max_samples = avgU)

clf2 = RandomForestClassifier(n_estimator = 1, criterion = 'entropy', bootstrap = False, class_weight = 'balanced_subsample')

clf2 = BaggingClassifier(base_estimator = clf2, n_estimator = 1000, max_samples = avgU, max_features = 1)
