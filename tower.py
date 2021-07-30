import pygame
import os
import math

TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def collide(self, enemy):
        """
        Q2.2)check whether the enemy is in the circle (attack range), if the enemy is in range return True
        :param enemy: Enemy() object
        :return: Bool
        """

        """
        Hint:
        x1, y1 = enemy.get_pos()
        ...
        """
        # use to get enemy position(x, y)
        x1, y1 = enemy.get_pos()

        # calculate distance between enemy and tower
        distance = math.sqrt((x1-self.center[0])**2+(y1-self.center[1])**2)

        if distance < self.radius:  # in tower range
            return True
        else:
            return False            # out of tower range
        pass

    def draw_transparent(self, win):
        """
        Q1) draw the tower effect range, which is a transparent circle.
        :param win: window surface
        :return: None
        """
        # create semi-transparent surface
        transparent_surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        transparency = 150  # define transparency: 0~255, 0 is fully transparent
        # draw the circle on the transparent surface
        pygame.draw.circle(transparent_surface, (100, 100, 100, transparency), (self.radius, self.radius), self.radius)

        # show the transparent_surface in window
        win.blit(transparent_surface, (self.center[0]-self.radius, self.center[1]-self.radius))
        pass


class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 2   # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.is_selected = True  # the state of whether the tower is selected
        self.type = "tower"

    def is_cool_down(self):
        """
        Q2.1) Return whether the tower is cooling down
        (1) Use a counter to computer whether the tower is cooling down (( self.cd_count
        :return: Bool
        """

        """
        Hint:
        let counter be 0
        if the counter < max counter then
            set counter to counter + 1
        else 
            counter return to zero
        end if
        """
        if self.cd_count < self.cd_max_count:   # is in cold_down
            self.cd_count += 1
            return False
        else:                                   # is end of cold_down
            self.cd_count = 0
            return True
        pass

    def attack(self, enemy_group):
        """
        Q2.3) Attack the enemy.
        (1) check the the tower is cool down ((self.is_cool_down()
        (2) if the enemy is in attack range, then enemy get hurt. ((Circle.collide(), enemy.get_hurt()
        :param enemy_group: EnemyGroup()
        :return: None
        """
        if self.is_cool_down():                         # if end of cold down
            for enemy in enemy_group.get():             # use to get one enemy each loop
                if self.range_circle.collide(enemy):    # detect enemy in tower range or not
                    enemy.get_hurt(self.damage)
                    return
                pass

    def is_clicked(self, x, y):
        """
        Bonus) Return whether the tower is clicked
        (1) If the mouse position is on the tower image, return True
        :param x: mouse pos x
        :param y: mouse pos y
        :return: Bool
        """
        # if mouse click the tower or not
        if self.rect.x <= x <= self.rect.topright[0] and self.rect.y <= y <= self.rect.bottomright[1]:
            return True
        else:
            return False
        pass

    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """
        self.is_selected = is_selected

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower

