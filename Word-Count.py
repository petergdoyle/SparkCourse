import re
from pyspark import SparkConf, SparkContext

def normalizeWords(text):
    return re.compile(r'\W+', re.UNICODE).split(text.lower())

conf = SparkConf().setMaster("local").setAppName("WordCount")
sc = SparkContext(conf = conf)

input = sc.textFile("/vagrant/Book.txt")
#a simple split works
#words = input.flatMap(lambda x: x.split())
#but let's clean the text up a bit and filter out special characters and consider upper and lowercase to be the same thing
words = input.flatMap(normalizeWords)
# results = words.collect()
# for result in results:
#    print result

# #python function
# #wordCounts = words.countByValue()

#take a spark approach...
#convert each word to a key/value pair with a value of 1
wordCountsMap = words.map(lambda x: (x,1))
# results = wordCountsMap.collect()
# for result in results:
#    print result


#count words with reduceByKey so reduceByKey will build a Set of each work and count the 1s!
wordCountsReduced = wordCountsMap.reduceByKey(lambda x, y: x + y)
results = wordCountsReduced.collect()
# for result in results:
#    print result

wordCountsSorted = wordCountsReduced.map(lambda (x,y): (y,x)).sortByKey()
results = wordCountsSorted.collect()

for result in results:
    # print result
    count = str(result[0])
    word = result[1].encode('ascii', 'ignore')
    if (word):
        print word + ":\t\t" + count
