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
    <rect x="10" y="10" width="1688" height="502" rx="13" fill="none" stroke="{accent_color}" stroke-width="2" opacity="0.5" />
    <rect x="20" y="20" width="1669" height="483" rx="3" fill="none" stroke="url(#border-pattern)" stroke-width="17" opacity="0.45" />

    <!-- Title area -->
    <text x="50" y="75" font-family="Georgia, serif" font-size="40" font-weight="bold" fill="{accent_color}" letter-spacing="2">{board_name}</text>
    <line x1="50" y1="86" x2="580" y2="86" stroke="{accent_color}" stroke-width="2" opacity="0.4" />

    <!-- Win condition -->
    <rect x="895" y="66" width="713" height="13" rx="3" fill="none" stroke="{accent_color}" stroke-width="17" opacity="0.65" />
    <text x="978" y="76" font-family="Courier New, monospace" font-size="16" font-weight="bold" fill="{bg_color}" opacity="0.8">FRAUDSTERS WIN IF TRICK-MEISTER IS ELECTED AS SUPPLIER</text>

    <!-- Slot labels row -->
    <g transform="translate(75, 116)">
        <rect x="0" y="0" width="232" height="315" rx="13" fill="none" stroke="{accent_color}" stroke-width="2" opacity="0.35"/>
        <text x="116" y="166" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="0.35">SLOT 1</text>
    </g>
    <g transform="translate(340, 116)">
        <rect x="0" y="0" width="232" height="315" rx="13" fill="none" stroke="{accent_color}" stroke-width="2" opacity="0.35"/>
        <text x="116" y="166" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="0.35">SLOT 2</text>
    </g>
    <g transform="translate(605, 116)">
        <rect x="0" y="0" width="232" height="315" rx="13" fill="none" stroke="{accent_color}" stroke-width="2" opacity="0.35"/>
        <text x="116" y="50" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="1">Authenticity test</text>
        <text x="116" y="166" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="0.35">SLOT 3</text>
        <text x="116" y="265" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="1">The trader examines</text> 
        <text x="116" y="290" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="1">the top 3 cards</text>
    </g>
    <g transform="translate(870, 116)">
        <rect x="0" y="0" width="232" height="315" rx="13" fill="none" stroke="{accent_color}" stroke-width="2" opacity="0.35"/>
        <text x="116" y="50" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="1">Reorganisation</text>
        <text x="116" y="166" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="0.35">SLOT 4</text>
        <text x="116" y="265" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="1">The trader must</text> 
        <text x="116" y="290" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="1">fire a player</text>
    </g>
    <g transform="translate(1135, 116)">
        <rect x="0" y="0" width="232" height="315" rx="13" fill="none" stroke="{accent_color}" stroke-width="2" opacity="0.35"/>
        <text x="116" y="50" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="1">Reorganisation</text>
        <text x="116" y="166" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="0.35">SLOT 5</text>
        <text x="116" y="265" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="1">The trader must</text> 
        <text x="116" y="290" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="1">fire a player</text>
    </g>
    <g transform="translate(1401, 116)">
        <rect x="0" y="0" width="232" height="315" rx="13" fill="none" stroke="{accent_color}" stroke-width="2" opacity="0.35"/>
        <text x="116" y="50" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="1">Fraudsters win!</text>
        <text x="116" y="166" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="0.35">SLOT 6</text>
        <text x="116" y="265" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="1">The supply chain has</text> 
        <text x="116" y="290" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="1">been fully infiltrated</text>
    </g>

    <!-- Set players -->
    <rect x="373" y="464" width="965" height="13" rx="3" fill="none" stroke="{accent_color}" stroke-width="17" opacity="0.65" />
    <text x="373" y="474" font-family="Courier New, monospace" font-size="16" font-weight="bold" fill="{bg_color}" opacity="0.8">5 OR 6 PLAYERS: PLAY WITH 1 FRAUDSTER AND TRICK-MEISTER, TRICK-MEISTER KNOWS WHO THE FRAUDSTER IS</text>

    <!-- Footer signature -->
    <text x="1625" y="489" font-family="Courier New, monospace" font-size="10" fill="{accent_color}" text-anchor="end" opacity="0.4">DIRTY MONEY</text>
</svg>
"""
    filename = f"board_56{board_type.lower()}.svg"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_template)
    print(f"Generated: {filename}")

# Run the generator - Fraudulent board (red theme)
create_policy_board("FRAUDULENT", "#200a0a", "#ba293b", "FRAUDULENT TRACK")