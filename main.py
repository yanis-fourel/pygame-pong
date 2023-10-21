import pygame
from pygame import Vector2

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class Pad:
    HEIGHT = 250
    WIDTH = 20
    MOVE_SPEED = 500

    def __init__(self, x: int):
        self.x = x
        self.y = SCREEN_HEIGHT / 2 - self.HEIGHT / 2

    def display(self):
        pygame.draw.rect(screen, "white", (self.x, self.y, self.WIDTH, self.HEIGHT))


class Ball:
    SIZE = 75
    INITIAL_SPEED = 300
    ACC_FACTOR = 1.1

    def __init__(self):
        self.x = SCREEN_WIDTH / 2 - self.SIZE / 2
        self.y = SCREEN_HEIGHT / 2 - self.SIZE / 2
        self.vel = Vector2(self.INITIAL_SPEED, self.INITIAL_SPEED)

    def display(self):
        pygame.draw.rect(screen, "white", (self.x, self.y, self.SIZE, self.SIZE))

def do_collide(ball: Ball, pad: Pad):
    ball_rect = pygame.Rect(ball.x, ball.y, ball.SIZE, ball.SIZE)
    pad_rect = pygame.Rect(pad.x, pad.y, pad.WIDTH, pad.HEIGHT)

    return ball_rect.colliderect(pad_rect)


class Scene:
    def __init__(self) -> None:
        self.ball = Ball()
        self.pad1 = Pad(20 + Pad.WIDTH)
        self.pad2 = Pad(SCREEN_WIDTH - 20 - Pad.WIDTH)
        self.p1_score = 0
        self.p2_score = 0

    def display(self):
        self.ball.display()
        self.pad1.display()
        self.pad2.display()

        font = pygame.font.SysFont("Arial", 50)
        text = font.render(f"{self.p1_score} - {self.p2_score}", True, "white")
        screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, 20))

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:
            self.pad1.y -= Pad.MOVE_SPEED * clock.get_time() / 1000
        if keys[pygame.K_a]:
            self.pad1.y += Pad.MOVE_SPEED * clock.get_time() / 1000

        self.pad1.y = pygame.math.clamp(self.pad1.y, 0, SCREEN_HEIGHT - self.pad1.HEIGHT)
        self.pad2.y = pygame.math.clamp(self.pad2.y, 0, SCREEN_HEIGHT - self.pad1.HEIGHT)

        if keys[pygame.K_p]:
            self.pad2.y -= Pad.MOVE_SPEED * clock.get_time() / 1000
        if keys[pygame.K_l]:
            self.pad2.y += Pad.MOVE_SPEED * clock.get_time() / 1000

        self.ball.x += self.ball.vel.x * clock.get_time() / 1000
        self.ball.y += self.ball.vel.y * clock.get_time() / 1000
        self.ball.vel *= Ball.ACC_FACTOR ** (clock.get_time() / 1000)

        if do_collide(self.ball, self.pad1) or do_collide(self.ball, self.pad2):
            self.ball.vel.x *= -1
        if self.ball.y < 0 or self.ball.y > SCREEN_HEIGHT - self.ball.SIZE:
            self.ball.vel.y *= -1

        if self.ball.x < 0:
            self.p2_score += 1
            self.ball = Ball()
        if self.ball.x > SCREEN_WIDTH - self.ball.SIZE:
            self.p1_score += 1
            self.ball = Ball()

        if self.p1_score > 10 or self.p2_score > 10:
            print('Game over')


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

scene = Scene()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    scene.update()
    scene.display()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
