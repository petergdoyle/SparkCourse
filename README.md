# SparkCourse
## Taming Big Data with Apache Spark and Python - Hands On

####Resources and downloads
https://www.udemy.com/taming-big-data-with-apache-spark-hands-on/learn/v4/content 


####12.[Activity] Running the Average Friends by Age Example
#####Social Network Dataset
the original dataset is in the form (id,name,age,number_of_friends): fakefriends.csv
```
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
```

#####Friends-By-Age.py
the pyspark program to work on the dataset is given here 
```python
           1 from pyspark import SparkConf, SparkContext
      2 
      3 conf = SparkConf().setMaster("local").setAppName("WordCount")
      4 sc = SparkContext(conf = conf)
      5 
      6 input = sc.textFile("/vagrant/Book.txt")
      7 words = input.flatMap(lambda x: x.split())
      8 # results = words.collect()
      9 # for result in results:
     10 #    print result
     11 
     12 # #python function
     13 # #wordCounts = words.countByValue()
     14 
     15 #take a spark approach...
     16 #convert each word to a key/value pair with a value of 1
     17 wordCountsMap = words.map(lambda x: (x,1))
     18 # results = wordCountsMap.collect()
     19 # for result in results:
     20 #    print result
     21 
     22 
     23 #count words with reduceByKey so reduceByKey will build a Set of each work and count the 1s!
     24 wordCountsReduce = wordCountsMap.reduceByKey(lambda x, y: x + y)
     25 results = wordCountsReduce.collect()
     26 for result in results:
     27    print result
     28 #
     29 # for word, count in wordCountsMap.items():
     30 #     cleanWord = word.encode('ascii', 'ignore')
     31 #     if (cleanWord):
     32 #         print cleanWord, count
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
okay, now lets build the second rdd by grouping the new dataset by age. ultimately what we will be doing is determining the average friends per age. in order to do that we need to be able to total the friends for a particular age and then divide by the number of friends for that age. so the new dataset will consist look like this (K,V) or (age, (friends,1)). so the mapValues spark function will take the old (age,friends) dataset and then emit the new one with a 1 for each so that a count can be performed later.

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
okay so now we need to then tally the friends for each age and divide by the number of friends for that age. that can be done with a reduceByKey function (which collapes rows that are grouped by the same key). which take the set of values for each age(the key) and then applies the function that adds the friends (x) and the count (y) and emits the total for that age. 

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
and finally we need to divide the total by the count in order to get the average for each age. to do this we are mapping a function onto each item in the dataset that will do the division and emit a new kay value pair that contains the age and the average number of friends. 

```python
     22 averagesByAge = totalsByAge.mapValues(lambda x: x[0] / x[1])
     23 results = averagesByAge.collect()
     24 
     25 for result in results:
     26     print result
```
and the output looks like this (for age 43). so it looks like for age 43 in this dataset they have an average of 230 friends.
```
[vagrant@sparkcourse vagrant]$ spark-submit Friends-By-Age.py |grep '(43,'
(43, 230)
```

####16.[Activity] Counting Word Occurrences using flatmap() 
The data for this exercise is in the form of a book that is in text form: Book.txt. The objective is to get a wordcount for all words in the book text.

```python
      1 import re
      2 from pyspark import SparkConf, SparkContext
      3 
      4 def normalizeWords(text):
      5     return re.compile(r'\W+', re.UNICODE).split(text.lower())
      6 
      7 conf = SparkConf().setMaster("local").setAppName("WordCount")
      8 sc = SparkContext(conf = conf)
      9 
     10 input = sc.textFile("/vagrant/Book.txt")
     11 #a simple split works
     12 #words = input.flatMap(lambda x: x.split())
     13 #but let's clean the text up a bit and filter out special characters and consider upper and lowercase to be the same thing
     14 words = input.flatMap(normalizeWords)
     15 # results = words.collect()
     16 # for result in results:
     17 #    print result
     18 
     19 # #python function
     20 # #wordCounts = words.countByValue()
     21 
     22 #take a spark approach...
     23 #convert each word to a key/value pair with a value of 1
     24 wordCountsMap = words.map(lambda x: (x,1))
     25 # results = wordCountsMap.collect()
     26 # for result in results:
     27 #    print result
     28 
     29 
     30 #count words with reduceByKey so reduceByKey will build a Set of each work and count the 1s!
     31 wordCountsReduced = wordCountsMap.reduceByKey(lambda x, y: x + y)
     32 results = wordCountsReduced.collect()
     33 # for result in results:
     34 #    print result
     35 
     36 wordCountsSorted = wordCountsReduced.map(lambda (x,y): (y,x)).sortByKey()
     37 results = wordCountsSorted.collect()
     38 
     39 for result in results:
     40     # print result
     41     count = str(result[0])
     42     word = result[1].encode('ascii', 'ignore')
     43     if (word):
     44         print word + ":\t\t" + count
```
so to start off we need to build a dataset consisting of each word in the book. we can do this with python and spark and building the first rdd based on each word in the book and using a split() function (on whitespace by default). the flatMap function can do that take a single input and produce multiple outputs and apply the given function on the input:
```python
     10 input = sc.textFile("/vagrant/Book.txt")
     11 #a simple split works
     12 #words = input.flatMap(lambda x: x.split())
     13 #but let's clean the text up a bit and filter out special characters and consider upper and lowercase to be the same thing
     14 words = input.flatMap(normalizeWords)
```
taking a look at the ```word``` rdd after the content of the book is split into words:
```
Self-Employment:
Building
an
Internet
Business
of
One
Achieving
Financial
and
Personal
Freedom
through
a
Lifestyle
Technology
Business
By
Frank
Kane
...
```
okay now we need to be able to provide a count (of 1) for each of the words so that eventually we can tally up the count of each word. we can do this by applying a map function to each of the words in the rdd dataset 
```python     
	 23 #convert each word to a key/value pair with a value of 1
     24 wordCountsMap = words.map(lambda x: (x,1))
```
and that will yield a second rdd with the following key,value dataset:
```
(u'Self-Employment:', 1)
(u'Building', 1)
(u'an', 1)
(u'Internet', 1)
(u'Business', 1)
(u'of', 1)
(u'One', 1)
(u'Achieving', 1)
(u'Financial', 1)
(u'and', 1)
(u'Personal', 1)
(u'Freedom', 1)
(u'through', 1)
(u'a', 1)
(u'Lifestyle', 1)
(u'Technology', 1)
(u'Business', 1)
(u'By', 1)
(u'Frank', 1)
(u'Kane', 1)
...
```
and now we can use a reduceByKey function that will group by each word and tally up the counts
```python
     30 #count words with reduceByKey so reduceByKey will build a Set of each work and count the 1s!
     31 wordCountsReduced = wordCountsMap.reduceByKey(lambda x, y: x + y)
```
now we can see the counts for each word from the wordCountReduced rdd:
```
...
(u'daughters.', 2)
(u'ability', 14)
(u'opening', 1)
(u'self-fund,', 1)
(u'merit.', 1)
(u'merit,', 2)
(u'moz.com', 1)
...
```
but things are still unordered, so lets sort them ascending with another map function. since we have the totals stored in the value part of the key,value pair, we need to flip the key and the value and then apply a sortByKey function to the dataset
```python
     36 wordCountsSorted = wordCountsReduced.map(lambda (x,y): (y,x)).sortByKey()
```
and now the last part of the wordCountsSorted should end with the highest word count entries:
```
...
(747, u'that')
(772, u'')
(934, u'and')
(970, u'of')
(1191, u'a')
(1292, u'the')
(1420, u'your')
(1828, u'to')
(1878, u'you')
```
and the formatted output looks like this:
```
...
that: 	   747
and:		 934
of: 		 970
a:	  	1191
the:		1292
your:   	1420
to:		 1828
you:		1878
```