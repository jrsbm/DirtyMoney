import os

def create_role_card(card_type, bg_color, accent_color, role_title, role_description):
    # Standard Card Size: 2.5 x 3.5 inches (225 x 315 px at 90dpi)
    # Role card with person silhouette
    svg_template = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg 
    width="2.5in" 
    height="3.5in" 
    viewBox="0 0 225 315"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:cc="http://creativecommons.org/ns#"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:svg="http://www.w3.org/2000/svg"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape">
    
    <metadata>
        <rdf:RDF><cc:Work rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage" /><dc:title>Dirty Money - {role_title}</dc:title></cc:Work></rdf:RDF>
    </metadata>

    <!-- Card base -->
    <rect x="0" y="0" width="225" height="315" rx="8" fill="{bg_color}" />
    <rect x="1" y="1" width="223" height="313" rx="7" fill="none" stroke="{accent_color}" stroke-width="0.8" opacity="0.3"/>
    
    <!-- Top decorative line -->
    <line x1="20" y1="15" x2="205" y2="15" stroke="{accent_color}" stroke-width="1" opacity="0.6" />
    
    <!-- Header -->
    <text x="112.5" y="32" font-family="Georgia, serif" font-size="11" font-weight="bold" fill="{accent_color}" text-anchor="middle" letter-spacing="1">DIRTY MONEY</text>
    <text x="112.5" y="42" font-family="Courier New, monospace" font-size="7" fill="{accent_color}" text-anchor="middle" opacity="0.6">CONFIDENTIAL</text>
    
    <!-- Divider -->
    <line x1="30" y1="50" x2="195" y2="50" stroke="{accent_color}" stroke-width="0.5" opacity="0.4" />
    
    <!-- Person Silhouette - Head and shoulders -->
    <g transform="translate(112.5, 130)">
        <!-- Head circle -->
        <circle cx="0" cy="-25" r="22" fill="none" stroke="{accent_color}" stroke-width="1.2" opacity="0.7"/>
        
        <!-- Shoulders/Body -->
        <path d="M -35 25 Q -35 5 -20 0 Q 0 -5 20 0 Q 35 5 35 25" 
              fill="none" stroke="{accent_color}" stroke-width="1" opacity="0.6"/>
        
        <!-- Collar detail -->
        <path d="M -15 5 Q 0 12 15 5" fill="none" stroke="{accent_color}" stroke-width="0.8" opacity="0.5"/>
    </g>
    
    <!-- Role Title -->
    <text x="112.5" y="175" font-family="Georgia, serif" font-size="14" font-weight="bold" fill="{accent_color}" text-anchor="middle" letter-spacing="0.5">{role_title}</text>
    
    <!-- Decorative line -->
    <line x1="60" y1="182" x2="165" y2="182" stroke="{accent_color}" stroke-width="0.8" opacity="0.4" />
    
    <!-- Role description -->
    <text x="112.5" y="195" font-family="Arial, sans-serif" font-size="7" fill="{accent_color}" text-anchor="middle" opacity="0.8">{role_description}</text>
    
    <!-- Team indicator -->
    <g transform="translate(112.5, 250)">
        <rect x="-60" y="-15" width="120" height="30" rx="3" fill="none" stroke="{accent_color}" stroke-width="0.8" opacity="0.5"/>
        <text x="0" y="4" font-family="Courier New, monospace" font-size="20" fill="{accent_color}" text-anchor="middle" font-weight="bold">
            {"AUTHENTIC" if card_type == "AUTHENTIC" else "FRAUDSTER" if card_type == "FRAUDSTER" else "FRAUDSTER"}
        </text>
    </g>
    
    <!-- Footer -->
    <text x="112.5" y="295" font-family="Courier New, monospace" font-size="5" fill="{accent_color}" text-anchor="middle" opacity="0.4">KEEP YOUR IDENTITY SECRET</text>
</svg>
"""
    filename = f"{card_type.lower()}_{role_title.replace(' ','_').lower()}_card.svg"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_template)
    print(f"Generated: {filename}")

create_role_card(
    "AUTHENTIC", 
    "#0a1520", 
    "#0070c4", 
    "CONTRACT ADMIN",
    "Negotiates fair, transparent contracts"
)

create_role_card(
    "AUTHENTIC", 
    "#0a1520", 
    "#0070c4", 
    "QA MANAGER",
    "Making sure every batch meets the standards"
)

create_role_card(
    "AUTHENTIC", 
    "#0a1520", 
    "#0070c4", 
    "PROCUREMENT SPEC.",
    "Sourcing authentic products and managing supplier relationships"
)

create_role_card(
    "AUTHENTIC", 
    "#0a1520", 
    "#0070c4", 
    "PURCHASING AGENT",
    "Evaluating suppliers and negotiating deals"
)

create_role_card(
    "AUTHENTIC", 
    "#0a1520", 
    "#0070c4", 
    "LOGISTICS MANAGER",
    "Coordinating secure transportation and storage"
)

create_role_card(
    "FRAUDSTER", 
    "#200a0a", 
    "#ba293b", 
    "DOCKWORKER",
    "Has some questionable connections in the port..."
)

create_role_card(
    "FRAUDSTER", 
    "#200a0a", 
    "#ba293b", 
    "PROCUREMENT SPEC.",
    "Drives a slightly too expensive car..."
)

create_role_card(
    "TRICKMEISTER", 
    "#200a0a",
    "#ba293b",
    "TRICK-MEISTER",
    "Master Manipulator"
)