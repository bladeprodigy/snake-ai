import pygame
import random
import math


pygame.init()


class SnakeGame:
    def __init__(self):
        self.window_width = 800
        self.window_height = 600
        self.game_window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Snake')

        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)

        self.snake_size = 20
        self.snake_pos = [self.window_width // 2, self.window_height // 2]
        self.snake_body = [self.snake_pos.copy()]
        self.direction = None
        self.change_to = self.direction

        self.food_pos = self.generate_food()
        self.food_size = 20
        self.score = 0

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 25)

        self.last_moves = []
        self.move_limit = 100
        self.moves_without_food = 0

    def generate_food(self):
        while True:
            x = random.randrange(1, (self.window_width // self.snake_size)) * self.snake_size
            y = random.randrange(1, (self.window_height // self.snake_size)) * self.snake_size
            food_position = [x, y]
            if food_position not in self.snake_body:
                return food_position

    def angle_with_food(self):
        head_x, head_y = self.snake_pos
        food_x, food_y = self.food_pos
        delta_x = food_x - head_x
        delta_y = food_y - head_y
        angle = math.atan2(delta_y, delta_x)
        return math.degrees(angle)

    def play_game(self, net):
        total_distance_moved_towards_food = 0
        initial_angle = self.angle_with_food()
        final_angle = initial_angle

        try:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        final_angle = self.angle_with_food()
                        return self.score, len(
                            self.snake_body), total_distance_moved_towards_food, initial_angle, final_angle

                state = self.get_state()
                action = net.activate(state)
                self.direction = self.select_action(action)

                self.move_snake(self.direction)
                self.snake_body.insert(0, list(self.snake_pos))

                if self.snake_pos == self.food_pos:
                    self.score += 1
                    self.food_pos = self.generate_food()
                    self.move_limit = 100
                    self.moves_without_food = 0
                else:
                    self.snake_body.pop()
                    self.move_limit -= 1
                    self.moves_without_food += 1

                if self.is_collision() or self.move_limit == 0:
                    final_angle = self.angle_with_food()
                    break

                current_distance_to_food = abs(self.food_pos[0] - self.snake_pos[0]) + abs(
                    self.food_pos[1] - self.snake_pos[1])
                total_distance_moved_towards_food += current_distance_to_food

                self.game_window.fill(self.black)
                self.draw_snake()
                self.draw_food()
                self.show_score()
                pygame.display.update()
                self.clock.tick(100)

        except Exception as e:
            print(f"Exception occurred: {e}")

        return self.score, len(self.snake_body), total_distance_moved_towards_food, initial_angle, final_angle

    def select_action(self, output):
        suggested_direction = ['UP', 'RIGHT', 'DOWN', 'LEFT'][output.index(max(output))]
        if (suggested_direction == 'UP' and self.direction == 'DOWN') or \
                (suggested_direction == 'DOWN' and self.direction == 'UP') or \
                (suggested_direction == 'LEFT' and self.direction == 'RIGHT') or \
                (suggested_direction == 'RIGHT' and self.direction == 'LEFT'):
            return self.direction
        return suggested_direction

    def move_snake(self, direction):
        if direction == 'UP':
            self.snake_pos[1] -= self.snake_size
        elif direction == 'DOWN':
            self.snake_pos[1] += self.snake_size
        elif direction == 'LEFT':
            self.snake_pos[0] -= self.snake_size
        elif direction == 'RIGHT':
            self.snake_pos[0] += self.snake_size

        self.last_moves.append(direction)
        if len(self.last_moves) > 10:
            self.last_moves.pop(0)

    def get_last_moves(self):
        return self.last_moves

    def is_collision(self):
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.window_width - self.snake_size:
            return True
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.window_height - self.snake_size:
            return True
        for block in self.snake_body[1:]:
            if self.snake_pos == block:
                return True
        return False

    def draw_snake(self):
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, self.green,
                             pygame.Rect(pos[0], pos[1], self.snake_size, self.snake_size))

    def draw_food(self):
        pygame.draw.rect(self.game_window, self.red,
                         pygame.Rect(self.food_pos[0], self.food_pos[1], self.food_size, self.food_size))

    def show_score(self):
        score_text = self.font.render("Score: " + str(self.score), True, self.white)
        self.game_window.blit(score_text, [0, 0])

    def get_state(self):
        head_x, head_y = self.snake_pos

        dist_to_wall_up = (head_y / self.snake_size) / (self.window_height / self.snake_size)
        dist_to_wall_down = ((self.window_height - head_y) / self.snake_size) / (self.window_height / self.snake_size)
        dist_to_wall_left = (head_x / self.snake_size) / (self.window_width / self.snake_size)
        dist_to_wall_right = ((self.window_width - head_x) / self.snake_size) / (self.window_width / self.snake_size)

        food_dx = (self.food_pos[0] - head_x) / self.window_width
        food_dy = (self.food_pos[1] - head_y) / self.window_height

        danger_up = (head_y - self.snake_size < 0 or [head_x, head_y - self.snake_size] in self.snake_body)
        danger_down = (head_y + self.snake_size >= self.window_height or [head_x,
                                                                          head_y + self.snake_size] in self.snake_body)
        danger_left = (head_x - self.snake_size < 0 or [head_x - self.snake_size, head_y] in self.snake_body)
        danger_right = (head_x + self.snake_size >= self.window_width or [head_x + self.snake_size,
                                                                          head_y] in self.snake_body)

        angle = self.angle_with_food()

        return [
            food_dx,
            food_dy,
            danger_up,
            danger_down,
            danger_left,
            danger_right,
            dist_to_wall_up,
            dist_to_wall_down,
            dist_to_wall_left,
            dist_to_wall_right,
            angle
        ]

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != 'DOWN':
                    self.direction = 'UP'
                elif event.key == pygame.K_DOWN and self.direction != 'UP':
                    self.direction = 'DOWN'
                elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                    self.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                    self.direction = 'RIGHT'
        return True

    def update_game_state(self):
        self.move_snake(self.direction)
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos == self.food_pos:
            self.score += 1
            self.food_pos = self.generate_food()
        else:
            self.snake_body.pop()

    def render_game(self):
        self.game_window.fill(self.black)
        self.draw_snake()
        self.draw_food()
        self.show_score()
        pygame.display.flip()

    def run_game(self):
        running = True
        while running:
            running = self.process_events()
            self.update_game_state()

            if self.is_collision():
                print("Game Over! Your final score is: ", self.score)
                break

            self.render_game()
            self.clock.tick(100)

        pygame.time.delay(2000)
        pygame.quit()
