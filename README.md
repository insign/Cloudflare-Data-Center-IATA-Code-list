# [Cloudflare-Data-Center-IATA-Code-list](https://github.com/LufsX/Cloudflare-Data-Center-IATA-Code-list)

Cloudflare 最全数据中心及其 IATA 代码列表

---

Cloudflare's Comprehensive Data Center and IATA Code List

## 数据文件 Data Files

### 基础数据 Basic Data

仅包含 IATA 代码和对应的位置名称。格式为键值对：`{ "IATA 代码": "位置名称" }`

Only includes IATA codes and their corresponding location names. The format is a key-value object: `{ "IATA Code": "Location Name" }`

- 中文 Chinese
  - GitHub Raw: `https://github.com/LufsX/Cloudflare-Data-Center-IATA-Code-list/raw/main/cloudflare-iata-zh.json`
  - Jsdelivr CDN: `https://cdn.jsdelivr.net/gh/LufsX/Cloudflare-Data-Center-IATA-Code-list/cloudflare-iata-zh.json`
- 英文 English
  - GitHub Raw: `https://github.com/LufsX/Cloudflare-Data-Center-IATA-Code-list/raw/main/cloudflare-iata.json`
  - Jsdelivr CDN: `https://cdn.jsdelivr.net/gh/LufsX/Cloudflare-Data-Center-IATA-Code-list/cloudflare-iata.json`

### 完整地理位置数据 Full Data with Geolocation

包含每个数据中心的中英文位置名称、经纬度信息。格式为键值对：`{ "IATA 代码": { "place_en": "英文位置", "place_zh": "中文位置", "lat": 纬度, "lng": 经度 } }`

Contains the location in both English and Chinese, along with latitude and longitude for each data center. The format is a key-value object: `{ "IATA Code": { "place_en": "English Location", "place_zh": "Chinese Location", "lat": Latitude, "lng": Longitude } }`

- GitHub Raw: `https://github.com/LufsX/Cloudflare-Data-Center-IATA-Code-list/raw/main/cloudflare-iata-full.json`
- Jsdelivr CDN: `https://cdn.jsdelivr.net/gh/LufsX/Cloudflare-Data-Center-IATA-Code-list/cloudflare-iata-full.json`

## API

用法 Example Usage:

- `https://iata.isteed.cc/<zh|en>/<IATA Code>`
  - `<zh|en>`: 语言 Language，`zh` 中文 Chinese，`en` 英文 English
  - `<IATA Code>`: IATA 代码

示例 Example:

- `https://iata.isteed.cc/zh/LAX`
  返回值 Return Value: `美国洛杉矶`
- `https://iata.isteed.cc/en/LAX`
  返回值 Return Value: `Los Angeles, United States`

## 其它 Others

数据抓取自 [Cloudflare System Status](https://www.cloudflarestatus.com/api/v2/components.json)

位置数据来源于 [speed.cloudflare.com](https://speed.cloudflare.com/locations)

其中添加了一个特例: `LOCAL` 用于标识本地网络，以便在本地网络中使用

地名对照表: `en2zh.json`

欢迎纠错补充～

---

Data retrieved from [Cloudflare System Status](https://www.cloudflarestatus.com/api/v2/components.json)

Location data sourced from [speed.cloudflare.com](https://speed.cloudflare.com/locations)

A special case has been added: `LOCAL` is used to identify the local network for use in the local network

Pull requests and issues are welcome ~
