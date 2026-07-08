import math
import pygame


class WireTrack:
    """
    Извилистая дорожка (электрический кабель) из двух параллельных линий,
    идущая от левого края экрана к правому.
    Форма центральной линии кабеля задаётся синусоидой.
    """

    def __init__(self, screen_width, screen_height,
                 corridor_width=90, amplitude=120, wavelength=400,
                 margin=60, color=(255, 200, 0)):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.corridor_width = corridor_width
        self.half_width = corridor_width / 2
        self.amplitude = amplitude
        self.wavelength = wavelength
        self.margin = margin
        self.color = color
        self.base_y = screen_height // 2

        self.start_x = margin
        self.finish_x = screen_width - margin

        self._upper_points = []
        self._lower_points = []
        self._build_points()

    def center_y(self, x):
        """Y-координата центральной линии кабеля в точке x (синусоида)."""
        return self.base_y + self.amplitude * math.sin(
            2 * math.pi * (x - self.start_x) / self.wavelength
        )

    def bounds_at(self, x):
        """Возвращает (top_y, bottom_y) — границы коридора кабеля в точке x."""
        cy = self.center_y(x)
        return cy - self.half_width, cy + self.half_width

    def _build_points(self, step=4):
        self._upper_points = []
        self._lower_points = []
        x = self.start_x
        while x <= self.finish_x:
            top, bottom = self.bounds_at(x)
            self._upper_points.append((x, top))
            self._lower_points.append((x, bottom))
            x += step

    def draw(self, surface):
        if len(self._upper_points) > 1:
            pygame.draw.lines(surface, self.color, False, self._upper_points, 4)
            pygame.draw.lines(surface, self.color, False, self._lower_points, 4)

        # отметки старта (зелёная) и финиша (красная)
        start_top, start_bottom = self.bounds_at(self.start_x)
        finish_top, finish_bottom = self.bounds_at(self.finish_x)
        pygame.draw.line(surface, (0, 255, 0), (self.start_x, start_top), (self.start_x, start_bottom), 4)
        pygame.draw.line(surface, (255, 0, 0), (self.finish_x, finish_top), (self.finish_x, finish_bottom), 4)

    def is_within_bounds(self, x, y, radius):
        """True, если заряд (круг радиуса radius с центром x,y) не задевает стенки коридора."""
        if x < self.start_x or x > self.finish_x:
            return True  # за пределами дорожки коллизия не проверяется
        top, bottom = self.bounds_at(x)
        return (y - radius) > top and (y + radius) < bottom

    def reached_finish(self, x):
        return x >= self.finish_x

    def at_start(self, x):
        return x <= self.start_x + 10