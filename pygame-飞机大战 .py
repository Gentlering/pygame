import pygame
import time
from pygame.locals import *
import random
#界面元素的基类
class Base(object):
    #飞机的基类
    def __init__(self,screen,x,y,imgsrc):
        #设置飞机默认位置
        self.x=x
        self.y=y

        #设置要显示内容的窗口
        self.screen=screen

        #保存英雄飞机的显示图片名字
        self.imageName=imgsrc

        #根据名字在背景图上生成飞机的图片
        self.image=pygame.image.load(self.imageName)


    def display(self):

        self.screen.blit(self.image,(self.x,self.y))


class BasePlane(Base):
    #飞机的基类
    def __init__(self,screen,x,y,imgsrc):
        super(BasePlane, self).__init__(screen,x,y,imgsrc)


        #用来保存英雄飞机发射出的所有的子弹
        self.bullets=[]
        #显示加载实物在页面
    def display(self):

        super(BasePlane, self).display()

        tmp=[]
        for bullet in self.bullets:
            bullet.display()
            bullet.move()
            if bullet.judge():
                tmp.append(bullet)
        for bullet in tmp:
            self.bullets.remove(bullet)
            #如果子弹已经移动到屏幕顶部则可从列表已移除

    def moveLeft(self):
        self.x-=5
    def moveRight(self):
        self.x+=5


class hero_plane(BasePlane):
    #玩家飞机
    def __init__(self,screen):

        super(hero_plane, self).__init__(screen,120,400,'./pic/hero.gif')

    def moveLeft(self):
        if self.x>0:
            self.x-=20
    def moveRight(self):
        if self.x<220:
            self.x+=20
    def moveUp(self):
        if self.y>0:
            self.y-=20
    def moveDown(self):
        if self.y<420:
            self.y+=20
    #射击
    def biu(self):
        #射出子弹的显示位置
        newBullet=Bullet(self.x,self.y,self.screen)
        self.bullets.append(newBullet)
        #把显示出的子弹添加到列表里多个显示

#  敌人的飞机
class enemy_plane(BasePlane):

    def __init__(self,screen):
        super(enemy_plane, self).__init__(screen, 0, 0, './pic/enemy1.png')

        self.direction="right"
     #敌机移动的轨迹
    def move(self):

        if self.x==0:
            self.direction='right'

        elif self.x==(320-60):
            self.direction='left'

        if self.direction=='right':
            self.moveRight()
        else:
            self.moveLeft()

    #射击
    def biu(self):
        #射出子弹的显示位置
        num=random.randint(1,50)
        if num==10:
            newBullet=EnemyBullet(self.x,self.y,self.screen)
            self.bullets.append(newBullet)  #把显示出的子弹添加到列表里多个显示


#子弹的基类
class BaseBullet(Base):
    #初始化显示属性
    def __init__(self,screen,x,y,imgsrc):
        super(BaseBullet, self).__init__(screen,x,y,imgsrc)

#hero子弹的类
class Bullet(BaseBullet):
    #初始化显示属性
    def __init__(self,x,y,screen):
        super(Bullet, self).__init__(screen,x+40,y-20,'./pic/bullet-3.gif')

    #子弹向上移动击中敌机    
    def move(self):
        self.y-=5

    def judge(self):
        return self.y<=0

#敌机子弹的类
class EnemyBullet(BaseBullet):
    #初始化显示属性
    def __init__(self,x,y,screen):
        super(EnemyBullet, self).__init__(screen,x+60,y+60,'./pic/bullet2.png')
    #子弹的运动轨迹
    def move(self):
        self.y+=5
    #子弹的越界
    def judge(self):
        return self.y>=550

def main():
    #创建窗口
    screen=pygame.display.set_mode((320,550),0,32)
    #创建bgc图片
    bgc=pygame.image.load('./pic/background.png')
    #创建英雄飞机
    hero=hero_plane(screen)
    #创建敌人飞机
    enemy=enemy_plane(screen)

#利用循环刷新图片移动位置更新界面
    while True:
        #显示背景图片
        screen.blit(bgc,(0,0))

        # 显示飞机
        hero.display()

        #显示敌机
        enemy.display()

        #敌机移动
        enemy.move()

        #敌机自动随机发弹
        enemy.biu()

        #检测键盘
        for event in pygame.event.get():
            #判断退出
            if event.type==QUIT:
                print("退出")
                exit()
            #判断是否按下键盘
            elif event.type==KEYDOWN:
                if event.key==K_a or event.key==K_LEFT:
                    print("向左移动")
                    hero.moveLeft()
                elif event.key==K_d or event.key==K_RIGHT:
                    print("向右移动")
                    hero.moveRight()
                elif event.key==K_w or event.key==K_UP:
                    print("向上移动")
                    hero.moveUp()
                elif event.key==K_s or event.key==K_DOWN:
                    print("向下移动")
                    hero.moveDown()
                elif event.key==K_SPACE:
                    print("射击")
                    hero.biu()
        pygame.display.update()
        #延迟循环执行时间提升cpu性能
        time.sleep(1/100)
if __name__=='__main__':
    print('程序开始')
    main()
else:
    print('程序结束')
