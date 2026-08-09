from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.core.window import Window
import random

GRID_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 30

class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snake = [(10, 15), (9, 15), (8, 15)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.score_label = None

        Window.bind(on_key_down=self.on_key_down)
        Clock.schedule_interval(self.update, 0.15)

    def spawn_food(self):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in self.snake:
                return pos

    def on_key_down(self, window, key, *args):
        if key == 273 and self.direction != (0, -1):      # up
            self.next_direction = (0, 1)
        elif key == 274 and self.direction != (0, 1):     # down
            self.next_direction = (0, -1)
        elif key == 276 and self.direction != (1, 0):      # left
            self.next_direction = (-1, 0)
        elif key == 275 and self.direction != (-1, 0):     # right
            self.next_direction = (1, 0)

    def update(self, dt):
        if self.game_over:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        if not (0 <= new_head[0] < GRID_WIDTH) or not (0 <= new_head[1] < GRID_HEIGHT):
            self.game_over = True
            return

        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(0.1, 0.1, 0.1, 1)
            Rectangle(pos=self.pos, size=self.size)

            Color(0, 1, 0, 1)
            for segment in self.snake:
                x = segment[0] * GRID_SIZE
                y = segment[1] * GRID_SIZE
                Rectangle(pos=(x, y), size=(GRID_SIZE - 2, GRID_SIZE - 2))

            Color(1, 0, 0, 1)
            fx = self.food[0] * GRID_SIZE
            fy = self.food[1] * GRID_SIZE
            Rectangle(pos=(fx, fy), size=(GRID_SIZE - 2, GRID_SIZE - 2))

        if self.score_label:
            self.score_label.text = f"Score: {self.score}" + (
                "  GAME OVER" if self.game_over else ""
            )


class SnakeApp(App):
    def build(self):
        Window.size = (GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE + 40)

        root = BoxLayout(orientation='vertical')
        score_label = Label(text="Score: 0", size_hint=(1, None), height=40)
        game = SnakeGame()
        game.score_label = score_label

        root.add_widget(score_label)
        root.add_widget(game)
        return root


if __name__ == '__main__':
    SnakeApp().run()

