import pytest

from datauri import DataURI

pydantic = pytest.importorskip("pydantic")

try:
    pydantic.version.version_info()
    func_json = "model_dump_json"
except:
    pydantic.utils.version_info()
    func_json = "json"


def test_pydantic():
    class Model(pydantic.BaseModel):
        content: DataURI

    t = "data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu"
    instance = Model(content=t)
    assert isinstance(instance.content, DataURI)
    assert (
        instance.__getattr__(func_json)()
        == '{"content":"data:text/plain;charset=utf-8;base64,VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cu"}'
    )
    assert instance.dict() == {"content": DataURI(t)}
