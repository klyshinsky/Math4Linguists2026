# Данный файл генерирует видео с примером разбора строк конечным автоматом.
# Импортируем библиотеку для генерации красивых видосиков.
import manim as ma

# Класс для генерации должен наследоваться от Scene и обладать методом construct.
# Нет, в самом лучшем случае надо было написать движок для интерпретации конечного автомата,
# но я этого не сделал.
class CreateCircle(ma.Scene):
    # Эта функция будет отрисовывать состояния в виде окружностей.
    def create_states(self):
        # Радиусы окружностей, часть из них вложенные с меньшим радиусом.
        radii = [0.5, 0.5, 0.4, 0.5, 0.4, 0.5, 0.4, 0.5, 0.4, 0.5]
        # Положения окружностей (могут задаваться через константы Manim).
        shifts = [3 * ma.LEFT + 2.5 * ma.UP, 
                  0.5 * ma.LEFT + 2.5 * ma.UP, 
                  0.5 * ma.LEFT + 2.5 * ma.UP,
                  2 * ma.RIGHT + 2.5 * ma.UP, 
                  2 * ma.RIGHT + 2.5 * ma.UP,
                  2 * ma.RIGHT,
                  2 * ma.RIGHT,
                  4.5 * ma.RIGHT,
                  4.5 * ma.RIGHT,
                  2 * ma.RIGHT + 2.5 * ma.DOWN,
                 ]
        # Метки состояний.
        labels = ["p0", "p1", "p2", "p3", "p4", "p5"]
        # Координаты меток.
        label_shifts = [3 * ma.LEFT + 2.5 * ma.UP, 
                        0.5 * ma.LEFT + 2.5 * ma.UP, 
                        2 * ma.RIGHT + 2.5 * ma.UP, 
                        2 * ma.RIGHT,
                        4.5 * ma.RIGHT,
                        2 * ma.RIGHT + 2.5 * ma.DOWN,
                       ]
        
        # Генерируем список кружочков, при этом задаем метод как они будут появляться (просто добавить).
        self.states = []
        for radius, shift in zip(radii, shifts):
            self.states.append(ma.Add(ma.Circle(radius=radius, color=ma.BLUE).shift(shift)))
        # Генерируем список меток.
        self.labels = []
        for label, shift in zip(labels, label_shifts):
            self.labels.append(ma.Add(ma.Text(label, color=ma.WHITE, font_size=24).shift(shift)))
            
        # Проигрывыаем появление кружочков и их меток.
        self.play(self.states, self.labels, ma.Wait(0.4))
        # Даем небольшую паузу.
        self.wait(0.2)

    # Данная функция будет добавлять стрелочки между состояниями, которые будут появляться не вдруг.
    def create_arrows(self):
        # Координаты дуг.
        self.arrow_coords = [([-2.5, 2.5, 0], [-1, 2.5, 0]),    # 0-1
                             ([0, 2.5, 0], [1.5, 2.5, 0]),      # 1-2
                             ([2, 2, 0], [2, 0.5, 0]),          # 2-3 
                             ([2.35, 2.15, 0], [4.25, 0.5, 0]), # 2-4
                             ([2, -0.5, 0], [2, -2, 0]),        # 3-5
                             ([2, -2, 0], [2, -0.5, 0]),        # 5-3
                             ([4.2, -0.4, 0], [4.8, -0.4, 0]),  # 4-4
                            ]
        # Для дуг стоит задать степень и направление их выгнутости.
        self.arrow_angle = [-ma.TAU/4, -ma.TAU/4, -ma.TAU/4, -ma.TAU/4, -ma.TAU/4, -ma.TAU/4, ma.TAU/2, ]
        # Генерируем список дуг, при этом говорим, что они плавно появляются, а про просто возникают.
        self.arrows = []
        for coord, angle in zip(self.arrow_coords, self.arrow_angle):
            self.arrows.append(ma.Create(ma.CurvedArrow(coord[0], coord[1], angle=angle), run_time=1))
        # У дуг есть метки.
        self.arrow_names = ["a", "b", "a", "b", "b", "a", "b"]
        # Задаем координаты меток дуг.
        self.arrow_shifts = [[0, 1.2],
                             [0, 1.2],
                             [0, 0],
                             [1.2, 1.2],
                             [1.2, 0],
                             [-1.2, 0],
                             [0, -1.5],
                            ]
        # Создаем список меток дуг, при этом говорим, что они должны красиво появляться.
        self.arrow_labels = []
        for coord, label, shift in zip(self.arrow_coords, self.arrow_names, self.arrow_shifts):
            self.arrow_labels.append(ma.Create(ma.Text(label, color=ma.WHITE, font_size=24).
                shift((coord[0][0]+coord[1][0]+shift[0])/2 * ma.RIGHT + (coord[0][1]+coord[1][1]+shift[1])/2 * ma.UP)))

        # Проигрывыаем появление дуг и их меток.
        self.play(self.arrows, self.arrow_labels, ma.Wait(0.4))
        # Даем небольшую паузу.
        self.wait(0.2)

    # Эта функция будет отрисосывать перемещение разбираемого токена.
    # В нее передеются сам токен, координаты его перемещений (и разобранной части тоже)и успешен ли разбор.
    def do_parse_token(self, token_word0, positions, success):
        parsed_word0 = ""
        # Разделим траектории оставшейся и разобранной части токена.
        positions1 = positions[0]
        positions2 = positions[1]
        
        # Создадим объекты для начального положения оставшейся и разобранной части токена.
        text01 = ma.Text(token_word0, color=ma.YELLOW, font_size=24).shift(positions1[0])
        text02 = ma.Text(parsed_word0, color=ma.LIGHT_BROWN, font_size=24).shift(positions2[0])

        # Плавно покажем их, дадим зрителю обратить на это внимание.
        self.play(ma.Create(text01), ma.Create(text02))
        self.wait(0.5)

        # Перебираем точки в траектории.
        for index in range(1, len(positions1)):
            # Создаем линии, вдоль которых двигаются части токена.
            line1 = ma.Line(positions1[index-1], positions1[index])
            line2 = ma.Line(positions2[index-1], positions2[index])
            # Проигрвыаем перемещение частей токена.
            self.play(ma.MoveAlongPath(text01, line1), ma.MoveAlongPath(text02, line2))
            # Покажем отделение символа, по которому проходил переход.
            # Отделим разобраннуючасть от оставшейся.
            token_word2 = token_word0[index:]
            parsed_word2 = token_word0[:index]
            # Создадим новые объекты для нового разделения.
            text11 = ma.Text(token_word2, color=ma.YELLOW, font_size=24).shift(positions1[index])
            text12 = ma.Text(parsed_word2, color=ma.LIGHT_BROWN, font_size=24).shift(positions2[index])
            # Попросим плавно преобразовать одно в другое.
            self.play(ma.Transform(text01, text11), ma.Transform(text02, text12))

            # Запомним старые объекты, чтобы удалить их потом.
            t1 = text01
            t2 = text02
            # Сдвиг в новое состояние.
            token_word = token_word2
            parsed_word = parsed_word2
            text01 = text11
            text02 = text12

            # Зафиксируем изменения и удалим ненужные объекты с экрана 
            # (а то они на нем так и останутся).
            self.wait(0.5)
            self.remove(t1, t2)

        # Разбор завершен, выберем цвет для обозначающего успехили неуспех прямоугольника.
        if success:
            clr = ma.GREEN
        else:
            clr = ma.RED
        
        # Для смены цвета разобранной строки создадим новый объект.
        text22 = ma.Text(parsed_word2, color=ma.YELLOW, font_size=24).shift(positions2[-1])
        # Текст и прямоугольник должны быть в группе, а то текст может оказаться под прямоугольником.
        rct = ma.Rectangle(height=1, width=2, color=clr, fill_opacity=0.2).shift(positions2[-1])
        gr = ma.VGroup().add(text22, rct)
        # Поменяли цвет, показали прямоугольник.
        self.play(
                  ma.Transform(text02, text22), 
                  ma.Create(gr)
                 )
        # Зафиксировали взгляд на прошедших изменениях, удалили за собой метки для следующей сцены.
        self.wait(1)
        self.remove(gr, text22, text02)

    # Это основная функция, которая проигрывает весь сценарий.
    def construct(self):
        # Создаем слова и кооринаты их перемещений по автомату.
        word1 = "abababa"
        positions1 = ([3 * ma.LEFT + 1.5 * ma.UP, 0.5 * ma.LEFT + 1.5 * ma.UP, 1 * ma.RIGHT + 1.5 * ma.UP, 
                       1 * ma.RIGHT, 1 * ma.RIGHT + 2.5 * ma.DOWN, 1 * ma.RIGHT, 1 * ma.RIGHT + 2.5 * ma.DOWN, 1 * ma.RIGHT
                      ],
                      [4 * ma.LEFT + 1.5 * ma.UP, 1.5 * ma.LEFT + 1.5 * ma.UP, 0 * ma.RIGHT + 1.5 * ma.UP, 
                       0 * ma.RIGHT, 0 * ma.RIGHT + 2.5 * ma.DOWN, 0 * ma.RIGHT, 0 * ma.RIGHT + 2.5 * ma.DOWN, 0 * ma.RIGHT
                      ]
                     )
        word2 = "abab"
        positions2 = ([3 * ma.LEFT + 1.5 * ma.UP, 0.5 * ma.LEFT + 1.5 * ma.UP, 1 * ma.RIGHT + 1.5 * ma.UP, 
                       1 * ma.RIGHT, 1 * ma.RIGHT + 2.5 * ma.DOWN
                      ],
                      [4 * ma.LEFT + 1.5 * ma.UP, 1.5 * ma.LEFT + 1.5 * ma.UP, 0 * ma.RIGHT + 1.5 * ma.UP, 
                       0 * ma.RIGHT, 0 * ma.RIGHT + 2.5 * ma.DOWN
                      ]
                     )
        word3 = "abaa"
        positions3 = ([3 * ma.LEFT + 1.5 * ma.UP, 0.5 * ma.LEFT + 1.5 * ma.UP, 1 * ma.RIGHT + 1.5 * ma.UP, 
                       1 * ma.RIGHT, 
                      ],
                      [4 * ma.LEFT + 1.5 * ma.UP, 1.5 * ma.LEFT + 1.5 * ma.UP, 0 * ma.RIGHT + 1.5 * ma.UP, 
                       0 * ma.RIGHT, 
                      ]
                     )

        
        # Создаем состояния, дуги, проигрываем три сцены.
        self.create_states()
        self.create_arrows()
        self.do_parse_token(word1, positions1, True)    
        self.do_parse_token(word2, positions2, False)    
        self.do_parse_token(word3, positions3, False)    

if __name__ == "__main__":
    ci = CreateCircle()
    # Если запустить этот скрипт 100 раз, можно получить 5800 коротких видосико на диске. Стоит чистить временные файлы.
    # !rm media/videos/720p60/partial_movie_files/CreateCircle/*.mp4

    # Как зовут файл с итоговым видео.
    ma.config.output_file = "FA_parse"
    # Разрешение ролика.
    ma.config.frame_size = (1280, 720)

    # Уже начинай генерировать видео.
    ci.render()


# ci.call_it()