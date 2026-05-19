from abc import ABC, abstractmethod
from functools import reduce

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

class ConverterRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._mapping = {}
        return cls._instance

    def register(self, converter_obj):
        key = converter_obj.supported_formats
        self._mapping[key] = converter_obj

    def get_converter(self, src: str, dst: str):
        return self._mapping.get((src, dst))

    def list_pairs(self):
        return list(self._mapping.keys())

def register(target_class):
    office = ConverterRegistry()
    worker = target_class()
    office.register(worker)
    return target_class

class ConverterError(Exception):
    pass

class PipelineError(ConverterError):
    pass

class Pipeline:
    def __init__(self, converters_list):
        self.converters = converters_list
        self._validate_pipeline()

    def _validate_pipeline(self):
        if not self.converters:
            raise PipelineError("Pipeline is empty.")
        for i in range(len(self.converters) - 1):
            current_output = self.converters[i].supported_formats[1]
            next_input = self.converters[i + 1].supported_formats[0]
            if current_output != next_input:
                raise PipelineError(
                    f"Format mismatch: {self.converters[i].__class__.__name__} outputs [{current_output}] "
                    f"which cannot connect to {self.converters[i+1].__class__.__name__} requiring [{next_input}]"
                )

    def run(self, input_data: str) -> str:
        current_data = input_data
        for converter in self.converters:
            current_data = converter.convert(current_data)
        return current_data

def resolve_chain(registry, source_fmt: str, target_fmt: str) -> Pipeline:
    if source_fmt == target_fmt:
        raise PipelineError("Source and target formats are identical.")
        
    pairs = registry.list_pairs()
    queue = [[source_fmt]]
    visited = {source_fmt}
    path = None
    
    while queue:
        curr_path = queue.pop(0)
        node = curr_path[-1]
        
        if node == target_fmt:
            path = curr_path
            break
            
        neighbors = [dst for src, dst in pairs if src == node and dst not in visited]
        for nxt in neighbors:
            visited.add(nxt)
            queue.append(curr_path + [nxt])
            
    if not path:
        raise PipelineError(f"No conversion path found from {source_fmt} to {target_fmt}")
        
    pairs_list = list(zip(path[:-1], path[1:]))
    converters = list(map(lambda p: registry.get_converter(p[0], p[1]), pairs_list))
    
    return reduce(lambda acc, c: Pipeline(acc.converters + [c]), converters[1:], Pipeline([converters[0]]))

def convert(input_data: str, source_fmt: str, target_fmt: str) -> str:
    registry = ConverterRegistry()
    pipeline = resolve_chain(registry, source_fmt, target_fmt)
    return pipeline.run(input_data)