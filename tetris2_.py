import sys, pygame
from shapes import *
from pprint import pprint as print
import random
from typing import *

pygame.init()

size = width, height = 500, 1000
black = 0, 0, 0
white = 255, 255, 255

colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255)]

rows, cols = 20, 10
delta_rows, delta_cols = height//rows, width//cols

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

possible_shapes:List[List[List[int]]] = [I, J, L, CUBE, Z, BZ, T]

medium_column = 5

class Part:
  def __init__(self, pos:Tuple[int, int], color: Tuple[int, int, int] = white):
    self.x =pos[0]
    self.y = pos[1]
    self.color = color

  def draw(self):
    pygame.draw.rect(screen, self.color, (self.x*delta_rows, self.y * delta_cols, delta_rows, delta_cols ))

  def move_down(self):
    self.y += 1

  def move_right(self):
    self.x += 1

  def move_left(self):
    self.x -= 1

  def __str__(self):
    return f'({self.x}, {self.y})'
  
  def __repr__(self):
    return str(self)

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

class Shape:
  def __init__(self, shape_description:List[List[int]], grid: List[List[int]]):
    shape:List[List[Part]] = [[] for i in range(len(shape_description))]
    color = random.choice(colors)
    for i in range(len(shape_description)):
      row = shape_description[i]
      for j in range(len(row)):
        x = row[j]
        if x:
          part = Part((j + (len(row) % rows), i), color=color)
          shape[i].append(part)
    self.shape = shape
    self.grid = grid

  @property
  def active(self) -> bool:
    return not self.collides_with_bottom() 

  @property
  def flat_shape(self) -> List[Part]:
    return sum(self.shape, [])

  def _execute_fn_for_all_parts(self, fn: Callable):
    for row in self.shape:
      for part in row:
        fn(part)
  
  def _find_lowest_y(self) -> int:
    bottom_row = self.shape[-1]
    return bottom_row[0].y

  def _find_lowest_row(self) -> List[Part]:
    bottom_row = self.shape[-1]
    return bottom_row

  def _find_most_left_x(self) -> int:
    lefts = [rows[0].x  for rows in self.shape]
    return min(lefts)

  def _find_most_right_x(self) -> int:
    rights = [rows[-1].x  for rows in self.shape]
    return max(rights)

  def draw(self):
    self._execute_fn_for_all_parts(Part.draw)

  def move_down(self):
    self._execute_fn_for_all_parts(Part.move_down) if not self.collides_with_bottom() else None

  def move_right(self):
    self._execute_fn_for_all_parts(Part.move_right) if not self.collides_with_right() else None


  def move_left(self):
    self._execute_fn_for_all_parts(Part.move_left) if not self.collides_with_left() else None

  def rotate(self):
    pass

  def _future(self, axis: str,  movement: int, rotation: int = 0):
    # rotation 0 means no rotation, other possible values are 1 for clockwise and -1 for counterclockwise
    flat_shape = self.flat_shape
    if axis == "x" and movement == 1: # down
      pass
    elif axis == "y" and movement == 1: # right
      pass
    elif axis == "y" and movement == -1: # left
      pass

    
  def collides_with(self, grid: List[List[int]], axis:str, movement: int, rotation: int) -> bool:
    # remove self from grid
    flat_shape = self.flat_shape
    for part in flat_shape:
      grid[part.y][part.x] = 0
    
    future_shape = self._future(movement, rotation) 
    # calculate future position and rotation
    # check if future self will collide with anything
    pass

  def collides_with_bottom(self) -> bool:
    return self._find_lowest_y() == rows - 1
  
  def collides_with_left(self) -> bool:
    return self._find_most_left_x() == 0

  def collides_with_right(self) -> bool:
    return self._find_most_right_x() == cols - 1


class Field:
  def __init__(self):
    self.grid = [[0 for i in range(cols)] for j in range(rows)]
    first_shape = Shape(shape_description = T, grid= self.grid)
    self.shapes:List[Shape] = [first_shape]
    self.current_shape = first_shape

  def draw_grid(self):
    x, y = 0, 0
    for i in range(rows):
        x += delta_rows
        pygame.draw.line(screen, white, (0, x), (height, x))
    for i in range(cols):
        y += delta_cols
        pygame.draw.line(screen, white, (y, 0), (y, height))

  def draw_shapes(self):
    for shape in self.shapes:
      shape.draw()

  def add_random_shape(self):
    shape = Shape(shape_description=random.choice(possible_shapes), grid= self.grid)
    self.current_shape = shape
    self.shapes.append(shape)

  def move_curent_shape_down(self):
    self.current_shape.move_down()
    if not self.current_shape.active:
      self.add_random_shape()

  def move_current_shape_left(self):
    self.current_shape.move_left()

  def move_current_shape_right(self):
    self.current_shape.move_right()

  def udpate_grid(self):
    self.grid = [[0 for i in range(cols)] for j in range(rows)]
    for shape in self.shapes:
      flat_shape = shape.flat_shape
      for part in flat_shape:
        self.grid[part.y][part.x] = 1
    for shape in self.shapes:
      shape.grid = self.grid

if __name__ == "__main__":
  field = Field()
  FALLEVENT, t, trail = pygame.USEREVENT+1, 250, []
  pygame.time.set_timer(FALLEVENT, t)
  while True:
    if pygame.event.get(pygame.QUIT): 
      sys.exit()

    field.udpate_grid()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
      field.move_current_shape_left()
    elif keys[pygame.K_RIGHT]:
      field.move_current_shape_right()
    elif keys[pygame.K_DOWN]:
      field.move_curent_shape_down()

    for event in pygame.event.get():
      if event.type == FALLEVENT:
        field.move_curent_shape_down()

    screen.fill(black)
    field.draw_grid()
    
    field.draw_shapes()
    clock.tick(30)
    pygame.display.update()
