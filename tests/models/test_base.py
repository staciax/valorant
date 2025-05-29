from uuid import uuid4

from valorant.models.base import BaseModel, BaseUUIDModel
from valorant.utils import is_running_in_pytest


def test_base_model_config_forbids_extra_in_pytest() -> None:
    assert is_running_in_pytest()
    assert BaseModel.model_config['extra'] == 'forbid'


def test_base_uuid_model_eq_same_uuid_same_class() -> None:
    uuid_val = uuid4()
    model1 = BaseUUIDModel(uuid=uuid_val)
    model2 = BaseUUIDModel(uuid=uuid_val)
    assert model1 == model2


def test_base_uuid_model_eq_different_uuid_same_class() -> None:
    model1 = BaseUUIDModel(uuid=uuid4())
    model2 = BaseUUIDModel(uuid=uuid4())
    assert model1 != model2


def test_base_uuid_model_eq_different_class() -> None:
    uuid_val = uuid4()

    class DifferentModel(BaseUUIDModel):
        pass

    model1 = BaseUUIDModel(uuid=uuid_val)
    model2 = DifferentModel(uuid=uuid_val)
    assert model1 != model2


def test_base_uuid_model_eq_non_basemodel_object() -> None:
    model = BaseUUIDModel(uuid=uuid4())
    assert model != 'not a model'
    assert model != 123  # noqa: PLR2004
    assert model != None  # noqa: E711


def test_base_uuid_model_ne_different_uuid() -> None:
    model1 = BaseUUIDModel(uuid=uuid4())
    model2 = BaseUUIDModel(uuid=uuid4())
    assert (model1 != model2) is True


def test_base_uuid_model_ne_same_uuid() -> None:
    uuid_val = uuid4()
    model1 = BaseUUIDModel(uuid=uuid_val)
    model2 = BaseUUIDModel(uuid=uuid_val)
    assert (model1 != model2) is False


def test_base_uuid_model_hash_same_uuid() -> None:
    uuid_val = uuid4()
    model1 = BaseUUIDModel(uuid=uuid_val)
    model2 = BaseUUIDModel(uuid=uuid_val)
    assert hash(model1) == hash(model2)


def test_base_uuid_model_hash_different_uuid() -> None:
    model1 = BaseUUIDModel(uuid=uuid4())
    model2 = BaseUUIDModel(uuid=uuid4())
    assert hash(model1) != hash(model2)


def test_base_uuid_model_hash_equals_uuid_hash() -> None:
    uuid_val = uuid4()
    model = BaseUUIDModel(uuid=uuid_val)
    assert hash(model) == hash(uuid_val)
