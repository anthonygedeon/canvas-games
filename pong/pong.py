import random
import os

import pygame

class Color:
    white = (255, 255, 255)
    black = (0, 0, 0)

class Player:
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

        player_1 = Player()
        player_2 = Player()
    
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

            self.clock.tick(self.fps)

            self.pong_sprites.draw(self.screen)

            # Collision Detection for Ping Pong Ball
            if pong_ball.rect.colliderect(left_paddle.rect):
                pong_ball.vector = pygame.Vector2(-10, random.randrange(0, 10))
            elif pong_ball.rect.colliderect(right_paddle.rect):
                pong_ball.vector = pygame.Vector2(10, (random.randrange(0, 10) * -1))

            if pong_ball.rect.x > self.width:
                pong_ball.spawn()
                player_1.add_to_score()
            elif pong_ball.rect.x < 0:
                pong_ball.spawn()
                player_2.add_to_score()
            elif pong_ball.rect.y < 0:
                pong_ball.vector = pygame.Vector2(10, -10)
            elif pong_ball.rect.y > self.height:
                pong_ball.vector = pygame.Vector2(10, 10)

            score_1 = font.render(str(player_1.get_current_score), True, Color.white)
            score_2 = font.render(str(player_2.get_current_score), True, Color.white)

            self.screen.blit(score_1, (((self.width - 58) // 2) - 150, 20))
            self.screen.blit(score_2, (((self.width - 58) // 2) + 150, 20))

            pygame.display.flip()

            pygame.display.update()

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

        self.vector = pygame.Vector2(10, 1)

        self.rect = self.image.get_rect()

    def spawn(self):
        self.vector = pygame.Vector2(10, 1)
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

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.pressed_up]:
            self.rect.y -= 10

        if keys[self.pressed_down]:
            self.rect.y += 10

        # Collision Detection for Paddle
        if self.rect.bottom > Start.height:
            self.rect.y = Start.height - self.rect.height
        elif self.rect.top < 0:
            self.rect.y = 0


class Button:
    pass


class Transition:
    pass

if __name__ == "__main__":
    Start()
