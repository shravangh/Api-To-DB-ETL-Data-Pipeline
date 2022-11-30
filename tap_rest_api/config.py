BASE_URL = "https://api.sunrise-sunset.org/json"
SOURCE_LATITUDE = "18.5204"
SOURCE_LONGITUDE = "73.8567"

SCHEMA = {"properties": {
                        "sunrise": {"type": "string"},
                        "sunset": {"type": "string"},
                        "timestamp": {"type": "string"},
                        },
        }

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
}
