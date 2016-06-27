
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("TotalAmountByCustomer")
sc = SparkContext(conf = conf)

def parseLine(line):
    fields = line.split(',')
    customerId = int(fields[0])
    itemId = fields[1]
    itemAmt = float(fields[2])
    return (customerId, itemAmt)

input = sc.textFile("/vagrant/customer-orders.csv")
orders = input.map(parseLine)
totals = orders.reduceByKey(lambda x, y: x + y)
sortedTotals = totals.map(lambda (x,y): (y,x)).sortByKey(False)

results = sortedTotals .collect()
for result in results:
    # print result
    print result[1],"\t${:.2f}".format(result[0])
