'''
    Based on a tutorial: https://www.youtube.com/watch?v=8nIi2x2m6yE&ab_channel=TechWithTim
    Code By Martyna Budrewicz
'''
import pygame
import time
import random
import math

WIDTH, HEIGHT = 800, 600
FPS = 60
LAUNCH_AMT = 5
LAUNCHER_OFFSET = 50
def hex_to_rgb(hex): # takes a string starting with a '#'
    hex = hex[1:]
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
COLORS = [
    hex_to_rgb("#060761"),
    hex_to_rgb("#050437"),
    hex_to_rgb("#C54A85"),
    hex_to_rgb("#113BC6"),
    hex_to_rgb("#060406"),
]
BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))

launchers = []

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HAPPY NEW YEAR!!")

def draw():
    win.blit(BG, (0,0))
    
    for launcher in launchers:
        launcher.draw(win)
    
    pygame.display.update()

class Projectile:
    WIDTH, HEIGHT = 3, 10
    ALPHA_DECREMENT_MIN, ALPHA_DECREMENT_MAX = 3, 7
    
    def __init__(self, x, y, x_vel, y_vel, color):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.color = color
        self.alpha = 255
        self.alpha_dec = random.randrange(self.ALPHA_DECREMENT_MIN, self.ALPHA_DECREMENT_MAX)
        
    def draw(self, win):
        self.draw_rect_alpha(win, self.color + (self.alpha, ), (self.x, self.y, self.WIDTH, self.HEIGHT))
        
    @staticmethod
    def draw_rect_alpha(surface, color, rect):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect) 
        
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.alpha = max(0, self.alpha - self.alpha_dec)
        
class Firework:
    RADIUS = 10
    MIN_PROJECTILES = 25
    MAX_PROJECTILES = 50
    PROJECTILE_VEL = 4
    
    def __init__(self, x, y, y_vel, explode_height, color):
        self.x = x
        self.y = y
        self.y_vel = y_vel
        self.explode_height = explode_height
        self.color = color
        self.exploded = False
        self.projectiles = []
        
    def explode(self):
        self.exploded = True
        
        if random.randint(0, 10) == 0: # 10% chance for star
            self.create_star_projectiles()
        else:
            self.create_circ_projectiles()
        
    def create_circ_projectiles(self):
        num_projectiles = random.randrange(self.MIN_PROJECTILES, self.MAX_PROJECTILES)
        vel = random.randrange(self.PROJECTILE_VEL-1, self.PROJECTILE_VEL+1)
        angle_dif = math.pi*2 / num_projectiles
        current_angle = 0
        for _ in range(num_projectiles):
            x_vel = vel * math.cos(current_angle)
            y_vel = vel * math.sin(current_angle)
            color = random.choice(COLORS)
            self.projectiles.append(
                Projectile(self.x, self.y, x_vel, y_vel, color))
            current_angle += angle_dif
    
    def create_star_projectiles(self):
        ARMS = 8
        PROJ_AMT = ARMS * ARMS
        angle_dif = math.pi*2 / ARMS
        current_angle = 0
        for i in range(1, PROJ_AMT+1):
            vel = max(1, self.PROJECTILE_VEL-3) + (i % ARMS)
            x_vel = vel * math.cos(current_angle)
            y_vel = vel * math.sin(current_angle)
            color = random.choice(COLORS)
            self.projectiles.append(
                Projectile(self.x, self.y, x_vel, y_vel, color))
            if i % ARMS == 0:
                current_angle += angle_dif
            
        
    def move(self):
        if not self.exploded:
            self.y += self.y_vel
            if self.y <= self.explode_height:
                self.explode()
                
        projectiles_to_remove = []
        for projectile in self.projectiles:
            projectile.move()
            if projectile.x < 0 or projectile.x >= WIDTH or projectile.y < 0 or projectile.y >= HEIGHT:
                projectiles_to_remove.append(projectile)
            
        for projectile in projectiles_to_remove:
            self.projectiles.remove(projectile)

        
    def draw(self, win):
        if not self.exploded:
            pygame.draw.circle(win, self.color, (self.x, self.y), self.RADIUS)
            
        for projectile in self.projectiles:
            projectile.draw(win)

class Launcher:
    LWIDTH = LHEIGHT = 20
    FREQ_MIN, FREQ_MAX = 1000, 3000
    COLOR = "Grey"
    
    def __init__(self, x, y):
        self.x = x - self.LWIDTH/2
        self.y = y - self.LHEIGHT
        self.freq = random.randrange(self.FREQ_MIN, self.FREQ_MAX) # ms
        self.start_time = time.time()
        self.fireworks = []
    
    def draw(self, win): # win - window (surface)
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.LWIDTH, self.LHEIGHT))
        
        for firework in self.fireworks:
            firework.draw(win)
        
    def launch(self):
        y_vel = -5
        explode_height = random.randrange(60, int(HEIGHT/2))
        color = random.choice(COLORS)
        firework = Firework(self.x + self.LWIDTH/2, self.y, y_vel, explode_height, color)
        self.fireworks.append(firework)
        
    def loop(self): # generating fireworks
        current_time = time.time()
        time_elapsed = (current_time - self.start_time) * 1000 # ms
        
        if(time_elapsed >= self.freq):
            self.start_time = time.time()
            self.launch()
            self.freq = random.randrange(self.FREQ_MIN, self.FREQ_MAX)
       
        # move all of the fireworks and remove those that are exploded and don't have any projectiles left
        fireworks_to_remove = []
        for firework in self.fireworks:
            firework.move()
            if firework.exploded and len(firework.projectiles) == 0:
                fireworks_to_remove.append(firework)
                
        for firework in fireworks_to_remove:
            self.fireworks.remove(firework)
    

def main():    
    # creating launchers
    DIST_BETWEEN = (WIDTH - 2*LAUNCHER_OFFSET) / (LAUNCH_AMT-1)
    
    for i in range(LAUNCH_AMT):
        l = Launcher(i*DIST_BETWEEN + LAUNCHER_OFFSET, HEIGHT)
        launchers.append(l)
    
    # game loop
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
              
        for launcher in launchers:
            launcher.loop()
            
        # drawing what we've got
        draw()
                
    pygame.quit()

if __name__ == "__main__":
    main()