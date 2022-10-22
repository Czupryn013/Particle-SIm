import random
import sys

import pygame
from particle import Particle

class Simulation:
    def __init__(self, num, colors, attracts, repulses,radius):
        pygame.init()
        pygame.display.set_caption("Particle Simulation")

        self.num = num #number of particles
        self.WIDTH = 1000
        self.HEIGHT = 800
        self.FPS = 30
        self.speed = 10
        self.rgb_colors = {"blue" : (0,0,255), "red" : (255,0,0), "green" : (0,255,0)}
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.particles = []
        self.radius = radius
        self.colors = colors

    def start(self):
        for color in self.colors:
            for i in range(self.num):
                rnd_x = random.randint(0, self.WIDTH)
                rnd_y = random.randint(0, self.HEIGHT)

                tmp = Particle(color,rnd_x,rnd_y)
                self.particles.append(tmp)
        self.main()

    def check_radius(self, par):
        output = []
        for particle in self.particles:
            x_l = 0
            if particle.x < par.x:  # particle po lewej
                x_l = par.x - particle.x
                x_l -= x_l * 2 #bo chcemy żeby szedł do "tyłu"
            else:  # particle po prawej
                x_l = particle.x - par.x

            if particle.y > par.y: #particle niżej
                y_l = particle.y - par.y
            else: #particle wyżej
                y_l =par.y - particle.y
                y_l -= y_l *2
            dist = (x_l ** 2 + y_l ** 2) ** 0.5
            moves = dist / self.speed
            if dist <= 200 and x_l != 0 and y_l != 0:
                move = (x_l / moves, y_l / moves)
                output.append(move)
        return output

    def handle_particles(self):
        for par in self.particles:
            in_radius = self.check_radius(par)
            x_sum = 0
            y_sum = 0
            for move in in_radius:
                x_sum += move[0]
                y_sum += move[1]
            moves = (x_sum / len(in_radius), y_sum / len(in_radius))
            if 0 < par.x + moves[0] < self.WIDTH:
                par.x += moves[0]
            if 0 < par.y + moves[1] < self.HEIGHT:
                par.y += moves[1]

    def draw(self):
        self.WIN.fill((0,0,0))
        for par in self.particles:
            pygame.draw.circle(self.WIN,self.rgb_colors[par.color], (par.x, par.y), 4)

        pygame.display.update()

    def main(self):
        draw = False
        running = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        if draw: draw = False
                        else: draw = True
                if draw and event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    tmp = Particle("blue", mouse_pos[0], mouse_pos[1])
                    self.particles.append(tmp)
            self.handle_particles()
            self.draw()







