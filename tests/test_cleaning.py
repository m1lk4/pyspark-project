import pytest
from pyspark.sql import SparkSession
from src.cleaning import clean_data
from pyspark.sql.functions import col


@pytest.fixture(scope="module")
def spark():
    spark = (
        SparkSession.builder.master("local[*]").appName("pytest-cleaning").getOrCreate()
    )
    yield spark
    spark.stop()


def test_clean_data(spark):
    data = [("25", "Male", "23.4", "0", "Yes", "Northeast", "3200.5")]
    columns = ["age", "sex", "bmi", "children", "smoker", "region", "charges"]
    df = spark.createDataFrame(data, columns)

    df_clean = clean_data(df)

    assert df_clean.filter(col("age").isNull()).count() == 0
    assert df_clean.filter(col("bmi").isNull()).count() == 0
    assert df_clean.select("sex").first()[0] == "male"
    assert df_clean.select("smoker").first()[0] == "yes"
    assert df_clean.select("region").first()[0] == "northeast"
    assert df_clean.select("charges").first()[0] == 3200.5

    schema = dict(df_clean.dtypes)

    assert schema["age"] in ("int", "bigint")
    assert schema["children"] in ("int", "bigint")
    assert schema["bmi"] in ("float", "double")
    assert schema["charges"] in ("float", "double")
    assert schema["sex"] == "string"
    assert schema["smoker"] == "string"
    assert schema["region"] == "string"
