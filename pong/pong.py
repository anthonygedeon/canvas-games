import random
import os

import pygame

class Color:
    white = (255, 255, 255)
    black = (0, 0, 0)

class ScoreBoard:
    def __init__(self):
        self.score = 0

    def add_to_score(self):
        self.score += 1
        return self.score

    @property
    def get_current_score(self):
        return self.score


class Start:

    width = 800
    height = 500

    def __init__(self):

        pygame.init()
        pygame.key.set_repeat(50, 50)

        score_left = ScoreBoard()
        score_right = ScoreBoard()
    
        pygame.display.set_caption("Pong")
        font = pygame.font.Font(os.path.join("pong", "font", "Pong.ttf"), 72)

        pong_ball = PongBall()
        left_paddle = PongPaddle(pygame.K_w, pygame.K_s)
        right_paddle = PongPaddle(pygame.K_UP, pygame.K_DOWN)

        # Clock Settings
        self.fps = 60
        self.clock = pygame.time.Clock()

        # Pygame Settings
        self.screen = pygame.display.set_mode([self.width, self.height])

        self.running = True

        self.MARGIN_LEFT = left_paddle.rect.width
        self.MARGIN_RIGHT = self.width - right_paddle.rect.width * 2

        # Sprite Handling
        self.pong_sprites = pygame.sprite.Group()

        # Handle position of LEFT Paddle
        left_paddle.rect.y = (self.height - left_paddle.height) // 2
        left_paddle.rect.x = self.MARGIN_LEFT

        # Handle position of RIGHT Paddle
        right_paddle.rect.y = (self.height - right_paddle.height) // 2
        right_paddle.rect.x = self.MARGIN_RIGHT

        # Position the Pong Ball in the center of window
        pong_ball.spawn()

        self.pong_sprites.add(pong_ball, left_paddle, right_paddle)

        while self.running:

            self.pong_sprites.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(Color.black)
            self.pong_sprites.draw(self.screen)

            # Draw Net
            for box in range(0, self.width, 40):
                pygame.draw.rect(self.screen, Color.white, [self.width // 2, box, 10, 20])

            # Collision Detection for Ping Pong Ball
            pong_ball.handle_collision_detection(left_paddle, right_paddle)

            # This makes sure that the pong ball doesn't leave the window
            if pong_ball.rect.x > self.width:
                pong_ball.spawn()
                score_left.add_to_score()
            elif pong_ball.rect.x < 0:
                pong_ball.spawn()
                score_right.add_to_score()

            score_1 = font.render(str(score_left.get_current_score), True, Color.white)
            score_2 = font.render(str(score_right.get_current_score), True, Color.white)

            self.screen.blit(score_1, (((self.width - 58) // 2) - 150, 20))
            self.screen.blit(score_2, (((self.width - 58) // 2) + 150, 20))

            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(self.fps)

        pygame.quit()


class PongBall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.width = 20
        self.height = self.width

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(Color.white)
        self.image.set_colorkey()

        pygame.draw.rect(self.image, Color.white, [0, 0, self.width, self.height])

        self.vector = pygame.Vector2(10, 0)

        self.rect = self.image.get_rect()

    def handle_collision_detection(self, object_a, object_b):
        if self.rect.colliderect(object_a.rect):
            self.vector = pygame.Vector2(-10, random.randrange(0, 10))
        elif self.rect.colliderect(object_b.rect):
            self.vector = pygame.Vector2(10, (random.randrange(0, 10) * -1))

        if self.rect.y < 0:
            self.vector = pygame.Vector2(10, -10)
        elif self.rect.y > Start.height:
            self.vector = pygame.Vector2(10, 10)

    def spawn(self):
        self.vector = self.vector
        self.rect.x = Start.width // 2
        self.rect.y = Start.height // 2

    def update(self):
        self.rect.x -= self.vector.x
        self.rect.y -= self.vector.y

class Move:
    pass

class PongPaddle(pygame.sprite.Sprite):
    def __init__(self, pressed_up, pressed_down):
        super().__init__()

        self.width = 20
        self.height = 120

        self.pressed_up = pressed_up
        self.pressed_down = pressed_down

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(Color.white)
        self.image.set_colorkey()

        pygame.draw.rect(self.image, Color.white, [0, 0, self.width, self.height])

        self.rect = self.image.get_rect()

    def handle_collision_detection(self):
        if self.rect.bottom > Start.height:
            self.rect.y = Start.height - self.rect.height
        elif self.rect.top < 0:
            self.rect.y = 0

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[self.pressed_up]:
            self.rect.y -= 10

        if keys[self.pressed_down]:
            self.rect.y += 10

        self.handle_collision_detection()


class Button:
    pass


class Transition:
    pass

if __name__ == "__main__":
    Start()
