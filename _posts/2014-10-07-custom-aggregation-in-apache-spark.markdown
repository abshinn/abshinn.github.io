---
layout: post
comments: true
title:  "Custom Aggregation in Apache Spark"
date:   2014-10-07 00:00:00
categories: python, apache-spark
---

Aggregating data is a fairly straight-forward task, but what if you are working with a distributed data set, one that does not fit in local memory? 

In this post I am going to make use of key-value pairs and Apache-Spark's `combineByKey` method to compute the average-by-key using Python. 

Useful for implementing: KMeans, NaiveBayes, and TF-IDF (Term Frequency - Inverse Document Frequency), to name a few. 

In Apache-Spark, custom aggregations can be implemented several different ways. One of these ways involves the `combineByKey` method.

In this post, I would like to cover Apache Spark's `combineByKey` method in detail.


### Average By Key

```python

from pyspark import SparkContext
sc = SparkContext(appName="avgByKey", conf=SparkConf().set("spark.driver.host", "localhost"))


data = sc.parallelize([(0, 2.), (0, 4.), (1, 0.), (1, 10.), (1, 20.)])

sumCount = data.combineByKey(lambda x: (x, 1),
                             lambda t, value: (t[0] + value, t[1] + 1),
                             lambda t, u: (t[0] + u[0], t[1] + u[1]))

averageByKey = sumCount.map(lambda (label, (value_sum, count)): (label, value_sum / count))

print averageByKey.collectAsMap()
```


```python
{0: 3.0, 1: 10.0}
```


### combineByKey

In order to make a custom aggregation, a Spark RDD's `combineByKey` method requires three functions:

- `createCombiner`
- `mergeValue`
- `mergeCombiner`


#### Create a Combiner

The first required argument in the `combineByKey` method is a combiner function to be used as the very first aggregation step.

So, if we want to end up with the average by key, we need both the sum of the values and the count by key. To begin, we will place the value 

```python
lambda x: (x, 1)
```

#### Merge a Value

```python
lambda t, value: (t[0] + value, t[1] + 1)
```

#### Merge two Combiners

```python
lambda t, u: (t[0] + u[0], t[1] + u[1])
```

#### Compute the Average

```python
averageByKey = sumCount.map(lambda (label, (value_sum, count)): (label, value_sum / count))
```

### Examples


### Discussion

This may seem like a complicated way to do a simple task.
