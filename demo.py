import json
from CORE import convert
import converter

def main():
    # 這是最頂端的強制輸出，只要有跑就一定會印字！
    print("\n==================================================")
    print(">>> [TEST] 全自動閉環迴路測試正式啟動...")
    print("==================================================")
    
    initial_structure = {
        "name": "Alice",
        "hobbies": ["reading", "climbing"],
        "address": {"city": "Taipei"}
    }
    
    initial_json_str = json.dumps(initial_structure)
    print(f"[{chr(128052)} 初始 JSON 資料]: {initial_json_str}")
    
    # 開始瘋狂轉生大鏈條
    print("\n>>> [1/6] 正在將 JSON 轉為 TOML...")
    toml_data = convert(initial_json_str, "json", "toml")
    
    print(">>> [2/6] 正在將 TOML 轉為 YAML...")
    yaml_data = convert(toml_data, "toml", "yaml")
    
    print(">>> [3/6] 正在將 YAML 轉為 HTML5...")
    html_data = convert(yaml_data, "yaml", "html")
    print(f"[{chr(127881)} 中間產出的 HTML5]: {html_data}")
    
    print("\n>>> [4/6] 正在將 HTML5 轉回 YAML...")
    yaml_back = convert(html_data, "html", "yaml")
    
    print(">>> [5/6] 正在將 YAML 轉回 TOML...")
    toml_back = convert(yaml_back, "yaml", "toml")
    
    print(">>> [6/6] 正在將 TOML 轉回 JSON...")
    final_json_str = convert(toml_back, "toml", "json")
    
    final_structure = json.loads(final_json_str)
    
    print("\n==================================================")
    if initial_structure == final_structure:
        print(">>> 🎉 🎉 🎉 測試完美成功！！！")
        print(">>> 經歷 6 階段轉生，頭尾資料 100% 完全一致！")
    else:
        print(">>> ❌ 糟糕，頭尾資料不一致，演算法有漏洞！")
    print("==================================================\n")

if __name__ == "__main__":
    main()