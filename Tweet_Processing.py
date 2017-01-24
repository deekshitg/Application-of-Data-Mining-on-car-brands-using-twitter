#import regex
import re
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from nltk.stem import PorterStemmer

ps = PorterStemmer()

#start process_tweet
def processTweet(tweet):
    # process the tweets
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','',tweet)
    #Remove additiobnal white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet
#end
#initialize stopWords
stopWords = []

#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end
#start extract_features
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features
#end
stopWords = (stopwords.words("english"))
#start getfeatureVector
def getFeatureVector(tweet,stopWords):
    featureVector = []
    #split tweet into words
    words = word_tokenize(tweet)
    for w in words:
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        #strip punctuation
        w = w.strip('\'",.:`()')
        if w:
            w = ps.stem(w)
            #check if the word stats with an alphabet
            val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
            #ignore if it is a stop word
            if(w in stopWords or val is None):
                continue
            else:
                featureVector.append(w.lower())
    return featureVector
#end

###Read the tweets one by one and process it
##fp = open('C:/Users/Sai Duth/Desktop/abc.csv', 'r')
##line = fp.readline()

##st = open('C:/Users/Sai Duth/Desktop/stop_words.txt', 'r')
##stopWords = getStopWordList('C:/Users/Sai Duth/Desktop/stop_words.txt')


#Read the tweets one by one and process it
inpTweets = csv.reader(open('C:/Users/Sai Duth/Desktop/experiment/train_dataset.csv', 'r'))
featureList = []
tweets = []
for row in inpTweets:
    sentiment = row[0]
    tweet = row[1]
    processedTweet = processTweet(tweet)
    featureVector = getFeatureVector(processedTweet, stopWords)
    featureList.extend(featureVector)
    tweets.append((featureVector,sentiment));


# Remove featureList duplicates
featureList = list(set(featureList))

# Extract feature vector
training_set = nltk.classify.util.apply_features(extract_features, tweets)


# Train the classifier
NBClassifier = nltk.NaiveBayesClassifier.train(training_set)
test_set = []
test_class = []
# Test the classifier
inpTestSet = csv.reader(open('C:/Users/Sai Duth/Desktop/experiment/test_dt.csv','r'))
for row in inpTestSet:
    testTweet = row[1]
    senti = row[0]
    processedTestTweet = processTweet(testTweet)
    sent = NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet, stopWords)))
    test_set.append((testTweet,senti));
    test_class.append((testTweet,sent))
    
#print(NBClassifier.show_most_informative_features(10))
with open('test_result.csv', 'w') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile, dialect='excel')
    for row in test_class:
        thedatawriter.writerow(row)

test_set1 = nltk.classify.util.apply_features(extract_features, test_set)
print('Accuracy of Naiave Bayes classifier in percentage',nltk.classify.accuracy(NBClassifier, test_set1)*100)


