#!/usr/bin/env spark-submit

from pyspark import SparkContext, SparkConf


if __name__ == "__main__":
    sc = SparkContext(appName="avgByKey", conf=SparkConf().set("spark.driver.host", "localhost"))

    data = sc.parallelize( [(0, 2.), (0, 4.), (1, 0.), (1, 10.), (1, 20.)] )

    sumCount = data.combineByKey(lambda value: (value, 1),
                                 lambda x, value: (x[0] + value, x[1] + 1),
                                 lambda x, y: (x[0] + y[0], x[1] + y[1]))

    averageByKey = sumCount.map(lambda (label, (value_sum, count)): (label, value_sum / count))

    print averageByKey.collectAsMap()
