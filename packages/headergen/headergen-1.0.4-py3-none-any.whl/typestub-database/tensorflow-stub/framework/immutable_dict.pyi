import collections.abc

class ImmutableDict(collections.abc.Mapping):
    def __init__(self, *args, **kwargs) -> None: ...
    def __getitem__(self, key): ...
    def __contains__(self, key): ...
    def __iter__(self): ...
    def __len__(self): ...
