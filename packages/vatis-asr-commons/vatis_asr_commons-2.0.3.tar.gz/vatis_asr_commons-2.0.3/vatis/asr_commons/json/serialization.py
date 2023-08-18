import abc


class JSONSerializable(abc.ABC):
    @abc.abstractmethod
    def to_json(self):
        pass
