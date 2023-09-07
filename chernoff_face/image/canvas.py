from PIL import Image


class Canvas:
    """Two-dimensional array of 1s and 0s, where 0 represent black pixel and 1 represent white pixel"""

    def __init__(self, x_low, x_high, y_low, y_high):
        """Initializes canvas
        :param x_low: minimal x coordinate of image
        :param x_high: maximal x coordinate of image
        :param y_low: minimal y coordinate of image
        :param y_high: maximal y coordinate of image"""
        self.x_low = x_low
        self.x_high = x_high
        self.y_low = y_low
        self.y_high = y_high
        self.ox, self.oy = -x_low, -y_low
        self.px = [[1] * (y_high - y_low) for _ in range(x_high - x_low)]

    def __getitem__(self, item):
        if 0 <= item < len(self.px):
            return self.px[item]
        else:
            raise IndexError

    def to_image(self, filename="face"):
        img = Image.new("1", (self.x_high - self.x_low, self.y_high - self.y_low), "white")
        pixels = img.load()
        for x in range(self.x_high - self.x_low):
            for y in range(self.y_high - self.y_low):
                pixels[x, y] = self.px[x][y]
        img.save("{}.png".format(filename), "png")
