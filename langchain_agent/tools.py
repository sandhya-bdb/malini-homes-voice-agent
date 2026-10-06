import asyncio
from datetime import datetime

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from config import settings
from langchain_agent.rag import retrieve, build_context


# ---------------------------------------------------------------------------
# Shared singletons — initialized once at import time
# ---------------------------------------------------------------------------

embedder = SentenceTransformer(settings.embedding_model)
qdrant = QdrantClient(path=settings.qdrant_path)

try:
    _count = qdrant.get_collection(settings.collection_name).points_count
    print(f"[OK] Connected to '{settings.collection_name}' — {_count} points", flush=True)
except Exception:
    print(f"[NOTE] Collection '{settings.collection_name}' not yet found. Run `python ingest.py` to index docs.", flush=True)


# ---------------------------------------------------------------------------
# Malini Homes Properties & Room Catalog
# ---------------------------------------------------------------------------

MOCK_PROPERTIES_DB = {
    "silpukhuri": {
        "name": "Malini Homes - Silpukhuri (Unit 1)",
        "unit": "Unit 1, 2nd Floor",
        "address": "House no. 10, Nirupama Bhawan, Krishna Nagar, Pension Para Road, Goswami Service, Silpukhuri, Guwahati",
        "contact": "+91 8011110315",
        "location_type": "Central City Hub",
        "full_unit_rate": 3500,
        "max_guests": 7,
        "rooms": {
            "Full Unit (2BHK)": {
                "price": 3500,
                "capacity": "Up to 6 guests (₹4,000 for 7 guests)",
                "description": "Entire 2BHK flat with 2 bedrooms, 2 attached bathrooms, living room, full kitchen, and city-view balcony."
            },
            "Hummingbird Magic Room": {
                "price": 1800,
                "capacity": "1 to 2 guests",
                "description": "Private deluxe room with king bed, attached bathroom, private city balcony, AC, and Smart TV."
            },
            "Butterfly Effect Room": {
                "price": 1800,
                "capacity": "1 to 2 guests",
                "description": "Artistic bohemian style room with attached bathroom, private balcony, AC, and high-speed Wi-Fi."
            }
        },
        "amenities": [
            "High-Speed Wi-Fi", "Air Conditioning", "Washing Machine / Laundry",
            "Daily Housekeeping", "City View Balcony", "Smart TVs", "Full Kitchen Access", "24/7 Security"
        ],
        "highlights": "Walking distance to Goswami Service, 3.5 km from Guwahati Railway Station, great local cafes."
    },
    "zooroad": {
        "name": "Malini Homes - Zoo Road (Unit 2)",
        "unit": "Unit 2, 1st Floor",
        "address": "House no. 5, Panchali Apartment, Padma Path, By Lane 8, Zoo Road Tiniali, Guwahati",
        "contact": "+91 8011110315",
        "location_type": "Upscale Urban Corridor",
        "full_unit_rate": 3500,
        "max_guests": 7,
        "rooms": {
            "Serene Dwell (Full 2BHK)": {
                "price": 3500,
                "capacity": "Up to 6 guests (₹4,000 for 7 guests)",
                "description": "Full 2BHK unit with 2 full bedrooms, 3 beds, 2 bathrooms, spacious lounge, and fully equipped kitchen."
            },
            "Serene Deluxe Room": {
                "price": 1800,
                "capacity": "1 to 2 guests",
                "description": "Attached bathroom, AC, wardrobe, work desk, and shared living room access."
            },
            "Serene Delight Room": {
                "price": 1800,
                "capacity": "1 to 2 guests",
                "description": "Comfortable bedroom, attached bathroom, silent cooling AC, and modern decor."
            }
        },
        "amenities": [
            "High-Speed Wi-Fi", "Air Conditioning", "Fully Furnished",
            "Daily Housekeeping", "24/7 Security", "Flexible Check-in"
        ],
        "highlights": "Located in upscale Zoo Road, minutes away from the State Zoo, shopping malls, and premium restaurants."
    },
    "bhangagarh": {
        "name": "Malini Homes - Bhangagarh (Unit 3)",
        "unit": "Unit 3 (Healing Sanctuary & Food/Lodging)",
        "address": "House no. 4, Sewali Path, Bhangagarh Tiniali, Guwahati",
        "contact": "+91 8011110315",
        "location_type": "Medical & Hospital Hub",
        "rooms": {
            "Premium Room (with Kitchen)": {
                "price": 1500,
                "capacity": "2 guests (₹1,800 for 3 guests)",
                "description": "Attached private kitchenette, ideal for long recovery stays, AC, attached bath."
            },
            "Executive Triple Room": {
                "price": 1600,
                "capacity": "Up to 3 guests",
                "description": "Spacious triple bedding setup with attached bathroom, TV, AC, perfect for families and caregivers."
            },
            "Deluxe Room": {
                "price": 1400,
                "capacity": "1 to 2 guests",
                "description": "Comfortable room with double bed, attached private bath, and air conditioning."
            },
            "Budget Room": {
                "price": 1000,
                "capacity": "1 to 2 guests",
                "description": "Affordable room with essential amenities, attached bathroom, and Wi-Fi."
            }
        },
        "amenities": [
            "High-Speed Wi-Fi", "Air Conditioning", "Home-Cooked Assamese Meals Available",
            "Attached Bathrooms & TV", "Secure Parking", "Pet-Friendly"
        ],
        "highlights": "Immediate access to GMCH, Nemcare, Dr. B. Barooah Cancer Institute, and Apollo Hospitals. Nourishing home-cooked meals."
    }
}


# ---------------------------------------------------------------------------
# LangChain tools for Malini Voice
# ---------------------------------------------------------------------------

@tool
def search_homestay_info(query: str) -> str:
    """Search Malini Homes documentation for property details, tariffs, amenities,
    check-in policies, house rules, nearby hospitals, or Guwahati tourist attractions.
    Use this whenever the guest asks questions about Malini Homes or visiting Guwahati."""
    try:
        chunks = retrieve(qdrant, embedder, query, top_k=4)
        if not chunks:
            return "No relevant information found in the Malini Homes knowledge base."
        return build_context(chunks)
    except Exception as e:
        return f"Unable to query knowledge base: {e}"


@tool
def check_property_availability(property_name: str, guests: int = 2) -> str:
    """Check accommodation options and capacity for a given Malini Homes property.
    Supported properties: 'silpukhuri', 'zoo road', or 'bhangagarh'."""
    key = property_name.lower().replace(" ", "").replace("-", "")

    matched_key = None
    for k in MOCK_PROPERTIES_DB:
        if k in key or key in k:
            matched_key = k
            break

    if not matched_key:
        return (
            "We have three properties in Guwahati: Silpukhuri (Unit 1), Zoo Road (Unit 2), "
            "and Bhangagarh (Unit 3). Which location are you interested in?"
        )

    prop = MOCK_PROPERTIES_DB[matched_key]
    room_list = []
    for rname, rinfo in prop["rooms"].items():
        price = rinfo.get("price") or rinfo.get("price_2_guests", 1500)
        room_list.append(f"{rname} (₹{price}/night, {rinfo['capacity']})")

    rooms_str = "; ".join(room_list)
    return (
        f"{prop['name']} has availability for {guests} guest(s). "
        f"Available options: {rooms_str}. "
        f"Address: {prop['address']}."
    )


@tool
def calculate_stay_quote(property_name: str, room_type: str = "full", nights: int = 1, guests: int = 2) -> str:
    """Calculate the estimated stay cost in Indian Rupees (₹) based on property, room type,
    number of nights, and number of guests.
    Property: 'silpukhuri', 'zooroad', or 'bhangagarh'.
    Nights: Number of nights (default 1).
    Guests: Number of guests (default 2)."""
    key = property_name.lower().replace(" ", "").replace("-", "")

    matched_key = None
    for k in MOCK_PROPERTIES_DB:
        if k in key or key in k:
            matched_key = k
            break

    if not matched_key:
        return "Please specify if you want a quote for Silpukhuri, Zoo Road, or Bhangagarh."

    prop = MOCK_PROPERTIES_DB[matched_key]

    # Calculate rate per night
    rate_per_night = 0
    room_desc = "Selected Room"

    if matched_key in ["silpukhuri", "zooroad"]:
        if "room" in room_type.lower() or "private" in room_type.lower() or "deluxe" in room_type.lower():
            rate_per_night = 1800
            room_desc = "Private Deluxe Room"
        else:
            if guests >= 7:
                rate_per_night = 4000
                room_desc = "Full 2BHK Apartment (7 guests)"
            else:
                rate_per_night = 3500
                room_desc = "Full 2BHK Apartment (up to 6 guests)"
    else:  # bhangagarh
        if "kitchen" in room_type.lower() or "premium" in room_type.lower():
            rate_per_night = 1800 if guests >= 3 else 1500
            room_desc = "Premium Room with Attached Kitchen"
        elif "triple" in room_type.lower() or "executive" in room_type.lower():
            rate_per_night = 1600
            room_desc = "Executive Triple Room"
        elif "budget" in room_type.lower():
            rate_per_night = 1000
            room_desc = "Budget Room"
        else:
            rate_per_night = 1400
            room_desc = "Deluxe Room"

    total = rate_per_night * max(1, nights)
    return (
        f"For {prop['name']}, {room_desc} for {nights} night(s) and {guests} guest(s): "
        f"The rate is ₹{rate_per_night} per night, totaling ₹{total:,}."
    )


@tool
def get_property_details(property_name: str) -> str:
    """Get location address, key amenities, and contact information for a Malini Homes property.
    Property: 'silpukhuri', 'zooroad', or 'bhangagarh'."""
    key = property_name.lower().replace(" ", "").replace("-", "")

    matched_key = None
    for k in MOCK_PROPERTIES_DB:
        if k in key or key in k:
            matched_key = k
            break

    if not matched_key:
        return "Available properties are Silpukhuri (Unit 1), Zoo Road (Unit 2), and Bhangagarh (Unit 3)."

    prop = MOCK_PROPERTIES_DB[matched_key]
    amenities = ", ".join(prop["amenities"][:5])
    return (
        f"{prop['name']}: Located at {prop['address']}. "
        f"Key amenities include: {amenities}. "
        f"Highlights: {prop['highlights']} "
        f"Official Contact: {prop['contact']}."
    )


@tool
def create_booking_inquiry(guest_name: str, phone_number: str, property_name: str, details_or_dates: str) -> str:
    """Create a reservation or inquiry ticket when a guest wants to book or connect with the host.
    Requires guest name, 10-digit Indian phone number, preferred property, and dates/details."""
    phone_clean = phone_number.strip().replace("+91", "").replace("-", "").replace(" ", "")

    ticket_id = "MALINI-" + str(abs(hash(phone_clean + guest_name + datetime.now().isoformat())) % 100000).zfill(5)
    timestamp = datetime.now().isoformat()

    print(f"[BOOKING INQUIRY] ID={ticket_id} time={timestamp} guest={guest_name} phone={phone_clean} prop={property_name} notes={details_or_dates}")

    return (
        f"Thank you, {guest_name}! I have registered your booking inquiry with reference ID {ticket_id} "
        f"for {property_name}. Our host team will connect with you via WhatsApp or call on {phone_clean} shortly."
    )


@tool
def escalate_to_host(reason: str) -> str:
    """Escalate to a human host representative for custom requests, long-term medical stay discounts,
    group bookings, or urgent assistance."""
    ticket_id = "MALINI-" + str(abs(hash(reason)) % 100000).zfill(5)
    timestamp = datetime.now().isoformat()

    print(f"[ESCALATION] ID={ticket_id} time={timestamp} reason={reason!r}")

    return (
        f"I've logged request {ticket_id} for our host team. "
        f"A representative will reach out to you within 30 minutes. "
        f"Your reference number is {ticket_id}."
    )


# ---------------------------------------------------------------------------
# System Prompt for Malini Voice
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "You are Malini Voice, the friendly and gracious voice assistant for Malini Homes — "
    "a brand of premium, government-registered homestays in Guwahati, Assam.\n"
    "\n"
    "ABOUT MALINI HOMES:\n"
    "- Unit 1: Silpukhuri (Central city hub, artistic bohemian rooms, Hummingbird & Butterfly rooms or full 2BHK).\n"
    "- Unit 2: Zoo Road (Upscale urban retreat near dining/shopping, Serene Deluxe, Serene Delight or full 2BHK).\n"
    "- Unit 3: Bhangagarh (Healing sanctuary near GMCH, Apollo & top hospitals, in-house Assamese meals, pet-friendly).\n"
    "- Contact: +91 8011110315 | Website: malinihomes.netlify.app\n"
    "\n"
    "GUIDELINES:\n"
    "- Use search_homestay_info for questions about house rules, check-in (1 PM), check-out (11 AM), ID requirements, nearby temples (Kamakhya), Brahmaputra cruises, and amenities.\n"
    "- Use check_property_availability when guests ask which property or room is available.\n"
    "- Use calculate_stay_quote to give clear price breakdowns in Indian Rupees (₹).\n"
    "- Use get_property_details for addresses, landmarks, and contact numbers.\n"
    "- Use create_booking_inquiry when a guest wants to book or leave their contact details.\n"
    "- Use escalate_to_host for special medical discounts, long stays, or urgent host support.\n"
    "\n"
    "VOICE TONE & CONSTRAINTS:\n"
    "- Speak with the legendary warmth of Assamese hospitality ('Atithi Devo Bhava').\n"
    "- Keep answers BRIEF and CONVERSATIONAL for voice calls (1 to 2 sentences per turn).\n"
    "- Always quote prices with ₹ symbol.\n"
    "- Never invent policies or rates. If unsure, offer to connect them with the host.\n"
    "- Do not respond with bullet lists, tables, or markdown diagrams — speak naturally as in a phone call."
)


# ---------------------------------------------------------------------------
# Build the LangChain agent graph
# ---------------------------------------------------------------------------

ALL_TOOLS = [
    search_homestay_info,
    check_property_availability,
    calculate_stay_quote,
    get_property_details,
    create_booking_inquiry,
    escalate_to_host,
]

llm = ChatGroq(model=settings.groq_model, temperature=0.0)

malini_agent = create_agent(model=llm, tools=ALL_TOOLS, system_prompt=SYSTEM_PROMPT)


