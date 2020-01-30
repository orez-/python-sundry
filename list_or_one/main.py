import pytest
import voluptuous


def list_or_one(element_schema):
    """
    Schema decorator to allow a list of `schema`s, or just a singular `schema`
    which is converted to a list of one element.
    """
    def list_or_one_fn(value):
        try:
            return voluptuous.Schema([element_schema])(value)
        except voluptuous.Invalid as list_exc:
            try:
                return [voluptuous.Schema(element_schema)(value)]
            except voluptuous.Invalid:
                if isinstance(value, list):
                    raise list_exc
                raise
    return list_or_one_fn

# ---

def test_convert_single():
    schema = voluptuous.Schema(list_or_one(str))
    assert schema("hey") == ["hey"]


def test_allow_single_list():
    schema = voluptuous.Schema(list_or_one(str))
    assert schema(["wow"]) == ["wow"]


def test_allow_multi_list():
    schema = voluptuous.Schema(list_or_one(str))
    assert schema(["one", "two", "three"]) == ["one", "two", "three"]


def test_disallow_mixed_list():
    schema = voluptuous.Schema(list_or_one(str))
    with pytest.raises(voluptuous.Invalid) as exc:
        schema(["one", 2, "three"])
    assert str(exc).endswith("expected str @ data[1]")


def test_disallow_bad_type_single():
    schema = voluptuous.Schema(list_or_one(str))
    with pytest.raises(voluptuous.Invalid) as exc:
        schema(2)
    assert str(exc).endswith("expected str")
