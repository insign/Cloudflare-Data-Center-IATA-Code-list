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
        # Use a delay to respect API rate limits
        time.sleep(1)
        location = geolocator.geocode(place, timeout=10)
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

def generate_combined_full_data(en_path, zh_path, output_path):
    """
    Reads English and Chinese IATA files, enriches them with latitude and longitude,
    and writes a combined result to a new file.
    """
    if not os.path.exists(en_path) or not os.path.exists(zh_path):
        print("Error: Input files (en or zh) not found.")
        return

    with open(en_path, 'r', encoding='utf-8') as f:
        data_en = json.load(f)

    with open(zh_path, 'r', encoding='utf-8') as f:
        data_zh = json.load(f)

    full_data = {}
    # Sort by IATA code for consistent processing and output order
    sorted_slugs = sorted(data_en.keys())

    for slug in sorted_slugs:
        place_en = data_en[slug]
        # Fallback to English name if no translation exists
        place_zh = data_zh.get(slug, place_en)

        print(f"Processing: {slug} - {place_en}")
        lat, lng = get_lat_lng(place_en)

        full_data[slug] = {
            "en": place_en,
            "zh": place_zh,
            "lat": lat,
            "lng": lng
        }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated {output_path} with {len(full_data)} entries.")


if __name__ == "__main__":
    en_input = 'cloudflare-iata.json'
    zh_input = 'cloudflare-iata-zh.json'
    # The single new output file
    output_full = 'cloudflare-iata-full.json'

    print("--- Starting Geocoding for Combined Full Data File ---")
    generate_combined_full_data(en_input, zh_input, output_full)