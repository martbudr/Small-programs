from typing import NamedTuple

SCORE_FONT = ("Helvetica", 24)
SCORE_COLOR = "#000000"
CELL_FONT = ("Helvetica", 16)
BG_COLOR = "#E0EDCA"
EMPTY_CELL_COLOR = "#E9F2DA"
GRID_COLOR = "#BBD789"
WON_FONT_COLOR = "green"
LOST_FONT_COLOR = "red"

class CellColor(NamedTuple):
    color: str
    font: str
    
CELL_COLORS = {
    2: CellColor(color="#CEEC97", font="#000000"),
    4: CellColor(color="#E1D095", font="#000000"),
    8: CellColor(color="#F4B393", font="#000000"),
    16: CellColor(color="#F69F99", font="#000000"),
    32: CellColor(color="#F88A9E", font="#000000"),
    64: CellColor(color="#FC60A8", font="#000000"),
    128: CellColor(color="#BB44BA", font="#000000"),
    256: CellColor(color="#9B36C3", font="#000000"),
    512: CellColor(color="#7A28CB", font="#000000"),
    1024: CellColor(color="#62369A", font="#DFDDEB"),
    2048: CellColor(color="#494368", font="#DFDDEB"),
}