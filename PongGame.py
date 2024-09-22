import pygame
pygame.init()

Width,Height=700,500
screen=pygame.display.set_mode((Width,Height))
pygame.display.set_caption("Pong")
Paddle_width,Paddle_height=20,100

White=(255,255,255)
clock=pygame.time.Clock()
fps=60
Radius=7
Score_font=pygame.font.SysFont("comicssans",50)
Winning_score=10
class Paddle:
    vel=4
    def __init__(self,x,y,width,height):
        self.x=self.orignal_x=x
        self.y=self.orignal_y=y
        self.width=width
        self.height=height

    def draw(self):
        pygame.draw.rect(screen,White,(self.x,self.y,self.width,self.height))
    def move(self,up=True):
        if up:
            self.y-=self.vel
        else:
            self.y+=self.vel
    def reset(self):
        self.x=self.orignal_x
        self.y=self.orignal_y




class Ball:
    Max_vel=5
    def __init__(self,x,y,radius):
        self.x=self.orignal_x=x
        self.y=self.orignal_y=y
        self.radius=radius
        self.x_vel=self.Max_vel
        self.y_vel=0
    def draw(self):
        pygame.draw.circle(screen,White,(self.x,self.y),self.radius)
    def move(self):
        self.x += self.x_vel
        self.y+=self.y_vel
    def reset(self):
        self.x = self.orignal_x
        self.y=self.orignal_y
        self.y_vel=0
        self.x_vel*=-1


def handle_collision(ball,left_paddle,right_paddle):
    if ball.y+ball.radius >=Height:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel*= -1

    if ball.x_vel <0:
        if ball.y >= left_paddle.y and ball.y<=left_paddle.y+ left_paddle.height:
            if ball.x-ball.radius<= left_paddle.x+left_paddle.width:
                ball.x_vel *=-1

                middle_y=left_paddle.y + left_paddle.height/2
                difference_in_y=middle_y-ball.y
                reduction_factor = (left_paddle.height/2)/ball.Max_vel
                y_vel=difference_in_y/reduction_factor
                ball.y_vel = -1* y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel*=-1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.Max_vel
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1*y_vel


def paddle_movement(keys,left_paddle,right_paddle):
    if keys[pygame.K_w] and left_paddle.y>=0 :
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y+left_paddle.height<=Height:
        left_paddle.move(up=False)

    if  keys[pygame.K_UP] and right_paddle.y>=0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y+right_paddle.height<=Height:
        right_paddle.move(up=False)


def dotted_line():
    for i in range(10,Height,Height//20):
        if i % 2==1:
            continue
        pygame.draw.rect(screen,White,(Width//2-5,i,10,Height//20))

def Score(left_score,right_score,Score_font):
    left_score_text = Score_font.render(f"{left_score}",1,White)
    screen.blit(left_score_text,(Width//4-left_score_text.get_width()//2,20))

    right_score_text = Score_font.render(f"{right_score}", 1, White)
    screen.blit(right_score_text, (Width *(3/4) - right_score_text.get_width() // 2, 20))

left_paddle=Paddle(10,Height//2-Paddle_height//2,Paddle_width,Paddle_height)
right_paddle=Paddle(Width-10-Paddle_width,Height//2-Paddle_height//2,Paddle_width,Paddle_height)
ball=Ball(Width//2,Height//2,Radius)

left_score=0
right_score=0

run=True
while run:

    screen.fill((0,0,0))
    Score(left_score,right_score,Score_font)
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    left_paddle.draw()
    right_paddle.draw()
    ball.draw()

    ball.move()

    keys=pygame.key.get_pressed()
    paddle_movement(keys,left_paddle,right_paddle)

    dotted_line()

    handle_collision(ball, left_paddle, right_paddle)

    if ball.x<0:
        right_score +=1
        ball.reset()
    elif ball.x>Width:
        left_score+=1
        ball.reset()

    won=False
    if left_score>=Winning_score:
        won=True
        win_text='Left Player Won!'
    elif right_score>= Winning_score:
        won=True
        win_text="Right Player Won!"

    if won:
        ball.reset()
        left_paddle.reset()
        right_paddle.reset()
        text=Score_font.render(win_text,1,White)
        screen.blit(text,(Width//2-text.get_width()//2,Height//2))
        pygame.display.update()
        pygame.time.delay(5000)
        left_score=0
        right_score=0


    pygame.display.update()