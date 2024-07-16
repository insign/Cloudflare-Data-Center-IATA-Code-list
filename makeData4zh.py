import json

# 加载数据
with open("cloudflare-iata.json", "r", encoding="utf-8", newline="\n") as f:
    result = json.load(f)

# 加载字典
with open("en2zh.json", "r", encoding="utf-8") as f:
    en2zh = json.load(f)

zh_result = {}
for code, name in result.items():
    if name in en2zh:
        zh_result[code] = en2zh[name]
    else:
        print(f"原文 {name} 暂无翻译")

with open("cloudflare-iata-zh.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(zh_result, f, ensure_ascii=False, indent=2)
