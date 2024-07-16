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


generate_files("cloudflare-iata.json", os.path.join("dist", "en"))
generate_files("cloudflare-iata-zh.json", os.path.join("dist", "zh"))
