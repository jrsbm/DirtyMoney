import os

def create_policy_board(board_type, bg_color, accent_color, board_name):
    # Board size: 18.98 inches wide x 5.8 inches tall (1708 x 522 px at 90 DPI) for a horizontal policy track
    # Scale factor: 1.658 (to fit poker-sized cards 225px x 315px)
    # Original card slots: 210 x 130 px → Scaled slots: 232 x 315 px (poker card height)
    svg_template = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg 
    width="18.98in" 
    height="5.8in" 
    viewBox="0 0 1708 522"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:cc="http://creativecommons.org/ns#"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:svg="http://www.w3.org/2000/svg"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape">
    
    <metadata>
        <rdf:RDF><cc:Work rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage" /><dc:title>Dirty Money - {board_name}</dc:title></cc:Work></rdf:RDF>
    </metadata>

    <!-- Board base -->
    <rect x="0" y="0" width="1708" height="522" rx="17" fill="{bg_color}" />

    <!-- Decorative repeating border pattern -->
    <defs>
        <pattern id="border-pattern" x="0" y="0" width="12" height="12" patternUnits="userSpaceOnUse">
            <circle cx="2" cy="2" r="1" fill="{accent_color}" opacity="0.35"/>
            <circle cx="8" cy="8" r="1" fill="{accent_color}" opacity="0.35"/>
            <circle cx="8" cy="2" r="2" fill="{accent_color}" opacity="0.55"/>
            <circle cx="2" cy="8" r="2" fill="{accent_color}" opacity="0.55"/>
        </pattern>
    </defs>
    
    <!-- Discard pile -->
    <rect x="10" y="10" width="123" height="502" rx="13" fill="none" stroke="{accent_color}" stroke-width="2" opacity="0.5" />
    <text x="71" y="277" font-family="Georgia, serif" font-size="33" font-weight="bold" fill="{accent_color}" text-anchor="middle" transform="rotate(-90 71 261)">DISCARD PILE</text>
    <path d="M 25 261 L 41 245 L 41 278 Z" fill="{accent_color}" opacity="0.7" />
    <rect x="50" y="41" width="33" height="50" rx="3" fill="{accent_color}" opacity="0.6" />
    <rect x="58" y="50" width="33" height="50" rx="3" fill="{accent_color}" opacity="0.6" />
    <rect x="50" y="431" width="33" height="50" rx="3" fill="{accent_color}" opacity="0.6" />
    <rect x="58" y="423" width="33" height="50" rx="3" fill="{accent_color}" opacity="0.6" />

    <!-- Draw pile -->
    <rect x="1575" y="10" width="123" height="502" rx="13" fill="none" stroke="{accent_color}" stroke-width="2" opacity="0.5" />
    <text x="1637" y="277" font-family="Georgia, serif" font-size="37" font-weight="bold" fill="{accent_color}" text-anchor="middle" transform="rotate(90 1637 261)">DRAW PILE</text>
    <path d="M 1683 261 L 1667 245 L 1667 278 Z" fill="{accent_color}" opacity="0.7" />
    <rect x="1625" y="33" width="33" height="50" rx="3" fill="{accent_color}" opacity="0.6" />
    <rect x="1617" y="41" width="33" height="50" rx="3" fill="{accent_color}" opacity="0.6" />
    <rect x="1609" y="50" width="33" height="50" rx="3" fill="{accent_color}" opacity="0.6" />
    <rect x="1625" y="431" width="33" height="50" rx="3" fill="{accent_color}" opacity="0.6" />
    <rect x="1617" y="423" width="33" height="50" rx="3" fill="{accent_color}" opacity="0.6" />
    <rect x="1609" y="414" width="33" height="50" rx="3" fill="{accent_color}" opacity="0.6" />

    <!-- Main board area -->
    <rect x="143" y="10" width="1423" height="502" rx="13" fill="none" stroke="{accent_color}" stroke-width="2" opacity="0.5" />
    <rect x="153" y="20" width="1403" height="483" rx="3" fill="none" stroke="url(#border-pattern)" stroke-width="17" opacity="0.45" />

    <!-- Title area -->
    <text x="182" y="75" font-family="Georgia, serif" font-size="40" font-weight="bold" fill="{accent_color}" letter-spacing="2">{board_name}</text>
    <line x1="182" y1="86" x2="713" y2="86" stroke="{accent_color}" stroke-width="2" opacity="0.4" />

    <!-- Slot labels row -->
    <g transform="translate(207, 116)">
        <rect x="0" y="0" width="232" height="315" rx="13" fill="none" stroke="{accent_color}" stroke-width="2" opacity="0.35"/>
        <text x="116" y="166" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="0.35">SLOT 1</text>
    </g>
    <g transform="translate(473, 116)">
        <rect x="0" y="0" width="232" height="315" rx="13" fill="none" stroke="{accent_color}" stroke-width="2" opacity="0.35"/>
        <text x="116" y="166" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="0.35">SLOT 2</text>
    </g>
    <g transform="translate(738, 116)">
        <rect x="0" y="0" width="232" height="315" rx="13" fill="none" stroke="{accent_color}" stroke-width="2" opacity="0.35"/>
        <text x="116" y="166" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="0.35">SLOT 3</text>
    </g>
    <g transform="translate(1003, 116)">
        <rect x="0" y="0" width="232" height="315" rx="13" fill="none" stroke="{accent_color}" stroke-width="2" opacity="0.35"/>
        <text x="116" y="166" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="0.35">SLOT 4</text>
    </g>
    <g transform="translate(1269, 116)">
        <rect x="0" y="0" width="232" height="315" rx="13" fill="none" stroke="{accent_color}" stroke-width="2" opacity="0.35"/>
        <text x="116" y="50" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="1">Authentic team wins!</text>
        <text x="116" y="166" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="0.35">SLOT 5</text>
        <text x="116" y="265" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="1">Authentic food</text> 
        <text x="116" y="290" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="1">perseveres</text>
    </g>

    <!-- Footer signature -->
    <text x="1492" y="489" font-family="Courier New, monospace" font-size="10" fill="{accent_color}" text-anchor="end" opacity="0.4">DIRTY MONEY</text>
</svg>
"""
    filename = f"board_56{board_type.lower()}.svg"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_template)
    print(f"Generated: {filename}")

# Run the generator - Fraudulent board (red theme)
create_policy_board("AUTHENTIC", "#0a1520", "#0070c4", "AUTHENTIC TRACK")