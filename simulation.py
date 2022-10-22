import random
import sys
import pygame
from particle import Particle

class Simulation:
    def __init__(self, num, colors, attracts, repulses,radius):
        pygame.init()
        pygame.display.set_caption("Particle Simulation")

        self.num = num #number of particles
        self.S_WIDTH = 1000 #simulation width
        self.S_HEIGHT = 800 #simulation height
        self.FPS = 40
        self.rgb_colors = {"blue" : (0,0,255), "red" : (255,0,0), "green" : (0,255,0),
                           "yellow" : (255,255,50), "purple":(191, 64, 191)}
        self.colors_speed = {"blue" : 10, "red" : 20, "green" : 30, "yellow":40, "purple":50}
        self.WIN = pygame.display.set_mode((1200, 800))
        self.particles = []
        self.radius = radius
        self.colors = colors
        self.attracts = attracts
        self.repulses = repulses

    def start(self):
        self.particles = []
        for color in self.colors:
            for i in range(1,self.num+1):
                rnd_x = random.randint(5, self.S_WIDTH -5)
                rnd_y = random.randint(5, self.S_HEIGHT-5)

                tmp = Particle(color,rnd_x,rnd_y, self.colors_speed[color])
                self.particles.append(tmp)
        self.main()

    def draw_text(self,content, color, size, x, y, x_center=False, y_center = False):
        font = pygame.font.SysFont("arialblack", size)
        text = font.render(str(content), True, color)
        if x_center and y_center:
            t_width = text.get_rect().width
            t_height = text.get_rect().height
            self.WIN.blit(text, (x - (t_width // 2), y - (t_height//2)))
        elif x_center:
            t_width = text.get_rect().width
            self.WIN.blit(text, (x - (t_width // 2), y))
        elif y_center:
            t_height = text.get_rect().height
            self.WIN.blit(text, (x, y - t_height))
        else:
            self.WIN.blit(text, (x, y))

    def calculate_move(self, par):
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
            if dist <= self.radius and x_l != 0 and y_l != 0:
                moves = dist / self.colors_speed[par.color]
                move = None
                if dist <= 12:
                    x_move = x_l / moves
                    y_move = y_l / moves
                    move = (x_move - x_move * 2, y_move - y_move * 2)
                elif (par.color,particle.color) in self.attracts:
                    move = (x_l / moves, y_l / moves) #attracts
                elif (par.color,particle.color) in self.repulses and dist <= self.radius /2:
                    x_move = x_l / moves
                    y_move = y_l / moves
                    move = (x_move - x_move *2,y_move - y_move*2)
                else:
                    move = (0,0)
                output.append(move)
        return output

    def handle_particles(self):
        for par in self.particles:
            in_radius = self.calculate_move(par)
            x_sum = 0
            y_sum = 0
            for move in in_radius:
                x_sum += move[0]
                y_sum += move[1]
            if in_radius:
                moves = (x_sum / len(in_radius), y_sum / len(in_radius))
                if 5 < par.x + moves[0] < self.S_WIDTH - 5:
                    par.x += moves[0]
                if 5 < par.y + moves[1] < self.S_HEIGHT - 5:
                    par.y += moves[1]

    def draw(self):
        self.WIN.fill((0,0,0))
        #particles
        for par in self.particles:
            pygame.draw.circle(self.WIN,self.rgb_colors[par.color], (par.x, par.y), 4)

        #menu
        menu_bg = pygame.Rect(self.S_WIDTH, 0, 200, self.S_HEIGHT)
        pygame.draw.rect(self.WIN, (200,200,200), menu_bg)
        self.draw_text("1 - Draw On/Off", (255,0,0), 15,1100, 20, x_center= True)
        self.draw_text("2 - Change color", (255,0,0), 15,1100, 50, x_center= True)
        self.draw_text("3 - Start again", (255,0,0), 15,1100, 80, x_center= True)
        self.draw_text("4 - Sandbox", (255,0,0), 15,1100, 110, x_center= True)

        pygame.display.update()

    def main(self):
        draw = False
        c_indx = 0
        color = self.colors[c_indx]
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
                    if event.key == pygame.K_2:
                        if c_indx == len(self.colors) - 1:
                            c_indx = 0
                        else:
                            c_indx += 1
                        color = self.colors[c_indx]
                    if event.key == pygame.K_3:
                        self.start()
                    if event.key == pygame.K_4:
                        self.WIN.fill((0,0,0))
                        self.particles = []
                if draw and event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    tmp = Particle(color, mouse_pos[0], mouse_pos[1],self.colors_speed[color])
                    self.particles.append(tmp)
            self.handle_particles()
            self.draw()







