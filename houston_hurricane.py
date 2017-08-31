from TwitterSearch import *
from collections import defaultdict # we will save unique urls here


#querries to search
sets_of_keywords=[
        ['Houston', '#hurricane','#HoustonStrong','Harvey','help'],
        ['Houston','flood','help'],
        ['texas','Harvey' ,'help' ],
        ['texas','Harvey' ,'hurricane' ],  
        ['texas','help' ,'flood' ],     
        ['texas','help' ,'Storm' ], 
        ['Houston','help' ,'Storm' ], 
        ['#hurricane','texas' ,'Storm' ],   
        ['hurricane','Houston' ,'help' ],         
        ]

hold_unique_urls=defaultdict(lambda:list) # holds url and lambda        

printed_data_all=open("tweets_for_hurricane_houston_mini.csv","w",1)
printed_data_all.write("url,date,text\n")
try:
    keys_passes=0
    for set_of_keys in sets_of_keywords:
        
        print (" searching for ", set_of_keys)
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.set_keywords(set_of_keys) # let's define all words we would like to have a look for
        tso.set_language('en') # we want to see english tweets only
        tso.set_include_entities(False) # and don't give us all those entity information
    
        # it's about time to create a TwitterSearch object with our secret tokens
        ts = TwitterSearch(
            consumer_key = 'your consumer_key',
            consumer_secret = 'your consumer_secret',
            access_token = 'your access_token',
            access_token_secret = 'your access_token_secret'
         )
         # this is where the fun actually starts :)
        count=0
        errors=0
        for tweet in ts.search_tweets_iterable(tso):
            #print (tweet['user']['entities']['url']['urls'][0]['url'])
            try:
                url="https://twitter.com/"+str(tweet['user']['screen_name']) + "/status/" + str(tweet['id'])
                tweet_txt= str(tweet['text']).replace(",","").replace("\n"," ").replace("\r"," ")
                date= str(tweet['created_at']).replace(" +0000","").replace(",","")
                hold_unique_urls[url]=[tweet_txt,date]
                printed_data_all.write("%s,%s,%s\n" % (url,date,tweet_txt))
                count+=1
            except:
                errors+=1
                
        keys_passes +=1
        print (" pass %d had %d tweets and %d errors " % (keys_passes,count,errors))        
        print (" finished pass %d " % (keys_passes))
    printed_data_all.close()
    
    print ("relevant tweets %d found " % (count))
    print (" unique tweets = %d " %(len(hold_unique_urls)))
    print (" writting down tweets ")
    
    printed_data=open("tweets_for_hurricane_houston.csv","w",1)
    printed_data.write("url,date,text\n")
    for tweet_url,list_elements in hold_unique_urls.items():
        printed_data.write("%s,%s,%s\n" % (tweet_url,list_elements[1],list_elements[0]))
    printed_data.close()
     
except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)


    
    
    