#Should add the 4 Player version as well
#Should handel WSS connection

WIDTH, HEIGHT = 1700, 1100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 150
BALL_RADIUS = 1
WINNING_SCORE = 11
CONST_VEL = 10
VEL_INCREMENT = 2

class Ball:
    VEL = CONST_VEL
    COLOR = (255, 255, 255)

    def __init__(self, y, x, radius):
        self.original_x = x
        self.original_y = y
        self.x = self.original_x
        self.y = self.original_y
        self.radius = radius
        self.x_vel = self.VEL
        self.y_vel = 0
        self.winner = -1

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self, direction):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.VEL = CONST_VEL
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

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


class PingPong:
  def __init__(self):
    self.paddle_r = Player(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, WHITE)
    self.paddle_l = Player(WIDTH - 10 - PADDLE_WIDTH, (HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT, WHITE)
    self.ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
    self.ready = False
    self.game_over = False
    self.scorer = -1
    self.speedPlayer = 100


  def handle_collision(self):

    if self.ball.y + self.ball.radius >= HEIGHT:
        self.ball.y_vel *= -1
    elif self.ball.y - self.ball.radius <= 0:
        self.ball.y_vel *= -1
    print(self.ball.VEL)
    if self.ball.x_vel < 0:
        if self.ball.y >= self.paddle_l.y and self.ball.y <= self.paddle_l.y + self.paddle_l.height: # Check for collision with left paddle
            if self.ball.x - self.ball.radius <= self.paddle_l.x + self.paddle_l.width: # Check if ball is within the width of the paddle
                self.scorer = 0
                self.ball.x_vel *= -1
                if self.ball.x_vel <= 20:
                    self.ball.x_vel += 0.5
                middle_y = self.paddle_l.y + self.paddle_l.height / 2
                self.ball.VEL += VEL_INCREMENT
                difference_in_y = middle_y - self.ball.y
                reduction_factor = (self.paddle_l.height / 2) / self.ball.VEL
                y_vel = difference_in_y / reduction_factor
                self.ball.y_vel = -1 * y_vel
    else:
        if self.ball.y >= self.paddle_r.y and self.ball.y <= self.paddle_r.y + self.paddle_r.height:
            if self.ball.x + self.ball.radius >= self.paddle_r.x:
                self.scorer = 1
                if self.ball.x_vel <= 20:
                    self.ball.x_vel += 0.5
                self.ball.x_vel *= -1
                self.ball.VEL += VEL_INCREMENT
                middle_y = self.paddle_r.y + self.paddle_r.height / 2
                difference_in_y = middle_y - self.ball.y
                reduction_factor = (self.paddle_r.height / 2) / self.ball.VEL
                y_vel = difference_in_y / reduction_factor
                self.ball.y_vel = -1 * y_vel
    print(self.ball.VEL)

    if self.ball.x + self.ball.radius <= 0:
      self.scorer = 1  # Player 1 scores
      self.reset_game()
    elif self.ball.x - self.ball.radius >= WIDTH:
      self.scorer = 0  # Player 2 scores
      self.reset_game()


  def get_game_state(self):
    self.handle_collision()
    self.ball.move()
    game_state ={
      'type': 'update',
      'ball_x': self.ball.x,
      'ball_y': self.ball.y,
      'paddle_l': self.paddle_l.y,
      'paddle_r': self.paddle_r.y,
      'leftPlyrScore': self.paddle_l.score,
      'rightPlyrScore': self.paddle_r.score,
      'game_over': self.game_over
    }
    return game_state

  def startWithInitialValues(self, message):
    if message:
        global WIDTH, HEIGHT, PADDLE_HEIGHT, PADDLE_WIDTH, BALL_RADIUS, WINNING_SCORE
        WIDTH = message.get('screen').get('_width')
        HEIGHT = message.get('screen').get('_height')
        PADDLE_HEIGHT = message.get('paddle_l').get('_height')  
        PADDLE_WIDTH = message.get('paddle_l').get('_width')
        BALL_RADIUS = message.get('ball').get('_radius')

        self.paddle_l.y = message.get('paddle_l').get('_y')
        self.paddle_l.x = message.get('paddle_l').get('_x')
        self.paddle_l.width = message.get('paddle_l').get('_width')
        self.paddle_l.height = message.get('paddle_l').get('_height')
        self.paddle_r.y = message.get('paddle_r').get('_y')
        self.paddle_r.x = message.get('paddle_r').get('_x')
        self.paddle_r.width = message.get('paddle_r').get('_width')
        self.paddle_r.height = message.get('paddle_r').get('_height')

        self.ball.x = message.get('ball').get('_x')
        self.ball.y = message.get('ball').get('_y')
        self.ball.radius = message.get('ball').get('_radius')

    self.paddle_l.score = 0
    self.paddle_r.score = 0
    self.scorer = -1
    self.game_over = False
    self.ready = True

  def update_paddle_position(self, message):
    direction = message.get('direction')
    net_height = HEIGHT - PADDLE_HEIGHT
    if  self.game_over and direction == 'ENTER':
        self.reset_game()
        self.paddle_l.score = 0
        self.paddle_r.score = 0
        self.dir_x = 3
        self.dir_y = 1
    if direction == 'UP':
        if self.paddle_l.y - self.speedPlayer >= 0:
            self.paddle_l.y -= self.speedPlayer
        else:
            self.paddle_l.y = 0
    elif direction == 'DOWN':
        if self.paddle_l.y + self.speedPlayer <= net_height:
            self.paddle_l.y += self.speedPlayer
        else:
            self.paddle_l.y = net_height
    elif direction == 'AUP':
        if self.paddle_r.y - self.speedPlayer >= 0:
            self.paddle_r.y -= self.speedPlayer
        else:
            self.paddle_r.y = 0
    elif direction == 'ADOWN':
        if self.paddle_r.y + self.speedPlayer <= net_height:
            self.paddle_r.y += self.speedPlayer
        else:
            self.paddle_r.y = net_height

  def reset_game(self):
    self.ball.reset(direction=("left" if self.scorer == 1 else "right"))
    self.paddle_l.score += (1 if self.scorer == 0 else 0)
    self.paddle_r.score += (1 if self.scorer == 1 else 0)
    self.scorer = -1
    self.check_game_over()

  def check_game_over(self):
    self.game_over = self.paddle_l.score >= WINNING_SCORE or self.paddle_r.score >= WINNING_SCORE


#     if (self.ball.x - self.ball.radius <= self.paddle_l.x + self.paddle_l.width and
  #      self.ball.y >= self.paddle_l.y and self.ball.y <= self.paddle_l.y + self.paddle_l.height):
 #     self.ball.x_vel = -self.ball.x_vel
#
  #  elif (self.ball.x + self.ball.radius >= self.paddle_r.x and
 #         self.ball.y >= self.paddle_r.y and self.ball.y <= self.paddle_r.y + self.paddle_r.height):
#      self.ball.x_vel = -self.ball.x_vel

   # Check for wall collision
#   if self.ball.y + self.ball.radius >= HEIGHT or self.ball.y - self.ball.radius <= 0:
#      self.ball.y_vel = -self.ball.y_vel