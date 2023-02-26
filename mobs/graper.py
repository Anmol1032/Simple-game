from ursina import *
import random


def sound():
    from ursina.prefabs.ursfx import ursfx
    ursfx([(0.0, 1.0), (0.01, 0.8), (0.06, 0.01), (0.99, 1.0), (1.0, 0.0)], volume=0.25, wave='square', pitch=38, speed=3.2)

class Enemy(Entity):
    def __init__(self, max_hp=5, color_=color.light_gray, **kwargs):
        super().__init__(model='sphere', origin_y=-.5, color=color_,
                         collider='box', scale=2, **kwargs)

        self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.red, world_scale=(1.5, .1, .1))

        self.max_hp = max_hp
        self.hp = self.max_hp
        self.graper = 'its type'
        self.its_type = 'graper'
        self.delay = True
        self.xp_to_give = 2
        invoke(destroy, self, delay=random.uniform(40, 80))

    def update(self):
        if random.random() < 0.01:
            self.rotation_y += random.uniform(0, 360)

        ray = raycast(self.position, self.forward, ignore=(self,), distance=.5)

        if not ray.hit:
            self.position += self.forward * time.dt * 1
        else:
            self.rotation_y += random.uniform(0, 360)

        ray = raycast(self.world_position, self.down, ignore=(self,), distance=.5)

        if ray.distance <= .1:
            self.grounded = True
            # make sure it's not a wall and that the point is not too far up
            if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5:  # walk up slope
                self.y = ray.world_point[1]
            return
        else:
            self.grounded = False

        # if not on ground and not on way up in jump, fall
        self.y -= ray.distance - .05 * time.dt

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if value < self.max_hp:
            sound()
        if value <= 0:
            ep_giver = Entity(model='sphere', origin_y=-.5, color=color.green,
                              collider='box', scale=2, position=self.position, parent=self.parent)
            setattr(ep_giver, 'xp_give', self.xp_to_give)
            destroy(self)
            return
        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1


