import sys
import itertools
import pygame as pg


CAPTION = "Animate"
SCREEN_SIZE = (500, 500)
BACKGROUND_COLOR = (30, 20, 30)


class Loop(object):
    def __init__(self, sheet, size, fps, rows, columns, missing=0):
        self.delay = 1.0/fps
        self.accumulator = 0.0
        self.frames = self.make_cycle(sheet, size, rows, columns, missing)
        self.frame = None
        self.get_next()

    def make_cycle(self, sheet, size, rows, columns, missing=0):
        subsurfaces = []
        total = rows*columns-missing
        for frame in range(total):
            y, x = divmod(frame, columns)
            rect = pg.Rect((x*size[0], y*size[1]), size)
            subsurfaces.append(sheet.subsurface(rect))
        return itertools.cycle(subsurfaces)

    def get_next(self, dt=0):
        self.accumulator += dt
        if not self.frame:
            self.frame = next(self.frames)
        while self.accumulator >= self.delay:
            self.frame = next(self.frames)
            self.accumulator -= self.delay
        return self.frame

    
class Asteroid(pg.sprite.Sprite):
    def __init__(self, pos, *groups):
        super(Asteroid, self).__init__(*groups)
        self.frames = Loop(ASTEROID_SHEET, (96, 80), 60, 7, 21, missing=4)
        self.image = self.frames.frame
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt):
        self.image = self.frames.get_next(dt)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class App(object):
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.done = False
        self.asteroid = Asteroid(self.screen_rect.center)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def display_fps(self):
        """Show the program's FPS in the window handle."""
        caption = "{} - FPS: {:.2f}".format(CAPTION, self.clock.get_fps())
        pg.display.set_caption(caption)

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.asteroid.draw(self.screen)
        pg.display.update()
        
    def main_loop(self):
        dt = self.clock.tick(self.fps)/1000.0
        while not self.done:
            self.event_loop()
            self.asteroid.update(dt)
            self.render()
            self.display_fps()
            dt = self.clock.tick(self.fps)/1000.0


def main():
    global ASTEROID_SHEET
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    ASTEROID_SHEET = pg.image.load("asteroid_simple.png").convert_alpha()
    App().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
