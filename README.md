#  B💣mberman!!! #
*[28.02.2025]*

Веб-игра на питоне на:
- python arcade-3.0.1 library
- websockets-15.0 (планируется)
  
## Описание геймплея ##
Будет доступно несколько режимов игры:
- Однопользовательская против компьютера
- Для двоих на одной машине
- Для двоих по локальной сети

Классическая игра Bomberman на игровой приставке Dendi с нововедениями (возможно)

<details>
<summary>ДОКА</summary>
<br>

[*Game*](https://github.com/SPSUITD/2-md-15-ShtonDeLon/blob/master/game.py)
- Инициализирует игровое окно
  ```
  def __init__(self):
      super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
      self.background_color = arcade.csscolor.LIGHT_GREEN
  ```
- Инициализирует игроков
  ```
  def __new__player__(self, name = "player", position = Vector(0, 0), rotation = 0, size = 1, speed = 5, keymap = KeyMap(), spawn_object = None):
          player = Player(
              sprite=arcade.Sprite(arcade.load_texture(TEXTURES.PLAYER_TEXTURE)),
              name=name,
              size=size,
              rotation=rotation,
              position=position,
              speed=speed,
              keymap=keymap,
              spawner=Spawner(external_spawn=self.spawn, abstract_object=spawn_object) if spawn_object is not None else None
          )
          self.game_objects.append(player)
          self.sprite_list.append(player.sprite)
          self.controllers.append(player.controller)
  ```
- Создает абстрактные геймобджекты для спавна
  ```
  self.box = AbstractObject(
      sprite_path=TEXTURES.BOX,
      name='box',
      size=0.5
      )
        
  self.box1 = AbstractObject(
      sprite_path=TEXTURES.BOX1,
      name='box',
      size=0.5
      )
  ```
- Перемещает центр координат игрового мира в центр игрового окна
  - Путем создания дополнительной камеры
    ```
    def __camera_setup(self):
        self.camera = arcade.camera.Camera2D()
        self.camera.use()
        self.camera.position = (0, 0)
        self.game_objects.append(self.camera)
    ```
- Обрабатывает инпуты
  ```
  def on_key_press(self, key, modifiers):
      for c in self.controllers:
          c.on_key_press(key)

  def on_key_release(self, key, modifiers):
      for c in self.controllers:
          c.on_key_release(key)
  ```
- В цикле обновляет состояния контроллеров
  ```
  def on_update(self, delta_time = 1/30):
      for c in self.controllers:
      c.on_update()
  ```
- Отрисовывает сцену со всеми спрайтами геймобджектов
  ```
  def on_draw(self):
      self.clear()
      self.camera.use()
      self.sprite_list.draw()
  ```
  

### *src:* ###
- [*Vector*](https://github.com/SPSUITD/2-md-15-ShtonDeLon/blob/master/src/vector.py)
  - Реализует структуру плоского вектора с полями X и Y
  - Имеет метод нахождения длины
    ```
    def lenght(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    ```
  - Имеет метод нормализации (для односкоростного передвижения и по диагонали)
    ```
    def normalize(self):
        l = self.lenght()
        if l != 0:
            self.x /= l
            self.y /= l
    ```

- [*AbstractObject*](https://github.com/SPSUITD/2-md-15-ShtonDeLon/blob/master/src/abstractobject.py)
  - Хранит в себе путь к спрайту объекта
  - Размер
  - Имя объекта
    
- [*GameObject*](https://github.com/SPSUITD/2-md-15-ShtonDeLon/blob/master/src/gameobject.py)
  - Создает именнованный игровой объект со спрайтом и его настройкой (положением и размером)
  - Имеет метод передвижения (пока что изменяет положение центра спрайта)
  - Сеттер положения
    ```
    def set_position(self, position: Vector):
        self.sprite.center_x = position.x
        self.sprite.center_y = position.y
    ```
  - Геттер положения
    ```
    def get_position(self):
        return Vector(self.sprite.center_x, self.sprite.center_y)
    ```
  - Метод поворота спрайта (на будущее, но может не пригодится)
    ```
    def rotate(self, a: float):
        self.sprite.angle += a
    ```
  - Метод передвижения геймобджекта (пока что центра спрайта)  
    ```
    def move(self, v: Vector):
        self.sprite.center_x += v.x * self.speed
        self.sprite.center_y += v.y * self.speed
    ```
    
- [*Player(GameObject)*](https://github.com/SPSUITD/2-md-15-ShtonDeLon/blob/master/src/player.py)
  - Наследуемый класс от [*GameObject*](https://github.com/SPSUITD/2-md-15-ShtonDeLon/blob/master/src/gameobject.py)
  - Также имеет поле controller: [*PlayerController*](https://github.com/SPSUITD/2-md-15-ShtonDeLon/blob/master/src/playercontroller.py) по которому обрабатываются нажатия на клавиши в GameView в [*Game*](https://github.com/SPSUITD/2-md-15-ShtonDeLon/blob/master/game.py)
      
- [*KeyMap*](https://github.com/SPSUITD/2-md-15-ShtonDeLon/blob/master/src/keymap.py)
  - Хранит в себе ключи клавиш клавиатуры:
    - left
    - up
    - right
    - down
    - spawn (не обязательное поле)

- [*Spawner*](https://github.com/SPSUITD/2-md-15-ShtonDeLon/blob/master/src/keymap.py)
  - Хранит внешнюю функцию спавна (из GameView `spawn()`) в поле `__external_spawn`
  - Реализует метод вызова этой функции
    ```
    def spawn(self, position: Vector):
        if self.__abstract_object is not None:
            self.__external_spawn(self.__abstract_object, position)
    ```
  
- [*PlayerController*](https://github.com/SPSUITD/2-md-15-ShtonDeLon/blob/master/src/playercontroller.py)
  - Обработчик импутов клавиатуры
  - Хранит в себе экземпляр класса [*Spawner*](https://github.com/SPSUITD/2-md-15-ShtonDeLon/blob/master/src/keymap.py)
  - Хранит в себе экземпляр класса [*KeyMap*](https://github.com/SPSUITD/2-md-15-ShtonDeLon/blob/master/src/keymap.py)
  - Хранит один управляемый [*GameObject*](https://github.com/SPSUITD/2-md-15-ShtonDeLon/blob/master/src/gameobject.py)
  - Имеет поле направления (для функции перемещения), которое меняется в `on_key_press(key, modifiers)` и `on_key_release(key, modifiers)`
  - При нажатии клавиш, обрабатываемых в GameView в [*Game*](https://github.com/SPSUITD/2-md-15-ShtonDeLon/blob/master/game.py), вызывается on_key_press во всех созданных контроллерах:
    ```
    def on_key_press(self, key, modifiers):
        for c in self.controllers:
            c.on_key_press(key)
    ```
  - При отпускании клавиш, обрабатываемых в GameView в [*Game*](https://github.com/SPSUITD/2-md-15-ShtonDeLon/blob/master/game.py), вызывается on_key_release во всех созданных контроллерах:
    ```
    def on_key_release(self, key, modifiers):
        for c in self.controllers:
            c.on_key_release(key)
    ```
  - При обновлении в GameView в Game вызывается обновление управляемых игровых объектов:
    ```
    def on_update(self, delta_time = 1/30):
        for c in self.controllers:
             c.on_update()
    ```
    В котором вызывается функция передвижения управляемого геймобджекта с передачей направления:
    ```
    def on_update(self):
        self.game_object.move(self.direction)
    ```
    
- [*Logger*](https://github.com/SPSUITD/2-md-15-ShtonDeLon/blob/master/src/logger.py)
  - Деббажный класс
  - Используется для логонирования
  - Имеет методы `Error(msg)`, `Message(msg)`, `Warning(msg)` с разными цветовыми выделениями
  - При выводе также указыается время лога
    
- *Config*
  - ГитИгнорный класс (создайте сами)
  - Используется для хранения путей к файлам на компьютере (пример):
    ```
    class TEXTURES:
        PLAYER_TEXTURE = "fullpath/image.png"
        BOX = "fullpath/image.png"
        BOX1 = "fullpath/image.png"
        ...
    ```

</details>
