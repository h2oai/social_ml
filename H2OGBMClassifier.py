from sklearn.base import BaseEstimator, ClassifierMixin
import pandas as pd
import sys
import numpy as np
import h2o
import gc
             
from h2o.estimators.gbm import H2OGradientBoostingEstimator
class H2OGBMClassifier(BaseEstimator, ClassifierMixin):
  def __init__(self,
           ntrees=100,
            learn_rate=0.1,
            balance_classes=True,
            distribution="bernoulli",
            stopping_metric="logloss",
            max_depth=7,
            stopping_tolerance=0.01, #10-fold increase in threshold as defined in rf_v1
            stopping_rounds=20,
            model_id="gbm",
            col_sample_rate=0.5,
            col_sample_rate_per_tree =0.5,
            nthread=-1,
            ram="60G",
            sample_rate=0.9,
            nbins=255,
            min_rows=1,
            seed=1
      ):    
    assert distribution in [ 'bernoulli', 'multinomial', 'poisson', 'gamma', 'tweedie', 'laplace', 'quantile', 'gaussian']
    assert stopping_metric in ['AUTO', 'deviance', 'logloss', 'MSE', 'AUC', 'r2', 'misclassification']
    
    self.distribution=distribution
    self.stopping_metric=stopping_metric
    self.stopping_tolerance = stopping_tolerance
    self.model_id = model_id
    self.ntrees = ntrees
    self.learn_rate = learn_rate
    self.nthread = nthread 
    self.sample_rate=sample_rate
    self.nbins=nbins
    self.ram=ram    
    self.min_rows=min_rows
    self.col_sample_rate = col_sample_rate
    self.col_sample_rate_per_tree = col_sample_rate_per_tree     
    self.stopping_rounds = stopping_rounds
    self.balance_classes=balance_classes
    self.max_depth=max_depth
    self.seed=seed
    self.model=None
    h2o.init(max_mem_size = self.ram ,nthreads = self.nthread)  
    

  def build_matrix(self, X, opt_y=None):
      
    if  type(opt_y) is type(None):
        ytemp=np.array([0 for k in range (0,X.shape[0])])
        Xtemp=np.column_stack((ytemp,X))
        Xtemp=h2o.H2OFrame(Xtemp)
    else :
        ytemp=np.array(opt_y)
        Xtemp=np.column_stack((ytemp,X))
        Xtemp=h2o.H2OFrame(Xtemp)        
        
    #covtype_X = Xtemp.col_names[1:]     #last column is Cover_Type, our desired response variable 
    covtype_y = Xtemp.col_names[0]
    if self.distribution in [ 'bernoulli', 'multinomial']:
        Xtemp[covtype_y] = Xtemp[covtype_y].asfactor()    #make factor  
    return Xtemp

  def set_params(self,random_state=1):
      self.seed=random_state


  def fit(self, X, y):   
      
    X = self.build_matrix(X, y)
    
    
    self.model = H2OGradientBoostingEstimator(
        ntrees=self.ntrees,
        learn_rate=self.learn_rate,
        balance_classes=self.balance_classes,
        distribution=self.distribution,
        stopping_metric=self.stopping_metric,
        max_depth=self.max_depth,
        stopping_tolerance=self.stopping_tolerance, 
        stopping_rounds=self.stopping_rounds,
        model_id=self.model_id,
        seed=self.seed,
        min_rows=self.min_rows,
        sample_rate=self.sample_rate,
        nbins=self.nbins,
        col_sample_rate=self.col_sample_rate,
        col_sample_rate_per_tree=self.col_sample_rate_per_tree
    )    
    
    self.model.train( X.col_names[1:], X.col_names[0], training_frame=X  ) # training
    #finish training relase memory
    #there is probably much better was to release memory from the cluster
    X=None
    gc.collect()

    return self

  def predict(self, X):  #this predicts classification
    X = self.build_matrix(X)    
    if self.distribution in [ 'bernoulli', 'multinomial']:
        preds = self.model.predict(X ).as_data_frame().as_matrix()[:,2] 
        preds=np.arra([1 if pr >=0.5 else 0 for pr in preds]) 
    else :
        preds = self.model.predict(X ).as_data_frame().as_matrix()[:,0]
    X=None
    gc.collect()    
    return preds
  
  def predict_proba(self, X): 
    X = self.build_matrix(X)
    preds = self.model.predict(X ).as_data_frame().as_matrix()[:,1:]     
    X=None
    gc.collect()    
    return preds

def close_cluster(self): 
    h2o.cluster().shutdown() #should be invoked after all preds are done to relase memory   
    gc.collect()     
    