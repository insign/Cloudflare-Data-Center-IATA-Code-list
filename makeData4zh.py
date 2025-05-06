import json
import requests
import time
from urllib.parse import quote

# 加载数据
with open("cloudflare-iata.json", "r", encoding="utf-8", newline="\n") as f:
    result = json.load(f)

# 加载字典
with open("en2zh.json", "r", encoding="utf-8") as f:
    en2zh = json.load(f)


# 谷歌翻译 API
def google_translate(text, target_language="zh-CN"):
    """使用 Google Translate API 翻译文本"""
    base_url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "auto",
        "tl": target_language,
        "dt": "t",
        "q": text,
    }

    try:
        encoded_params = "&".join([f"{k}={quote(str(v))}" for k, v in params.items()])
        url = f"{base_url}?{encoded_params}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()[0][0][0]

        print(f"谷歌翻译请求失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"谷歌翻译过程中出错: {e}")

    return None


# 处理翻译
zh_result = {}

for code, name in result.items():
    if name in en2zh:
        zh_result[code] = en2zh[name]
    else:
        print(f"原文 {name} 暂无翻译，尝试机器翻译...")

        # 使用谷歌翻译
        translated = google_translate(name)
        if translated:
            print(f"谷歌翻译: {name} -> {translated}")
            zh_result[code] = translated
            time.sleep(0.5)
        else:
            print(f"无法翻译: {name}")
            zh_result[code] = name

# 保存结果
with open("cloudflare-iata-zh.json", "w", encoding="utf-8") as f:
    json.dump(zh_result, f, ensure_ascii=False, indent=2, sort_keys=True)

print(f"已保存，共 {len(zh_result)} 个节点翻译")
