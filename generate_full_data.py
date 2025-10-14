import json
import time
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# Initialize the geocoder
geolocator = Nominatim(user_agent="cloudflare_iata_geocoder/1.0")

def get_lat_lng(place, retries=3, delay=2):
    """
    Geocode a place name to get latitude and longitude, with retries on timeout.
    """
    if place == "LOCAL":
        return 0.0, 0.0

    try:
        location = geolocator.geocode(place)
        time.sleep(1)  # Respect the 1-second rate limit of Nominatim
        if location:
            return location.latitude, location.longitude
        else:
            print(f"Warning: Could not geocode '{place}'. Location not found.")
            return None, None
    except GeocoderTimedOut:
        print(f"Warning: Geocoding timed out for '{place}'. Retrying in {delay}s...")
        if retries > 0:
            time.sleep(delay)
            return get_lat_lng(place, retries - 1, delay * 2)
        else:
            print(f"Error: Failed to geocode '{place}' after multiple retries.")
            return None, None
    except GeocoderServiceError as e:
        print(f"Error: Geocoding service error for '{place}': {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred for '{place}': {e}")
        return None, None


def process_iata_file(input_path, output_path):
    """
    Reads an IATA JSON file, enriches it with latitude and longitude,
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

        if lat is not None and lng is not None:
            full_data.append({
                "slug": slug,
                "place": place,
                "lat": lat,
                "lng": lng
            })
        else:
            # Append even if geocoding fails to keep the entry
            full_data.append({
                "slug": slug,
                "place": place,
                "lat": None,
                "lng": None
            })

    # Sort the data by slug for consistency
    full_data.sort(key=lambda x: x['slug'])

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated {output_path} with {len(full_data)} entries.")


if __name__ == "__main__":
    # Process the English file
    process_iata_file(
        'cloudflare-iata.json',
        'cloudflare-iata-full.json'
    )

    # Process the Chinese file
    process_iata_file(
        'cloudflare-iata-zh.json',
        'cloudflare-iata-full-zh.json'
    )