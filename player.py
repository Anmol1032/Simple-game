import ursina.prefabs.first_person_controller as fpc
import ursina.prefabs.health_bar as health_bar
from ursina import *

import inventory


def xpsound():
    from ursina.prefabs.ursfx import ursfx
    ursfx([(0.0, 0.74), (0.11, 0.0), (0.58, 0.09), (0.6, 0.75), (1.0, 0.0)], volume=0.75, wave='triangle', pitch=32,
          pitch_change=7, speed=1.1)


class FPC(fpc.FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cursor = Cursor(modal='quad', texture='cursor', scale=0.1, color=color.green)
        self.cursor.visible = False

        camera.fov = 110
        camera.clip_plane_far = 100

        self.max_health = 10
        self.health = self.max_health
        self.prv_health = self.max_health

        self.default_xp = 50
        self.xp = self.default_xp

        self.HB = health_bar.HealthBar(10, roundness=.4, x=-0.3, y=-0.3, )
        self.HB.value = self.health

        self.XP = health_bar.HealthBar(500, roundness=.4, x=-0.3, y=-0.4, bar_color=color.green.tint(-.5),
                                       animation_duration=1.1)
        self.XP.value = self.xp

        self.speed = 30

        self.damage = 1

        self.Inventory = inventory.Inventory()
        self.Inventory.update_weapon = self.update_weapon
        self.Inventory.update_health = self.update_health

        self.in_air = 0

        pause_handler = Entity(ignore_paused=True)
        self.pause_text = Text('PAUSED', origin=(0, 0), scale=2,
                               enabled=False)  # Make a Text saying "PAUSED" just to make it clear when it's paused.

        pause_handler.input = self.pause_handler_input  # Assign the input function to the pause handler.

        self.auto_regen = True
        # self.attack = True

    def pause_handler_input(self, key):
        if key == 'escape':
            if not self.Inventory.enabled:
                application.paused = not application.paused  # Pause/unpause the game.
                self.pause_text.enabled = application.paused  # Also toggle "PAUSED" graphic.
                mouse.locked = not application.paused
            else:
                self.Inventory.enabled = not self.Inventory.enabled
                mouse.locked = not self.Inventory.enabled
                self.cursor.visible = self.Inventory.enabled
                mouse.visible = False
                mouse.position = Vec3(0, 0, 0)

    def update(self):
        super().update()
        if not self.grounded:
            self.in_air += time.dt
        else:
            if self.in_air != 0:
                damage = (((self.in_air - 0.5) * 4 // 1))
                if damage > 0:
                    self.health -= damage
            self.in_air = 0

        if self.Inventory.enabled:  # cursor wIll not show wHen mouse is NOT on window
            if mouse.position == Vec3(0, 0, 0):
                self.cursor.visible = False
            else:
                self.cursor.visible = True

        if self.auto_regen and self.health < self.HB.max_value:
            self.auto_regen = False
            invoke(setattr, self, 'auto_regen', True, delay=5)
            invoke(self.inc_health_temp, delay=2.5)

    def inc_health_temp(self):
        self.health = self.HB.value + 1 if not self.health > self.HB.max_value else self.HB.max_value

    def input(self, key):
        super().input(key)
        if key == Keys.left_mouse_down and mouse.locked:
            # if self.attack:
            # self.attack = False
            # invoke(setattr, self, 'attack', True, delay=.5)

            if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp') and distance(mouse.hovered_entity,
                                                                                         self) < 10:
                mouse.hovered_entity.hp -= self.damage
                mouse.hovered_entity.blink(color.red, duration=.1)

            if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'xp_give') and distance(mouse.hovered_entity,
                                                                                              self) < 10:
                destroy(mouse.hovered_entity)
                self.xp += mouse.hovered_entity.xp_give
                xpsound()

        if key == Keys.left_mouse_down and not mouse.locked:
            self.cursor.color = color.cyan

            invoke(setattr, self.cursor, 'color', color.green, delay=.3)

        if key == 'tab':
            self.Inventory.enabled = not self.Inventory.enabled
            mouse.locked = not self.Inventory.enabled
            self.cursor.visible = self.Inventory.enabled
            mouse.visible = False
            mouse.position = Vec3(0, 0, 0)

    @property
    def health(self):

        return self._health

    @health.setter
    def health(self, value):
        if value <= 0:
            destroy(self)
            exit()
            return

        self._health = value

        self.HB.value = value

        if value < self.prv_health:
            Audio('hurt_2', pitch=random.uniform(.5, 1), volume=10, loop=False, autoplay=True)

        self.prv_health = value

    @property
    def xp(self):
        return self._xp

    @xp.setter
    def xp(self, value):
        if value <= 0:
            value = 0
        elif value >= 100:
            value = 100

        self._xp = value

        self.XP.value = value

    def update_weapon(self):
        if self.xp >= 10:
            self.damage += 1
            self.xp -= 10
            xpsound()

    def update_health(self):
        if self.xp >= 10:
            self.HB.max_value += 1
            self.health += 1
            self.xp -= 10
            xpsound()
