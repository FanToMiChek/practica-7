import pygame


class Charge:
    """Заряд (точка), который игрок ведёт мышью вдоль дорожки-кабеля."""

    def __init__(self, x, y, thickness=10, color=(0, 200, 255)):
        self.x = x
        self.y = y
        self.thickness = thickness  # диаметр, задаётся ползунком GUI (5..20 px)
        self.color = color

    @property
    def radius(self):
        return self.thickness / 2

    def set_thickness(self, thickness):
        self.thickness = thickness

    def follow_mouse(self, mouse_pos):
        """Заряд строго привязан к курсору мыши."""
        self.x, self.y = mouse_pos

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), int(self.radius), 1)