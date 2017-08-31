# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 15:08:13 2017

@author: mimar
"""
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf-8')

import pandas as pd
import numpy as np
from scipy.stats import pearsonr #correlation
from sklearn.feature_extraction.text import TfidfVectorizer
import H2OGBMClassifier as hgb
from sklearn.metrics import roc_auc_score
import sys
from collections import defaultdict
import operator
#import sys

#reload(sys)  # Reload does the trick!
#sys.setdefaultencoding('utf-8')

data=pd.read_csv("sentiment_m140_.csv")

print (data.shape)
target=data["target"].astype(float) #retrieve target
print (" average target is %f "  % np.mean(target))

text=data["text"].values #retrieve text


#load twitter houston data
#contaiins  url, date, tweet,

unique_dicts=defaultdict(lambda:list)
houston_file=open("tweets_for_hurricane_houston.csv","r")
houston_file.readline()
k=0
for line in houston_file:
    line=line.replace("\n","")
    splits=line.split(",")
    try:
        unique_dicts[splits[0]]=[splits[1],splits[2]]
    except:
        print("problem in %d"% (k))
    k+=1
    
print ("uniqur tweets %d " % (len(unique_dicts)))

url=[]
text_houston=[]
date=[]
    
for link,list_elements in unique_dicts.items():
    url.append(link)
    text_houston.append(list_elements[1])
    date.append(list_elements[0]) 
    

#tf-idf model
tfv=TfidfVectorizer(min_df=0, max_features=3000, strip_accents='unicode',lowercase =True,
                            analyzer='word', token_pattern=r'\w{3,}', ngram_range=(1,1),
                            use_idf=True,smooth_idf=True, sublinear_tf=True, stop_words = "english")   
#h2o gbm model
model=hgb.H2OGBMClassifier (ntrees=100,learn_rate=0.1,distribution="bernoulli",col_sample_rate=1.0,col_sample_rate_per_tree =0.5,
            nthread=15,sample_rate=0.9,stopping_metric="logloss",nbins=255,min_rows=1,ram="20G",max_depth=4,seed=1)

#apply tf idf
data=tfv.fit_transform(text)
data=data.toarray()
print (data.shape)

#transform tweets
houston_data=tfv.transform(text_houston)
houston_data=houston_data.toarray()
print (houston_data.shape)

#fit model
model.fit(data,np.array(target)) # feed target

#make predictions)probabilities) on tweets
preds=model.predict_proba(houston_data)[:,1]

array_with_all_elements=[]
for i in range (len(preds)):
    array_with_all_elements.append([url[i], date[i],text_houston[i],preds[i] ])

#sort in ascending manner based on prediction
array_with_all_elements=sorted(array_with_all_elements, key=operator.itemgetter(3)) 

#save results to ranked_tweets.csv

save_results=open("ranked_tweets.csv" , "w")
save_results.write("url,date,tweet,severity\n")
for i in range (len(array_with_all_elements)): 
    save_results.write("%s,%s,%s,%s\n" % (array_with_all_elements[i][0],array_with_all_elements[i][1],array_with_all_elements[i][2],array_with_all_elements[i][3]))
save_results.close()

#print ("training auc is %f" %roc_auc_score(target,preds) )
