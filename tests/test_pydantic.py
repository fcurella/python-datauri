import json

import pytest

from datauri import DataURI

pydantic = pytest.importorskip("pydantic")


@pytest.mark.skipif(pydantic.__version__.rsplit(".", 3)[0] > "1", reason="pydantic v2")
def test_pydantic():
    class Model(pydantic.BaseModel):
        content: DataURI

    t = "data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu"
    instance = Model(content=t)
    assert isinstance(instance.content, DataURI)
    assert (
        instance.json()
        == '{"content": "data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0'
        'aGUgbGF6eSBkb2cu"}'
    )
    assert instance.dict() == {"content": DataURI(t)}


@pytest.mark.skipif(
    pydantic.__version__.rsplit(".", 3)[0] < "2", reason="pydantic v2 required"
)
def test_pydantic_v2():
    class Model(pydantic.BaseModel):
        content: DataURI

    t = "data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu"
    instance = Model(content=t)
    assert isinstance(instance.content, DataURI)
    assert (
        instance.model_dump_json()
        == '{"content":"data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0'
        'aGUgbGF6eSBkb2cu"}'
    )
    assert instance.model_dump() == {"content": DataURI(t)}


@pytest.mark.skipif(
    pydantic.__version__.rsplit(".", 3)[0] < "2", reason="pydantic v2 required"
)
def test_pydantic_v2_json_schema():
    class Model(pydantic.BaseModel):
        content: DataURI

    schema = Model.model_json_schema(
        schema_generator=pydantic.json_schema.GenerateJsonSchema
    )
    schema_json = json.dumps(schema)
    val = (
        r'{"properties": {"content": {"examples": ["data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveC'
        r'BqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu"], "pattern": "data:(?P<mimetype>[\\w]+\\/[\\w\\-\\+\\.]+)?(?:\\;name\\='
        r"(?P<name>[\\w\\.\\-%!*'~\\(\\)]+))?(?:\\;charset\\=(?P<charset>[\\w\\-\\+\\.]+))?(?P<base64>\\;base64)?,(?P"
        r'<data>.*)", "title": "DataURI", "type": "string"}}, "required": ["content"], "title": "Model", "type": "obj'
        r'ect"}'
    )
    assert schema_json == val
