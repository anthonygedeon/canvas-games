import os
import sys

import pygame

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

FONT_FAMILY = "slkscrb.ttf"
SOUND = "pong-sound.mp3"

color = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "lightgray": (211, 211, 211)
}

is_running = True

current_scene_controller = [True, False, False] # Crude way of displaying certain screens to the user

class StartMenuScene(pygame.Surface):
    """"""
    
    def __init__(self):
        self.start_menu_sprites = pygame.sprite.Group()
        self.play_button = Button(color.get("white"), "PLAY", 48, ((WINDOW_WIDTH - 160) // 2, 180))
        self.quit_button = Button(color.get("white"), "QUIT", 48, ((WINDOW_WIDTH - 140) // 2, 240))
        self.mouse = Mouse2DPoint()
    
        self.screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.start_menu_sprites.add(self.play_button, self.quit_button)
    
        menu_title = pygame.font.Font(os.path.join("pong", "resources/font", FONT_FAMILY), 102)
        self.title = menu_title.render("Pong", True, color.get("white"))
        
    def display(self):
        self.screen.fill(color.get("black"))
        self.start_menu_sprites.update()

        self.screen.blit(self.title, (((WINDOW_WIDTH - self.title.get_width()) // 2), 20))
        
        self.start_menu_sprites.draw(self.screen)

        self.play_button.render(self.screen)
        self.quit_button.render(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.quit_button.is_clicked(event, self.mouse.get_mouse_pos):
                global is_running
                is_running = False
            elif self.play_button.is_clicked(event, self.mouse.get_mouse_pos):
                current_scene_controller[0] = False
                current_scene_controller[1] = True
                current_scene_controller[2] = False

class GameScene(pygame.Surface):
    """"""
    def __init__(self):

        self.pong_ball = PongBall()
        self.left_paddle = PongPaddle(pygame.K_w, pygame.K_s)
        self.right_paddle = PongPaddle(pygame.K_UP, pygame.K_DOWN)
        self.score_manager = ScoreManager()

        self.screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.font = pygame.font.Font(os.path.join("pong", "resources/font", FONT_FAMILY), 72)

        self.MARGIN_LEFT = self.left_paddle.rect.width
        self.MARGIN_RIGHT = WINDOW_WIDTH - self.right_paddle.rect.width * 2

        self.pong_sprites = pygame.sprite.Group()

        # Handle position of LEFT Paddle
        self.left_paddle.rect.y = (WINDOW_HEIGHT - self.left_paddle.height) // 2
        self.left_paddle.rect.x = self.MARGIN_LEFT

        # Handle position of RIGHT Paddle
        self.right_paddle.rect.y = (WINDOW_HEIGHT - self.right_paddle.height) // 2
        self.right_paddle.rect.x = self.MARGIN_RIGHT

        # Position the Pong Ball in the center of window
        self.pong_ball.spawn((5, 5))
        self.pong_sprites.add(self.pong_ball, self.left_paddle, self.right_paddle)

    def display(self):
        self.pong_sprites.update()
        self.screen.fill(color.get("black"))
        self.pong_sprites.draw(self.screen)

        # Collision Detection for Ping Pong Ball
        self.pong_ball.handle_collision_detection(self.left_paddle, self.right_paddle)

        # Draw Net
        for box in range(0, WINDOW_WIDTH, 40):
            pygame.draw.rect(self.screen, color.get("white"), [WINDOW_WIDTH // 2, box, 10, 20])

        # This makes sure that the pong ball is touching the window frame
        if self.pong_ball.rect.x > WINDOW_WIDTH:
            self.pong_ball.spawn((-5, 5))
            self.score_manager.add_left_score()
        elif self.pong_ball.rect.x < 0:
            self.pong_ball.spawn((5, 5))
            self.score_manager.add_right_score()

        if self.score_manager.is_winner():
            current_scene_controller[0] = False
            current_scene_controller[1] = False
            current_scene_controller[2] = True
            return

        score_1 = self.font.render(str(self.score_manager.get_score[0]), True, color.get("white"))
        score_2 = self.font.render(str(self.score_manager.get_score[1]), True, color.get("white"))

        self.screen.blit(score_1, (((WINDOW_WIDTH - 58) // 2) - 150, 20))
        self.screen.blit(score_2, (((WINDOW_WIDTH - 58) // 2) + 150, 20))

class GameOverScene(pygame.Surface):
    """"""
    def __init__(self):
        self.screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.game_over_sprites = pygame.sprite.Group()
        self.menu_title = pygame.font.Font(os.path.join("pong", "resources/font", FONT_FAMILY), 72)

        self.retry_button = Button(color.get("white"), "Retry", 48, ((WINDOW_WIDTH - 160) // 2, 180))
        self.menu_button = Button(color.get("white"), "MENU", 48, ((WINDOW_WIDTH - 140) // 2, 240))

        self.mouse = Mouse2DPoint()
        self.title = self.menu_title.render("Game Over", True, color.get("white"))
        self.game_over_sprites.add(self.retry_button, self.menu_button)

    def display(self):
        """"""
        self.screen.fill(color.get("black"))
        self.game_over_sprites.update()
        self.game_over_sprites.draw(self.screen)

        title = self.menu_title.render("Game Over", True, color.get("white"))

        self.screen.blit(title, (((WINDOW_WIDTH - title.get_width()) // 2), 20))
        self.retry_button.render(self.screen)
        self.menu_button.render(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global is_running
                is_running = False
            elif self.retry_button.is_clicked(event, self.mouse.get_mouse_pos):
                current_scene_controller[0] = False
                current_scene_controller[1] = True
                current_scene_controller[2] = False
            elif self.menu_button.is_clicked(event, self.mouse.get_mouse_pos):
                current_scene_controller[0] = True
                current_scene_controller[1] = False
                current_scene_controller[2] = False

class ScoreManager:
    """"""
    def __init__(self):
        self.score = [0, 0]
        self.winning_score = 1
        self.point_amount = 1

    def add_left_score(self):
        """"""
        self.score[0] += self.point_amount

    def add_right_score(self):
        """"""
        self.score[1] += self.point_amount

    def is_winner(self):
        """"""
        if self.score[0] >= self.winning_score or self.score[1] >= self.winning_score:
            self._reset_score()
            return True
        return False

    def _reset_score(self):
        """"""
        self.score[0] = 0
        self.score[1] = 0

    @property
    def get_score(self):
        """"""
        return self.score

class Mouse2DPoint():
    
    @property
    def get_mouse_pos(self):
        return pygame.mouse.get_pos()

class Start:

    def __init__(self):

        pygame.key.set_repeat(50, 50)

        # Screens
        self.main_game = GameScene()
        self.start_menu = StartMenuScene()
        self.game_over = GameOverScene()

        self.fps = 60
        self.clock = pygame.time.Clock()

        while is_running:

            start_menu_screen, game_screen, game_over_screen = current_scene_controller
            
            if start_menu_screen:
                self.start_menu.display()
            elif game_screen:
                self.main_game.display()
            elif game_over_screen:
                self.game_over.display()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

            # Seeing sudden frame drops after 30 second gameplay
            pygame.display.set_caption("Pong - FPS: {}".format(self.clock.tick(self.fps)))
            pygame.display.flip()
            pygame.display.update()

        pygame.quit()
        sys.exit()

class PongBall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self._is_collision = False

        self.width = 20
        self.height = self.width

        self.velocity = pygame.Vector2(5, 5)

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color.get("white"))
        self.image.set_colorkey()

        pygame.draw.rect(self.image, color.get("white"), [0, 0, self.width, self.height])
        self.rect = self.image.get_rect()

    @staticmethod
    def _play_sound():
        hit_sound = pygame.mixer.Sound(os.path.join("pong", "resources/sounds", SOUND))
        pygame.mixer.Sound.play(hit_sound)

    def handle_collision_detection(self, object_a, object_b):
        
        if self.rect.colliderect(object_a.rect) or self.rect.colliderect(object_b.rect):
            PongBall._play_sound()
            self.velocity.x = -self.velocity.x
            self._is_collision = True

        # Handle collision for TOP and BOTTOM window
        if self.rect.y < 0:
            self.velocity.y = -self.velocity.y
        elif self.rect.y > WINDOW_HEIGHT:
            self.velocity.y = -self.velocity.y

    def spawn(self, vector):
        x, y = vector
        self.velocity = pygame.Vector2(x, y)
        self.rect.x = WINDOW_WIDTH // 2
        self.rect.y = WINDOW_HEIGHT // 2

    def update(self):
        self.rect.x += self.velocity.x
        if self._is_collision: # I need the ball to move on the x-axis first and once the ball collides with an object, then start updating the y
            self.rect.y += self.velocity.y

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
        self.image.fill(color.get("white"))
        self.image.set_colorkey()

        pygame.draw.rect(self.image, color.get("white"), [0, 0, self.width, self.height])
        self.rect = self.image.get_rect()

    def _handle_collision_detection(self):
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.y = WINDOW_HEIGHT - self.rect.height
        elif self.rect.top < 0:
            self.rect.y = 0

    def _move_up(self, y):
        self.rect.y -= y

    def _move_down(self, y):
        self.rect.y += y

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.pressed_up]:
            self._move_up(10)
        if keys[self.pressed_down]:
            self._move_down(10)

        self._handle_collision_detection()

class Text():
    """"""

    def __init__(self, text, color, font_size, font_family):
        try: 
            if len(text) == 0:
                raise Exception

            self.text = text
            self.color = color
            self.font_size = font_size
            self.font_family = font_family

        except Exception:
            print("No text available")

    def _create_text(self):
        """"""
        pass

    def get_width(self):
        """"""
        pass

    def get_height(self):
        """"""
        pass

    def render(self):
        """"""
        pass

class Button(pygame.sprite.Sprite):

    def __init__(self, 
        background_color, 
        button_text, 
        font_size, 
        position):

        super().__init__()
        
        self.font_size = font_size
        self.button_text = button_text
        self.button_font = pygame.font.Font(os.path.join("pong", "resources/font", FONT_FAMILY), font_size)
        self.button_inner_text = self.button_font.render(self.button_text, True, color.get("black"))
        self.font_width, self.font_height =  self.button_inner_text.get_width(), self.button_inner_text.get_height()

        self.position = position
        
        self.background_color = background_color

        self.image = pygame.Surface([self.font_width, self.font_height])
        self.image.fill(self.background_color)
        self.image.set_colorkey()

        pygame.draw.rect(self.image, self.background_color, [0, 0, self.font_width, self.font_height])

        self.rect = self.image.get_rect()

    def is_clicked(self, press, mouse_pos):
        if press.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(mouse_pos):
            return True
        return False

    def render(self, screen):
        x, y = self.position
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.button_inner_text, (x, y))

if __name__ == "__main__":
    Start()
