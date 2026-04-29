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
    <rect x="0" y="0" width="315" height="225" rx="6" fill="{bg_color}" />
    <rect x="1.5" y="1.5" width="312" height="222" rx="5" fill="none" stroke="{accent_color}" stroke-width="1" opacity="0.4"/>
    
    <!-- Left accent bar -->
    <rect x="0" y="0" width="8" height="225" rx="0" fill="{accent_color}" opacity="0.8"/>
    
    <!-- Header section -->
    <text x="24" y="22" font-family="Courier New, monospace" font-size="11" font-weight="bold" fill="{accent_color}" letter-spacing="1">VOTE CARD</text>
    <text x="290" y="22" font-family="Courier New, monospace" font-size="8" fill="{accent_color}" opacity="0.6" text-anchor="end">CASE #{card_type}</text>
    
    <!-- Divider -->
    <line x1="24" y1="30" x2="290" y2="30" stroke="{accent_color}" stroke-width="0.5" opacity="0.4" />
    
    <!-- Main verdict area -->
    <text x="157" y="150" font-family="Georgia, serif" font-size="96" font-weight="bold" fill="{accent_color}" text-anchor="middle" letter-spacing="3">{vote_text}</text>
    
    <!-- Footer -->
    <line x1="24" y1="185" x2="290" y2="185" stroke="{accent_color}" stroke-width="0.5" opacity="0.3" />
    <text x="157" y="200" font-family="Courier New, monospace" font-size="6" fill="{accent_color}" opacity="0.5" text-anchor="middle">DIRTY MONEY - A FOOD FRAUD GAME</text>
    <text x="157" y="212" font-family="Courier New, monospace" font-size="5" fill="{accent_color}" opacity="0.4" text-anchor="middle">CONFIDENTIAL - FOR INVESTIGATIVE USE ONLY</text>
</svg>
"""
    filename = f"vote_{vote_text.lower()}_card.svg"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_template)
    print(f"Generated: {filename}")

# Run the generator - Yes (blue/authentic) and No (red/fraudulent)
create_voting_card("847", "#0a1520", "#0070c4", "YES")
create_voting_card("848", "#200a0a", "#ba293b", "NO")
