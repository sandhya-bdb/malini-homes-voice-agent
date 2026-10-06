"""
Script to generate 3 official knowledge base PDFs for Malini Homes Voice Agent:
1. docs/malini-properties-and-pricing.pdf
2. docs/malini-booking-policies-and-faq.pdf
3. docs/malini-guwahati-guide-and-experiences.pdf
"""

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

DOCS_DIR = Path("docs")
DOCS_DIR.mkdir(exist_ok=True)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "DocTitle",
    parent=styles["Heading1"],
    fontSize=22,
    leading=26,
    textColor=colors.HexColor("#1e3a8a"),
    spaceAfter=6,
)

subtitle_style = ParagraphStyle(
    "DocSubTitle",
    parent=styles["Normal"],
    fontSize=11,
    leading=14,
    textColor=colors.HexColor("#4b5563"),
    spaceAfter=15,
)

h1_style = ParagraphStyle(
    "SectionH1",
    parent=styles["Heading2"],
    fontSize=15,
    leading=19,
    textColor=colors.HexColor("#1e40af"),
    spaceBefore=14,
    spaceAfter=6,
    keepWithNext=True,
)

h2_style = ParagraphStyle(
    "SectionH2",
    parent=styles["Heading3"],
    fontSize=12,
    leading=16,
    textColor=colors.HexColor("#0f766e"),
    spaceBefore=8,
    spaceAfter=4,
    keepWithNext=True,
)

body_style = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontSize=10,
    leading=14,
    textColor=colors.HexColor("#1f2937"),
    spaceAfter=6,
)

bullet_style = ParagraphStyle(
    "BulletText",
    parent=styles["Normal"],
    fontSize=9.5,
    leading=13.5,
    textColor=colors.HexColor("#374151"),
    leftIndent=15,
    spaceAfter=3,
)

table_header_style = ParagraphStyle(
    "TableHeader",
    parent=styles["Normal"],
    fontSize=9.5,
    leading=12,
    textColor=colors.white,
    fontName="Helvetica-Bold",
)

table_cell_style = ParagraphStyle(
    "TableCell",
    parent=styles["Normal"],
    fontSize=9,
    leading=12,
    textColor=colors.HexColor("#1f2937"),
)


def create_properties_pdf():
    pdf_path = DOCS_DIR / "malini-properties-and-pricing.pdf"
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40
    )
    story = []

    # Title
    story.append(Paragraph("Malini Homes — Properties, Room Categories & Tariff Guide", title_style))
    story.append(Paragraph("Official Directory & Tariff Sheet | Guwahati, Assam | Contact: +91 8011110315", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=12))

    # Overview
    story.append(Paragraph("About Malini Homes", h1_style))
    story.append(Paragraph(
        "Malini Homes offers curated premium homestays in Guwahati, blending the legendary warmth of "
        "Assamese hospitality ('Atithi Devo Bhava') with modern luxury, complete safety, and prime urban locations. "
        "Designed for families, corporate professionals, couples, and medical travelers.",
        body_style
    ))

    # Unit 1
    story.append(Paragraph("Unit 1: Malini Homes — Silpukhuri (Central City Hub)", h1_style))
    story.append(Paragraph(
        "<b>Address:</b> Unit 1, Second Floor, House No. 10, Nirupama Bhawan, Krishna Nagar, Pension Para Road, Goswami Service, Silpukhuri, Guwahati.<br/>"
        "<b>Description:</b> Centrally located in the heart of Guwahati, Silpukhuri Unit 1 is an artistic, cozy haven. "
        "It features two deluxe private rooms with dedicated balconies and attached bathrooms, plus access to a shared living lounge and full kitchen.",
        body_style
    ))
    story.append(Paragraph("Available Accommodation & Pricing:", h2_style))

    data_u1 = [
        [Paragraph("Category / Option", table_header_style), Paragraph("Capacity", table_header_style), Paragraph("Rate per Night", table_header_style), Paragraph("Key Features", table_header_style)],
        [Paragraph("Full Unit (Entire 2BHK)", table_cell_style), Paragraph("Up to 6 Guests", table_cell_style), Paragraph("₹3,500 / night<br/>(₹4,000 for 7 guests)", table_cell_style), Paragraph("Complete privacy, 2 bedrooms, 2 attached baths, full kitchen, living room, private balconies.", table_cell_style)],
        [Paragraph("Hummingbird Magic Room", table_cell_style), Paragraph("1-2 Guests", table_cell_style), Paragraph("₹1,800 / night", table_cell_style), Paragraph("Private deluxe room, king bed, attached bathroom, private city-view balcony, AC, Smart TV.", table_cell_style)],
        [Paragraph("Butterfly Effect Room", table_cell_style), Paragraph("1-2 Guests", table_cell_style), Paragraph("₹1,800 / night", table_cell_style), Paragraph("Artistic bohemian ambiance, attached private bath, private balcony, AC, high-speed WiFi.", table_cell_style)],
    ]
    t1 = Table(data_u1, colWidths=[130, 85, 120, 195])
    t1.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t1)
    story.append(Spacer(1, 10))

    # Unit 2
    story.append(Paragraph("Unit 2: Malini Homes — Zoo Road (Upscale Retreat)", h1_style))
    story.append(Paragraph(
        "<b>Address:</b> First Floor, House No. 5, Panchali Apartment, Padma Path, By-Lane 8, Zoo Road Tiniali, Guwahati.<br/>"
        "<b>Description:</b> Located in Guwahati's vibrant and upscale commercial corridor, close to premier cafes, dining, and shopping. "
        "Provides total privacy and luxury for larger family groups and business executives.",
        body_style
    ))
    story.append(Paragraph("Available Accommodation & Pricing:", h2_style))

    data_u2 = [
        [Paragraph("Category / Option", table_header_style), Paragraph("Capacity", table_header_style), Paragraph("Rate per Night", table_header_style), Paragraph("Key Features", table_header_style)],
        [Paragraph("Serene Dwell (Full 2BHK)", table_cell_style), Paragraph("Up to 6 Guests", table_cell_style), Paragraph("₹3,500 / night<br/>(₹4,000 for 7 guests)", table_cell_style), Paragraph("2 full bedrooms, 3 comfortable beds, 2 bathrooms, spacious living hall, fully equipped modular kitchen.", table_cell_style)],
        [Paragraph("Serene Deluxe Room", table_cell_style), Paragraph("1-2 Guests", table_cell_style), Paragraph("₹1,800 / night", table_cell_style), Paragraph("Attached private bathroom, air-conditioned, high-speed WiFi, wardrobe, shared lounge access.", table_cell_style)],
        [Paragraph("Serene Delight Room", table_cell_style), Paragraph("1-2 Guests", table_cell_style), Paragraph("₹1,800 / night", table_cell_style), Paragraph("Cozy premium bedroom, queen/twin bedding, attached bath, silent cooling AC, work desk.", table_cell_style)],
    ]
    t2 = Table(data_u2, colWidths=[130, 85, 120, 195])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f766e")),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0fdfa")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t2)
    story.append(Spacer(1, 10))

    # Unit 3
    story.append(Paragraph("Unit 3: Malini Homes — Bhangagarh (Healing Sanctuary & Food/Lodging)", h1_style))
    story.append(Paragraph(
        "<b>Address:</b> House No. 4, Sewali Path, Bhangagarh Tiniali, Guwahati.<br/>"
        "<b>Description:</b> Thoughtfully positioned in the primary medical and institutional district of Guwahati. "
        "Just 3 to 10 minutes from GMCH, Nemcare, Dr. B. Barooah Cancer Institute, Apollo, Down Town, and Excelcare Hospitals. "
        "Features home-cooked nourishing meals, elevator/easy accessibility, in-house kitchen, and is <b>pet-friendly</b>.",
        body_style
    ))
    story.append(Paragraph("Available Accommodation & Pricing:", h2_style))

    data_u3 = [
        [Paragraph("Category / Option", table_header_style), Paragraph("Capacity", table_header_style), Paragraph("Rate per Night", table_header_style), Paragraph("Key Features", table_header_style)],
        [Paragraph("Premium Room (with Kitchen)", table_cell_style), Paragraph("2-3 Guests", table_cell_style), Paragraph("₹1,500 (2 guests)<br/>₹1,800 (3 guests)", table_cell_style), Paragraph("Attached private kitchenette, ideal for long recovery stays, AC, attached bath.", table_cell_style)],
        [Paragraph("Executive Triple Room", table_cell_style), Paragraph("Up to 3 Guests", table_cell_style), Paragraph("₹1,600 / night", table_cell_style), Paragraph("3 beds, attached bathroom, TV, AC, spacious setup for patient caregivers and families.", table_cell_style)],
        [Paragraph("Deluxe Room", table_cell_style), Paragraph("1-2 Guests", table_cell_style), Paragraph("₹1,400 / night", table_cell_style), Paragraph("Comfortable double bed, AC, attached private bathroom, peaceful ambient lighting.", table_cell_style)],
        [Paragraph("Budget Room", table_cell_style), Paragraph("1-2 Guests", table_cell_style), Paragraph("₹1,000 / night", table_cell_style), Paragraph("Economical option with essential comforts, attached bath, fan/cooling, WiFi.", table_cell_style)],
    ]
    t3 = Table(data_u3, colWidths=[130, 85, 120, 195])
    t3.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7c2d12")),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fef2f2")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t3)
    story.append(Spacer(1, 12))

    # Common Amenities
    story.append(Paragraph("Standard Amenities Across All Units", h1_style))
    amenities = [
        "High-Speed Fiber Optical Wi-Fi (complimentary throughout)",
        "Air Conditioning and heating/geyser in all primary rooms",
        "Daily housekeeping and fresh linen change",
        "Washing machine & laundry facilities",
        "Fully equipped kitchenettes (cookware, gas/induction, refrigerator, microwave, RO water filter)",
        "24/7 Security personnel, smart digital door locks, and CCTV surveillance in exterior & common areas",
        "Power backup / inverter for uninterrupted comfort",
        "Dedicated workspace and dining areas",
    ]
    for a in amenities:
        story.append(Paragraph(f"• {a}", bullet_style))

    doc.build(story)
    print(f"[OK] Generated {pdf_path}")


def create_policies_pdf():
    pdf_path = DOCS_DIR / "malini-booking-policies-and-faq.pdf"
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40
    )
    story = []

    story.append(Paragraph("Malini Homes — Booking Rules, Compliance & Guest FAQ", title_style))
    story.append(Paragraph("Official Guest Policies & Terms of Stay | Malini Homes Guwahati", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=12))

    story.append(Paragraph("Check-In and Check-Out Timings", h1_style))
    story.append(Paragraph("• <b>Standard Check-In Time:</b> 1:00 PM onwards.", bullet_style))
    story.append(Paragraph("• <b>Standard Check-Out Time:</b> 11:00 AM.", bullet_style))
    story.append(Paragraph("• <b>Early Check-In / Late Check-Out:</b> Subject to room availability and prior coordination with our host team. Luggage storage is available free of charge if you arrive early.", bullet_style))

    story.append(Paragraph("Statutory Registrations & Trust Infrastructure", h1_style))
    story.append(Paragraph(
        "Malini Homes operates under full statutory compliance with Assam Tourism and Government of India regulations:",
        body_style
    ))
    story.append(Paragraph("• <b>The Indian Sarais Act, 1867:</b> Registered compliance with historic hospitality security protocols.", bullet_style))
    story.append(Paragraph("• <b>Assam Tourism Registration:</b> Formally accredited homestay accommodation provider.", bullet_style))
    story.append(Paragraph("• <b>MSME Registered:</b> Recognized Ministry of Micro, Small & Medium Enterprises hospitality enterprise.", bullet_style))
    story.append(Paragraph("• <b>Fire Safety Compliance:</b> Fire safety equipment and smoke detection installed and serviced.", bullet_style))
    story.append(Paragraph("• <b>24/7 Security:</b> On-site caretakers, security guards, and CCTV surveillance of public areas.", bullet_style))

    story.append(Paragraph("Mandatory Guest Identification Rules", h1_style))
    story.append(Paragraph(
        "In accordance with local regulations, all adult guests must present a valid government-issued photo ID at or prior to check-in "
        "(Aadhaar Card, Passport, Voter ID, or Driving License). PAN cards are not accepted as valid address proof. "
        "Foreign nationals must provide a valid passport, visa, and complete Form C registration.",
        body_style
    ))

    story.append(Paragraph("House Rules & Stay Etiquette", h1_style))
    story.append(Paragraph("• <b>Parties & Events:</b> Strictly prohibited. Loud music and rowdy gatherings are not permitted.", bullet_style))
    story.append(Paragraph("• <b>Quiet Hours:</b> 10:00 PM to 7:00 AM to preserve serenity for all residential neighbors and guests.", bullet_style))
    story.append(Paragraph("• <b>Smoking Policy:</b> Smoking inside bedrooms and living halls is strictly banned. Guests may smoke only in designated open balconies or exterior terraces.", bullet_style))
    story.append(Paragraph("• <b>Pets:</b> Pets are warmly welcomed at our <b>Bhangagarh (Unit 3)</b> property. Prior notice is required. Not permitted at Silpukhuri or Zoo Road units.", bullet_style))
    story.append(Paragraph("• <b>Visitors:</b> Outside visitors are permitted in common areas until 8:00 PM. Overnight stay is allowed only for registered guests with ID on file.", bullet_style))

    story.append(Paragraph("Food & Dining Services", h1_style))
    story.append(Paragraph(
        "• <b>Self-Catering Kitchens:</b> All units (or attached kitchenettes) feature cookware, stove, microwave, and refrigerator for self-cooking.<br/>"
        "• <b>Home-Cooked Assamese Meals (Bhangagarh Unit):</b> Available upon request! Savor healthy, freshly prepared vegetarian and non-vegetarian Assamese thalis, khichdi, and customized patient-diet meals.<br/>"
        "• <b>Food Delivery:</b> Swiggy and Zomato deliver directly to all three locations with fast turnaround.",
        body_style
    ))

    story.append(Paragraph("Reservation, Payment & Cancellation", h1_style))
    story.append(Paragraph("• <b>Instant Reservation:</b> Direct booking via WhatsApp (+91 8011110315) or online payment gateway.", bullet_style))
    story.append(Paragraph("• <b>Advance Deposit:</b> 50% advance required to lock dates; balance payable at check-in.", bullet_style))
    story.append(Paragraph("• <b>Cancellation Terms:</b> 100% refund for cancellations made 48 hours prior to check-in date. 50% refund within 24-48 hours. Non-refundable for same-day cancellations.", bullet_style))

    doc.build(story)
    print(f"[OK] Generated {pdf_path}")


def create_guwahati_guide_pdf():
    pdf_path = DOCS_DIR / "malini-guwahati-guide-and-experiences.pdf"
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40
    )
    story = []

    story.append(Paragraph("Malini Homes — Guwahati City & Travel Experience Guide", title_style))
    story.append(Paragraph("Curated Travel Insights, Transit Distances & Local Attractions | Malini Homes", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=12))

    story.append(Paragraph("Welcome to the Gateway of Northeast India", h1_style))
    story.append(Paragraph(
        "Guwahati is a mesmerizing tapestry of sacred traditions, the majestic Brahmaputra River, lush wildlife, "
        "and rich Assamese heritage. Staying at Malini Homes places you at the center of the best cultural, culinary, "
        "and spiritual destinations.",
        body_style
    ))

    story.append(Paragraph("Key Attractions & Proximity from Malini Homes", h1_style))

    guide_data = [
        [Paragraph("Destination", table_header_style), Paragraph("Distance / Travel Time", table_header_style), Paragraph("Highlights & Experience", table_header_style)],
        [Paragraph("Maa Kamakhya Temple<br/>(Nilachal Hill)", table_cell_style), Paragraph("8 - 10 km<br/>(25 - 35 mins)", table_cell_style), Paragraph("One of the 51 Shakti Peethas in India. Best visited early morning. Direct cabs easily available from all Malini Homes units.", table_cell_style)],
        [Paragraph("Brahmaputra River Cruise & Ropeway", table_cell_style), Paragraph("3 - 5 km<br/>(10 - 15 mins from Silpukhuri)", table_cell_style), Paragraph("Take an evening sunset dinner cruise (Alfresco Grand). Ride India's longest river ropeway offering sweeping 360-degree aerial views.", table_cell_style)],
        [Paragraph("Umananda Temple<br/>(Peacock Island)", table_cell_style), Paragraph("4 km to ferry ghat<br/>(15 mins)", table_cell_style), Paragraph("Historic 17th-century Shiva temple perched on the smallest inhabited river island in the world.", table_cell_style)],
        [Paragraph("Assam State Zoo & Botanical Garden", table_cell_style), Paragraph("1.5 km<br/>(5 mins from Zoo Road unit)", table_cell_style), Paragraph("Sprawling wildlife reserve home to Greater One-Horned Rhinoceros, Royal Bengal Tigers, and rare birds.", table_cell_style)],
        [Paragraph("Srimanta Sankaradeva Kalakshetra", table_cell_style), Paragraph("6 - 8 km<br/>(20 mins)", table_cell_style), Paragraph("Grand cultural institution displaying Assamese ethnic museums, open-air theaters, traditional dance, and art galleries.", table_cell_style)],
        [Paragraph("Sualkuchi<br/>(Manchester of the East)", table_cell_style), Paragraph("32 km<br/>(50 mins)", table_cell_style), Paragraph("World-renowned artisanal weaving village crafting indigenous golden Muga, white Pat, and Eri silk.", table_cell_style)],
        [Paragraph("Pobitora Wildlife Sanctuary", table_cell_style), Paragraph("45 km<br/>(1 hr 15 mins)", table_cell_style), Paragraph("Highest density of Indian One-Horned Rhinoceros in the world. Ideal day excursion for jungle safari.", table_cell_style)],
    ]
    gt = Table(guide_data, colWidths=[140, 110, 280])
    gt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(gt)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Transit & Transportation Hubs", h1_style))
    story.append(Paragraph("• <b>Guwahati Railway Station (Paltan Bazar):</b> 3.5 km from Silpukhuri (10 mins), 5.5 km from Zoo Road, 4 km from Bhangagarh.", bullet_style))
    story.append(Paragraph("• <b>Lokpriya Gopinath Bordoloi International Airport (GAU):</b> ~23 km (45-55 mins via NH27 bypass). Airport cab drop and pickup can be arranged upon request.", bullet_style))
    story.append(Paragraph("• <b>Inter-State Bus Terminal (ISBT):</b> 11 km via G.S. Road bypass.", bullet_style))

    story.append(Paragraph("Dining & Shopping Recommendations Near Malini Homes", h1_style))
    story.append(Paragraph("• <b>Authentic Assamese Cuisine:</b> Paradise Restaurant (Silpukhuri), Khorikaa (G.S. Road), and Michinga for ethnic tribal flavors.", bullet_style))
    story.append(Paragraph("• <b>Shopping & Souvenirs:</b> Jagaran (Assam Govt Emporium), Pragjyotika Silk, and Fancy Bazaar for street shopping and local tea.", bullet_style))
    story.append(Paragraph("• <b>Medical Assistance (Bhangagarh Unit):</b> Walking distance to pharmacies, GMCH, Apollo Clinics, and 24/7 emergency diagnostic centers.", bullet_style))

    doc.build(story)
    print(f"[OK] Generated {pdf_path}")


if __name__ == "__main__":
    create_properties_pdf()
    create_policies_pdf()
    create_guwahati_guide_pdf()
    print("All 3 Malini Homes PDF documents generated successfully!")
