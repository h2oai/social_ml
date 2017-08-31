# Social ML

Wouldn't be great to use machine learning and artificial intelligence to help our neighbours, our friends who might be in danger? Who knows **someone might be able to help**. The web may be chaotic, yet contains significant information for those around us that might need our help. **Machine learning** can help us structure this data and hopefully make it more useful.

## Hurricane Harvey

In this instance we scrape data from [twitter](https://twitter.com/) including hashtags regrading [Hurricane Harvey](https://en.wikipedia.org/wiki/Hurricane_Harvey) and classifiy/order tweets with serious or negative intent. We built this classification model using [H2o's GBM](http://docs.h2o.ai/h2o/latest-stable/h2o-docs/data-science/gbm.html) and [sklearn's tf-idf](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) on a sample of the [sentiment140](http://help.sentiment140.com/for-students/) dataset.  

## requirements

### python 2.7

### Install python ml libraries
```
pip install sklearn
pip install numpy
pip install pandas
pip install scipy

```
### Install h2o

```
pip install requests
pip install tabulate
pip install scikit-learn
pip install colorama
pip install future
pip uninstall h2o
pip install http://h2o-release.s3.amazonaws.com/h2o/master/4010/Python/h2o-3.15.0.4010-py2.py3-none-any.whl
```

### Install TwitterSearch

```
pip install TwitterSearch
```

### set up a twitter app

-    Create a Twitter user account if you do not already have one.
-    Go to [https://apps.twitter.com/](https://apps.twitter.com/) and log in with your Twitter user account. This step gives you a Twitter dev account under the same name as your user account.
-    Click **Create New App**
-    Fill out the form, agree to the terms, and click **Create your Twitter application**
-    In the next page, click on **Keys and Access Tokens** tab, and copy your **API key** and **API secret**. Scroll down and click **Create my access token**, and copy your **Access token** and **Access token secret**.

source [here](http://socialmedia-class.org/twittertutorial.html)

## Run

```
git clone https://github.com/h2oai/social_ml.git
```


in `houston_hurricane.py` add your twitter info in :

```
consumer_key = 'your consumer_key',
consumer_secret = 'your consumer_secret',
access_token = 'your access_token',
access_token_secret = 'your access_token_secret'
```
consider changing your search terms/tags in 

```
sets_of_keywords=[
        ['Houston', '#hurricane','#HoustonStrong','Harvey','help'],
		['Houston','flood','help'],
        ['texas','Harvey' ,'help' ],
		...
		...
		]
```

run houston_hurricane.py

```
python houston_hurricane.py
```

the produced **tweets_for_hurricane_houston.csv** will save have 3 comman separated fields [url, date, tweet]


Then run model_sentiment.py

```
python model_sentiment.py

```
This will build a classifier based on the sentiment data (**sentiment_m140_.csv**) and classify the tweets (low score= severe comment, high score= positive comment). 
the ranked results will be placed in **ranked_tweets.csv** . 
The **ranked_houston_tweets.xls** was created manually from **ranked_tweets.csv** to make the output more clear

### Sample tweets

date | tweet | severity
--- | --- | ---
Thu Aug 31 2017	| Woke up feeling sad this morning for our neighbors in #texas. They need our help: https://t.co/oNJgtr6uZL	| 14.0%
Wed Aug 30 2017	| RT @BrettFOX46: This is so sad! The storm may be out of Houston but people still need help across the Gulf Coast! https://t.co/Pia1M3k2QW	| 16.9%
