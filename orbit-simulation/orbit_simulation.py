'''
    Based on a tutorial: https://www.youtube.com/watch?v=WTLPmUHTPqo&t=3132s&ab_channel=TechWithTim
    Code By Martyna Budrewicz
    
    Ideas to add:
        - make radiuses in scale of the real ones
'''
import pygame
import math

WIDTH, HEIGHT = 800, 800
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbit simulation")
FPS = 60
FONT = pygame.font.SysFont("comicsans", 16)

C_SUN = (245, 218, 7)
C_MERCURY = (253, 191, 0)
C_VENUS = (255, 200, 95)
C_EARTH = (135, 220, 255)
C_MARS = (219, 53, 41)

PLANETS = []

class Planet:
    G = 6.67428e-11
    AU = 149.6e6 * 1000 # m
    SCALE = 200 / AU # 1AU = 100 pixels
    TIMESTEP = 3600*24 # 1 day
    
    def __init__(self, x, y, radius, color, image, mass, y_vel):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.image = pygame.transform.scale(pygame.image.load(image), (radius*2, radius*2))
        self.mass = mass
        
        self.orbid = []
        self.is_sun = False
        self.sun_dist = x
        
        self.x_vel = 0
        self.y_vel = y_vel
        
    def draw(self):
        x = -self.x * self.SCALE + WIDTH/2
        y = -self.y * self.SCALE + HEIGHT/2
        
        if len(self.orbid) > 2:
            updated_points = []
            for point in self.orbid:
                x, y = point
                x = x * self.SCALE + WIDTH/2
                y = y * self.SCALE + HEIGHT/2
                updated_points.append((x, y))
            pygame.draw.lines(win, self.color, False, updated_points, 2)
            
        rect = self.image.get_rect().move((x - self.radius, y - self.radius))
        win.blit(self.image, rect)
        #pygame.draw.circle(win, self.color, (x, y), self.radius)    
            
        if not self.is_sun:
            distance_text = FONT.render(f"{round(self.sun_dist/1000, 0)}km", 1, "white")
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))
    
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        dist_x = other_x - self.x
        dist_y = other_y - self.y
        dist = math.sqrt(dist_x ** 2 + dist_y ** 2)
        
        if other.is_sun:
            self.sun_dist = dist
        
        theta = math.atan2(dist_y, dist_x)
        force = self.G * self.mass * other.mass / dist**2 # F
        force_x = force * math.cos(theta)
        force_y = force * math.sin(theta)
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
            
        self.x_vel += total_fx / self.mass * self.TIMESTEP # v = F/(mt)
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        
        self.x += self.x_vel * self.TIMESTEP # s = vt
        self.y += self.y_vel * self.TIMESTEP
        self.orbid.append((self.x, self.y))

def draw():
    win.fill("black")
    for planet in PLANETS:
        planet.update_position(PLANETS)
        planet.draw()
        
    pygame.display.update()

def main():
    sun = Planet(0, 0, 15, C_SUN, "sun.png", 1.98847 * 10**30, 0)
    sun.is_sun = True
    mercury = Planet(0.387 * Planet.AU, 0, 10, C_MERCURY, "mercury.png", 0.330 * 10**24, 47.4 * 1000)
    venus = Planet(0.723 * Planet.AU, 0, 10, C_VENUS, "venus.png", 4.87 * 10**24, -35.02 * 1000)
    earth = Planet(1 * Planet.AU, 0, 10, C_EARTH, "earth.png", 5.97 * 10**24, 29.783 * 1000)
    mars = Planet(1.524 * Planet.AU, 0, 10, C_MARS, "mars.png", 0.642 * 10**24, 24.077 * 1000)
    
    PLANETS.append(sun)
    PLANETS.append(mercury)
    PLANETS.append(venus)
    PLANETS.append(earth)
    PLANETS.append(mars)

    # game loop
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        draw()
            
    pygame.quit()

if __name__ == "__main__":
    main()