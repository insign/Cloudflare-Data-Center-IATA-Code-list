import requests
import json
import re
import os

# 从 Cloudflare 节点状态中获取
url = "https://www.cloudflarestatus.com/api/v2/components.json"

response = requests.get(url)
data = response.json()

components = data.get("components", [])
exclude_ids = set()
for component in components:
    # 排除掉在  Cloudflare Sites and Services 中的内容
    if component.get("id") == "1km35smx8p41":
        exclude_ids = set(component.get("components", []))
        break

# 尝试读取现有的数据文件
output_file = "cloudflare-iata.json"
existing_data = {}
if os.path.exists(output_file):
    try:
        with open(output_file, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
        print(f"已读取现有数据，包含 {len(existing_data)} 个节点")
    except Exception as e:
        print(f"读取现有数据失败: {e}")
        existing_data = {}

# 获取新数据
new_data = {}
for component in components:
    comp_id = component.get("id")
    name = component.get("name")

    # 跳过排除列表
    if comp_id in exclude_ids:
        continue

    # 除了排除列表的，有名字的且包含「-」的只有节点
    if name and "-" in name:
        parts = name.split("-")
        if len(parts) == 2:
            location = parts[0].strip()
            code = parts[1].strip().strip("()")
            new_data[code] = re.sub(",.*,", ",", location)

# 特殊处理
new_data["JIB"] = "Djibouti City"
new_data["SIN"] = "Singapore"
new_data["LOCAL"] = "LOCAL"

# 合并新旧数据（新数据优先）
result = {**existing_data, **new_data}

# 输出更新情况
new_entries = set(new_data.keys()) - set(existing_data.keys())
if new_entries:
    print(f"Added {len(new_entries)} nodes: {', '.join(new_entries)}")
else:
    print("No new nodes added")

updated_entries = {
    k for k in new_data.keys() & existing_data.keys() if new_data[k] != existing_data[k]
}
if updated_entries:
    print(f"Updated {len(updated_entries)} nodes: {', '.join(updated_entries)}")

# 保存结果
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, sort_keys=True)

print(f"Data has been saved, a total of {len(result)} nodes")
