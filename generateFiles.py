import json
import os
import requests


def generate_files(json_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with open(json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        for code, value in data.items():
            file_path = os.path.join(output_dir, code)
            if isinstance(value, dict):
                value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(value)


def write_headers_file(output_dir):
    headers = """/en/*
  Access-Control-Allow-Origin: *
  Access-Control-Expose-Headers: *
  Cache-Control: public, max-age=86400
  Content-Type: text/plain; charset=UTF-8
/zh/*
  Access-Control-Allow-Origin: *
  Access-Control-Expose-Headers: *
  Cache-Control: public, max-age=86400
  Content-Type: text/plain; charset=UTF-8
/full/*
  Access-Control-Allow-Origin: *
  Access-Control-Expose-Headers: *
  Cache-Control: public, max-age=86400
  Content-Type: application/json; charset=UTF-8
"""
    headers_file_path = os.path.join(output_dir, "_headers")
    with open(headers_file_path, "w", encoding="utf-8") as f:
        f.write(headers)


def convert_readme_to_html(readme_path, output_path, github_token=None):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(readme_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    github_api_url = "https://api.github.com/markdown"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    payload = {"text": md_content}

    response = requests.post(github_api_url, headers=headers, json=payload)

    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"GitHub API request failed, status code: {response.status_code}")
        print(f"Error message: {response.text}")
        return

    full_html = f"""<!DOCTYPE html><html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cloudflare Data Center IATA Code List</title>
<link rel="icon" href="https://cdn.isteed.cc/favicon_opt.png">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.8.1/github-markdown.min.css" integrity="sha512-BrOPA520KmDMqieeM7XFe6a3u3Sb3F1JBaQnrIAmWg3EYrciJ+Qqe6ZcKCdfPv26rGcgTrJnZ/IdQEct8h3Zhw==" crossorigin="anonymous" referrerpolicy="no-referrer" />
<style>
.markdown-body {{box-sizing: border-box;min-width: 200px;max-width: 980px;margin: 0 auto;padding: 45px;}}@media (max-width: 767px) {{.markdown-body {{padding: 15px;}}}}
</style>
</head>
<body class="markdown-body">{html_content}</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as html_file:
        html_file.write(full_html)


generate_files("cloudflare-iata.json", os.path.join("dist", "en"))
generate_files("cloudflare-iata-zh.json", os.path.join("dist", "zh"))
generate_files("cloudflare-iata-full.json", os.path.join("dist", "full"))
write_headers_file(os.path.join("dist"))
github_token = os.environ.get("GITHUB_TOKEN")
convert_readme_to_html("README.md", os.path.join("dist", "index.html"), github_token)

for filename in [
    "cloudflare-iata.json",
    "cloudflare-iata-zh.json",
    "cloudflare-iata-full.json",
    "en2zh.json",
]:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    output_path = os.path.join("dist", filename)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
