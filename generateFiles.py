import json
import os
import requests


def generate_files(json_path, output_dir):
    with open(json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        for code, value in data.items():
            file_path = os.path.join(output_dir, code)
            os.makedirs(output_dir, exist_ok=True)
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
<style>
.markdown-body {{box-sizing: border-box;min-width: 200px;max-width: 980px;margin: 0 auto;padding: 45px;}}@media (max-width: 767px) {{.markdown-body {{padding: 15px;}}}}.markdown-body {{font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;font-size: 16px;line-height: 1.5;word-wrap: break-word;color: #24292e;}}.markdown-body a {{color: #0366d6;text-decoration: none;}}.markdown-body a:hover {{text-decoration: underline;}}.markdown-body h1, .markdown-body h2, .markdown-body h3 {{margin-top: 24px;margin-bottom: 16px;font-weight: 600;line-height: 1.25;}}.markdown-body h1 {{font-size: 2em;border-bottom: 1px solid #eaecef;padding-bottom: .3em;}}.markdown-body h2 {{font-size: 1.5em;border-bottom: 1px solid #eaecef;padding-bottom: .3em;}}.markdown-body table {{border-collapse: collapse;width: 100%;}}.markdown-body table th, .markdown-body table td {{border: 1px solid #dfe2e5;padding: 6px 13px;}}.markdown-body table tr {{background-color: #fff;}}.markdown-body table tr:nth-child(2n) {{background-color: #f6f8fa;}}.markdown-body code {{padding: 0.2em 0.4em;margin: 0;font-size: 85%;background-color: rgba(27,31,35,.05);border-radius: 3px;}}.markdown-body pre {{padding: 16px;overflow: auto;font-size: 85%;line-height: 1.45;background-color: #f6f8fa;border-radius: 3px;}}.markdown-body pre code {{display: inline;padding: 0;margin: 0;overflow: visible;line-height: inherit;word-wrap: normal;background-color: transparent;border: 0;}}
</style>
</head>
<body class="markdown-body">
{html_content}
</body></html>"""

    with open(output_path, "w", encoding="utf-8") as html_file:
        html_file.write(full_html)


generate_files("cloudflare-iata.json", os.path.join("dist", "en"))
generate_files("cloudflare-iata-zh.json", os.path.join("dist", "zh"))
write_headers_file(os.path.join("dist"))
github_token = os.environ.get("GITHUB_TOKEN")
convert_readme_to_html("README.md", os.path.join("dist", "index.html"), github_token)
