# Mean Derease Impurity Test (for Random Forest)

# MDI is only for Random Forest. For each node of each tree in RF, the feature is chosen to be the best (to reduce impurity) from a random selected subset of features, instead from the whole set of features
# We will average those importance scores across all trees and rank the features accordingly.

def featImpMDI(fit,featNames):
    # feature importance based on In Sample impurity reduction 
    # fit is the RandomForest class in Sklearn, with max_feature = 1 
    df0 = {i:tree.feature_importances_ for i,tree in enumerate(fit.estimators_)} 
    # estimators_ is the collection of tress in the RF
    # feature_importances_ for a feature is the percentage of nodes/splits using this feature in the tree
    df0.columns = feaNames
    df0 = df0.replace(0,np.nan)
    imp = pd.concat({'mean':df0.mean(), 'std':df0.std()*df0.shape[0]**-.5},axis = 1)
    imp/=imp['mean'].sum()
    return imp
