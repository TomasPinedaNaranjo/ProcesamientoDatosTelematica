from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType, StructType

spark = SparkSession.builder.appName("AnalisisTrusted").getOrCreate()

ruta_trusted = "s3a://emurielrdatalake/trusted/clean_products/"

df = spark.read.option("multiline", "true").json(ruta_trusted)

df_clean = df.select("id", "category", "price")

resumen = df_clean.groupBy("category").agg(
    avg("price").alias("avg_price"),
    count("id").alias("products_quant")
)

ruta_refined = "s3a://emurielrdatalake/refined/an_products/"
resumen.write.mode("overwrite").json(ruta_refined)

spark.stop()
