---
layout: post
comments: true
title:  "Using combineByKey in Apache-Spark"
date:   2014-10-11 00:00:00
categories: python, apache-spark
---

Aggregating data is a fairly straight-forward task, but what if you are working with a distributed data set, one that does not fit in local memory? 

In this post I am going to make use of key-value pairs and [Apache-Spark](https://spark.apache.org/)'s `combineByKey` method to compute the average-by-key. Aggregating-by-key may seem like a trivial task, but it happens to play a major role in the implementation of algorithms such as KMeans, Naive Bayes, and TF-IDF. More importantly, implementing algorithms such as these in a distributed framework such as Spark is an invaluable skill to have.


### Average By Key

The example below uses data in the form of a list of tuples in the form: `(key, value)`. I turn that list into a [Resilient Distributed Dataset (RDD)](http://www.thecloudavenue.com/2014/01/resilient-distributed-datasets-rdd.html) with the `sc.parallelize` function, where `sc` is an instance of `pyspark.SparkContext`.

The next step is to use the `combineByKey` method, which is admittedly not very readable with its three lambda-function parameters. I will explain each lambda-function in the next section. The result, `sumCount`, is an RDD where its values are in the form of `(label, (sum, count))`.

To compute the average-by-key, I use the `map` method to divide the sum by the count for each key. 

Finally, I use the `collectAsMap` method to return the average-by-key as a dictionary.

```python

data = sc.parallelize( [(0, 2.), (0, 4.), (1, 0.), (1, 10.), (1, 20.)] )

sumCount = data.combineByKey(lambda value: (value, 1),
                             lambda x, value: (x[0] + value, x[1] + 1),
                             lambda x, y: (x[0] + y[0], x[1] + y[1]))

averageByKey = sumCount.map(lambda (label, (value_sum, count)): (label, value_sum / count))

print averageByKey.collectAsMap()
```

__Result:__

```python
{0: 3.0, 1: 10.0}
```

[See here](https://github.com/abshinn/abshinn.github.io/tree/master/extras/averageByKey.py) for the above example as an executable script.


### `combineByKey` Method

In order to aggregate an RDD's elements in parallel, Spark's `combineByKey` method requires three functions:

- `createCombiner`
- `mergeValue`
- `mergeCombiner`


#### Create a Combiner

```python
lambda value: (value, 1)
```

The first required argument in the `combineByKey` method is a function to be used as the very first aggregation step for each key. The argument of this function corresponds to the value in a key-value pair. If we want to compute the sum and count using `combineByKey`, then we can create this "combiner" to be a tuple in the form of `(sum, count)`. The very first step in `(sum, count)` is then `(value, 1)`, where `value` is the first RDD value that `combineByKey` comes across and `1` initializes the count.


#### Merge a Value

```python
lambda x, value: (x[0] + value, x[1] + 1)
```

The next required function tells `combineByKey` what to do when a combiner is given a new value. The arguments to this function are a combiner and a new value. The structure of the combiner is defined above as a tuple in the form of `(sum, count)` so we merge the new value by adding it to the first element of the tuple while incrementing `1` to the second element of the tuple.


#### Merge two Combiners

```python
lambda x, y: (x[0] + y[0], x[1] + y[1])
```

The final required function tells `combineByKey` how to merge two combiners. In this example with tuples as combiners in the form of `(sum, count)`, all we need to do is add the first and last elements together.


#### Compute the Average

```python
averageByKey = sumCount.map(lambda (label, (value_sum, count)): (label, value_sum / count))
```

Ultimately the goal is to compute the average-by-key. The result from `combineByKey` is an RDD with elements in the form `(label, (sum, count))`, so the average-by-key can easily be obtained by using the `map` method, mapping `(sum, count)` to `sum / count`. 

Note: I do not use `sum` as variable name in the code because it is a built-in function in Python.


### Learn More

To learn more about Spark and programming with key-value pairs in Spark, see:
- [Spark Documentation Overview](http://spark.apache.org/documentation.html) 
- [Spark Programming Guide](http://spark.apache.org/docs/latest/programming-guide.html)
- [O'Reilly: Learning Spark, Chapter 4](https://www.safaribooksonline.com/library/view/learning-spark/9781449359034/ch04.html)
- [PySpark Documentation](http://spark.apache.org/docs/latest/api/python/index.html)

