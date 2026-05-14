import os

def create_card(card_type, bg_color, accent_color):
    # Horizontal Card Size: 3.5 x 2.5 inches (315 x 225 px at 90dpi)
    # Certificate of Analysis design with detective theme
    svg_template = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg 
    width="3.5in" 
    height="2.5in" 
    viewBox="0 0 315 225"
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
    <rect id="card-base" x="0" y="0" width="315" height="225" rx="8" fill="{bg_color}" stroke="{accent_color}" stroke-width="5"/>
    <text x="157.5" y="125" font-family="Courier New, monospace" font-size="60" font-weight="bold" fill="{accent_color}" text-anchor="middle" opacity="0.5">{card_type.upper()}</text>

    <!-- Align -->
    <rect x="127.5" y="90.5" width="60" height="44" rx="2" stroke="{accent_color}" fill="none" opacity="0"/>
</svg>
"""
    filename = f"{card_type.lower()}_card.svg"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_template)
    print(f"Generated: {filename}")

# Run the generator
create_card("Supplier", "#172428", "#f1dfe4")