import json
from CORE import convert
import converter
print("\n")
print("程式碼強制執行成功")
print("\n")

initial_structure = {
    "name": "Alan",
    "hobbies": ["gaming", "playing"],
    "address": {"city": "Taipei"}
}

initial_json_str = json.dumps(initial_structure)
print(f" 初始 JSON: {initial_json_str}")

print("JSON 轉為 TOML")
toml_data = convert(initial_json_str, "json", "toml")

print("TOML 轉為 YAML")
yaml_data = convert(toml_data, "toml", "yaml")

print("YAML 轉為 HTML5")
html_data = convert(yaml_data, "yaml", "html")
print(f" 中間產出的 HTML5: {html_data}")

print("HTML5 轉回 YAML");
yaml_back = convert(html_data, "html", "yaml")

print("YAML 轉回 TOML")
toml_back = convert(yaml_back, "yaml", "toml")

print("TOML 轉回 JSON")
final_json_str = convert(toml_back, "toml", "json")

final_structure = json.loads(final_json_str)

print("\n")
if initial_structure == final_structure:
    print("成功")
else:
    print("頭尾資料不匹配")
print("\n")