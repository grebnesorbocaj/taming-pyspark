from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import round, mean, sum
from taming_pyspark.config import BaseConfig
from taming_pyspark.utils.spark_runner import spark_session_runner


def avg_friends_by_age(spark: SparkSession):
    """
    Reads a csv with index, first_name_, age, and number of friends
    as fields. Uses spark session to aggregrate a dataframe to calculate
    avg number of friends by age and total friends by age in the giving data set
    :param spark: SparkSession class
    :return: None
    """
    data_file = f'{BaseConfig.DATA_FOLDER}/{BaseConfig.FRIENDS_DATASET}/fakefriends.csv'
    schema = StructType([
        StructField("index", IntegerType(), nullable=False),
        StructField("name", StringType(), nullable=False),
        StructField("age", IntegerType(), nullable=False),
        StructField("numberOfFriends", IntegerType(), nullable=False)
    ])
    df = spark.read.csv(path=data_file, schema=schema, enforceSchema=True)
    # display both using dataframes
    df.groupby("age") \
        .agg(
            sum("numberOfFriends").alias("Total_Friends"),
            round(mean("numberOfFriends")).cast('integer').alias("Avg_Number_Of_Friends")
        ) \
        .show()


if __name__ == '__main__':
    spark_session_runner(avg_friends_by_age, app_name="Fake_Friends")
