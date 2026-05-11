import os

def create_card(card_type, bg_color, accent_color):
    # Standard Card Size: 2.5 x 3.5 inches (225 x 315 px at 90dpi)
    # Certificate of Analysis design with detective theme
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
        <rdf:RDF><cc:Work rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage" /><dc:title>Dirty Money - {card_type}</dc:title></cc:Work></rdf:RDF>
    </metadata>

    <!-- Card base -->
    <rect id="card-base" x="0" y="0" width="225" height="315" rx="8" fill="{bg_color}" stroke="{accent_color}" stroke-width="1.5"/>
    <text x="112.5" y="136" font-family="Courier New, monospace" font-size="30" fill="{accent_color}" text-anchor="middle" opacity="0.5">DIRTY</text>
    <text x="112.5" y="197" font-family="Courier New, monospace" font-size="30" fill="{accent_color}" text-anchor="middle" opacity="0.5">MONEY</text>

    <!-- Allign -->
    <rect x="82.5" y="135.5" width="60" height="44" rx="2" stroke="{accent_color}" fill="none" opacity="0"/>
    
    <!-- Money icon -->
    <g transform="translate(92.5, 145.5)" opacity="0.5">
    <rect width="40" height="24" rx="2" stroke="{accent_color}" stroke-width="1.2" fill="none"/>
    <circle cx="8" cy="12" r="1.5" fill="{accent_color}"/>
    <circle cx="20" cy="12" r="4" stroke="{accent_color}" stroke-width="1.22" fill="none"/>
    <circle cx="32" cy="12" r="1.5" fill="{accent_color}"/>
    </g>
</svg>
"""
    filename = f"{card_type.lower()}_card.svg"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_template)
    print(f"Generated: {filename}")

# Run the generator
create_card("Back", "#172428", "#f1dfe4")

