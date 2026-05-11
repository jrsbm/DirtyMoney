import os

# Board dimensions scaled to fit poker-sized cards (225px × 315px)
# Scale factor: 1.658 (poker card height 315px ÷ current slot height 190px)
# Final size: 1701×522 px (single board) = 18.9" × 5.8" = 480mm × 147mm
# Combined size: 1701×1061 px = 18.9" × 11.8" = 480mm × 300mm
# Total with 5mm bleed on all sides: 1737×1099 px
BLEED_OFFSET = 18  # 5mm bleed ≈ 18px at print resolution
BLEED_WIDTH = 1737
BLEED_HEIGHT = 1099
ARTWORK_WIDTH = 1701
ARTWORK_HEIGHT = 1061
BOARD_WIDTH = 1701
BOARD_HEIGHT = 522

def mirror_x(x, width=0):
    return ARTWORK_WIDTH - x - width


def make_slot_group(x, lines, accent_color):
    lines_svg = []
    for y, text, opacity in lines:
        lines_svg.append(
            f'        <text x="116" y="{y}" font-family="Courier New, monospace" font-size="30" font-weight="bold" fill="{accent_color}" text-anchor="middle" opacity="{opacity}">{text}</text>'
        )
    return f"""    <g transform=\"translate({x}, 116)\">
        <rect x=\"0\" y=\"0\" width=\"232\" height=\"315\" rx=\"13\" fill=\"none\" stroke=\"{accent_color}\" stroke-width=\"5\" opacity=\"1\"/>
{chr(10).join(lines_svg)}
    </g>
"""


def build_auth_board(bg_color, accent_color, board_name, y_offset=0, mirrored=False, pattern_id="border-pattern"):
    tx = mirror_x if mirrored else (lambda x, width=0: x)

    discard_text_x = tx(72)  # 71 + 1
    draw_text_x = tx(1630)   # 1637 - 7

    discard_arrow_path = f"M {tx(25)} 261 L {tx(41)} 245 L {tx(41)} 278 Z"
    draw_arrow_path = f"M {tx(1679)} 261 L {tx(1663)} 245 L {tx(1663)} 278 Z"  # 1683-4, 1667-4

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

    # Shift titles 1mm to center (≈4px)
    title_x = tx(186)  # 182 + 4
    line_x1 = tx(186)  # 182 + 4
    line_x2 = tx(709)  # 713 - 4
    if line_x1 > line_x2:
        line_x1, line_x2 = line_x2, line_x1

    slot_origins = [207, 473, 738, 1003, 1269]
    if mirrored:
        slot_origins = [mirror_x(x, 232) for x in slot_origins]

    slot_groups = [
        [(166, "SLOT 1", 1)],
        [(166, "SLOT 2", 1)],
        [(166, "SLOT 3", 1)],
        [(166, "SLOT 4", 1)],
        [
            (151, "Authentic", 1),
            (181, "team wins!", 1),
        ],
    ]

    slot_blocks = []
    for x, lines in zip(slot_origins, slot_groups):
        slot_blocks.append(make_slot_group(x, lines, accent_color))

    return f"""    <g transform=\"translate({BLEED_OFFSET}, {y_offset + BLEED_OFFSET + 1})\">
        <rect x=\"11\" y=\"10\" width=\"123\" height=\"502\" rx=\"13\" fill=\"none\" stroke=\"{accent_color}\" stroke-width=\"5\" opacity=\"1\" />
        <text x=\"{discard_text_x}\" y=\"277\" font-family=\"Georgia, serif\" font-size=\"33\" font-weight=\"bold\" fill=\"{accent_color}\" text-anchor=\"middle\" transform=\"rotate(-90 {discard_text_x} 261)\">DISCARD PILE</text>
        <path d=\"{discard_arrow_path}\" fill=\"{accent_color}\" opacity=\"1\" />
{chr(10).join(discard_cards)}

        <rect x=\"1568\" y=\"10\" width=\"123\" height=\"502\" rx=\"13\" fill=\"none\" stroke=\"{accent_color}\" stroke-width=\"5\" opacity=\"1\" />
        <text x=\"{draw_text_x}\" y=\"277\" font-family=\"Georgia, serif\" font-size=\"37\" font-weight=\"bold\" fill=\"{accent_color}\" text-anchor=\"middle\" transform=\"rotate(90 {draw_text_x} 261)\">DRAW PILE</text>
        <path d=\"{draw_arrow_path}\" fill=\"{accent_color}\" opacity=\"1\" />
{chr(10).join(draw_cards)}

        <rect x=\"143\" y=\"10\" width=\"1415\" height=\"502\" rx=\"13\" fill=\"none\" stroke=\"{accent_color}\" stroke-width=\"5\" opacity=\"1\" />
        <rect x=\"153\" y=\"20\" width=\"1395\" height=\"482\" rx=\"3\" fill=\"none\" stroke=\"url(#{pattern_id})\" stroke-width=\"24\" opacity=\"1\" />

        <text x=\"{title_x}\" y=\"75\" font-family=\"Georgia, serif\" font-size=\"40\" font-weight=\"bold\" fill=\"{accent_color}\" letter-spacing=\"2\">{board_name}</text>
        <line x1=\"{line_x1}\" y1=\"86\" x2=\"{line_x2}\" y2=\"86\" stroke=\"{accent_color}\" stroke-width=\"5\" opacity=\"1\" />

{''.join(slot_blocks)}
    </g>
"""


def build_fraud_board(bg_color, accent_color, board_name, y_offset=0, mirrored=False, pattern_id="border-pattern"):
    tx = mirror_x if mirrored else (lambda x, width=0: x)

    # Shift titles 1mm to center (≈4px)
    title_x = tx(54)  # 50 + 4
    line_x1 = tx(54)  # 50 + 4
    line_x2 = tx(576)  # 580 - 4
    if line_x1 > line_x2:
        line_x1, line_x2 = line_x2, line_x1

    slot_origins = [75, 340, 605, 870, 1135, 1401]
    if mirrored:
        slot_origins = [mirror_x(x, 232) for x in slot_origins]

    slot_groups = [
        [(166, "SLOT 1", 1)],
        [
            (50, "Audit", 1),
            (190, "The trader", 1),
            (215, "investigates", 1),
            (240, "a player's", 1),
            (265, "identity", 1),
            (290, "card", 1),
        ],
        [
            (50, "Sweetheart", 1),
            (75, "agreement", 1),
            (190, "The trader", 1),
            (215, "picks the", 1),
            (240, "trader for ", 1),
            (265, "the next", 1),
            (290, "round", 1),
        ],
        [
            (50, "Reorgani", 1),
            (75, "-sation", 1),
            (215, "The trader", 1),
            (240, "must fire", 1),
            (265, "a player", 1),
        ],
        [
            (50, "Reorgani", 1),
            (75, "-sation", 1),
            (215, "The trader", 1),
            (240, "must fire", 1),
            (265, "a player", 1),
        ],
        [
            (151, "Fraudster", 1),
            (181, "team wins!", 1),
        ],
    ]

    slot_blocks = []
    for x, lines in zip(slot_origins, slot_groups):
        slot_blocks.append(make_slot_group(x, lines, accent_color))

    return f"""    <g transform=\"translate({BLEED_OFFSET}, {y_offset})\">
        <rect x=\"10\" y=\"10\" width=\"1680\" height=\"502\" rx=\"13\" fill=\"none\" stroke=\"{accent_color}\" stroke-width=\"5\" opacity=\"1\" />
        <rect x=\"20\" y=\"20\" width=\"1660\" height=\"482\" rx=\"3\" fill=\"none\" stroke=\"url(#{pattern_id})\" stroke-width=\"24\" opacity=\"1\" />

        <text x=\"{title_x}\" y=\"75\" font-family=\"Georgia, serif\" font-size=\"40\" font-weight=\"bold\" fill=\"{accent_color}\" letter-spacing=\"2\">{board_name}</text>
        <line x1=\"{line_x1}\" y1=\"86\" x2=\"{line_x2}\" y2=\"86\" stroke=\"{accent_color}\" stroke-width=\"5\" opacity=\"1\" />

        <rect x=\"893\" y=\"66\" width=\"713\" height=\"13\" rx=\"3\" fill=\"none\" stroke=\"{accent_color}\" stroke-width=\"17\" opacity=\"1\" />
        <text x=\"893\" y=\"78\" font-family=\"Courier New, monospace\" font-size=\"22\" font-weight=\"bold\" fill=\"{bg_color}\" opacity=\"1\">FRAUDSTERS WIN IF TRICK-MEISTER IS ELECTED AS SUPPLIER</text>

{''.join(slot_blocks)}
        <rect x=\"140\" y=\"462\" width=\"1427\" height=\"13\" rx=\"3\" fill=\"none\" stroke=\"{accent_color}\" stroke-width=\"17\" opacity=\"1\" />
        <text x=\"150\" y=\"474\" font-family=\"Courier New, monospace\" font-size=\"22\" font-weight=\"bold\" fill=\"{bg_color}\" opacity=\"1\">7 OR 8 PLAYERS: PLAY WITH 2 FRAUDSTERS AND TRICK-MEISTER, TRICK-MEISTER DOESN'T KNOW WHO THE FRAUDSTERS ARE</text>
    </g>
"""


def create_policy_board(board_type, bg_color, accent_color, board_name):
    if board_type.lower().startswith("fraud"):
        board_inner = build_fraud_board(bg_color, accent_color, board_name, y_offset=-BLEED_OFFSET)
    else:
        board_inner = build_auth_board(bg_color, accent_color, board_name, y_offset=-BLEED_OFFSET)

    single_board_height = BOARD_HEIGHT
    svg_template = f"""<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>
<svg 
    width=\"490mm\" 
    height=\"155mm\" 
    viewBox=\"0 0 {BLEED_WIDTH} {single_board_height}\"
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
        <pattern id=\"border-pattern\" x=\"0\" y=\"0\" width=\"49\" height=\"49\" patternUnits=\"userSpaceOnUse\">
            <circle cx=\"16\" cy=\"16\" r=\"4\" fill="{accent_color}\" opacity=\"1\"/>
            <circle cx=\"40\" cy=\"40\" r=\"4\" fill="{accent_color}\" opacity=\"1\"/>
            <circle cx=\"40\" cy=\"16\" r=\"8\" fill="{accent_color}\" opacity=\"1\"/>
            <circle cx=\"16\" cy=\"40\" r=\"8\" fill="{accent_color}\" opacity=\"1\"/>
        </pattern>
    </defs>
    <rect x=\"0\" y=\"0\" width=\"{BLEED_WIDTH}\" height=\"{single_board_height}\" fill=\"{bg_color}\" />
{board_inner}
</svg>
"""
    filename = f"board_78{board_type.lower()}.svg"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_template)
    print(f"Generated: {filename}")


def create_combined_policy_board():
    combined_inner = '<g transform="translate(1737, 540) rotate(180)">\n'
    combined_inner += build_fraud_board("#231f20", "#ba293b", "FRAUDULENT TRACK", y_offset=0, mirrored=False, pattern_id="border-pattern-fraud")
    combined_inner += '</g>\n'
    combined_inner += build_auth_board("#231f20", "#0b6fb7", "AUTHENTIC TRACK", y_offset=540, mirrored=False, pattern_id="border-pattern-auth")

    svg_template = f"""<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>
<svg 
    width=\"490mm\" 
    height=\"310mm\" 
    viewBox=\"0 0 {BLEED_WIDTH} {BLEED_HEIGHT}\"
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
        <pattern id=\"border-pattern-fraud\" x=\"0\" y=\"0\" width=\"49\" height=\"49\" patternUnits=\"userSpaceOnUse\">
            <circle cx=\"16\" cy=\"16\" r=\"4\" fill=\"#ba293b\" opacity=\"1\"/>
            <circle cx=\"40\" cy=\"40\" r=\"4\" fill=\"#ba293b\" opacity=\"1\"/>
            <circle cx=\"40\" cy=\"16\" r=\"8\" fill=\"#ba293b\" opacity=\"1\"/>
            <circle cx=\"16\" cy=\"40\" r=\"8\" fill=\"#ba293b\" opacity=\"1\"/>
        </pattern>
        <pattern id=\"border-pattern-auth\" x=\"0\" y=\"0\" width=\"48\" height=\"49\" patternUnits=\"userSpaceOnUse\">
            <circle cx=\"12\" cy=\"16\" r=\"4\" fill=\"#0b6fb7\" opacity=\"1\"/>
            <circle cx=\"36\" cy=\"40\" r=\"4\" fill=\"#0b6fb7\" opacity=\"1\"/>
            <circle cx=\"36\" cy=\"16\" r=\"8\" fill=\"#0b6fb7\" opacity=\"1\"/>
            <circle cx=\"12\" cy=\"40\" r=\"8\" fill=\"#0b6fb7\" opacity=\"1\"/>
        </pattern>
    </defs>
    <rect x=\"0\" y=\"0\" width=\"{BLEED_WIDTH}\" height=\"{BLEED_HEIGHT}\" fill=\"#231f20\" />
{combined_inner}
</svg>
"""
    filename = "board_78combined.svg"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_template)
    print(f"Generated: {filename}")

create_policy_board("AUTHENTIC", "#231f20", "#0b6fb7", "AUTHENTIC TRACK")
create_policy_board("FRAUDULENT", "#231f20", "#ba293b", "FRAUDULENT TRACK")
create_combined_policy_board()