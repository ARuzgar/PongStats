

class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 3
        self.score = 0

    def move(self, posY):
        if posY == -1:
            self.y -= self.vel
        if posY == 1:
            self.y += self.vel
        self.update()

    def move_sideways(self, posX):
        if posX == -1:
            self.x -= self.vel
        if posX == 1:
            self.x += self.vel
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
        
class Ball:
    VEL = 5
    COLOR = (255, 255, 255)

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.VEL
        self.y_vel = 0
        self.winner = -1

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self, direction):
        self.x = self.original_x
        self.y = self.original_y
        self.VEL = 5
        if direction == "left":
            self.x_vel = self.VEL
            self.y_vel = 0
        elif direction == "right":
            self.x_vel = -self.VEL
            self.y_vel = 0
        elif direction == "up":
            self.x_vel = 0
            self.y_vel = self.VEL
        elif direction == "down":
            self.x_vel = 0
            self.y_vel = -self.VEL