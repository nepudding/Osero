import pygame
from pygame.locals import *
import time
import sys

SCREEN = Rect(0,0,600,700)       
B_RECT = Rect(0,100,600,600)
COLOR = ["","黒","白"]

class Stone():
    def __init__ (self,pos,size,side): # 位置、大きさ、向き(0無 1黒 2白)
        self.pos = pos
        self.side = side
        self.size = size
    def draw(self,screen):
        rgb = [[],[0,0,0],[255,255,255],[255,0,0]][self.side]
        if self.side > 0:
            pygame.draw.circle(screen,rgb,self.pos,self.size,0)
    def set_side(self,side):
        self.side = side

class Message():
    def __init__(self,S,pos,rgb,font,size,time):
        self.sysfont = pygame.font.SysFont(font,size)
        self.text = self.sysfont.render(S,True,rgb)
        sx,sy = self.text.get_size()
        x,y = pos
        x -= sx//2
        y -= sy//2
        self.x = x
        self.y = y
        self.time = time
    def update(self):
        if self.time < time.time():
            self.text = None
    
    def draw(self,screen):
        self.update()
        if self.text: screen.blit(self.text,(self.x,self.y))


class ScoreBoard():
    white = 2
    black = 2
    def __init__(self):
        self.sysfont = pygame.font.SysFont("hg行書体hgp行書体hgs行書体",80)
        self.text = self.sysfont.render("黒の番",True,(0,0,0))
        self.b_score = self.sysfont.render(str(self.black),True,(255,255,255))
        self.w_score = self.sysfont.render(str(self.white),True,(0,0,0))
    def draw(self,screen):
        x,y = self.text.get_size()
        screen.blit(self.text,(300-x/2,50-y/2))
        x,y = self.b_score.get_size()
        pygame.draw.circle(screen,(0,0,0),(50,50),48,0)
        screen.blit(self.b_score,(50-x/2,50-y/2))
        x,y = self.w_score.get_size()
        pygame.draw.circle(screen,(255,255,255),(550,50),48,0)
        screen.blit(self.w_score,(550-x/2,50-y/2))
        
    def add_score(self,side,i):
        if side == 1:
            self.black += 1+i
            self.white -= i
        elif side == 2:
            self.black -= i
            self.white += 1+i
        self.b_score = self.sysfont.render(str(self.black),True,(255,255,255))
        self.w_score = self.sysfont.render(str(self.white),True,(0,0,0))
    def set_text(self,S,side):
        rgb = [[120,0,0],[0,0,0],[255,255,255]][side]
        self.text = self.sysfont.render(S,True,rgb)
class Board():
    turn = 0 # 1黒 2白
    a = [[0]*8 for i in range(8)] # 石の情報を保存,スコアボードも内蔵
    assist = [[0]*8 for i in range(8)]  # アシストの情報を保存
    def __init__(self,X):
        self.score = ScoreBoard()
        self.message = Message("",(0,0),(0,0,0),"hg行書体hgp行書体hgs行書体",0,0)
        sx,sy,ex,ey = X
        for y in range(8):
            for x in range(8):
                pos = (int(sx+(ex)/16 * (x*2+1)),int(sy+(ey)/16 * (y*2+1)))
                self.a[y][x] = Stone(pos,33,0)
                self.assist[y][x] = Stone(pos,5,0)
        for i in range(3,5):
            for j in range(3,5):
                self.a[i][j].set_side((i+j+1)%2+1)
        
        self.next_turn()
        
    def draw(self,screen):
        self.score.draw(screen)
        for i in range(8):
            for j in range(8):
                self.a[i][j].draw(screen)
                self.assist[i][j].draw(screen)
        self.message.draw(screen)
    
    def set_stone(self,x,y):
        q = self.can_put(x,y)
        if q:
            self.score.add_score(self.turn,len(q))
            self.a[y][x].set_side(self.turn)
            for xq,yq in q:
                self.a[yq][xq].set_side(self.turn)
            # ターン交代
            if self.next_turn() == 0:
                self.pass_turn()
                if self.next_turn() == 0:
                    self.game_end()
    def next_turn(self):
        self.turn = self.turn%2 +1
        self.score.set_text(COLOR[self.turn]+"の番",self.turn)
        hoge = 0
        for i in range(8):
            for j in range(8):
                can = bool(self.can_put(j,i))
                hoge += can
                self.assist[i][j].set_side(can*3)
        return hoge
    
    def game_end(self):
        self.message = Message("",(0,0),(0,0,0),"hg行書体hgp行書体hgs行書体",0,0)
        if self.score.white > self.score.black:
           win = 2
        elif self.score.white < self.score.black:
            win = 1
        else:
            win = 0
        text = ["引き分け","黒の勝ち","白の勝ち"][win]
        self.score.set_text(text,win)
    def pass_turn(self):
        self.message = Message("パ ス",(300,200),(255,0,0),"hg行書体hgp行書体hgs行書体",150,time.time()+0.8)#,(0,0),(0,0,0),"hg行書体hgp行書体hgs行書体",0,0)

    def can_put(self,x,y):
        if self.a[y][x].side != 0:
            return []
        reverse_stone = []
        for vx in [-1,0,1]:
            for vy in [-1,0,1]:
                if vx == vy == 0:
                    continue
                i = 1
                hoge = []
                while 0<=(x+vx*i)<8 and 0<=(y+vy*i)<8:
                    if self.a[y+vy*i][x+vx*i].side == self.turn:
                        reverse_stone += hoge
                        break
                    elif self.a[y+vy*i][x+vx*i].side == 0:
                        break
                    else:
                        hoge.append([x+vx*i,y+vy*i])
                        i += 1
        return reverse_stone

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN.size)
    pygame.display.set_caption('オセロを作りたかった')
    stoneSize = 33
    clock = pygame.time.Clock()

    # 盤
    board = Board(B_RECT)
    # スコアボード
    side = 0

    while 1:
        clock.tick(30) # フレームレート 30fps
        screen.fill((150,150,150))
        pygame.draw.rect(screen,(0,80,0),B_RECT)
        draw_line(screen)
        board.draw(screen)
        pygame.display.update()
        
        # イベント管理
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                x,y = event.pos
                x = x//75
                y = (y-100)//75
            if event.type == MOUSEBUTTONDOWN:
                if x >=0 and y>=0:
                    board.set_stone(x,y)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

def draw_line(screen):
    S = 600
    for i in range(1,8):
        pygame.draw.line(screen,(0,0,0),(0,100+S/8*i),(S,S/8*i+100),3) # screen,RGB,始点,終点,太さ
        pygame.draw.line(screen,(0,0,0),(S/8*i,100),(S/8*i,S+100),3) # screen,RGB,始点,終点,太さ


if __name__ == "__main__":
    main()