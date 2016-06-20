from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("FriendsByAge")
sc = SparkContext(conf = conf)

def parseLine(line):
    fields = line.split(',')
    age = int(fields[2])
    numFriends = int(fields[3])
    return (age, numFriends)

lines = sc.textFile("/vagrant/fakefriends.csv")
rdd = lines.map(parseLine)
#results = rdd.collect()

groupByAge = rdd.mapValues(lambda x: (x,1))
#results = groupByAge.collect()

totalsByAge = groupByAge.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
#results = totalsByAge.collect()

averagesByAge = totalsByAge.mapValues(lambda x: x[0] / x[1])
results = averagesByAge.collect()

for result in results:
    print result
