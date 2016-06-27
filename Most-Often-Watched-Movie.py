
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("MostOftenWatchedMovies")
sc = SparkContext(conf = conf)

def parseLineAll(line):
    fields = line.split()
    userId = int(fields[0])
    movieId = int(fields[1])
    rating = int(fields[2])
    timestamp = long(fields[3])
    return (userId,(movieId,rating,timestamp))

def parseLine(line):
    fields = line.split()
    movieId = int(fields[1])
    return movieId

input = sc.textFile("/vagrant/u.data")
rdd1 = input.map(parseLine) #parse each line of the input db
rdd2 = rdd1.map(lambda x: (x,1))
rdd3 = rdd2.reduceByKey(lambda x,y: x+y)

rdd4 = rdd3.map(lambda (x,y): (y,x)).sortByKey()

results = rdd4.collect()
for result in results:
    print result
