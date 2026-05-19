import time
import logging
from abc import ABC, abstractmethod
from functools import reduce, wraps

logger = logging.getLogger("ConverterFramework")

class ConverterError(Exception):
    pass

class PipelineError(ConverterError):
    pass

class UnsupportedFormatError(ConverterError):
    pass

class Converter(ABC):
    @property
    @abstractmethod
    def supported_formats(self) -> tuple[str, str]:
        pass

    @abstractmethod
    def convert(self, input_data: str) -> str:
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.supported_formats[0]} -> {self.supported_formats[1]}>"

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
    registry = ConverterRegistry()
    instance = target_class()
    registry.register(instance)
    return target_class

def logging_decorator(func):
    @wraps(func)
    def wrapper(self, input_data: str, *args, **kwargs):
        class_name = self.__class__.__name__
        src, dst = self.supported_formats
        logger.debug(f"[{class_name}] Stage start ({src} -> {dst}). Input chunk length: {len(input_data)}")
        start_time = time.time()
        try:
            result = func(self, input_data, *args, **kwargs)
            elapsed = time.time() - start_time
            logger.debug(f"[{class_name}] Stage complete. Output chunk length: {len(result)} | Execution time: {elapsed:.4f}s")
            return result
        except Exception as e:
            logger.error(f"[{class_name}] Critical error during staging: {str(e)}")
            raise e
    return wrapper

class Pipeline:
    def __init__(self, converters_list):
        self.converters = converters_list
        self._validate_pipeline()

    def _validate_pipeline(self):
        if not self.converters:
            logger.error("Failed to construct pipeline: Converter sequence empty")
            raise PipelineError("Pipeline queue cannot be empty.")
        for i in range(len(self.converters) - 1):
            curr_out = self.converters[i].supported_formats[1]
            next_in = self.converters[i + 1].supported_formats[0]
            if curr_out != next_in:
                err_msg = f"Incompatible pipeline stages: {self.converters[i]} outputs '{curr_out}', but {self.converters[i+1]} demands '{next_in}'"
                logger.error(err_msg)
                raise PipelineError(err_msg)

    def run(self, input_data: str) -> str:
        current_data = input_data
        for converter in self.converters:
            current_data = converter.convert(current_data)
        return current_data

def resolve_chain(registry, source_fmt: str, target_fmt: str) -> Pipeline:
    if source_fmt == target_fmt:
        logger.error(f"Routing halted: source and target formats are identical ({source_fmt})")
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
        logger.error(f"Routing failed: no path discovered between '{source_fmt}' and '{target_fmt}'")
        raise PipelineError(f"No conversion path found from {source_fmt} to {target_fmt}")

    if len(path) > 2:
        logger.warning(f"Indirect path fallback required. Resolved multi-stage route: {' -> '.join(path)}")

    pairs_list = list(zip(path[:-1], path[1:]))
    converters = list(map(lambda p: registry.get_converter(p[0], p[1]), pairs_list))

    return reduce(lambda acc, c: Pipeline(acc.converters + [c]), converters[1:], Pipeline([converters[0]]))

def convert(input_data: str, source_fmt: str, target_fmt: str) -> str:
    logger.info(f"Initiating global conversion pipeline: internal route triggered for '{source_fmt}' to '{target_fmt}'")
    start_time = time.time()
    try:
        registry = ConverterRegistry()
        pipeline = resolve_chain(registry, source_fmt, target_fmt)
        logger.info(f"Pipeline successfully compiled with {len(pipeline.converters)} active stages")
        output_data = pipeline.run(input_data)
        elapsed = time.time() - start_time
        logger.info(f"Global conversion lifecycle completed successfully in {elapsed:.4f}s")
        return output_data
    except Exception as e:
        logger.error(f"Global conversion pipeline collapsed: {str(e)}")
        raise e