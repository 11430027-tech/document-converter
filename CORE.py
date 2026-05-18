from abc import ABC, abstractmethod

class Converter(ABC):
    
    @property
    @abstractmethod
    def supported_formats(self) -> tuple[str, str]:
        pass

    @abstractmethod
    def convert(self, input_data: str) -> str:
        pass

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        src_format = self.supported_formats[0]
        dst_format = self.supported_formats[1]
        return f"<{class_name}: {src_format} -> {dst_format}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Converter):
            return False
        return self.supported_formats == other.supported_formats