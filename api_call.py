import http.client
import json
from ocr import extract_plates
import os


def get_vehicle_details(plate_number):
    conn = http.client.HTTPSConnection(
        "vehicle-rc-verification-advance.p.rapidapi.com")

    payload = json.dumps({
        "rcnumber": plate_number
    })

    headers = {
        'x-rapidapi-key': os.getenv("RAPIDAPI_KEY"),
        'x-rapidapi-host': "vehicle-rc-verification-advance.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    conn.request("POST", "/Getrcfulldetails", payload, headers)
    res = conn.getresponse()
    data = res.read()

    try:
        return json.loads(data.decode("utf-8"))
    except json.JSONDecodeError:
        return {"error": "Invalid response from API", "raw": data.decode("utf-8")}


if __name__ == "__main__":
    print("Fetching vehicle details from API...")
    plates = extract_plates()

    if not plates:
        print("No valid plates detected.")
    else:
        for plate in plates:
            print(f"\n[INFO] Checking plate: {plate}")
            result = get_vehicle_details(plate)
            print(json.dumps(result, indent=2))
