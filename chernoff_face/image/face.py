import os

import PIL.Image
from PIL import Image, ImageDraw, ImageFont


class Face:
    """Two-dimensional array of 1s and 0s, where 0 represent black pixel and 1 represent white pixel"""
    caption_font_size = 22
    x_low = -150
    x_high = 150
    y_low = -150
    y_high = 150

    def __init__(self, caption: str):
        """Initializes face canvas
        :param x_low: minimal x coordinate of image
        :param x_high: maximal x coordinate of image
        :param y_low: minimal y coordinate of image
        :param y_high: maximal y coordinate of image"""

        self.px = [[1] * (self.y_high - self.y_low) for _ in range(self.x_high - self.x_low)]
        self.caption = caption
        p = os.path.dirname(__file__)
        fontpath = os.path.abspath(os.path.join(p, "arial.ttf"))
        self.font = ImageFont.truetype(fontpath, size=self.caption_font_size)
        bbox = self.font.getbbox(self.caption)
        self.caption_size = bbox[2] - bbox[0], bbox[3] - bbox[1]
        self.ox, self.oy = -self.x_low, -self.y_low + self.caption_size[1]

    def __getitem__(self, item):
        if 0 <= item < len(self.px):
            return self.px[item]
        else:
            raise IndexError

    def _caption_coords(self) -> tuple[int, int]:
        """:returns: Coordinates of face's caption top left corner"""
        return self.ox - self.caption_size[0] // 2, 15

    def to_image(self, filename="face"):
        img = Image.new("1", (self.x_high - self.x_low, self.y_high - self.y_low), "white")
        pixels = img.load()
        for x in range(self.x_high - self.x_low):
            for y in range(self.y_high - self.y_low):
                pixels[x, y] = self.px[x][y]
        draw = ImageDraw.Draw(img)
        draw.text(self._caption_coords(), self.caption, font=self.font)
        img.save(filename)

    def draw_on_image(self, coords: tuple[int, int], img: PIL.Image.Image):
        pixels = img.load()
        for x in range(self.x_high - self.x_low):
            for y in range(self.y_high - self.y_low):
                pixels[x + coords[0], y + coords[1]] = self.px[x][y]
        draw = ImageDraw.Draw(img)
        cap_coords = self._caption_coords()
        draw.text((cap_coords[0] + coords[0], cap_coords[1] + coords[1]), self.caption, font=self.font)
