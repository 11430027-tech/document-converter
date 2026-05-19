import json
import toml
import yaml
from html.parser import HTMLParser
from CORE import Converter, register, logging_decorator, logger

def dict_to_html5(data) -> str:
    if isinstance(data, dict):
        res = "<dl>"
        for k, v in data.items():
            res += f"<dt>{k}</dt><dd>{dict_to_html5(v)}</dd>"
        res += "</dl>"
        return res
    elif isinstance(data, list):
        res = "<ul>"
        for item in data:
            res += f"<li>{dict_to_html5(item)}</li>"
        res += "</ul>"
        return res
    else:
        return str(data)

class HTML5DlParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.current_tag = None
        self.current_key = None
        self.result = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag == 'dl':
            new_dict = {}
            self.stack.append(('dict', new_dict))
        elif tag == 'ul':
            new_list = []
            self.stack.append(('list', new_list))

    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
        if self.current_tag == 'dt':
            self.current_key = data
        elif self.current_tag in ('dd', 'li'):
            if self.stack:
                tag_type, obj = self.stack[-1]
                if tag_type == 'list':
                    obj.append(data)
                elif tag_type == 'dict' and self.current_key:
                    obj[self.current_key] = data

    def handle_endtag(self, tag):
        if tag in ('dl', 'ul'):
            if len(self.stack) > 1:
                tag_type, closed_obj = self.stack.pop()
                parent_type, parent_obj = self.stack[-1]
                if parent_type == 'dict' and self.current_key:
                    parent_obj[self.current_key] = closed_obj
                elif parent_type == 'list':
                    parent_obj.append(closed_obj)
            else:
                if self.stack:
                    _, self.result = self.stack.pop()

@register
class JsonToToml(Converter):
    @property
    def supported_formats(self) -> tuple[str, str]:
        return ("json", "toml")

    @logging_decorator
    def convert(self, input_data: str) -> str:
        parsed = json.loads(input_data)
        logger.debug(f"[{self.__class__.__name__}] Parsed middle-state structure: {parsed}")
        return toml.dumps(parsed)

@register
class TomlToJson(Converter):
    @property
    def supported_formats(self) -> tuple[str, str]:
        return ("toml", "json")

    @logging_decorator
    def convert(self, input_data: str) -> str:
        parsed = toml.loads(input_data)
        logger.debug(f"[{self.__class__.__name__}] Parsed middle-state structure: {parsed}")
        return json.dumps(parsed)

@register
class TomlToYaml(Converter):
    @property
    def supported_formats(self) -> tuple[str, str]:
        return ("toml", "yaml")

    @logging_decorator
    def convert(self, input_data: str) -> str:
        parsed = toml.loads(input_data)
        logger.debug(f"[{self.__class__.__name__}] Parsed middle-state structure: {parsed}")
        return yaml.dump(parsed, allow_unicode=True)

@register
class YamlToToml(Converter):
    @property
    def supported_formats(self) -> tuple[str, str]:
        return ("yaml", "toml")

    @logging_decorator
    def convert(self, input_data: str) -> str:
        parsed = yaml.safe_load(input_data)
        logger.debug(f"[{self.__class__.__name__}] Parsed middle-state structure: {parsed}")
        return toml.dumps(parsed)

@register
class YamlToHtml(Converter):
    @property
    def supported_formats(self) -> tuple[str, str]:
        return ("yaml", "html")

    @logging_decorator
    def convert(self, input_data: str) -> str:
        parsed = yaml.safe_load(input_data)
        logger.debug(f"[{self.__class__.__name__}] Parsed middle-state structure: {parsed}")
        return dict_to_html5(parsed)

@register
class HtmlToYaml(Converter):
    @property
    def supported_formats(self) -> tuple[str, str]:
        return ("html", "yaml")

    @logging_decorator
    def convert(self, input_data: str) -> str:
        parser = HTML5DlParser()
        parser.feed(input_data)
        parsed = parser.result
        logger.debug(f"[{self.__class__.__name__}] Parsed middle-state structure: {parsed}")
        return yaml.dump(parsed, allow_unicode=True)