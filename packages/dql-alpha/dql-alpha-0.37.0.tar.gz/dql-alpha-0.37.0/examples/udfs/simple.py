from sqlalchemy import Integer
from tabulate import tabulate

from dql.query import C, DatasetQuery, udf

# To install script dependencies: pip install tabulate


# Define the UDF:
@udf(
    (
        ("path_len", Integer),
    ),  # Signals being returned by the UDF, with the signal name and type.
    (C.name,),  # Columns consumed by the UDF.
)
def name_len(name):
    if name.endswith(".json"):
        return (-1,)
    else:
        return (len(name),)


if __name__ == "__main__":
    # Save as a new shadow dataset
    DatasetQuery(path="s3://ldb-public/remote/data-lakes/dogs-and-cats/").filter(
        C.name.glob("*cat*")
    ).add_signals(name_len).save("cats_with_signal")

    # Output the contents of the new dataset.
    print(tabulate(DatasetQuery(name="cats_with_signal").results()[:10]))
