"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""
import board
import terminalio
import displayio
import time
import pwmio
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction
# Starting in CircuitPython 9.x fourwire will be a seperate internal library
# rather than a component of the displayio library
try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire
from adafruit_display_text import label
from adafruit_st7789 import ST7789

# First set some parameters used for shapes and text
BORDER = 20
FONTSCALE = 2
BACKGROUND_COLOR = 0x00FF00  # Bright Green
FOREGROUND_COLOR = 0xAA0088  # Purple
TEXT_COLOR = 0xFFFF00

# Release any resources currently in use for the displays
displayio.release_displays()

spi = board.SPI()
tft_cs = board.D2
tft_dc = board.D3

display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(
    display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53
)

# Make the display context
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(
    display.width - BORDER * 2, display.height - BORDER * 2, 1
)
inner_palette = displayio.Palette(1)
inner_palette[0] = FOREGROUND_COLOR
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)

# Draw a label

pot = AnalogIn(board.A0)

updating_label = label.Label(
font=terminalio.FONT, text=str ("hi"), scale=2)
updating_label.anchor_point = (0, 0)
updating_label.anchored_position = (20, 20)
splash.append(updating_label)


MAXpot = 65535
x = 0
v = 65535
p = 0

while True:

    a = pot.value
    b = (a /MAXpot) * 3.3
    c = (b - 0.5) * 100
    d = (c*(1.8) + 32.0)
    e = round(d,2)
    print(e)
    text = str (e) + " Deg F"
    text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
    text_width = text_area.bounding_box[2] * FONTSCALE
    text_group = displayio.Group(
        scale=FONTSCALE,
        x=display.width // 2 - text_width // 2,
        y=display.height // 2,
    )
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)

    # add label to group that is showing on display
    updating_label.text = str (e)
    time.sleep(5)
    splash.remove(text_group)
