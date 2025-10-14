import json
import time
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# Initialize the geocoder
geolocator = Nominatim(user_agent="cloudflare_iata_geocoder/1.0")

# Hardcoded fallback coordinates for Antarctica
ANTARCTICA_COORDS = (-82.8628, 135.0000)

def get_lat_lng(place, retries=3, delay=2):
    """
    Geocode a place name to get latitude and longitude, with retries and a hardcoded fallback.
    """
    if place == "LOCAL":
        return 0.0, 0.0

    try:
        location = geolocator.geocode(place)
        time.sleep(1)  # Respect the 1-second rate limit of Nominatim
        if location:
            return location.latitude, location.longitude
        else:
            print(f"Warning: Could not geocode '{place}'. Using Antarctica fallback.")
            return ANTARCTICA_COORDS
    except GeocoderTimedOut:
        print(f"Warning: Geocoding timed out for '{place}'. Retrying in {delay}s...")
        if retries > 0:
            time.sleep(delay)
            return get_lat_lng(place, retries - 1, delay * 2)
        else:
            print(f"Error: Failed to geocode '{place}' after multiple retries. Using Antarctica fallback.")
            return ANTARCTICA_COORDS
    except GeocoderServiceError as e:
        print(f"Error: Geocoding service error for '{place}': {e}. Using Antarctica fallback.")
        return ANTARCTICA_COORDS
    except Exception as e:
        print(f"An unexpected error occurred for '{place}': {e}. Using Antarctica fallback.")
        return ANTARCTICA_COORDS

def process_iata_file_en(input_path, output_path):
    """
    Reads the English IATA JSON file, enriches it with latitude and longitude,
    and writes the result to a new file.
    """
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    full_data = []
    for slug, place in data.items():
        print(f"Processing: {slug} - {place}")
        lat, lng = get_lat_lng(place)

        full_data.append({
            "slug": slug,
            "place": place,
            "lat": lat,
            "lng": lng
        })

    full_data.sort(key=lambda x: x['slug'])

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated {output_path} with {len(full_data)} entries.")

def generate_zh_full_data_from_en(en_full_path, zh_path, output_path_zh):
    """
    Generates the Chinese full data file by merging coordinates from the English
    full data file with place names from the Chinese IATA file.
    """
    if not all(os.path.exists(p) for p in [en_full_path, zh_path]):
        print(f"Error: One or more input files are missing.")
        return

    with open(en_full_path, 'r', encoding='utf-8') as f:
        en_data = json.load(f)

    with open(zh_path, 'r', encoding='utf-8') as f:
        zh_data = json.load(f)

    # Create a lookup dictionary for geo data from the English file for efficiency
    geo_data_map = {item['slug']: {'lat': item['lat'], 'lng': item['lng']} for item in en_data}

    full_data_zh = []
    for slug, place_zh in zh_data.items():
        geo_coords = geo_data_map.get(slug)
        if geo_coords:
            full_data_zh.append({
                "slug": slug,
                "place": place_zh,
                "lat": geo_coords['lat'],
                "lng": geo_coords['lng']
            })
        else:
            print(f"Warning: Slug '{slug}' found in Chinese file but not in English geo data. Using Antarctica fallback.")
            full_data_zh.append({
                "slug": slug,
                "place": place_zh,
                "lat": ANTARCTICA_COORDS[0],
                "lng": ANTARCTICA_COORDS[1]
            })

    full_data_zh.sort(key=lambda x: x['slug'])

    with open(output_path_zh, 'w', encoding='utf-8') as f:
        json.dump(full_data_zh, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated {output_path_zh} with {len(full_data_zh)} entries based on existing geo data.")


if __name__ == "__main__":
    en_input = 'cloudflare-iata.json'
    en_output_full = 'cloudflare-iata-full.json'
    zh_input = 'cloudflare-iata-zh.json'
    zh_output_full = 'cloudflare-iata-full-zh.json'

    # Step 1: Process the English file to get geo coordinates
    print("--- Starting Geocoding for English File ---")
    process_iata_file_en(en_input, en_output_full)

    # Step 2: Generate the Chinese full data file using the results from Step 1
    print("\n--- Generating Chinese File from English Geo Data ---")
    generate_zh_full_data_from_en(en_output_full, zh_input, zh_output_full)