import csv
import json
import os
import requests

# Cloudflare location endpoint used for coordinates lookup
CLOUDFLARE_LOCATIONS_URL = "https://speed.cloudflare.com/locations"
OURAIRPORTS_AIRPORTS_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"


# Cache for Cloudflare locations keyed by IATA code
def load_cloudflare_locations():
    try:
        response = requests.get(CLOUDFLARE_LOCATIONS_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            entry.get("iata"): {
                "lat": entry.get("lat"),
                "lng": entry.get("lon"),
                "cca2": entry.get("cca2"),
            }
            for entry in data
            if entry.get("iata")
            and entry.get("lat") is not None
            and entry.get("lon") is not None
            and entry.get("cca2")
        }
    except Exception as e:
        print(f"Error: Failed to load Cloudflare locations: {e}")
        return {}


CLOUDFLARE_LOCATIONS = load_cloudflare_locations()
OURAIRPORTS_LOCATIONS = None


def load_ourairports_locations():
    """Lazy-load OurAirports data for fallback lookups."""
    global OURAIRPORTS_LOCATIONS
    if OURAIRPORTS_LOCATIONS is not None:
        return OURAIRPORTS_LOCATIONS

    try:
        response = requests.get(OURAIRPORTS_AIRPORTS_URL, timeout=10)
        response.raise_for_status()

        # Parse CSV in-memory to build an IATA keyed lookup table
        decoded_content = response.text.splitlines()
        reader = csv.DictReader(decoded_content)

        airports = {}
        for row in reader:
            iata = (row.get("iata_code") or "").strip().upper()
            lat = row.get("latitude_deg")
            lon = row.get("longitude_deg")
            cca2 = (row.get("iso_country") or "").strip().upper() or None

            if not iata or not lat or not lon:
                continue

            try:
                airports[iata] = {
                    "lat": float(lat),
                    "lng": float(lon),
                    "cca2": cca2,
                }
            except ValueError:
                continue

        OURAIRPORTS_LOCATIONS = airports
        return OURAIRPORTS_LOCATIONS
    except Exception as e:
        print(f"Error: Failed to load OurAirports data: {e}")
        OURAIRPORTS_LOCATIONS = {}
        return OURAIRPORTS_LOCATIONS


def get_location_details(iata_code):
    """
    Look up latitude, longitude, and country code for an IATA code using Cloudflare data.
    """
    if iata_code == "LOCAL":
        return None, None, None

    location = CLOUDFLARE_LOCATIONS.get(iata_code.upper())
    if location:
        return location["lat"], location["lng"], location["cca2"]

    airports_locations = load_ourairports_locations()
    fallback_location = airports_locations.get(iata_code.upper())
    if fallback_location:
        return fallback_location["lat"], fallback_location["lng"], fallback_location["cca2"]

    print(f"Warning: Could not find coordinates for '{iata_code}'.")
    return None, None, None


def generate_combined_full_data(en_path, zh_path, output_path):
    """
    Reads English and Chinese IATA files, enriches them with latitude and longitude,
    and writes a combined result to a new file.
    """
    if not os.path.exists(en_path) or not os.path.exists(zh_path):
        print("Error: Input files (en or zh) not found.")
        return

    with open(en_path, "r", encoding="utf-8") as f:
        data_en = json.load(f)

    with open(zh_path, "r", encoding="utf-8") as f:
        data_zh = json.load(f)

    full_data = {}
    # Sort by IATA code for consistent processing and output order
    sorted_slugs = sorted(data_en.keys())

    for slug in sorted_slugs:
        place_en = data_en[slug]
        # Fallback to English name if no translation exists
        place_zh = data_zh.get(slug, place_en)

        print(f"Processing: {slug} - {place_en}")
        lat, lng, cca2 = get_location_details(slug)

        full_data[slug] = {
            "place": place_en,
            "place_zh": place_zh,
            "lat": lat,
            "lng": lng,
            "cca2": cca2,
        }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated {output_path} with {len(full_data)} entries.")


if __name__ == "__main__":
    en_input = "cloudflare-iata.json"
    zh_input = "cloudflare-iata-zh.json"
    # The single new output file
    output_full = "cloudflare-iata-full.json"

    print("--- Starting Geocoding for Combined Full Data File ---")
    generate_combined_full_data(en_input, zh_input, output_full)
