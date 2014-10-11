#!/usr/bin/env spark-submit

from pyspark import SparkContext, SparkConf


if __name__ == "__main__":
    sc = SparkContext(appName="avgByKey", conf=SparkConf().set("spark.driver.host", "localhost"))

    data = sc.parallelize( [(0, 2.), (0, 4.), (1, 0.), (1, 10.), (1, 20.)] )

    sumCount = data.combineByKey(lambda x: (x, 1),
                                 lambda t, value: (t[0] + value, t[1] + 1),
                                 lambda t, u: (t[0] + u[0], t[1] + u[1]))

    averageByKey = sumCount.map(lambda (label, (value_sum, count)): (label, value_sum / count))

    print averageByKey.collectAsMap()
