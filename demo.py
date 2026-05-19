import json
from CORE import convert
import converter
print("\n==================================================")
print("程式碼強制執行成功")
print("==================================================")

initial_structure = {
    "name": "Alice",
    "hobbies": ["reading", "climbing"],
    "address": {"city": "Taipei"}
}

initial_json_str = json.dumps(initial_structure)
print(f" 初始 JSON 資料: {initial_json_str}")

print("\n>>>  正在將 JSON 轉為 TOML...")
toml_data = convert(initial_json_str, "json", "toml")

print(">>>  正在將 TOML 轉為 YAML...")
yaml_data = convert(toml_data, "toml", "yaml")

print(">>>  正在將 YAML 轉為 HTML5...")
html_data = convert(yaml_data, "yaml", "html")
print(f" 中間產出的 HTML5: {html_data}")

print("\n>>>  正在將 HTML5 轉回 YAML...")
yaml_back = convert(html_data, "html", "yaml")

print(">>>  正在將 YAML 轉回 TOML...")
toml_back = convert(yaml_back, "yaml", "toml")

print(">>>  正在將 TOML 轉回 JSON...")
final_json_str = convert(toml_back, "toml", "json")

final_structure = json.loads(final_json_str)

print("\n==================================================")
if initial_structure == final_structure:
    print(">>> 🎉 🎉 🎉 6階段轉生圓滿成功！！！頭尾資料完全一致！")
else:
    print(">>> ❌ 糟糕，頭尾資料不匹配！")
print("==================================================\n")