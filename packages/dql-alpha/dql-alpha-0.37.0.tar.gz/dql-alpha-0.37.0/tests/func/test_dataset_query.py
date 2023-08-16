import io
import json
from random import getrandbits
from textwrap import dedent

import pytest
import sqlalchemy
from sqlalchemy import Integer, String

from dql.catalog import indexer_formats
from dql.data_storage.abstract import RANDOM_BITS
from dql.data_storage.schema import DATASET_CORE_COLUMN_NAMES
from dql.dataset import Status as DatasetStatus
from dql.loader import DataView
from dql.query import C, DatasetQuery, Object, generator, udf
from dql.query.builtins import checksum, index_tar

from ..utils import DEFAULT_TREE, TARRED_TREE


@pytest.mark.parametrize("from_path", [True, False])
@pytest.mark.parametrize("save", [True, False])
@pytest.mark.parametrize(
    "cloud_type,version_aware",
    [("s3", True)],
    indirect=True,
)
def test_filter(cloud_test_catalog, save, from_path):
    catalog = cloud_test_catalog.catalog
    conf = cloud_test_catalog.client_config
    # ensure we can select a subset of a bucket properly
    path = f"{cloud_test_catalog.src_uri}/cats"
    if from_path:
        ds = DatasetQuery(path=path, catalog=catalog, client_config=conf)
    else:
        sources = [path]
        globs = [s.rstrip("/") + "/*" for s in sources]
        catalog.index(sources, client_config=conf)
        catalog.create_shadow_dataset(
            "animals", globs, client_config=conf, recursive=True
        )
        ds = DatasetQuery(name="animals", catalog=catalog)
    q = ds.filter(C.size < 13).filter(C.parent.glob("cats*") | (C.size < 4))
    if save:
        ds_name = "animals_cats"
        q.save(ds_name)
        q = DatasetQuery(name=ds_name, catalog=catalog)
        dataset_record = catalog.get_dataset(ds_name)
        assert dataset_record.status == DatasetStatus.COMPLETE
    result = q.results()
    count = q.count()
    assert len(result) == 2
    assert count == 2


@pytest.mark.parametrize(
    "cloud_type,version_aware",
    [("s3", True)],
    indirect=True,
)
def test_select(cloud_test_catalog):
    catalog = cloud_test_catalog.catalog
    conf = cloud_test_catalog.client_config
    path = cloud_test_catalog.src_uri
    ds = DatasetQuery(path=path, catalog=catalog, client_config=conf)
    q = (
        ds.order_by(C.size.desc(), C.name)
        .limit(6)
        .select(C.name, size10x=C.size * 10, size100x=C.size * 100)
    )
    result = q.results()
    assert result == [
        ("description", 130, 1300),
        ("cat1", 40, 400),
        ("cat2", 40, 400),
        ("dog1", 40, 400),
        ("dog3", 40, 400),
        ("dog4", 40, 400),
    ]


@pytest.mark.parametrize(
    "cloud_type,version_aware",
    [("s3", True)],
    indirect=True,
)
def test_select_missing_column(cloud_test_catalog):
    catalog = cloud_test_catalog.catalog
    conf = cloud_test_catalog.client_config
    path = cloud_test_catalog.src_uri
    ds = DatasetQuery(path=path, catalog=catalog, client_config=conf)
    ds1 = ds.select(C.missing_column_name)
    ds2 = ds.select("missing_column_name")
    # The exception type varies by database backend
    exc1 = pytest.raises(Exception, ds1.results)
    assert "missing_column_name" in str(exc1.value)
    exc2 = pytest.raises(KeyError, ds2.results)
    assert "missing_column_name" in str(exc2.value)


@pytest.mark.parametrize(
    "cloud_type,version_aware",
    [("s3", True)],
    indirect=True,
)
def test_select_except(cloud_test_catalog):
    catalog = cloud_test_catalog.catalog
    conf = cloud_test_catalog.client_config
    path = cloud_test_catalog.src_uri
    ds = DatasetQuery(path=path, catalog=catalog, client_config=conf)
    q = (
        ds.order_by(C.size.desc(), C.name)
        .limit(6)
        .select(C.parent, "name", C.size, size10x=C.size * 10, size100x=C.size * 100)
        .select_except(C.parent, C.size10x)
    )
    result = q.results()
    assert result == [
        ("description", 13, 1300),
        ("cat1", 4, 400),
        ("cat2", 4, 400),
        ("dog1", 4, 400),
        ("dog3", 4, 400),
        ("dog4", 4, 400),
    ]


@pytest.mark.parametrize(
    "cloud_type,version_aware",
    [("s3", True)],
    indirect=True,
)
def test_select_default(cloud_test_catalog):
    catalog = cloud_test_catalog.catalog
    conf = cloud_test_catalog.client_config
    path = cloud_test_catalog.src_uri
    ds = DatasetQuery(path=path, catalog=catalog, client_config=conf)
    original_result = ds.order_by(C.size.desc(), C.name).limit(6).results()
    q = (
        ds.order_by(C.size.desc(), C.name)
        .limit(6)
        .mutate(size10x=C.size * 10, size100x=C.size * 100)
        .select_default()
    )
    result = q.results()
    assert result == original_result
    assert len(result[0]) == len(DATASET_CORE_COLUMN_NAMES)


@pytest.mark.parametrize("save", [True, False])
@pytest.mark.parametrize(
    "cloud_type,version_aware",
    [("s3", True)],
    indirect=True,
)
def test_mutate(cloud_test_catalog, save):
    catalog = cloud_test_catalog.catalog
    conf = cloud_test_catalog.client_config
    path = cloud_test_catalog.src_uri
    ds = DatasetQuery(path=path, catalog=catalog, client_config=conf)
    q = (
        ds.mutate(size10x=C.size * 10)
        .mutate(size1000x=C.size10x * 100)
        .filter((C.size10x < 40) | (C.size10x > 100) | C.name.glob("cat*"))
        .order_by(C.size10x.desc(), C.name)
    )
    if save:
        ds_name = "animals_cats"
        q.save(ds_name)
        new_query = DatasetQuery(name=ds_name, catalog=catalog).order_by(
            C.size10x.desc(), C.name
        )
        result = new_query.results()
        dataset_record = catalog.get_dataset(ds_name)
        assert dataset_record.status == DatasetStatus.COMPLETE
    else:
        result = q.results()
    assert len(result) == 4
    assert len(result[0]) == 20
    assert [r[-2:] for r in result] == [
        (130, 13000),
        (40, 4000),
        (40, 4000),
        (30, 3000),
    ]


@pytest.mark.parametrize("save", [True, False])
@pytest.mark.parametrize(
    "cloud_type,version_aware",
    [("s3", True)],
    indirect=True,
)
def test_order_by_limit(cloud_test_catalog, save):
    catalog = cloud_test_catalog.catalog
    conf = cloud_test_catalog.client_config
    path = cloud_test_catalog.src_uri
    ds = DatasetQuery(path=path, catalog=catalog, client_config=conf)
    q = ds.order_by(C.name.desc()).limit(5)
    if save:
        ds_name = "animals_cats"
        q.save(ds_name)
        new_query = DatasetQuery(name=ds_name, catalog=catalog).order_by(C.name.desc())
        result = new_query.results()
        dataset_record = catalog.get_dataset(ds_name)
        assert dataset_record.status == DatasetStatus.COMPLETE
    else:
        result = q.results()
    assert [r[5] for r in result] == ["dog4", "dog3", "dog2", "dog1", "description"]


@pytest.mark.parametrize(
    "cloud_type,version_aware",
    [("s3", True)],
    indirect=True,
)
def test_udf(cloud_test_catalog):
    catalog = cloud_test_catalog.catalog
    conf = cloud_test_catalog.client_config
    sources = [cloud_test_catalog.src_uri]
    globs = [s.rstrip("/") + "/*" for s in sources]
    catalog.index(sources, client_config=conf)
    catalog.create_shadow_dataset("animals", globs, client_config=conf, recursive=True)

    @udf((("name_len", Integer),), (C.name,))
    def name_len(name):
        # A very simple udf.
        return (len(name),)

    q = (
        DatasetQuery(name="animals", catalog=catalog)
        .filter(C.size < 13)
        .filter(C.parent.glob("cats*") | (C.size < 4))
        .add_signals(name_len)
    )
    result1 = q.results()
    # ensure that we're able to run with same query multiple times
    result2 = q.results()
    count = q.count()
    # ensure that temporary tables are cleaned up
    assert [
        t
        for t in sqlalchemy.inspect(catalog.data_storage.data_engine).get_table_names()
        if t.startswith("udf_")
    ] == []
    assert len(result1) == 3
    assert len(result2) == 3
    assert count == 3


@pytest.mark.parametrize(
    "cloud_type,version_aware",
    [("s3", True)],
    indirect=True,
)
@pytest.mark.parametrize("batch", [1, 4])
def test_class_udf(cloud_test_catalog, batch):
    catalog = cloud_test_catalog.catalog
    conf = cloud_test_catalog.client_config
    sources = [cloud_test_catalog.src_uri]
    globs = [s.rstrip("/") + "/*" for s in sources]
    catalog.index(sources, client_config=conf)
    catalog.create_shadow_dataset("animals", globs, client_config=conf, recursive=True)

    @udf((("total", Integer),), (C.size,), method="sum", batch=batch)
    class MyUDF:
        def __init__(self, constant, multiplier=1):
            self.constant = constant
            self.multiplier = multiplier
            self.batch = batch

        def sum(self, size):
            if self.batch > 1:
                return [(self.constant + size_ * self.multiplier,) for (size_,) in size]
            return (self.constant + size * self.multiplier,)

    q = (
        DatasetQuery(name="animals", catalog=catalog)
        .filter(C.size < 13)
        .add_signals(MyUDF(5, multiplier=2))
    )
    results = q.select(C.size, C.total).order_by(C.size).results()
    assert results == [
        (3, 11),
        (4, 13),
        (4, 13),
        (4, 13),
        (4, 13),
        (4, 13),
    ]


@pytest.mark.parametrize(
    "cloud_type,version_aware",
    [("s3", True)],
    indirect=True,
)
@pytest.mark.parametrize("batch", [False, True])
def test_udf_parallel(cloud_test_catalog, batch):
    catalog = cloud_test_catalog.catalog
    conf = cloud_test_catalog.client_config
    sources = [cloud_test_catalog.src_uri]
    globs = [s.rstrip("/") + "/*" for s in sources]
    catalog.index(sources, client_config=conf)
    catalog.create_shadow_dataset("animals", globs, client_config=conf, recursive=True)

    @udf((("name_len", Integer),), (C.name,))
    def name_len_local(name):
        # A very simple udf.
        return (len(name),)

    @udf((("name_len", Integer),), (C.name,), batch=2)
    def name_len_batch(names):
        # A very simple udf.
        return [(len(name),) for (name,) in names]

    if batch:
        # Batching is enabled, we need a udf that acts on
        # lists of inputs.
        udf_func = name_len_batch
    else:
        udf_func = name_len_local

    q = (
        DatasetQuery(name="animals", catalog=catalog)
        .filter(C.size < 13)
        .filter(C.parent.glob("cats*") | (C.size < 4))
        .add_signals(udf_func, processes=True)
    )
    result = q.results()

    assert len(result) == 3


@pytest.mark.parametrize(
    "cloud_type,version_aware",
    [("s3", True)],
    indirect=True,
)
def test_udf_parallel_exec_error(cloud_test_catalog):
    catalog = cloud_test_catalog.catalog
    conf = cloud_test_catalog.client_config
    sources = [cloud_test_catalog.src_uri]
    globs = [s.rstrip("/") + "/*" for s in sources]
    catalog.index(sources, client_config=conf)
    catalog.create_shadow_dataset("animals", globs, client_config=conf, recursive=True)

    @udf((("name_len", Integer),), (C.name,))
    def name_len_error(_name):
        # A udf that raises an exception
        raise RuntimeError("Test Error!")

    q = (
        DatasetQuery(name="animals", catalog=catalog)
        .filter(C.size < 13)
        .filter(C.parent.glob("cats*") | (C.size < 4))
        .add_signals(name_len_error, processes=True)
    )
    with pytest.raises(RuntimeError, match="Test Error"):
        q.results()


def test_apply_udf(cloud_test_catalog, tmp_path):
    catalog = cloud_test_catalog.catalog
    sources = [cloud_test_catalog.src_uri]
    globs = [s.rstrip("/") + "/*" for s in sources]
    catalog.index(sources)
    catalog.create_shadow_dataset("animals", globs, recursive=True)

    code = """\
        from sqlalchemy import Integer
        from dql.query import C, udf

        @udf((("name_len", Integer),), (C.name,))
        def name_len(name):
            # A very simple udf.
            return (len(name),)
    """
    script = tmp_path / "foo.py"
    script.write_text(dedent(code))

    catalog.apply_udf(f"{script}:name_len", cloud_test_catalog.src_uri, "from-storage")
    q = DatasetQuery(name="from-storage", catalog=catalog).filter(C.name_len == 4)
    assert len(q.results()) == 6

    catalog.apply_udf(f"{script}:name_len", "ds://animals", "from-dataset")
    q = DatasetQuery(name="from-dataset", catalog=catalog).filter(C.name_len == 4)
    assert len(q.results()) == 6


def to_str(buf) -> str:
    return io.TextIOWrapper(buf, encoding="utf8").read()


def test_udf_object_param(cloud_test_catalog, dogs_shadow_dataset):
    # Setup catalog.
    catalog = cloud_test_catalog.catalog
    catalog.client_config = cloud_test_catalog.client_config

    @udf((("signal", String),), (C.name, Object(to_str)))
    def signal(name, obj):
        # A very simple udf.
        return (name + " -> " + obj,)

    q = DatasetQuery(name=dogs_shadow_dataset.name, catalog=catalog).add_signals(signal)
    result = q.results()

    assert len(result) == 4
    signals = {r[-1] for r in result}
    assert signals == {"dog1 -> woof", "dog2 -> arf", "dog3 -> bark", "dog4 -> ruff"}


@pytest.mark.parametrize(
    "cloud_type,version_aware",
    [("s3", True)],
    indirect=True,
)
def test_union(cloud_test_catalog):
    catalog = cloud_test_catalog.catalog
    conf = cloud_test_catalog.client_config
    sources = [str(cloud_test_catalog.src_uri)]
    catalog.index(sources, client_config=conf)

    src = cloud_test_catalog.src_uri
    catalog.create_shadow_dataset(
        "dogs", [f"{src}/dogs/*"], client_config=conf, recursive=True
    )
    catalog.create_shadow_dataset(
        "cats", [f"{src}/cats/*"], client_config=conf, recursive=True
    )

    dogs = DatasetQuery(name="dogs", catalog=catalog)
    cats = DatasetQuery(name="cats", catalog=catalog)

    (dogs | cats).save("dogs_cats")

    q = DatasetQuery(name="dogs_cats", catalog=catalog)
    result = q.results()
    count = q.count()
    assert len(result) == 6
    assert count == 6


def test_loader_from_query(cloud_test_catalog):
    catalog = cloud_test_catalog.catalog
    conf = cloud_test_catalog.client_config
    src_uri = cloud_test_catalog.src_uri
    catalog.index([src_uri], client_config=conf)
    catalog.create_shadow_dataset(
        "animals", [f"{src_uri}/*"], client_config=conf, recursive=True
    )
    q = DatasetQuery(name="animals", catalog=catalog).filter(C.parent.glob("cats*"))

    def transform(row, sample):
        return sample, row.name[-1]

    ds = DataView.from_query(
        q, reader=to_str, transform=transform, catalog=catalog, client_config=conf
    )
    assert set(ds) == {("meow", "1"), ("mrow", "2")}


def create_subobject(row, name: str, size: int):
    """Create a subobject with this row as its parent."""
    return {
        # Values that depend on the parent object.
        "vtype": "fake",
        "dir_type": 0,
        "parent_id": row.id,
        # Inherited values.
        "owner_name": row.owner_name,
        "owner_id": row.owner_id,
        "is_latest": row.is_latest,
        "source": row.source,
        # User-provided values.
        "name": name,
        "parent": row.path,
        "size": size,
        # Unspecified.
        "version": None,
        "etag": None,
        # Generated.
        "random": getrandbits(RANDOM_BITS),
    }


def test_row_generator(cloud_test_catalog, dogs_shadow_dataset):
    # Setup catalog.
    catalog = cloud_test_catalog.catalog
    catalog.client_config = cloud_test_catalog.client_config

    @generator(C.name, C.parent)
    def gen(parent, _, __):
        # A very simple generator.
        yield create_subobject(parent, "subobject", 50)

    q = DatasetQuery(name=dogs_shadow_dataset.name, catalog=catalog).generate(gen)
    result = q.results()

    assert len(result) == 8

    signals = {(r[4], r[5]) for r in result}  # parent, name
    assert signals == {
        ("dogs", "dog1"),
        ("dogs/dog1", "subobject"),
        ("dogs", "dog2"),
        ("dogs/dog2", "subobject"),
        ("dogs", "dog3"),
        ("dogs/dog3", "subobject"),
        ("dogs/others", "dog4"),
        ("dogs/others/dog4", "subobject"),
    }


@pytest.mark.parametrize("tree", [TARRED_TREE], indirect=True)
def test_index_tar(cloud_test_catalog):
    ctc = cloud_test_catalog
    catalog = ctc.catalog
    catalog.client_config = ctc.client_config
    catalog.index([ctc.src_uri])
    catalog.create_shadow_dataset("animals", [ctc.src_uri])

    q = DatasetQuery(name="animals", catalog=catalog).generate(index_tar)
    q.save("extracted")

    rows = list(catalog.ls_dataset_rows("extracted"))
    assert {row.name for row in rows} == {
        "animals.tar",
        "cat1",
        "cat2",
        "description",
        "dog1",
        "dog2",
        "dog3",
        "dog4",
    }

    offsets = [
        json.loads(row.location)[0]["offset"]
        for row in rows
        if row.name != "animals.tar"
    ]
    # Check that offsets are unique integers
    assert all(isinstance(offset, int) for offset in offsets)
    assert len(set(offsets)) == len(offsets)

    assert all(row.vtype == "tar" for row in rows if row.name != "animals.tar")


@pytest.mark.parametrize(
    "cloud_type,version_aware",
    [("s3", True)],
    indirect=True,
)
def test_checksum_udf(cloud_test_catalog, dogs_shadow_dataset):
    # Setup catalog.
    catalog = cloud_test_catalog.catalog
    catalog.client_config = cloud_test_catalog.client_config

    q = DatasetQuery(name=dogs_shadow_dataset.name, catalog=catalog).add_signals(
        checksum
    )
    result = q.results()

    assert len(result) == 4


@pytest.mark.parametrize("tree", [TARRED_TREE], indirect=True)
def test_tar_loader(cloud_test_catalog):
    ctc = cloud_test_catalog
    catalog = ctc.catalog
    catalog.client_config = ctc.client_config
    catalog.index([ctc.src_uri])
    catalog.create_shadow_dataset("animals", [ctc.src_uri])
    q = DatasetQuery(name="animals", catalog=catalog).generate(index_tar)
    q.save("extracted")

    q = DatasetQuery(name="extracted", catalog=catalog).filter(C.parent.glob("*/cats*"))
    assert len(q.results()) == 2

    def transform(row, sample):
        return sample, row.name[-1]

    ds = DataView.from_query(q, reader=to_str, transform=transform, catalog=catalog)
    assert set(ds) == {("meow", "1"), ("mrow", "2")}


@pytest.mark.parametrize("tree", [{**DEFAULT_TREE, **TARRED_TREE}], indirect=True)
def test_simple_dataset_query(cloud_test_catalog):
    ctc = cloud_test_catalog
    catalog = ctc.catalog
    data_storage = catalog.data_storage
    catalog.client_config = ctc.client_config
    catalog.index([ctc.src_uri], index_processors=indexer_formats["tar-files"])
    catalog.create_shadow_dataset("ds1", [ctc.src_uri], recursive=True)
    DatasetQuery(ctc.src_uri, catalog=catalog).save("ds2")

    n = data_storage.nodes_table(ctc.src_uri)
    nq = n.dataset_query().order_by(n.c.parent, n.c.name)
    ds_queries = [nq]
    for ds_name in ("ds1", "ds2"):
        dataset = data_storage.get_dataset(ds_name)
        d = data_storage.dataset_rows(dataset.id)
        dq = d.select().order_by(d.c.parent, d.c.name)
        ds_queries.append(dq)

    ignore_cols = ["id", "parent_id"]
    node_ds, ds1, ds2 = (
        [
            {k: v for k, v in zip(DATASET_CORE_COLUMN_NAMES, r) if k not in ignore_cols}
            for r in data_storage.data_execute(q)
        ]
        for q in ds_queries
    )

    # everything except the id field should match
    assert ds1 == node_ds
    assert ds2 == node_ds
    assert [(r["parent"], r["name"]) for r in node_ds] == [
        ("", "animals.tar"),
        ("", "description"),
        ("animals.tar", "description"),
        ("animals.tar/cats", "cat1"),
        ("animals.tar/cats", "cat2"),
        ("animals.tar/dogs", "dog1"),
        ("animals.tar/dogs", "dog2"),
        ("animals.tar/dogs", "dog3"),
        ("animals.tar/dogs/others", "dog4"),
        ("cats", "cat1"),
        ("cats", "cat2"),
        ("dogs", "dog1"),
        ("dogs", "dog2"),
        ("dogs", "dog3"),
        ("dogs/others", "dog4"),
    ]
