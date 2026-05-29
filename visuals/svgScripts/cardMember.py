import os

def create_member_card(card_type, bg_color, accent_color, team_name):
    # Standard Card Size: 2.5 x 3.5 inches (225 x 315 px at 90dpi)
    # Member/Role card inspired by Secret Hitler
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
        <rdf:RDF><cc:Work rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage" /><dc:title>Dirty Money - {team_name}</dc:title></cc:Work></rdf:RDF>
    </metadata>

    <!-- Card base -->
    <rect id="card-base" x="0" y="0" width="225" height="315" rx="8" fill="{bg_color}" stroke="{accent_color}" stroke-width="5"/>
    
    <!-- Top decorative line -->
    <line x1="20" y1="15" x2="205" y2="15" stroke="{accent_color}" stroke-width="2" opacity="1" />
    
    <!-- Header -->
    <text x="112.5" y="32" font-family="Georgia, serif" font-size="12" font-weight="bold" fill="{accent_color}" text-anchor="middle" letter-spacing="1">DIRTY MONEY</text>
    <text x="112.5" y="42" font-family="Courier New, monospace" font-size="10" fill="{accent_color}" text-anchor="middle" opacity="1">CONFIDENTIAL</text>
    
    <!-- Divider -->
    <line x1="30" y1="50" x2="195" y2="50" stroke="{accent_color}" stroke-width="2" opacity="1" />
    
    <!-- Logo/Illustration Area - Shield with symbol -->
    <g transform="translate(112.5, 100)">
        <!-- Shield shape -->
        <path d="M -45 -40 L 45 -40 L 45 10 C 45 35 0 55 0 55 C 0 55 -45 35 -45 10 Z" 
              fill="none" stroke="{accent_color}" stroke-width="3" opacity="1"/>
        
        <!-- Inner shield -->
        <path d="M -35 -30 L 35 -30 L 35 8 C 35 28 0 45 0 45 C 0 45 -35 28 -35 8 Z" 
              fill="none" stroke="{accent_color}" stroke-width="2" opacity="1"/>
        
        <!-- Symbol based on team type -->
        {"<!-- Authentic: Checkmark/Verified symbol -->" if card_type == "AUTHENTIC" else "<!-- Fraudulent: X/Alert symbol -->"}
        {"<path d=\"M -20 5 L -5 20 L 25 -15\" fill=\"none\" stroke=\"" + accent_color + "\" stroke-width=\"4\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/>" if card_type == "AUTHENTIC" else "<g stroke=\"" + accent_color + "\" stroke-width=\"4\" stroke-linecap=\"round\"><line x1=\"-15\" y1=\"-10\" x2=\"15\" y2=\"20\"/><line x1=\"15\" y1=\"-10\" x2=\"-15\" y2=\"20\"/></g>"}
    </g>
    
    <!-- Team name -->
    <text x="112.5" y="180" font-family="Georgia, serif" font-size="18" font-weight="bold" fill="{accent_color}" text-anchor="middle" letter-spacing="1">{card_type.upper()}</text>
    <text x="112.5" y="200" font-family="Georgia, serif" font-size="18" font-weight="bold" fill="{accent_color}" text-anchor="middle" letter-spacing="1">TEAM</text>
    
    <!-- Divider -->
    <line x1="30" y1="210" x2="195" y2="210" stroke="{accent_color}" stroke-width="2" opacity="1" />
    
    <!-- Instructions section -->
    <text x="112.5" y="224" font-family="Courier New, monospace" font-size="10" fill="{accent_color}" text-anchor="middle" font-weight="bold">OBJECTIVE</text>
    <text x="112.5" y="236" font-family="Arial, sans-serif" font-size="10" fill="{accent_color}" text-anchor="middle" opacity="1">
        {"Expose fraudulent food suppliers" if card_type == "AUTHENTIC" else " "}
        {"Evade detection and trade" if card_type == "FRAUDULENT" else " "}
    </text>
    <text x="112.5" y="248" font-family="Arial, sans-serif" font-size="10" fill="{accent_color}" text-anchor="middle" opacity="1">
        {" before they contaminate the food supply chain." if card_type == "AUTHENTIC" else " "}
        {" adulterated products." if card_type == "FRAUDULENT" else " "}
    </text>
    
    <!-- Bottom decorative element -->
    <g transform="translate(112.5, 270)">
        <circle cx="0" cy="0" r="8" fill="none" stroke="{accent_color}" stroke-width="1.5" opacity="1"/>
        <circle cx="0" cy="0" r="4" fill="none" stroke="{accent_color}" stroke-width="1" opacity="1"/>
    </g>
    
    <!-- Footer -->
    <text x="112.5" y="295" font-family="Courier New, monospace" font-size="10" fill="{accent_color}" text-anchor="middle" opacity="1">KEEP YOUR IDENTITY SECRET</text>
</svg>
"""
    filename = f"member_{card_type.lower()}_card.svg"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_template)
    print(f"Generated: {filename}")

# Run the generator - Authentic (blue) and Fraudulent (red)
create_member_card("AUTHENTIC", "#0a1520", "#0070c4", "Authentic Team")
create_member_card("FRAUDULENT", "#200a0a", "#ba293b", "Fraudulent Team")