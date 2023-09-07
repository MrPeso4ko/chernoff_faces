import math

from PIL import Image

sz = 130

x_low = -sz
x_high = sz
y_low = -sz
y_high = sz


# добавить документацию
# разбить файл
# добавить документацию к коду
# прогнать на каком-то датасете



px = [[]]
ox = oy = 0


def main():
    global ox, oy, px
    img = Image.new("1", (x_high - x_low, y_high - y_low), "white")



    pixels = img.load()
    ox, oy = -x_low, -y_low

    params = [0.5] * 18

    # обязательно сделать дефолтные значения



    draw_face(params)

    for x in range(x_high - x_low):
        for y in range(y_high - y_low):
            pixels[x, y] = px[x][y]
    img.save("face.png", "png")


if __name__ == '__main__':
    main()
