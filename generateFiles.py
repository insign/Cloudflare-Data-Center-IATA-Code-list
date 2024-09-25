import json
import os


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


generate_files("cloudflare-iata.json", os.path.join("dist", "en"))
generate_files("cloudflare-iata-zh.json", os.path.join("dist", "zh"))
write_headers_file(os.path.join("dist"))
