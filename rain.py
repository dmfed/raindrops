#!/usr/bin/env python3
import sys, argparse, random, pygame
from raindrop import Raindrop

class Engine:
    '''Engine doing the work'''
    def __init__(self, resx=800, resy=600, fullscreen=False):
        pygame.init()
        if fullscreen:
            self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((800, 600))
        self.screen_rect = self.screen.get_rect()
        self.max_drops = 700  # this max of drops can be drawn at the same time
        self.max_vertical_offset = 50
        pygame.display.set_caption('Raindrops')
#        self.bg_color = (255, 255, 255)
        self.bg_color = (0, 0, 0)
        self.drops = pygame.sprite.Group()
        self.counter = 0

    def run(self):
        '''Mainloop'''
        try:
            while True:
                self._update_display()
                self._check_events()
                self._counter()
                pygame.display.flip()
        except:
            sys.exit()

    def add_drop(self):
        '''adds drop to sprites group'''
        if len(self.drops) < self.max_drops:
            drop = Raindrop(self)
            # randomising x coordinate where the drop appears
            drop.rect.x = random.choice(range(0, self.screen_rect.width))
            self.drops.add(drop)

    def _counter(self):
        # randomising vertical axis (drops do not appear with each loop step)
        self.counter += random.choice(range(1, 6))
        self.drops.update()
        for drop in self.drops.copy():  # removes drops out of range
            if drop.rect.top >= self.screen_rect.height:
                self.drops.remove(drop)
        if self.counter >= self.max_vertical_offset:
            self.counter = 0  # 0 means we can add drops again

    def _update_display(self):
        self.screen.fill(self.bg_color)
        if self.counter == 0:
            self.add_drop()
        self.drops.draw(self.screen)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._stop()
            elif event.type == pygame.KEYDOWN:
                self._process_input(event)

    def _process_input(self, event):
        if event.key == pygame.K_q:  # quit with 'q'
            self._stop()
        elif event.key == pygame.K_ESCAPE:  # or 'Esc'
            self._stop()
        elif event.key == pygame.K_UP:
            self.max_drops += 15
        elif event.key == pygame.K_DOWN:
            self.max_drops -= 15
        elif event.key == pygame.K_RIGHT:
            self.max_vertical_offset += 15  #show less drops please
        elif event.key == pygame.K_LEFT:
            self.max_vertical_offset -= 15  # show more drops please

    def _stop(self):
        print(f'Vert_offset was {self.max_vertical_offset}, max drops {self.max_drops}')
        sys.exit()

def parse_args():
    parser = argparse.ArgumentParser(
        description='''Animates raindrops falling.
Use up and down to increase/decrase number of drops drawn simultaneously.
Use left and right to increase/decrease density of drops.

Press 'Q' to quit.''')
    parser.add_argument('-f', '--fullscreen',
                        help='Run in fullscreen mode.',
                        action="store_true")
    parser.add_argument('-x', '--resx',
                        help='Horizontal resolution.',
                        type=int)
    parser.add_argument('-y', '--resy',
                        help='Vertical resolution.',
                        type=int)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    engine = Engine(args.resx, args.resy, fullscreen=args.fullscreen)
    engine.run()
