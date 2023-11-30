from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SparkApp") \
    .master("local") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27017/ArticlesScraping.Articles") \
    .config("spark.mongodb.output.uri", "mongodb://localhost:27017/ArticlesScraping.Articles") \
    .getOrCreate()

df  = spark.read.format("com.mongodb.spark.sql.DefaultSource") \
    .option("uri", "mongodb://localhost:27017/ArticlesScraping.Articles").load()
df.printSchema()
