import json

from imgbeddings import imgbeddings
from PIL import Image
from sqlalchemy import JSON
from tabulate import tabulate

from dql.query import C, DatasetQuery, Object, udf

# To install script dependencies: pip install tabulate imgbeddings


def load_image(raw):
    img = Image.open(raw)
    img.load()
    return img


@udf(
    output=(("embedding_json", JSON),),
    parameters=(Object(load_image),),
    method="embedding",
)
class ImageEmbeddings:
    def __init__(self):
        self.emb = imgbeddings()

    def embedding(self, img):
        emb = self.emb.to_embeddings(img)
        return (json.dumps(emb[0].tolist()),)


if __name__ == "__main__":
    # Save as a new shadow dataset
    DatasetQuery(path="s3://ldb-public/remote/data-lakes/dogs-and-cats/").filter(
        C.name.glob("*cat*.jpg")
    ).limit(5).add_signals(ImageEmbeddings).save("cats_with_embeddings")

    print(tabulate(DatasetQuery(name="cats_with_embeddings").results()[:5]))
