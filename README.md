# chernoff_faces
## Библиотека для построения лиц Чернова
### Про лица Чернова
Лица Чернова - метод визуализации многомерных данных с использованием схематичных лиц.
Он был придуман Германом Черновым в 1971 году.
Подробнее про него можно прочитать в [Википедии](https://ru.wikipedia.org/wiki/%D0%9B%D0%B8%D1%86%D0%B0_%D0%A7%D0%B5%D1%80%D0%BD%D0%BE%D0%B2%D0%B0),
или в [этой статье](https://courses.isds.tugraz.at/ivis/surveys/ss2013/g3-survey-chernoff.pdf).

Лица Чернова позволяют визуализировать до 18 параметров путём изменения разных черт лица - формы лица, размера, глаз, носа, рта и т.д.

Пример случайных лиц Чернова, которые сгенерированы с помощью данной библиотеки:
![20 случайно сгенерированных лиц](examples/random_faces/random_faces.png)
### Применение библиотеки
Все файлы с примерами применения библиотеки доступны в папке `examples`.

Для построения лица используется функция `draw_face` она принимает словарь с параметрами лица и подпись к нему и возвращает объект типа `Face`

Словарь с параметрами лица должен быть построен следующим образом:
в качестве ключей должны быть строки с названиями параметра, а в качестве значений числа от 0 до 1.

Возможные параметры лица (их описания можно найти в docstring функции draw_face):
```
radius_to_corner
angle_to_corner
vertical_size
upper_part_eccentricity
lower_part_eccentricity
nose_length
mouth_vertical_pos
mouth_curvature
mouth_length
eyes_vertical_pos
eyes_horizontal_pos
eyes_slant
eyes_eccentricity
eyes_size
pupils_position
eyebrows_vertical_pos
eyebrows_slant
eyebrows_size
```
Пример создания лица с большими глазами и грустным ртом (не указанные параметры в словаре будут приняты за значение 0.5) и подписью "my face":
```py
my_face = chernoff_face.draw_face({"eyes_size": 1, "mouth_curvature": 0}, "my face")
```
Объект класса Face может быть использован далее тремя способами:

- Для создания одного изображения с лицом (пример использования этого метода и результат можно найти в папке [`default_face`](examples/default_face)):
```py
my_face.to_image("my_face.png")
```
- Разместить его поверх другого изображения PIL (Пример в папке [`covid_visualization`](examples/covid_visualization))
```py
my_image = PIL.Image.open("my_image.png")
my_face.draw_on_image((570, 770), my_image)
```
- Разместить несколько лиц в виде сетки заданной размерности (Примеры в папках [`random_faces`](examples/random_faces) и
[`iris_visualization`](examples/iris_visualization))

```py
chernoff_face.draw_grid(my_faces, 3, 5, "my_faces.png")
```
