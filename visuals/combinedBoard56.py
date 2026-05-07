import os

# Board dimensions scaled to fit poker-sized cards (225px × 315px)
# Scale factor: 1.658 (poker card height 315px ÷ current slot height 190px)
# Final size: 1708×522 px (single board) = 18.98" × 5.8" = 482mm × 147mm
# Combined size: 1708×1061 px = 18.98" × 11.8" = 482mm × 300mm
SVG_WIDTH = 1708
SVG_HEIGHT = 1061
BOARD_WIDTH = 1708
BOARD_HEIGHT = 522


def mirror_x(x, width=0):
    return SVG_WIDTH - x - width


def make_slot_group(x, lines, accent_color):
    lines_svg = []
    for y, text, opacity in lines:
        lines_svg.append(
            f'        <text x="116" y="{y}" font-family="Courier New, monospace" font-size="15" fill="{accent_color}" text-anchor="middle" opacity="{opacity}">{text}</text>'
        )
    return f"""    <g transform=\"translate({x}, 116)\">
        <rect x=\"0\" y=\"0\" width=\"232\" height=\"315\" rx=\"13\" fill=\"none\" stroke=\"{accent_color}\" stroke-width=\"2\" opacity=\"0.35\"/>
{chr(10).join(lines_svg)}
    </g>
"""


def build_auth_board(bg_color, accent_color, board_name, y_offset=0, mirrored=False, pattern_id="border-pattern"):
    tx = mirror_x if mirrored else (lambda x, width=0: x)

    discard_x = tx(10, 123)
    draw_x = tx(1575, 123)
    discard_text_x = tx(71)
    draw_text_x = tx(1637)

    discard_arrow_path = f"M {tx(25)} 261 L {tx(41)} 245 L {tx(41)} 278 Z"
    draw_arrow_path = f"M {tx(1683)} 261 L {tx(1667)} 245 L {tx(1667)} 278 Z"

    discard_cards = []
    for x, y in [(50, 41), (58, 50), (50, 431), (58, 423)]:
        discard_cards.append(
            f'    <rect x="{tx(x, 33)}" y="{y}" width="33" height="50" rx="3" fill="{accent_color}" opacity="0.6" />'
        )

    draw_cards = []
    for x, y in [(1625, 33), (1617, 41), (1609, 50), (1625, 431), (1617, 423), (1609, 414)]:
        draw_cards.append(
            f'    <rect x="{tx(x, 33)}" y="{y}" width="33" height="50" rx="3" fill="{accent_color}" opacity="0.6" />'
        )

    title_x = tx(182)
    line_x1 = tx(182)
    line_x2 = tx(713)
    if line_x1 > line_x2:
        line_x1, line_x2 = line_x2, line_x1

    slot_origins = [207, 473, 738, 1003, 1269]
    if mirrored:
        slot_origins = [mirror_x(x, 232) for x in slot_origins]

    slot_groups = [
        [(166, "SLOT 1", 0.35)],
        [(166, "SLOT 2", 0.35)],
        [(166, "SLOT 3", 0.35)],
        [(166, "SLOT 4", 0.35)],
        [
            (50, "Authentic team wins!", 1),
            (166, "SLOT 5", 0.35),
            (265, "Authentic food", 1),
            (290, "perseveres", 1),
        ],
    ]

    slot_blocks = []
    for x, lines in zip(slot_origins, slot_groups):
        slot_blocks.append(make_slot_group(x, lines, accent_color))

    return f"""    <g transform=\"translate(0, {y_offset})\">
        <rect x=\"0\" y=\"0\" width=\"{BOARD_WIDTH}\" height=\"{BOARD_HEIGHT}\" rx=\"17\" fill=\"{bg_color}\" />

        <rect x=\"{discard_x}\" y=\"10\" width=\"123\" height=\"502\" rx=\"13\" fill=\"none\" stroke=\"{accent_color}\" stroke-width=\"2\" opacity=\"0.5\" />
        <text x=\"{discard_text_x}\" y=\"277\" font-family=\"Georgia, serif\" font-size=\"33\" font-weight=\"bold\" fill=\"{accent_color}\" text-anchor=\"middle\" transform=\"rotate(-90 {discard_text_x} 261)\">DISCARD PILE</text>
        <path d=\"{discard_arrow_path}\" fill=\"{accent_color}\" opacity=\"0.7\" />
{chr(10).join(discard_cards)}

        <rect x=\"{draw_x}\" y=\"10\" width=\"123\" height=\"502\" rx=\"13\" fill=\"none\" stroke=\"{accent_color}\" stroke-width=\"2\" opacity=\"0.5\" />
        <text x=\"{draw_text_x}\" y=\"277\" font-family=\"Georgia, serif\" font-size=\"37\" font-weight=\"bold\" fill=\"{accent_color}\" text-anchor=\"middle\" transform=\"rotate(90 {draw_text_x} 261)\">DRAW PILE</text>
        <path d=\"{draw_arrow_path}\" fill=\"{accent_color}\" opacity=\"0.7\" />
{chr(10).join(draw_cards)}

        <rect x=\"143\" y=\"10\" width=\"1423\" height=\"502\" rx=\"13\" fill=\"none\" stroke=\"{accent_color}\" stroke-width=\"2\" opacity=\"0.5\" />
        <rect x=\"153\" y=\"20\" width=\"1403\" height=\"483\" rx=\"3\" fill=\"none\" stroke=\"url(#{pattern_id})\" stroke-width=\"17\" opacity=\"0.45\" />

        <text x=\"{title_x}\" y=\"75\" font-family=\"Georgia, serif\" font-size=\"40\" font-weight=\"bold\" fill=\"{accent_color}\" letter-spacing=\"2\">{board_name}</text>
        <line x1=\"{line_x1}\" y1=\"86\" x2=\"{line_x2}\" y2=\"86\" stroke=\"{accent_color}\" stroke-width=\"2\" opacity=\"0.4\" />

{''.join(slot_blocks)}

        <text x=\"1492\" y=\"489\" font-family=\"Courier New, monospace\" font-size=\"10\" fill=\"{accent_color}\" text-anchor=\"end\" opacity=\"0.4\">DIRTY MONEY</text>
    </g>
"""


def build_fraud_board(bg_color, accent_color, board_name, y_offset=0, mirrored=False, pattern_id="border-pattern"):
    tx = mirror_x if mirrored else (lambda x, width=0: x)

    title_x = tx(50)
    line_x1 = tx(50)
    line_x2 = tx(580)
    if line_x1 > line_x2:
        line_x1, line_x2 = line_x2, line_x1

    win_bar_x = tx(895, 713)
    win_text_x = tx(978)
    players_bar_x = tx(373)
    players_text_x = tx(373)

    slot_origins = [75, 340, 605, 870, 1135, 1401]
    if mirrored:
        slot_origins = [mirror_x(x, 232) for x in slot_origins]

    slot_groups = [
        [(166, "SLOT 1", 0.35)],
        [(166, "SLOT 2", 0.35)],
        [
            (50, "Authenticity test", 1),
            (166, "SLOT 3", 0.35),
            (265, "The trader examines", 1),
            (290, "the top 3 cards", 1),
        ],
        [
            (50, "Reorganisation", 1),
            (166, "SLOT 4", 0.35),
            (265, "The trader must", 1),
            (290, "fire a player", 1),
        ],
        [
            (50, "Reorganisation", 1),
            (166, "SLOT 5", 0.35),
            (265, "The trader must", 1),
            (290, "fire a player", 1),
        ],
        [
            (50, "Fraudsters win!", 1),
            (166, "SLOT 6", 0.35),
            (265, "The supply chain has", 1),
            (290, "been fully infiltrated", 1),
        ],
    ]

    slot_blocks = []
    for x, lines in zip(slot_origins, slot_groups):
        slot_blocks.append(make_slot_group(x, lines, accent_color))

    return f"""    <g transform=\"translate(0, {y_offset})\">
        <rect x=\"0\" y=\"0\" width=\"{BOARD_WIDTH}\" height=\"{BOARD_HEIGHT}\" rx=\"17\" fill=\"{bg_color}\" />

        <rect x=\"10\" y=\"10\" width=\"1688\" height=\"502\" rx=\"13\" fill=\"none\" stroke=\"{accent_color}\" stroke-width=\"2\" opacity=\"0.5\" />
        <rect x=\"20\" y=\"20\" width=\"1669\" height=\"483\" rx=\"3\" fill=\"none\" stroke=\"url(#{pattern_id})\" stroke-width=\"17\" opacity=\"0.45\" />

        <text x=\"{title_x}\" y=\"75\" font-family=\"Georgia, serif\" font-size=\"40\" font-weight=\"bold\" fill=\"{accent_color}\" letter-spacing=\"2\">{board_name}</text>
        <line x1=\"{line_x1}\" y1=\"86\" x2=\"{line_x2}\" y2=\"86\" stroke=\"{accent_color}\" stroke-width=\"2\" opacity=\"0.4\" />

        <rect x=\"{win_bar_x}\" y=\"66\" width=\"713\" height=\"13\" rx=\"3\" fill=\"none\" stroke=\"{accent_color}\" stroke-width=\"17\" opacity=\"0.65\" />
        <text x=\"{win_text_x}\" y=\"76\" font-family=\"Courier New, monospace\" font-size=\"16\" font-weight=\"bold\" fill=\"{bg_color}\" opacity=\"0.8\">FRAUDSTERS WIN IF TRICK-MEISTER IS ELECTED AS SUPPLIER</text>

{''.join(slot_blocks)}
        <rect x=\"{players_bar_x}\" y=\"464\" width=\"965\" height=\"13\" rx=\"3\" fill=\"none\" stroke=\"{accent_color}\" stroke-width=\"17\" opacity=\"0.65\" />
        <text x=\"{players_text_x}\" y=\"474\" font-family=\"Courier New, monospace\" font-size=\"16\" font-weight=\"bold\" fill=\"{bg_color}\" opacity=\"0.8\">5 OR 6 PLAYERS: PLAY WITH 1 FRAUDSTER AND TRICK-MEISTER, TRICK-MEISTER KNOWS WHO THE FRAUDSTER IS</text>

        <text x=\"1625\" y=\"489\" font-family=\"Courier New, monospace\" font-size=\"10\" fill=\"{accent_color}\" text-anchor=\"end\" opacity=\"0.4\">DIRTY MONEY</text>
    </g>
"""


def create_policy_board(board_type, bg_color, accent_color, board_name):
    if board_type.lower().startswith("fraud"):
        board_inner = build_fraud_board(bg_color, accent_color, board_name)
    else:
        board_inner = build_auth_board(bg_color, accent_color, board_name)

    svg_template = f"""<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>
<svg 
    width=\"18.98in\" 
    height=\"5.8in\" 
    viewBox=\"0 0 {SVG_WIDTH} {BOARD_HEIGHT}\"
    xmlns:dc=\"http://purl.org/dc/elements/1.1/\"
    xmlns:cc=\"http://creativecommons.org/ns#\"
    xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"
    xmlns:svg=\"http://www.w3.org/2000/svg\"
    xmlns=\"http://www.w3.org/2000/svg\"
    xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\">
    <metadata>
        <rdf:RDF><cc:Work rdf:about=\"\"><dc:format>image/svg+xml</dc:format><dc:type rdf:resource=\"http://purl.org/dc/dcmitype/StillImage\" /><dc:title>Dirty Money - {board_name}</dc:title></cc:Work></rdf:RDF>
    </metadata>

    <defs>
        <pattern id=\"border-pattern\" x=\"0\" y=\"0\" width=\"12\" height=\"12\" patternUnits=\"userSpaceOnUse\">
            <circle cx=\"2\" cy=\"2\" r=\"1\" fill=\"{accent_color}\" opacity=\"0.35\"/>
            <circle cx=\"8\" cy=\"8\" r=\"1\" fill=\"{accent_color}\" opacity=\"0.35\"/>
            <circle cx=\"8\" cy=\"2\" r=\"2\" fill=\"{accent_color}\" opacity=\"0.55\"/>
            <circle cx=\"2\" cy=\"8\" r=\"2\" fill=\"{accent_color}\" opacity=\"0.55\"/>
        </pattern>
    </defs>

{board_inner}
</svg>
"""
    filename = f"board_56{board_type.lower()}.svg"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_template)
    print(f"Generated: {filename}")


def create_combined_policy_board():
    combined_inner = '<g transform="translate(1708, 522) rotate(180)">\n'
    combined_inner += build_fraud_board("#200a0a", "#ba293b", "FRAUDULENT TRACK", y_offset=0, mirrored=False, pattern_id="border-pattern-fraud")
    combined_inner += '</g>\n'
    combined_inner += build_auth_board("#0a1520", "#0070c4", "AUTHENTIC TRACK", y_offset=539, mirrored=False, pattern_id="border-pattern-auth")

    svg_template = f"""<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>
<svg 
    width=\"18.98in\" 
    height=\"11.8in\" 
    viewBox=\"0 0 {SVG_WIDTH} {SVG_HEIGHT}\"
    xmlns:dc=\"http://purl.org/dc/elements/1.1/\"
    xmlns:cc=\"http://creativecommons.org/ns#\"
    xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"
    xmlns:svg=\"http://www.w3.org/2000/svg\"
    xmlns=\"http://www.w3.org/2000/svg\"
    xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\">
    <metadata>
        <rdf:RDF><cc:Work rdf:about=\"\"><dc:format>image/svg+xml</dc:format><dc:type rdf:resource=\"http://purl.org/dc/dcmitype/StillImage\" /><dc:title>Dirty Money - FRAUDULENT + AUTHENTIC COMBINED</dc:title></cc:Work></rdf:RDF>
    </metadata>

    <defs>
        <pattern id=\"border-pattern-fraud\" x=\"0\" y=\"0\" width=\"12\" height=\"12\" patternUnits=\"userSpaceOnUse\">
            <circle cx=\"2\" cy=\"2\" r=\"1\" fill=\"#ba293b\" opacity=\"0.35\"/>
            <circle cx=\"8\" cy=\"8\" r=\"1\" fill=\"#ba293b\" opacity=\"0.35\"/>
            <circle cx=\"8\" cy=\"2\" r=\"2\" fill=\"#ba293b\" opacity=\"0.55\"/>
            <circle cx=\"2\" cy=\"8\" r=\"2\" fill=\"#ba293b\" opacity=\"0.55\"/>
        </pattern>
        <pattern id=\"border-pattern-auth\" x=\"0\" y=\"0\" width=\"12\" height=\"12\" patternUnits=\"userSpaceOnUse\">
            <circle cx=\"2\" cy=\"2\" r=\"1\" fill=\"#0070c4\" opacity=\"0.35\"/>
            <circle cx=\"8\" cy=\"8\" r=\"1\" fill=\"#0070c4\" opacity=\"0.35\"/>
            <circle cx=\"8\" cy=\"2\" r=\"2\" fill=\"#0070c4\" opacity=\"0.55\"/>
            <circle cx=\"2\" cy=\"8\" r=\"2\" fill=\"#0070c4\" opacity=\"0.55\"/>
        </pattern>
    </defs>

{combined_inner}
</svg>
"""
    filename = "board_56_combined.svg"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_template)
    print(f"Generated: {filename}")


# Run the generator
create_policy_board("AUTHENTIC", "#0a1520", "#0070c4", "AUTHENTIC TRACK")
create_combined_policy_board()

