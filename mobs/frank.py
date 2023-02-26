from ursina import *
import random


def sound():
    from ursina.prefabs.ursfx import ursfx
    ursfx([(0.0, 0.45), (0.05, 0.81), (0.4, 1.0), (0.43, 0.59), (1.0, 1.0)], volume=0.44, wave='triangle', pitch=-5,
          pitch_change=6, speed=3.2)


class Enemy(Entity):
    def __init__(self, max_hp=10, color_=color.light_gray, player=Entity(position=(0, 0, 0)), **kwargs):
        super().__init__(model=Cone(4, .7), origin_y=-.5, color=color_,
                         collider='mesh', scale=2, **kwargs)

        self.player = player

        self.health_bar = Entity(parent=self, y=1.8, model='cube', color=color.red, world_scale=(1.5, .1, .1))

        self.max_hp = max_hp
        self.hp = self.max_hp
        self.frank = 'its type'
        self.its_type = 'frank'
        self.delay = True
        self.xp_to_give = 5
        self.run = False
        self.gravity = True
        invoke(destroy, self, delay=random.uniform(40, 80))

    def update(self):
        if self.run:
            self.look_at_2d(self.player.position, 'y')
            ray = raycast(self.position, self.back, ignore=(self,), distance=.5, debug=False)

            if not ray.hit:
                self.position += self.back * time.dt * 1
                invoke(setattr, self, 'gravity', True, delay=1)
            else:
                self.y += 1
                ray = raycast(self.position, self.back, ignore=(self,), distance=.5, debug=False)

                if not ray.hit:
                    self.position += self.back * time.dt * 5
                    invoke(setattr, self, 'gravity', True, delay=1)
                self.gravity = False
        else:
            if random.random() < 0.01:
                self.rotation_y += random.uniform(0, 360)

            ray = raycast(self.position, self.forward, ignore=(self,), distance=.5, debug=False)

            if not ray.hit:
                self.position += self.forward * time.dt * 1
            else:
                self.rotation_y += random.uniform(0, 360)

        ray = raycast(self.world_position, self.down, ignore=(self,), distance=.5)

        if self.gravity:
            if ray.distance <= .1:
                self.grounded = True
                # make sure it's not a wall and that the point is not too far up
                # if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5:  # walk up slope
                #    self.y = ray.world_point[1]
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
            self.run = True
        if value <= 0:
            ep_giver = Entity(model=Cone(4, .7), origin_y=-.5, color=color.green,
                              collider='mesh', scale=2, position=self.position, parent=self.parent)

            setattr(ep_giver, 'xp_give', self.xp_to_give)
            destroy(self)
            return
        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1
