import random
import os

import pygame

class Color:
    white = (255, 255, 255)
    black = (0, 0, 0)
    light_gray = (211, 211, 211)

class ScoreBoard:
    def __init__(self):
        self.score = 0

    def add_point(self):
        self.score += 1
        return self.score

    @property
    def get_current_score(self):
        return self.score

class Mouse2DBox(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()

        self.width = 20
        self.height = self.width

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(Color.black)
        self.image.set_colorkey()

        pygame.draw.rect(self.image, Color.white, [0, 0, self.width, self.height])

        self.rect = self.image.get_rect()

    def update(self):
        x_mouse, y_mouse = pygame.mouse.get_pos()
        self.rect.x = x_mouse
        self.rect.y = y_mouse

class Start:

    width = 800
    height = 500

    def __init__(self):

        pygame.init()
        pygame.key.set_repeat(50, 50)

        score_left = ScoreBoard()
        score_right = ScoreBoard()
    
        pygame.display.set_caption("Pong")
        
        font = pygame.font.Font(os.path.join("pong", "font", "slkscrb.ttf"), 72)
        menu_title = pygame.font.Font(os.path.join("pong", "font", "slkscrb.ttf"), 102)

        pong_ball = PongBall()
        left_paddle = PongPaddle(pygame.K_w, pygame.K_s)
        right_paddle = PongPaddle(pygame.K_UP, pygame.K_DOWN)
        mouse_collider = Mouse2DBox()
        
        # Buttons
        play_button = Button(Color.white, "PLAY", 48, ((self.width - 160) // 2, 180))
        quit_button = Button(Color.white, "QUIT", 48, ((self.width - 140) // 2, 240))

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
        self.start_menu_sprites = pygame.sprite.Group()

        self.is_playing = False

        # Handle position of LEFT Paddle
        left_paddle.rect.y = (self.height - left_paddle.height) // 2
        left_paddle.rect.x = self.MARGIN_LEFT

        # Handle position of RIGHT Paddle
        right_paddle.rect.y = (self.height - right_paddle.height) // 2
        right_paddle.rect.x = self.MARGIN_RIGHT

        # Position the Pong Ball in the center of window
        pong_ball.spawn()

        self.pong_sprites.add(pong_ball, left_paddle, right_paddle)
        self.start_menu_sprites.add(mouse_collider, play_button, quit_button)

        while self.running:

            if self.is_playing:

                self.pong_sprites.update()

                self.screen.fill(Color.black)
                self.pong_sprites.draw(self.screen)

                # Draw Net
                for box in range(0, self.width, 40):
                    pygame.draw.rect(self.screen, Color.white, [self.width // 2, box, 10, 20])

                # Collision Detection for Ping Pong Ball
                pong_ball.handle_collision_detection(left_paddle, right_paddle)

                # This makes sure that the pong ball is touching the window frame
                if pong_ball.rect.x > self.width:
                    pong_ball.spawn()
                    score_left.add_point()
                elif pong_ball.rect.x < 0:
                    pong_ball.spawn()
                    score_right.add_point()

                score_1 = font.render(str(score_left.get_current_score), True, Color.white)
                score_2 = font.render(str(score_right.get_current_score), True, Color.white)

                self.screen.blit(score_1, (((self.width - 58) // 2) - 150, 20))
                self.screen.blit(score_2, (((self.width - 58) // 2) + 150, 20))
            
            else:
                # GAME MENU
                self.screen.fill(Color.black)
                self.start_menu_sprites.update()
                self.start_menu_sprites.draw(self.screen)

                title = menu_title.render("Pong", True, Color.white)

                self.screen.blit(title, (((self.width - title.get_width()) // 2), 20))
                play_button.render(self.screen)
                quit_button.render(self.screen)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and mouse_collider.rect.colliderect(play_button.rect):
                        self.is_playing = True
                    elif event.type == pygame.MOUSEBUTTONDOWN and mouse_collider.rect.colliderect(quit_button.rect):
                        self.running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

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

        self.velocity = 10
        self.vector = pygame.Vector2(10, 0)

        self.rect = self.image.get_rect()

    def handle_collision_detection(self, object_a, object_b):
        if self.rect.colliderect(object_a.rect):
            self.vector = pygame.Vector2(-10, random.randrange(0, 10))
            self.sound()
        elif self.rect.colliderect(object_b.rect):
            self.vector = pygame.Vector2(10, (random.randrange(0, 10) * -1))
            self.sound()

        # Sim
        if self.rect.y < 0:
            self.vector = pygame.Vector2(10, -10)
        elif self.rect.y > Start.height:
            self.vector = pygame.Vector2(10, 10)

    def sound(self):
        hit_sound = pygame.mixer.Sound(os.path.join("pong", "sounds", "pong-sound.mp3"))
        pygame.mixer.Sound.play(hit_sound)

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
        self.height = 100

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

class Button(pygame.sprite.Sprite):

    def __init__(self, 
        background_color, 
        button_text, 
        font_size, 
        position):

        super().__init__()
        
        self.font_size = font_size
        self.button_text = button_text
        self.button_font = pygame.font.Font(os.path.join("pong", "font", "slkscrb.ttf"), font_size)
        self.button_inner_text = self.button_font.render(self.button_text, True, Color.black)
        self.font_width, self.font_height =  self.button_inner_text.get_width(), self.button_inner_text.get_height()

        self.position = position
        
        self.background_color = background_color

        self.image = pygame.Surface([self.font_width, self.font_height])
        self.image.fill(self.background_color)
        self.image.set_colorkey()

        pygame.draw.rect(self.image, self.background_color, [0, 0, self.font_width, self.font_height])

        self.rect = self.image.get_rect()

    def render(self, screen):
        x, y = self.position
        self.rect.x = x
        self.rect.y = y

        screen.blit(self.button_inner_text, (x, y))

class Scene:
    pass

if __name__ == "__main__":
    Start()
