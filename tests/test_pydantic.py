import pytest

from datauri import DataURI

pydantic = pytest.importorskip("pydantic")


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
