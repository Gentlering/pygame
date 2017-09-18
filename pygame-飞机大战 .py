import pygame
import time
from pygame.locals import *
import random

class Base(object):
    '基类的基类，也就是所有界面元素的基类'

    def __init__(self, screen, x, y, imagePath):
        # 子弹的坐标
        self.x = x
        self.y = y

        # 子弹的图片
        self.imagePath = imagePath
        self.image = pygame.image.load(self.imagePath)

        # 显示的窗口
        self.screen = screen

    def display(self):
        '显示子弹'
        self.screen.blit(self.image, (self.x,self.y))

class BasePlane(Base):
    '飞机基类'

    def __init__(self, screen, x, y, imagePath):
        super(BasePlane, self).__init__(screen, x, y, imagePath)

        # 子弹的列表
        self.bullets = []

    def display(self):
        '显示飞机'
        super(BasePlane, self).display()

        # 遍历列表的同时，删除列表的元素，是不稳定的代码
        # for bullet in self.bullets:
        #     bullet.display()
        #     bullet.move()
        #
        #     # 如果子弹已经移动到屏幕之外，则可以从子弹列表移除
        #     if bullet.y <= 0:
        #         self.bullets.remove(bullet)

        # 删除列表的数据，最好是使用一个临时列表來中转
        tmp = []
        for bullet in self.bullets:
            bullet.display()
            bullet.move()

            # 如果子弹已经移动到屏幕之外，则可以从子弹列表移除
            if bullet.judge():
                tmp.append(bullet)

        for bullet in tmp:
            self.bullets.remove(bullet)

    def moveLeft(self):
        '玩家飞机，向左移动'
        self.x -= 5

    def moveRight(self):
        '玩家飞机，向右移动'
        self.x += 5

class BaseBullet(Base):
    '子弹的基类'

    def __init__(self, screen, x, y, imagePath):
        super(BaseBullet, self).__init__(screen, x, y, imagePath)

class HeroPlane(BasePlane):
    '玩家飞机'

    def __init__(self, screen):
        super(HeroPlane, self).__init__(screen, 190, 550, './feiji/hero.gif')

    def shoot(self):
        '发射一颗子弹'
        # print('biu biu biu')
        bullet = Bullet(self.x, self.y, self.screen)
        self.bullets.append(bullet)

class EnemyPlane(BasePlane):
    '敌人飞机'

    def __init__(self, screen):
        super(EnemyPlane, self).__init__(screen, 0, 0,'./feiji/enemy-1.gif')

        # 移动的方向状态
        self.oritation = 'right'

    def move(self):
        '移动敌人飞机'
        if self.x == 0:
            self.oritation = 'right'
        elif self.x == (480-50):
            self.oritation = 'left'

        if self.oritation == 'right':
            self.moveRight()
        else:
            self.moveLeft()

    def shoot(self):
        '发射一颗子弹'
        # print('enemy biu biu biu')
        num = random.randint(1,10)
        if num == 10:
            bullet = EnemyBullet(self.x, self.y, self.screen)
            self.bullets.append(bullet)


class Bullet(BaseBullet):

    def __init__(self, planeX, planeY, screen):
        super(Bullet, self).__init__(screen, planeX+40, planeY-30,'./feiji/bullet.png')

    def move(self):
        self.y -= 10

    def judge(self):
        '判断子弹是否越界'
        return self.y <= 0

    def __del__(self):
        print('玩家子弹被销毁了')

class EnemyBullet(BaseBullet):

    def __init__(self, planeX, planeY, screen):
        super(EnemyBullet, self).__init__(screen, planeX+25, planeY+40, './feiji/bullet1.png')

    def move(self):
        self.y += 10

    def judge(self):
        '判断子弹是否越界'
        return self.y >= 700

    def __del__(self):
        print('敌人子弹被销毁了')

def main():
    '程序的主逻辑代码'

    # 创建窗口
    screen = pygame.display.set_mode((480, 700), 0, 32)

    # 创建背景图片
    bg = pygame.image.load('./feiji/background.png')

    # 创建玩家飞机图片
    hero = HeroPlane(screen)

    # 创建敌人飞机
    enemy = EnemyPlane(screen)

    while True:
        # print('刷新界面')
        # 显示背景图片
        screen.blit(bg, (0,0))

        # 显示玩家飞机
        hero.display()

        # 显示敌人飞机
        enemy.display()

        # 移动敌人飞机位置
        enemy.move()

        # 自动发射敌人的子弹
        enemy.shoot()

        # 获取事件，比如按键等
        for event in pygame.event.get():

            # 判断是否是点击了退出按钮
            if event.type == QUIT:
                print("exit")
                exit()
            # 判断是否是按下了键
            elif event.type == KEYDOWN:
                # 检测按键是否是a或者left
                if event.key == K_a or event.key == K_LEFT:
                    print('left')
                    hero.moveLeft()

                # 检测按键是否是d或者right
                elif event.key == K_d or event.key == K_RIGHT:
                    print('right')
                    hero.moveRight()

                # 检测按键是否是空格键
                elif event.key == K_SPACE:
                    print('space')
                    hero.shoot()

        # 刷新界面
        pygame.display.update()

        time.sleep(1/100) # 休息一段时间，再刷新界面

if __name__ == '__main__':
    print('程序开始')
    main()
    print('程序结束')