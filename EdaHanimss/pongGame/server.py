import json

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.paddle_r = Player()
        self.paddle_l = Player()
        self.ball = Ball()

scorer = -1

player_count = 2
WIDTH, HEIGHT = 700, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
WINNING_SCORE = 11

two_player_objects = [
    Player(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, WHITE),
    Player(WIDTH - 10 - PADDLE_WIDTH, (HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT, WHITE),
    Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
]

objects_to_send = two_player_objects

def score(last_to_touch, outside):
    global scorer
    if last_to_touch == -1:
        if outside == 0 or outside == 2:
            winner = outside + 1
        elif outside == 1 or outside == 3:
            winner = outside - 1
    else:
        winner = last_to_touch
    if outside == last_to_touch:
        objects_to_send[last_to_touch].score -= 1
    else:
        objects_to_send[winner].score += 1
        if objects_to_send[winner].score >= WINNING_SCORE:
            objects_to_send[player_count].winner = last_to_touch
    scorer = -1

def handle_collision(ball, left_paddle, right_paddle, upper_paddle=None, lower_paddle=None):
    global scorer
    if upper_paddle is not None:
        if ball.y_vel < 0:
            if ball.x >= upper_paddle.x and ball.x <= upper_paddle.x + upper_paddle.width:
                if ball.y - ball.radius <= upper_paddle.y + upper_paddle.height:
                    scorer = 2
                    ball.y_vel *= -1
                    if ball.y_vel <= 20:
                        ball.y_vel += 0.5
                    middle_x = upper_paddle.x + upper_paddle.width / 2
                    difference_in_x = middle_x - ball.x
                    reduction_factor = (upper_paddle.width / 2) / ball.VEL
                    x_vel = difference_in_x / reduction_factor
                    ball.x_vel = -1 * x_vel
        else:
            if ball.x >= lower_paddle.x and ball.x <= lower_paddle.x + lower_paddle.width:
                if ball.y + ball.radius >= lower_paddle.y:
                    scorer = 3
                    if ball.x_vel <= 20:
                        ball.x_vel += 0.5
                    ball.y_vel *= -1
                    middle_x = lower_paddle.x + lower_paddle.width / 2
                    difference_in_x = middle_x - ball.x
                    reduction_factor = (lower_paddle.width / 2) / ball.VEL
                    x_vel = difference_in_x / reduction_factor
                    ball.x_vel = -1 * x_vel
    else:
        if ball.y + ball.radius >= HEIGHT:
            ball.y_vel *= -1
        elif ball.y - ball.radius <= 0:
            ball.y_vel *= -1
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                scorer = 0
                ball.x_vel *= -1
                if ball.x_vel <= 20:
                    ball.x_vel += 0.5
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                scorer = 1
                if ball.x_vel <= 20:
                    ball.x_vel += 0.5
                ball.x_vel *= -1
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


async def get_game_state(self, player, messages):
    self.ball.move()
    handle_collision(self.ball, self.paddle_l, self.paddle_r)
    if self.ball.x - self.ball.radius < 0:
        self.ball.reset("left")
        score(self.scorer, 0)
    elif self.ball.x + self.ball.radius > self.WIDTH:
        self.ball.reset("right")
        score(self.scorer, 1)
    elif self.ball.y - self.ball.radius < 0:
        self.ball.reset("up")
        score(self.scorer, 2)
    elif self.ball.y + self.ball.radius > self.HEIGHT:
        self.ball.reset("down")
        score(self.scorer, 3)

    game_state = {
        'type': 'update',
        'ball_x': self.ball.x,
        'ball_y': self.ball.y,
        'paddle_l': self.paddle_l.y,
        'paddle_r': self.paddle_r.y,
        'left_score': self.paddle_l.score,
        'right_score': self.paddle_r.score,
    }

    await messages.send(json.dumps(game_state))

