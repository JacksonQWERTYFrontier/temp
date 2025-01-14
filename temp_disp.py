import time
import board
import terminalio
import displayio
from analogio import AnalogIn
from adafruit_ms8607 import MS8607
from adafruit_display_text import label
from fourwire import FourWire
from adafruit_st7789 import ST7789

# Set some parameters used for shapes and text
BORDER = 20
FONTSCALE = 2
BACKGROUND_COLOR = 0xAA0000  # Black
FOREGROUND_COLOR = 0xAA0000  # Purple
TEXT_COLOR = 0xFFFFFF

# Release any resources currently being used
displayio.release_displays()

# Initialize I2C and the MS8607 sensor
i2c = board.I2C()  # Initialize I2C bus
sensor = MS8607(i2c)  # Create MS8607 sensor object

# Set up SPI 
temp = AnalogIn(board.A0)
spi = board.SPI()
tft_cs = board.D2
tft_dc = board.D3
display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(
    display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53
)

# display context
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# This draws a smaller rectangle
inner_bitmap = displayio.Bitmap(
    display.width - BORDER * 2, display.height - BORDER * 2, 1
)
inner_palette = displayio.Palette(1)
inner_palette[0] = FOREGROUND_COLOR
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)

# This is the main Counter for cycling through Pressure, Humidity, and Temperature
counter = 0
maxxed = 65535
vlt = 0
# This is the main loop to display sensor data
while True:
    hot = temp.value / maxxed * 3.3
    temp_C = (hot - .5) *100
    temp_F = (9/5) * temp_C +32
    hot = round(temp_F,2)
    print(temp_F)
    pressure = sensor.pressure  
    humidity = sensor.relative_humidity
    if counter == 0:
        text = "Humidity: %.2f %% " % humidity
    elif counter == 1:
        text = "Pressure: %.2f hPa" % pressure
    elif counter == 2:
        text = str (hot) + " F"
    counter += 1
    if counter >= 3:
        counter = 0  
    text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
    text_width = text_area.bounding_box[2] * FONTSCALE
    text_group = displayio.Group(
        scale=FONTSCALE,
        x=display.width // 2 - text_width // 2,
        y=display.height // 2,
    )
    text_group.append(text_area)  
    splash.append(text_group)
    time.sleep(3)
    splash.remove(text_group)
