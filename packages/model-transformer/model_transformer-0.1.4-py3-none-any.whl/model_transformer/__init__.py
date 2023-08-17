from functools import partial
from typing import Any, Callable, Dict, Generic, List, TypeVar

_InputDict = TypeVar("_InputDict", bound=dict)
_OutputDict = TypeVar("_OutputDict", bound=dict)


class BaseField:
    def __call__(self, row: dict) -> Any:
        raise NotImplementedError("BaseField is an abstract class")


class Field(BaseField):
    def __init__(self, name, default=None, filter=None) -> None:
        self.name = name
        self.filter = filter
        self.default = default

    def __call__(self, row: dict) -> Any:
        data = row.get(self.name, self.default)

        if self.filter:
            data = self.filter(data)

        return data


class Transformer(Generic[_InputDict, _OutputDict]):
    """Schema is a base class for all schemas defined.

    It provides a way to define a schema for a given data source.
    """

    def __init__(self):
        self._multi_field_results = {}

    def __getattr__(self, name: str) -> Any:
        field = self.fields.get(name)

        if field is None:
            raise AttributeError(f"{name} is not a valid field")

        return field

    def clear(self):
        self._multi_field_results = {}

    def _split_multi_fields(self, fields: dict) -> dict:
        new_fields = {}

        def register_or_invoke(key: str, index: int, field: Callable, row: dict):
            if key in self._multi_field_results:
                data = self._multi_field_results[key]
            else:
                data = self._multi_field_results[key] = field(row)

            try:
                return data[index]
            except IndexError:
                return None

        for key, value in fields.items():
            if "__" in key:
                keys = key.split("__")

                for k in keys:
                    new_fields[k] = partial(
                        register_or_invoke, key, keys.index(k), value
                    )
            else:
                new_fields[key] = value

        return new_fields

    @property
    def fields(self):
        defined_fields = {
            key: value
            for key, value in vars(self.__class__).items()
            if isinstance(value, BaseField)
        }

        dynamic_fields = {
            key[4:]: partial(value, self)
            for key, value in vars(self.__class__).items()
            if key.startswith("get_") and not isinstance(value, BaseField)
        }

        return {
            **self._split_multi_fields(defined_fields),
            **self._split_multi_fields(dynamic_fields),
        }

    @property
    def field_names(self):
        return self.fields.keys()

    def transform_row(self, row: _InputDict) -> _OutputDict:
        self.clear()

        return {k: field(row) for k, field in self.fields.items()}

    def transform(self, rows: List[_InputDict]) -> List[_OutputDict]:
        return [self.transform_row(row) for row in rows]


class CombineTransformers:
    def __init__(self, **transformers) -> None:
        assert all(isinstance(t, Transformer) for t in transformers.values())

        self.transformers = transformers

    def transform(self, rows: List[Dict]) -> Any:
        return {
            name: transformer.transform(rows)
            for name, transformer in self.transformers.items()
        }

    def transform_row(self, row: dict) -> dict:
        return {
            name: transformer.transform_row(row)
            for name, transformer in self.transformers.items()
        }
