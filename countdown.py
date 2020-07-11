import os
import ctypes
from time import sleep
from datetime import datetime
from win32api import GetSystemMetrics
from PIL import Image, ImageDraw, ImageFont, ImageFilter


DAY = 27  # Day of your birthday
MONTH = 11  # Month of your birthday (11 = November)
FONT_NAME = 'Arial.ttf'  # Name of the font used for the text
FONT_SIZE = 150  # Size of the font
TEXT_COLOR = (0, 0, 0, 255)  # Color of the text in RGBA (red, green, blue, alpha)
BACKGROUND_COLOR = (255, 255, 255)  # Background color in RGB (useless if you pass image)
BACKGROUND_IMG = ''  # Optional, adds background image with that path
BLUR = 0  # Optional, blurs the background image
POSITION = 'center'  # Options: nw, n, ne, w, center, e, sw, s, se


class Counter:
    def __init__(self, day, month, pos, bg=None, blur=0):
        self.day = day
        self.month = month
        self.pos = pos
        self.bg = bg
        self.blur = blur

    def create_image(self, text):
        WIDTH, HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)

        if self.bg is not None:
            new = Image.open(self.bg).resize((WIDTH, HEIGHT))
            new = new.filter(ImageFilter.GaussianBlur(BLUR))
        else:
            new = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND_COLOR)

        font = ImageFont.truetype(f'C:/Windows/Fonts/{FONT_NAME}', FONT_SIZE)
        draw = ImageDraw.Draw(new)
        text = '{:,}'.format(text)
        x, y = draw.textsize(text, font=font)

        positions = {'nw': (0, 0),
                     'n': (WIDTH // 2 - x // 2, 0),
                     'ne': (WIDTH - x, 0),
                     'w': (0, HEIGHT // 2 - y // 2),
                     'center': (WIDTH // 2 - x // 2, HEIGHT // 2 - y // 2),
                     'e': (WIDTH - x, HEIGHT // 2 - y // 2),
                     'sw': (0, HEIGHT - y - HEIGHT // 15),
                     's': (WIDTH // 2 - x // 2, HEIGHT - y - HEIGHT // 15),
                     'se': (WIDTH - x, HEIGHT - y - HEIGHT // 15)}

        draw.text(positions[self.pos], text, font=font, fill=TEXT_COLOR)
        return new

    def get_time_left(self):
        now = datetime.now()
        date = now.replace(day=self.day, month=self.month, hour=0, minute=0, second=0)
        if date > now:
            return int((date - now).total_seconds())
        else:
            date = date.replace(year=now.year + 1)
            return int((date - now).total_seconds())

    def change_wallpaper(self):
        NAME = "countdown.bmp"
        secs = self.get_time_left()
        img = self.create_image(secs)
        img.save(NAME)
        ABS_PATH = os.path.abspath(NAME)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, ABS_PATH, 0)

    def main(self):
        while True:
            self.change_wallpaper()
            sleep(1)


if BACKGROUND_IMG:
    counter = Counter(DAY, MONTH, POSITION, BACKGROUND_IMG, BLUR)
else:
    counter = Counter(DAY, MONTH, POSITION)

counter.main()
