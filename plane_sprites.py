import random
import time
import pygame
from plane_main import PlaneGame

# 定义一个延时时钟
clock1 = pygame.time.Clock()
# 定义屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 720)
# 定义刷新帧率
FRAME_PER_SEC = 60
# 创建敌机的定时器常量（简单的说是让系统作出event，给这个event取一个特定的名字）
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 创建子弹的定时器事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1  # 与前一常量区别 pygame.USEREVENT 是一个整数常量
# 创建英雄状态显示事件
HERO_SIGNAL = pygame.USEREVENT + 2
# 显示敌机发射子弹事件
ENEMY_FIRE = pygame.USEREVENT + 3


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speed=1):
        # 基类非object的类一定要用 super() 调用父类的初始化方法
        super().__init__()
        # 定义对象的属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        # 在屏幕的垂直方向上移动
        self.rect.y += self.speed


class Background(GameSprite):
    """游戏背景精灵"""
    def __init__(self, is_alt=False):
        # 1 调用父类方法实现精灵的创建
        super().__init__("./images/background.png")
        # 2 判断是否是交替图像，如果是则设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        # 1 调用父类方法实现
        super().update()
        # 2 判断是否移出屏幕，移出则将图像设置到屏幕上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    def __init__(self):
        # 1 调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__("./images/diji.png")
        # 2 指定敌机的初始随机速度 1~3
        self.speed = random.randint(1, 3)
        # 3 指定敌机的初始随机位置
        # self.rect.y = -self.rect.height pygame提供的bottom参数：bottom=y+height
        self.rect.bottom = 0
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)
        # 4 设置撞击flag
        self.flag = 0
        # 5 创建敌机子弹精灵组
        self.bullet_group = pygame.sprite.Group()

    def update(self):
        if self.flag == 0:
            # 1 调用父类方法，保持垂直方向的飞行
            super().update()
            # 2 判断是否飞出屏幕，如果是，则删除敌机
            if self.rect.y >= SCREEN_RECT.height:
                # kill方法：把精灵从所有精灵组中删除，同时从内存中删除
                self.kill()
        if self.flag != 0:
            new_rect = self.rect
            super().__init__("./images/diji%d.png" % self.flag)
            self.rect = new_rect
            self.flag += 1
        elif self.flag == 4:
            self.kill()
            return

    def Fire(self):
        bullet = Bullet()
        bullet.image = pygame.image.load("./images/bullet1.png")
        bullet.speed = self.speed + 1
        bullet.rect.centerx = self.rect.centerx
        bullet.rect.top = self.rect.y + self.rect.height
        self.bullet_group.add(bullet)


class Hero(GameSprite):
    """英雄精灵"""
    def __init__(self):
        # 1 调用父类方法设置image&speed
        super().__init__("./images/hero.png", 0)
        # 2 设置英雄初始位置
        # centerx=x+0.5*width  centery=y+0.5height  bottom=y+height
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        # 3 创建子弹精灵组
        self.bullets = pygame.sprite.Group()
        # 4 设置hero移动方向标志的属性
        self.run = True
        # 5 signal标志
        self.a = "./images/hero0.png"
        self.b = "./images/hero.png"
        self.flag = 0

    def update(self):
        # 判断移动方向
        if self.run is True:
            self.rect.x += self.speed
            # 控制英雄不离开屏幕
            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.right >= SCREEN_RECT.right:  # right=x+width
                self.rect.right = SCREEN_RECT.right
        else:
            self.rect.y += self.speed
            if self.rect.top < 0:

                self.rect.top = 0
            elif self.rect.bottom >= SCREEN_RECT.bottom:
                self.rect.bottom = SCREEN_RECT.bottom
        if self.flag != 0:
            new_rect = self.rect
            time.sleep(0.1)
            super().__init__("./images/hero%d.png" % self.flag)
            self.rect = new_rect
            self.flag += 1
        elif self.flag == 4:
            self.kill()
            return

    def Fire(self):
        for i in (0, 1, 2):
            # 1 创建子弹精灵
            bullet = Bullet()
            # 2 设置精灵的位置
            bullet.rect.bottom = self.rect.y - 20 * i
            bullet.rect.centerx = self.rect.centerx
            # 3 将精灵添加到精灵组
            self.bullets.add(bullet)

    def Signal(self):
        self.image = pygame.image.load(self.a)
        (self.a, self.b) = (self.b, self.a)


class Bullet(GameSprite):
    """"子弹精灵"""
    def __init__(self):
        # 1 调用父类方法设置image/speed
        super().__init__("./images/bullet.png", -2)

    def update(self):
        # 1 调用父类方法让子弹沿垂直方向飞行
        super().update()
        # 2 判断子弹是否飞出屏幕，飞出则kill
        if self.rect.bottom < 0:
            self.kill()

