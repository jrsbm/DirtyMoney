import os

def create_voting_card(card_type, bg_color, accent_color, vote_text):
    # Horizontal Card Size: 3.5 x 2.5 inches (315 x 225 px at 90dpi)
    # Yes/No voting card with detective theme
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
        <rdf:RDF><cc:Work rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage" /><dc:title>Dirty Money - {vote_text}</dc:title></cc:Work></rdf:RDF>
    </metadata>

    <!-- Card base with subtle inner border -->
    <rect id="card-base" x="0" y="0" width="315" height="225" rx="8" fill="{bg_color}" stroke="{accent_color}" stroke-width="5"/>
    
    <!-- Header section -->
    <text x="24" y="22" font-family="Courier New, monospace" font-size="12" font-weight="bold" fill="{accent_color}" letter-spacing="1">VOTE CARD</text>
    
    <!-- Divider -->
    <line x1="24" y1="30" x2="290" y2="30" stroke="{accent_color}" stroke-width="2" opacity="1" />
    
    <!-- Main verdict area -->
    <text x="157" y="150" font-family="Georgia, serif" font-size="96" font-weight="bold" fill="{accent_color}" text-anchor="middle" letter-spacing="3">{vote_text}</text>
    
    <!-- Footer -->
    <line x1="24" y1="185" x2="290" y2="185" stroke="{accent_color}" stroke-width="2" opacity="1" />
    <text x="157" y="208" font-family="Courier New, monospace" font-size="12" fill="{accent_color}" opacity="1" text-anchor="middle">DIRTY MONEY - A FOOD FRAUD GAME</text>
</svg>
"""
    filename = f"vote_{vote_text.lower()}_card.svg"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_template)
    print(f"Generated: {filename}")

# Run the generator - Yes (blue/authentic) and No (red/fraudulent)
create_voting_card("847", "#0a1520", "#0070c4", "YES")
create_voting_card("848", "#200a0a", "#ba293b", "NO")
