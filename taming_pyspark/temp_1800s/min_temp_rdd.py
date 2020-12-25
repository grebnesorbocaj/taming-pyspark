from pyspark import SparkConf, SparkContext
from taming_pyspark.utils.rdd_line_parser import file_to_csv_tuple as csv_parser
from taming_pyspark.config import BaseConfig


def show_min_temps_rdd(sc: SparkContext):
    """
    Shows min weather temperature observed for each weather station
    Data:
        weather_station_id, date_identifier, observation_type, measurement, other... data

    date_identifier = f'{4-digit-year}{2-digit-month}-(2-digit-date-integer)'
    observation_type =
        TMIN - minimum temperature
        TMAX - maximum temperature
        PRCP - precipitation %
    :param sc: SparkSession class instance
    :param parser: Used to parsed the csv file
    :return: None
    """
    data_file = f'{BaseConfig.DATA_FOLDER}/{BaseConfig.TEMP_1800S}/1800.csv'
    lines = sc.textFile(data_file)
    relevant_points = {
        'start': 0,
        'end': 4
    }
    rdd = lines.map(lambda x: csv_parser(x, delimiter=',', **relevant_points))
    temp_min_rdd = \
        rdd.filter(
            lambda data_point: 'TMIN' in data_point[2]
        ).map(
            lambda data_point: (data_point[0], data_point[3])
        ).reduceByKey(lambda x1, x2: min(int(x1), int(x2))) \
        .collect()

    for record in temp_min_rdd:
        print(f'Weather Station Identifier: {record[0]} \tMinimum Temperature: {record[1]}', end='\n\n')


def run_show_temps_rdd():
    conf = SparkConf() \
        .setMaster('local') \
        .setAppName('Min_Temp_RDD')

    sc = SparkContext(conf=conf)
    show_min_temps_rdd(sc=sc)


if __name__ == '__main__':
    run_show_temps_rdd()