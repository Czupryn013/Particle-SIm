import random
import sys
import pygame
from particle import Particle
from grid import Grid


class Simulation:
    def __init__(self, num, colors,attracts, repulses,rules,radius, gravity = False):
        pygame.init()
        pygame.display.set_caption("Particle Simulation")

        self.num = num #number of particles
        self.S_WIDTH = 800 #simulation width
        self.S_HEIGHT = 800 #simulation height
        self.WIDTH = 1100
        self.HEIGHT = 800
        self.FPS = 40
        self.sim_speed = 1
        self.rgb_colors = {"blue" : (0,0,255), "red" : (255,0,0), "green" : (0,255,0),
                           "yellow" : (255,255,50), "purple":(191, 64, 191)}
        self.colors_speed = {"blue" : 10, "red" : 20, "green" : 30, "yellow":40, "purple":50}
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.particles = []
        self.grids = {}
        self.radius = radius
        self.colors = colors
        self.attracts = attracts
        self.repulses = repulses
        self.rules = rules
        self.gravity = gravity
        self.expirmental = False
        self.grids = {}
        self.G_SIDE = 100 #grid size

    def start(self):
        #spawning particles
        self.particles = []
        self.grids = {}

        for color in self.colors:
            for i in range(1,self.num+1):
                rnd_x = random.randint(5, self.S_WIDTH -5)
                rnd_y = random.randint(5, self.S_HEIGHT-5)

                tmp = Particle(color,rnd_x,rnd_y, 1)
                self.particles.append(tmp)

        for i in range(self.S_WIDTH // self.G_SIDE):
            for j in range(self.S_HEIGHT // self.G_SIDE):
                grid = Grid([], (i * self.G_SIDE, j * self.G_SIDE))
                self.grids[(i * self.G_SIDE, j * self.G_SIDE)] = grid

        self.assign_par_to_grids()
        self.main()
    def assign_par_to_grids(self):
        for i in range(len(self.particles)):
            par = self.particles[i]
            grid_x = 0
            grid_y = 0
            if par.x >= 100: grid_x = int(str(par.x)[0]) * 100
            if par.y >= 100: grid_y = int(str(par.y)[0]) * 100
            self.grids[(grid_x, grid_y)].particles.append(par)

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
        grids = self.check_radius(par)
        for grid in grids:
            for particle in grid.particles:
                x_l = particle.x - par.x
                y_l = particle.y - par.y
                dist = (x_l ** 2 + y_l ** 2) ** 0.5
                if dist <= self.radius and x_l != 0 and y_l != 0:
                    moves = dist / self.colors_speed[par.color]
                    move = None
                    if dist <= 15:
                        x_move = x_l * abs(dist - 15)
                        y_move = y_l * abs(dist - 15)
                        move = (x_move - x_move * 3, y_move - y_move * 3)
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

    def calculate_move2(self, par):
        output = []
        for particle in self.particles:
            x_l = particle.x - par.x
            y_l = particle.y - par.y
            if y_l > self.radius * 0.75 and x_l > self.radius * 0.75: continue
            dist = (x_l ** 2 + y_l ** 2) ** 0.5

            if dist <= self.radius and x_l != 0 and y_l != 0:
                move = None
                force = self.rules[par.color][particle.color]
                if force == 0: force = 0.001
                moves = dist / force

                if dist <= 15:
                    x_move = x_l
                    y_move = y_l
                    move = (x_move - x_move * 2, y_move - y_move * 2)
                elif dist <= self.radius / 2 and force < 0:
                    x_move = x_l / moves
                    y_move = y_l / moves
                    move = (x_move - x_move *2, y_move - y_move *2)  # repulse
                elif force > 0:
                    move = (x_l / moves, y_l / moves)  # attracts
                else:
                    move = (0, 0)
                output.append(move)
        return output

    def calculate_move1(self,par):
        to_check= self.check_radius(par)
        sum = 0
        for grid in to_check:
            sum += len(grid.particles)
        print(sum )
        return 0

    def check_radius(self, par):
        to_check = []
        if par.x <= 100 and par.y <= 100: to_check.append(self.grids[(0, 0)])
        elif par.x <= 100: to_check.append(self.grids[(0, int(str(par.y)[0]) * 100)])
        elif par.y <= 100: to_check.append(self.grids[(int(str(par.x)[0]) * 100, 0)])
        else: to_check.append(self.grids[(int(str(par.x)[0]) * 100, int(str(par.y)[0]) * 100)])
        grids_to_side = self.radius // self.G_SIDE
        for i in range(grids_to_side):  # x and y axis
            x_left = int(float(str(par.x)[0])) * 100 - 100 * (i + 1)
            x_right = int(float(str(par.x + 100 * (i + 1))[0])) * 100
            y_bottom = int(float(str(par.y + (100 * (i + 1)))[0])) * 100
            y_top = int(float(str(par.y)[0])) * 100 - 100 * (i + 1)
            x_hundread = int(str(par.x)[0]) * 100 #first number from
            y_hundread = int(str(par.y)[0]) * 100 #first number from
            if par.x <= 99:
                x_left = 0
                x_hundread = 0
            elif par.y <= 99:
                y_top =0
                y_hundread = 0

            tmp_left = self.grids.get((x_left, y_hundread))
            tmp_right = self.grids.get((x_right, y_hundread))
            tmp_top = self.grids.get((x_hundread, y_top))
            tmp_bottom = self.grids.get((x_hundread, y_bottom))
            left_top = self.grids.get((x_left, y_top))
            left_bottom = self.grids.get((x_left, y_bottom))
            right_top = self.grids.get((x_right, y_bottom))
            right_bottom = self.grids.get((x_right, y_bottom))

            if tmp_left: to_check.append(tmp_left)
            if tmp_right: to_check.append(tmp_right)
            if tmp_top: to_check.append(tmp_top)
            if tmp_bottom: to_check.append(tmp_bottom)
            if left_bottom: to_check.append(left_bottom)
            if left_top: to_check.append(left_top)
            if right_bottom: to_check.append(right_bottom)
            if right_top: to_check.append(right_top)
        return to_check

    def handle_particles1(self):
        for par in self.particles:
            in_radius = self.calculate_move1(par)
            # x_move, y_move = in_radius
            # if 5 < par.x + x_move * self.sim_speed < self.S_WIDTH - 5:
            #     par.x += x_move * self.sim_speed
            # if 5 < par.y + y_move * self.sim_speed < self.S_HEIGHT - 5:
            #     par.y += y_move * self.sim_speed

    def handle_particles(self):
        for par in self.particles:
            if self.expirmental:
                in_radius = self.calculate_move2(par)
            else:
                in_radius = self.calculate_move(par)
            x_sum = 0
            y_sum = 0
            if in_radius:
                for move in in_radius:
                    x_sum += move[0]
                    y_sum += move[1]
                moves = [x_sum / len(in_radius), y_sum / len(in_radius)]  # avrage move
                if 5 < par.x + moves[0] * self.sim_speed < self.S_WIDTH - 5:
                    par.x += moves[0] * self.sim_speed
                else:
                    par.x += (moves[0] * self.sim_speed) - (moves[0] * self.sim_speed) * 2
                if 5 < par.y + moves[1] * self.sim_speed < self.S_HEIGHT - 5:
                    par.y += moves[1] * self.sim_speed
                else:
                    par.y += (moves[1] * self.sim_speed) - (moves[1] * self.sim_speed) * 2

    def handle_gravitation(self):
        for par in self.particles:
            if 5 < par.y + par.yv < self.S_HEIGHT - 5:
                par.y += par.yv
            else:
                par.yv -= (par.yv *2) * 0.75
            par.yv += 0.03 * par.mass * self.sim_speed

    def draw(self):
        self.WIN.fill((0,0,0))
        #particles
        for par in self.particles:
            pygame.draw.circle(self.WIN,self.rgb_colors[par.color], (par.x, par.y), 4)

        #menu
        m_width = self.WIDTH - self.S_WIDTH #menu width
        menu_bg = pygame.Rect(self.S_WIDTH, 0, m_width, self.HEIGHT)
        pygame.draw.rect(self.WIN, (200,200,200), menu_bg)
        self.draw_text(f"Simulation speed: {self.sim_speed} | Particles: {len(self.particles)}",
                       (255, 0, 0), 15, self.S_WIDTH + m_width / 2, 10, x_center=True)
        self.draw_text("1 - Draw On/Off", (255,0,0), 15,self.S_WIDTH + m_width / 2, 40, x_center= True)
        self.draw_text("2 - Change color", (255,0,0), 15,self.S_WIDTH + m_width / 2, 70, x_center= True)
        self.draw_text("3 - Start again", (255,0,0), 15,self.S_WIDTH + m_width / 2, 100, x_center= True)
        self.draw_text("4 - Sandbox", (255,0,0), 15,self.S_WIDTH + m_width / 2, 130, x_center= True)
        self.draw_text("5 - Gravity On/Off", (255,0,0), 15,self.S_WIDTH + m_width / 2, 160, x_center= True)
        self.draw_text(f"6 - Experimental model {self.expirmental}", (255,0,0), 15,self.S_WIDTH + m_width / 2, 190, x_center= True)
        self.draw_text("Arrows up/down simulation speed", (255,0,0), 15,self.S_WIDTH + m_width / 2, 220, x_center= True)

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
                        #start simulation again
                    if event.key == pygame.K_4:
                        self.WIN.fill((0,0,0))
                        self.particles = []
                    if event.key == pygame.K_5:
                        self.gravity = not self.gravity
                    if event.key == pygame.K_6:
                        self.expirmental = not self.expirmental
                    if event.key == pygame.K_UP:
                        self.sim_speed += 1
                        #speed up
                    if event.key == pygame.K_DOWN:
                        self.sim_speed -= 1
                        # if self.sim_speed != 0: self.sim_speed -= 1
                        #i need to put a comment here so i can minimaze this if statment in IDE :)
                if draw and event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    tmp = Particle(color, mouse_pos[0], mouse_pos[1],10)
                    self.particles.append(tmp)
            self.handle_particles()
            if self.gravity: self.handle_gravitation()
            self.draw()







