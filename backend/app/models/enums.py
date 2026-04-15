from enum import Enum

class TripPlatform(str, Enum):
    UBER_EATS = "uber_eats"
    SPARK = "spark"
    DOORDASH = "doordash"
    LYFT = "lyft"
    UBER = "uber"
    GRUBHUB = "grubhub"
    INSTACART = "instacart"
    AMAZON_FLEX = "amazon_flex"
    SHIPT = "shipt"
    OTHER = "other"

class TripCategory(str, Enum):
    BUSINESS = "business"
    PERSONAL = "personal"
