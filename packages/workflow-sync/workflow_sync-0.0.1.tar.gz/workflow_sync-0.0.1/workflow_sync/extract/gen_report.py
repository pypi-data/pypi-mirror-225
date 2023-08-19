# # Databricks notebook source
# # MAGIC %md
# # MAGIC # Price Paid Datamail
# # MAGIC
# # MAGIC Welcome to the workflow_sync datamail for January 2023.
# # MAGIC
# # MAGIC In January there were a total of
#
# # COMMAND ----------
#
# df = spark.read.table("price_paid.gold")
#
#
#
# displayHTML(f"""
# <p style="font-family:'Lucida Console'">This is another paragraph.</p>
# <h1 font="Courier">Price Paid Datamail - {df.count()}</h1>
# <p>Welcome to the workflow_sync datamail for ** 2023.</p>
# """)
#
#
# # COMMAND ----------
#
# sql = "SELECT date, price FROM price_paid.gold where postcode like '%HU12%'" \
#       " order by date"
# df = spark.sql(sql)
# #df.price.rolling(5).mean()
#
# # COMMAND ----------
#
# #sql = "SELECT avg(price) from price_paid.gold where (year(date) = 2023 and
# # (month(date) <= 5)) or (year(date) = 2022 and (month(date) > 5))"
# sql = "SELECT avg(price) from price_paid.gold where date >= '2022-05-01' and" \
#       " date < '2023-06-01'"
# df = spark.sql(sql)
# df.show(500)
#
# # COMMAND ----------
#
# df = spark.table("price_paid.gold")
# df.display()
#
# # COMMAND ----------
#
# from pyspark.sql.window import Window
# from pyspark.sql.functions import col, udf, mean
# from pyspark.sql.types import FloatType
#
# w = Window().partitionBy("year").orderBy("month")
#
# def trimmed_mean():
#     return 1
#
# udf_trimmed_mean = udf(trimmed_mean, FloatType())
#
# new_df = df.withColumn("two_month_rolling_sum", mean(col("price"))
#                        .over(w.rangeBetween(-11, 0)))
# #new_df = df.groupby("year", "month").agg(mean(col("price")))
# display(new_df)
#
#
#
# # COMMAND ----------
#
# from pyspark.sql.DataFrame import approxQuantile
# df = spark.table("price_paid.gold")
# df_ave = df.groupBy("year").agg(approxQuantile("prices", [0.2, 0.8], 0.001))
# display(df_ave)
#
# # COMMAND ----------
#
# sql = "SELECT price from price_paid.gold where date >= '2021-03-01' and date" \
#       " < '2022-04-01'"
# df = spark.sql(sql)
# display(df)
# #df = spark.table("price_paid.gold")
# # from scipy import stats
# # m1 = stats.trim_mean(df.collect(), 0.2)
# # print(m1)
#
# # COMMAND ----------
#
# from dateutil.relativedelta import relativedelta
# from pyspark.sql.functions import col, mean, min, max
#
# gold_data = spark.table("price_paid.gold").cache()
#
# min_date = gold_data.select(min("date")).first()["min(date)"]
# max_date = gold_data.select(max("date")).first()["max(date)"]
#
# avg_prices = []
# while True:
#     year_later = min_date + relativedelta(months=13)
#     if year_later > max_date:
#         break
#     print(f"min is {min_date}, max is {year_later}")
#
#     sub_df = gold_data.filter((col("date") >= min_date) & (col("date")
#                                                            < year_later))
#     lowest_highest_20th_values = sub_df.approxQuantile("price", [0.05, 0.95],
#                                                        0.0001)
#     avg_price = sub_df.where((sub_df.price > lowest_highest_20th_values[0]) &
#                              (sub_df.price < lowest_highest_20th_values[1])) \
#                             .select(mean('price')).first()["avg(price)"]
#     avg_prices.append((year_later, avg_price))
#     print(avg_prices)
#
#     min_date = min_date + relativedelta(months=1)
#     #break
#
# #spark.createDataFrame(mylist, IntegerType()).show()
#
# # COMMAND ----------
#
# from pyspark.sql.types import StructType, StructField, DateType, FloatType
# #spark.createDataFrame(avg_prices, FloatType()).show()
# schema = StructType([StructField("date", DateType(), False),
#                      StructField("mean_price", FloatType(), False)])
# spark.createDataFrame(avg_prices, schema).write.mode("overwrite")\
#     .format("delta").saveAsTable("price_paid.monthly_average_prices")
#
# # COMMAND ----------
#
# display(spark.table("price_paid.monthly_average_prices"))
#
# # COMMAND ----------
#
# url = "http://publicdata.landregistry.gov.uk/market-trend-data/" \
#       "house-price-index-data/Average-prices-2023-04.csv"
# from pyspark import SparkFiles
# sc.addFile(url)
#
# path  = SparkFiles.get('download')
# df = spark.read.csv("file://" + path, header=True, inferSchema= True
#                     , sep = ";")
#
# # COMMAND ----------
#
# sdf = gold_data.filter((col("date") >= '1995-01-01') & (col("date")
#                                                         < '1996-02-01'))
# lowest_highest_20th_values = sub_df.approxQuantile("price", [0.05, 0.95],
#                                                    0.0001)
# avg_price = sub_df.where((sub_df.price > lowest_highest_20th_values[0]) &
#                          (sub_df.price < lowest_highest_20th_values[1])) \
#                             .select(mean('price')).first()["avg(price)"]
# print(avg_price)
#
# # COMMAND ----------
#
# from pyspark.sql.functions import col, avg
#
# df[(col("date") >= '2021-03-01') & (col("date") < '2022-04-01')]\
#     .agg(avg(col("price"))).show()
#
# # COMMAND ----------
#
# from pyspark.sql.functions import udf
# @udf("long")
# def squared_udf(s):
#   return s * s
# df = spark.table("test")
# display(df.select("id", squared_udf("id").alias("id_squared")))
#
# # COMMAND ----------
#
# sql = "SELECT price from price_paid.gold where date >= '2022-04-01' " \
#       "and date < '2023-05-01'"
# df = spark.sql(sql)
#
# from scipy import stats
# m2 = stats.trim_mean(df.collect(), 0.2)
# print(m1)
# print(m2/m1)
#
# # COMMAND ----------
#
# sql = "SELECT median(price) from price_paid.gold where date >= '2022-05-01' " \
#       "and date < '2023-06-01'"
# df = spark.sql(sql)
#
# from scipy import stats
# m = stats.trim_mean(df.collect(), 0.3)
# print(m)
#
# # COMMAND ----------
#
# prices = df.collect()
#
# for percentage in [x * 0.01 for x in range(0, 30)]:
#     print(stats.trim_mean(prices, percentage))
#     #print(percentage)
#
# # COMMAND ----------
#
# print(0.4 * len(prices))
#
# # COMMAND ----------
#
# #sql = "SELECT avg(price) from price_paid.gold where (year(date) = 2023
# # and (month(date) <= 5)) or (year(date) = 2022 and (month(date) > 5))"
# sql = "SELECT median(price) from price_paid.gold where date >= '2022-04-01' " \
#       "and date < '2023-05-01' order by price desc"
# df = spark.sql(sql)
# display(df)
#
# # COMMAND ----------
#
# sql = "SELECT avg(price) from price_paid.gold where year(date) = 2023 and " \
#       "month(date) = 5"
# df = spark.sql(sql)
# df.show(500)
#
# # COMMAND ----------
#
# sql = "SELECT price from price_paid.gold order by price desc"
# df = spark.sql(sql)
# display(df)
#
# # COMMAND ----------
#
# from pyspark.sql import functions as F
#
# df.select(F.sum("_c1")).collect()[0][0]
#
# # COMMAND ----------
#
# from pyspark.sql.functions import year, mean
#
# df = spark.read.table("price_paid.gold")
# mean_price = df.groupBy(year("date").alias("year")).agg(mean("price") \
#                                                         .alias("mean_price"))
#
#
# # COMMAND ----------
#
# display(mean_price)
#
# # COMMAND ----------
#
#
