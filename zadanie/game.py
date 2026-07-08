import pygame

from charge import Charge
from track import WireTrack


class GameState:
    READY = "ready"       # заряд ещё не взят со старта
    PLAYING = "playing"
    FAILED = "failed"
    WON = "won"


class CircuitGame:
    """
    Игра «Электрическая цепь» (Вариант 15).

    Игрок ведёт заряд (точку, привязанную к курсору мыши) вдоль извилистого
    провода от старта (слева) к финишу (справа). Если заряд касается
    ограничивающих линий кабеля — уровень мгновенно перезапускается.
    """

    WIDTH, HEIGHT = 900, 600
    BG_COLOR = (15, 15, 25)
    FPS = 60

    def __init__(self, thickness=10):
        pygame.init()
        pygame.display.set_caption("Электрическая цепь — Вариант 15")
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 22)

        self.thickness = thickness
        self.track = WireTrack(self.WIDTH, self.HEIGHT)
        self.charge = Charge(
            self.track.start_x,
            self.track.center_y(self.track.start_x),
            thickness,
        )

        self.state = GameState.READY
        self.fail_timer = 0
        self.running = True

    def reset_level(self):
        self.charge.x = self.track.start_x
        self.charge.y = self.track.center_y(self.track.start_x)
        self.state = GameState.READY

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_r:
                    self.reset_level()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.state == GameState.READY:
            # чтобы "подхватить" заряд, нужно подвести мышь к линии старта
            if self.track.at_start(mouse_pos[0]):
                self.state = GameState.PLAYING
                self.charge.follow_mouse(mouse_pos)
            return

        if self.state == GameState.PLAYING:
            self.charge.follow_mouse(mouse_pos)

            if self.track.reached_finish(self.charge.x):
                self.state = GameState.WON
                return

            if not self.track.is_within_bounds(self.charge.x, self.charge.y, self.charge.radius):
                self.state = GameState.FAILED
                self.fail_timer = pygame.time.get_ticks()
                return

        elif self.state == GameState.FAILED:
            # короткая пауза перед мгновенным перезапуском уровня
            if pygame.time.get_ticks() - self.fail_timer > 350:
                self.reset_level()

    def draw_hud(self):
        if self.state == GameState.READY:
            text = "Подведите курсор к зелёной линии (старт), чтобы взять заряд"
        elif self.state == GameState.PLAYING:
            text = "Ведите заряд к красной линии (финиш), не касаясь стенок провода"
        elif self.state == GameState.FAILED:
            text = "КОРОТКОЕ ЗАМЫКАНИЕ! Перезапуск уровня..."
        else:
            text = "Цепь замкнута успешно! R — заново, ESC — выход"

        surf = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(surf, (20, 20))

        thickness_surf = self.font.render(
            f"Толщина заряда: {self.thickness} px", True, (200, 200, 200)
        )
        self.screen.blit(thickness_surf, (20, self.HEIGHT - 34))

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.track.draw(self.screen)
        self.charge.draw(self.screen)
        self.draw_hud()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)

        pygame.quit()