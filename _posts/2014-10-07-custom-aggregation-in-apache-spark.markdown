---
layout: post
comments: true
title:  "Custom Aggregation in Apache Spark"
date:   2014-10-07 00:00:00
categories: python, apache-spark
---

Aggregating data is a fairly straight-forward task, but what if you are working with a distributed data set, one that does not fit in local memory? 

In this post I am going to use key-value pairs to compute the average by key in Apache Spark using python.

Useful for implementing: KMeans, NaiveBayes, and TFIDF, to name a few. 

In Apache-Spark, custom aggregations can be implemented several different ways. One of these ways involves the `combineByKey` method.

In this blog post, I would like to cover Apache Spark's `combineByKey` method in detail.

### combineByKey

In order to make a custom aggregation, a Spark RDD's `combineByKey` method requires three functions:

- `createCombiner`
- `mergeValue`
- `mergeCombiner`

#### Create a Combiner

#### Merge a Value

#### Merge Combiners


### Examples

