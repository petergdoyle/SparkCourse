# SparkCourse
### Taming Big Data with Apache Spark and Python - Hands On


#####Social Network Dataset

    0,Will,33,385
    1,Jean-Luc,26,2
    2,Hugh,55,221
    3,Deanna,40,465
    4,Quark,68,21
    5,Weyoun,59,318
    6,Gowron,37,220
    7,Will,54,307
    8,Jadzia,38,380
    9,Hugh,27,181
    10,Odo,53,191
    ...

#####Friends-By-Age.py
```python
      1 from pyspark import SparkConf, SparkContext
      2 
      3 conf = SparkConf().setMaster("local").setAppName("FriendsByAge")
      4 sc = SparkContext(conf = conf)
      5 
      6 def parseLine(line):
      7     fields = line.split(',')
      8     age = int(fields[2])
      9     numFriends = int(fields[3])
     10     return (age, numFriends)
     11 
     12 lines = sc.textFile("/vagrant/fakefriends.csv")
     13 rdd = lines.map(parseLine)
     14 #results = rdd.collect()
     15 
     16 groupByAge = rdd.mapValues(lambda x: (x,1))
     17 #results = groupByAge.collect()
     18 
     19 totalsByAge = groupByAge.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
     20 #results = totalsByAge.collect()
     21 
     22 averagesByAge = totalsByAge.mapValues(lambda x: x[0] / x[1])
     23 #results = averagesByAge.collect()
     24 
     25 for result in results:
     26     print result
```

#####step-by-step

define a function that can be mapped onto the dataset. 'parseLine' will accept a line of input and split the comma separated lines into fileds. we are only interested in the 3rd and 4th field and they need to be cast as integers.

```python
      6 def parseLine(line):
      7     fields = line.split(',')
      8     age = int(fields[2])
      9     numFriends = int(fields[3])
     10     return (age, numFriends)
     11 
```

build the first rdd by mapping the parseLine function onto each item (line) in the dataset. parselLine will emit the 3rd and 4th values of each line into the new rdd. 

```python
     12 lines = sc.textFile("/vagrant/fakefriends.csv")
     13 rdd = lines.map(parseLine)
     14 results = rdd.collect()
     ...
     25 for result in results:
     26     print result
```
if we output contents of this rdd and filter for values where the age (3rd field) is 43 we get the following:
```
[vagrant@sparkcourse vagrant]$ spark-submit Friends-By-Age.py |grep '(43,'
(43, 49)
(43, 249)
(43, 404)
(43, 101)
(43, 48)
(43, 335)
(43, 428)
```
okay, now lets build the second rdd by grouping the new dataset by age. ultimately what we will be trying to do is determining the average rating per age. in order to do that we need to be able to total the ratings for a particular age and then divide by the number of ratings for that age. so the new dataset will consist look like this (K,V) or (age, (rating,1)). so the mapValues spark function will take the old (age,rating) dataset and then emit the new one with a 1 for each so that a count can be performed later.

```python
     16 groupByAge = rdd.mapValues(lambda x: (x,1))
     17 results = groupByAge.collect()
     ...
     25 for result in results:
     26     print result
```
and so the output (for age 43) looks like this:
```
[vagrant@sparkcourse vagrant]$ spark-submit Friends-By-Age.py |grep '(43,'
(43, (49, 1))
(43, (249, 1))
(43, (404, 1))
(43, (101, 1))
(43, (48, 1))
(43, (335, 1))
(43, (428, 1))
```
okay so now we need to then tally the rating for each age and divide by the number of ratings for that age. that can be done with a reduceByKey function (which collapes rows that are grouped by the same key). which take the set of values for each age(the key) and then applies the function that adds the rating (x) and the count (y) and emits the total for that age. 

```python
     19 totalsByAge = groupByAge.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
     20 results = totalsByAge.collect()
     ...
     25 for result in results:
     26     print result
```
and the output (for age 43) looks like this:
```
[vagrant@sparkcourse vagrant]$ spark-submit Friends-By-Age.py |grep '(43,'
(43, (1614, 7))
```
and finally we need to divide the total by the count in order to get the average for each age. to do this we are mapping a function onto each item in the dataset that will do the division and emit a new kay value pair that contains the age and the average rating. 

```python
     22 averagesByAge = totalsByAge.mapValues(lambda x: x[0] / x[1])
     23 results = averagesByAge.collect()
     24 
     25 for result in results:
     26     print result
```
and the output looks like this (for age 43):
```
[vagrant@sparkcourse vagrant]$ spark-submit Friends-By-Age.py |grep '(43,'
(43, 230)
```
