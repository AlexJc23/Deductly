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

class IncomeType(str, Enum):
    GIG_PLATFORM = "gig_platform"
    BUSINESS = "business"
    EMPLOYMENT = "employment"
    PASSIVE = "passive"
    OTHER = "other"

class ExpenseCategory(str, Enum):
    FOOD = "food"                 # meals, snacks while working
    TRANSPORT = "transport"       # gas, rideshare, parking
    VEHICLE = "vehicle"           # maintenance, repairs
    SUPPLIES = "supplies"         # office, tools, materials
    SOFTWARE = "software"         # subscriptions, SaaS
    PHONE = "phone"               # phone bills
    INTERNET = "internet"         # internet bills
    MARKETING = "marketing"       # ads, promos
    EDUCATION = "education"       # courses, books
    RENT = "rent"                 # workspace (if applicable)
    UTILITIES = "utilities"       # electricity, etc
    OTHER = "other"               # catch-all (you will need it)
