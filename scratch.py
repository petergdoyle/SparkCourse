from pyspark import SparkConf, SparkContext
import collections

conf = SparkConf().setMaster("local").setAppName("RatingsHistogram")
sc = SparkContext(conf = conf)

rdd = sc.parallelize([1,2,3,4,5])
rdd.map(lambda x: print " %i" % (x*x)))
