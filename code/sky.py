import pygame
from settings import *
from support import import_folder
from sprites import Generic
from random import randint, choice


class Sky:

  def __init__(self) -> None:
    self.display_surface = pygame.display.get_surface()
    self.full_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.start_color = [255, 255, 255]
    self.end_color = (38, 101, 189)

  def display(self, dt):
    for idx, value in enumerate(self.end_color):
      if self.start_color[idx] > value:
        self.start_color[idx] -= 1 * dt
    self.full_surf.fill(self.start_color)
    self.display_surface.blit(
      self.full_surf, (0, 0),
      special_flags=pygame.BLEND_RGBA_MULT
    )


class Drop(Generic):

  def __init__(self, pos, surf, moving, groups, z):
    super().__init__(pos, surf, groups, z)

    # general setup
    self.lifetime = randint(400, 500)
    self.start_time = pygame.time.get_ticks()

    # moving
    self.moving = moving
    if self.moving:
      self.pos = pygame.Vector2(self.rect.topleft)
      self.direction = pygame.Vector2(-2, 4)
      self.speed = randint(200, 250)

  def update(self, dt):
    # movement
    if self.moving:
      self.pos += self.direction * self.speed * dt
      self.rect.topleft = round(self.pos.x), round(self.pos.y)

    # timer
    current_time = pygame.time.get_ticks()
    if current_time - self.start_time >= self.lifetime:
      self.kill()


class Rain:

  def __init__(self, all_sprites: pygame.sprite.Group) -> None:
    self.all_sprites = all_sprites
    self.rain_drops = import_folder(GRAPHICS_DIR / 'rain/drops')
    self.rain_floor = import_folder(GRAPHICS_DIR / 'rain/floor')
    self.floor_w, self.floor_h = pygame.image.load(
      GRAPHICS_DIR / 'world/ground.png').get_size()

  def create_floor(self):
    Drop(
      pos=(randint(0, self.floor_w), randint(0, self.floor_h)),
      surf=choice(self.rain_floor),
      moving=False,
      groups=self.all_sprites,
      z=LAYERS['rain floor']
    )

  def create_drops(self):
    Drop(
      pos=(randint(0, self.floor_w), randint(0, self.floor_h)),
      surf=choice(self.rain_drops),
      moving=True,
      groups=self.all_sprites,
      z=LAYERS['rain drops']
    )

  def update(self):
    self.create_floor()
    self.create_drops()
