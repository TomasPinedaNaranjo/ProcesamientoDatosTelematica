from pyspark.sql import SparkSession
from pyspark.sql.functions import col, rand
import json


def transform_data():
    with SparkSession.builder.appName("TransformData").getOrCreate() as spark:
        # Leer productos y usuarios
        df = spark.read.text(
            "s3a://emurielrdatalake/raw/todos_los_productos.txt")
        users_df = spark.read.format("parquet").load(
            "s3a://emurielrdatalake/raw/project_users/")

        # Convertir usuarios a texto y ordenar aleatoriamente
        users_text_df = users_df.selectExpr(
            "CAST(struct(*) AS STRING) AS value").orderBy(rand())
        users_list = users_text_df.rdd.map(lambda row: row.value).collect()

        # Obtener RDD de productos
        products_rdd = df.rdd.zipWithIndex()

        # Intercalar usuarios localmente
        def interleave(product_row):
            index = product_row[1]
            user_index = index % len(users_list)
            user_str = users_list[user_index]

            # Extraer nombre y email del string del usuario
            try:
                user_dict = json.loads(user_str.replace("'", '"'))
                user_line = f',"user": {{"name": {user_dict.get("name")}, "email": {user_dict.get("email")}}}'
            except Exception:
                parts = user_str.strip().strip("{}").split(",")
                name = parts[0].strip()
                email = parts[1].strip()
                user_line = f',"user": {{"name": "{name}", "email": "{email}"}}'

            product_line = product_row[0].value.strip()
            if product_line == '}':
                # Agregar línea del usuario justo después de la línea de cierre de rating
                return [(product_line,), (user_line,)]
            else:
                return [(product_line,)]

        interleaved_rdd = products_rdd.flatMap(interleave)

        # Eliminar la penúltima línea del RDD
        rdd_count = interleaved_rdd.count()
        if rdd_count >= 2:
            interleaved_rdd = interleaved_rdd.zipWithIndex().filter(
                lambda x: x[1] != rdd_count - 2
            ).map(lambda x: x[0])

        # Convertir a DataFrame y guardar
        interleaved_df = spark.createDataFrame(interleaved_rdd, ["value"])
        interleaved_df.write.mode("overwrite").text(
            "s3a://emurielrdatalake/trusted/clean_products/")


transform_data()
