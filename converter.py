import json
import toml
import yaml
from html.parser import HTMLParser
from CORE import Converter, register
@register
class JsonToToml(Converter):
    @property
    def supported_formats(self):
        return ('json', 'toml')
    def convert(self, input_data: str) -> str:
        python_dict = json.loads(input_data)
        return toml.dumps(python_dict)
@register
class TomlToJson(Converter):
    @property
    def supported_formats(self):
        return ('toml', 'json')
    def convert(self, input_data: str) -> str:
        python_dict = toml.loads(input_data)
        return json.dumps(python_dict, indent=4)
@register
class TomlToYaml(Converter):
    @property
    def supported_formats(self):
        return ('toml', 'yaml')

    def convert(self, input_data: str) -> str:
        python_dict = toml.loads(input_data)
        return yaml.safe_dump(python_dict)
@register
class YamlToToml(Converter):
    @property
    def supported_formats(self):
        return ('yaml', 'toml')

    def convert(self, input_data: str) -> str:
        python_dict = yaml.safe_load(input_data)
        return toml.dumps(python_dict)
def _dict_to_html(data) -> str:
    if isinstance(data, dict):
        res = "<dl>"
        for k, v in data.items():
            res += f"<dt>{k}</dt><dd>{_dict_to_html(v)}</dd>"
        res += "</dl>"
        return res
    elif isinstance(data, list):
        res = "<ul>"
        for item in data:
            res += f"<li>{_dict_to_html(item)}</li>"
        res += "</ul>"
        return res
    else:
        return str(data)
@register
class YamlToHtml(Converter):
    @property
    def supported_formats(self):
        return ('yaml', 'html5')

    def convert(self, input_data: str) -> str:
        python_dict = yaml.safe_load(input_data)
        return _dict_to_html(python_dict)
class HtmlToDictParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.root = None
        self.stack = []
        self.current_text = ""

    def handle_starttag(self, tag, attrs):
        self.current_text = ""
        if tag == 'dl':
            new_dict = {}
            if not self.stack:
                self.root = new_dict
            else:
                p_type, p_obj, key = self.stack[-1]
                if p_type == 'dict':
                    p_obj[key] = new_dict
                elif p_type == 'list':
                    p_obj.append(new_dict)
            self.stack.append(('dict', new_dict, None))
        elif tag == 'ul':
            new_list = []
            p_type, p_obj, key = self.stack[-1]
            if p_type == 'dict':
                p_obj[key] = new_list
            elif p_type == 'list':
                p_obj.append(new_list)
            self.stack.append(('list', new_list, None))

    def handle_endtag(self, tag):
        text = self.current_text.strip()
        if tag == 'dt':
            if self.stack and self.stack[-1][0] == 'dict':
                t, obj, _ = self.stack.pop()
                self.stack.append((t, obj, text))
        elif tag == 'dd':
            if text:
                t, obj, key = self.stack[-1]
                if t == 'dict' and key not in obj:
                    obj[key] = text
        elif tag == 'li':
            if text:
                t, obj, _ = self.stack[-1]
                if t == 'list':
                    obj.append(text)
        elif tag in ('dl', 'ul'):
            if self.stack:
                self.stack.pop()
        self.current_text = ""

    def handle_data(self, data):
        self.current_text += data
@register
class HtmlToYaml(Converter):
    @property
    def supported_formats(self):
        return ('html5', 'yaml')

    def convert(self, input_data: str) -> str:
        parser = HtmlToDictParser()
        parser.feed(input_data)
        return yaml.safe_dump(parser.root)