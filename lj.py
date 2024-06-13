import pygame
import math
import random
pygame.init()

space_size = 500
screen = pygame.display.set_mode([space_size, space_size])

clock = pygame.time.Clock()
rate = 60  # frames per second
dt = 1 / rate  # Time step between frames
sigma = 10
sigma2 = sigma*sigma
e = 5

def LJ_force(p1,p2):
    rx = p1.x - p2.x
    ry = p1.y - p2.y

    r2 = rx*rx+ry*ry

    r2s = r2/sigma2+1
    r6s = r2s*r2s*r2s
    f = 24*e*( 2/(r6s*r6s) - 1/(r6s) )

    p1.ax += f*(rx/r2)
    p1.ay += f*(ry/r2)
    p2.ax -= f*(rx/r2)
    p2.ay -= f*(ry/r2)

def Verlet_step(particles, h):
    for p in particles:
        p.verlet1_update_vx(h)
        p.handle_wall_collision(space_size)
    for i, p1 in enumerate(particles):
        for p2 in particles[i+1:]:
            LJ_force(p1,p2)
    for p in particles:
        p.verlet2_update_v(h)


class Particle:
    def __init__(self, x, y, vx, vy, size, color):
        # x = x position, y = y position, vx = velosity of x, vy = velocity of y, r = radius, color = color of bead
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.color = color
        self.m = 1
        self.ax = 0
        self.ay = 0
    
    def verlet1_update_vx(self,h):
        self.vx += self.ax*h/2
        self.vy += self.ay*h/2
        self.x += self.vx*h
        self.y += self.vy*h
        self.ax = 0
        self.ay = 0

    def verlet2_update_v(self,h):
        self.vx += self.ax*h/2
        self.vy += self.ay*h/2

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
    
    def handle_wall_collision(self, space_size):
        # wall collision
        if (self.x - self.size < 0) or (self.x + self.size > space_size):
            self.vx = -self.vx
        if (self.y - self.size < 0) or (self.y + self.size > space_size):
            self.vy = -self.vy

width, height = 100, 100
number_of_particles = 50
my_particles = []
timesteps = 10 

for n in range(number_of_particles):
    x = 1.0*random.randint(15, width-15)
    y = 1.0*random.randint(15, height-15)
    vx, vy = 0., 0.
    for k in range(6):
        vx += random.randint(-10, 10)/2.
        vy += random.randint(-10, 10)/2.

    particle = Particle(x, y,vx,vy, 10,(255, 0, 0))

    my_particles.append(particle)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for k in range(timesteps):
        Verlet_step(my_particles, dt/timesteps)

    for particle in my_particles:
        particle.handle_wall_collision(space_size)
        particle.draw(screen)

    pygame.display.flip()

    clock.tick(rate)


pygame.quit()

    

    
