from ursina import *


class Inventory(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model=Quad(.1, 16, 2),
            scale=(1.6, .8),
            origin=(0, 0),
            position=(0, 0),
            texture='files/img',
            texture_scale=(8, 6),
            color=color.rgba(10, 10, 100, 230),
        )

        self.update_weapon = None

        self.but = Button(
            parent=self,
            model=Quad(.1, 16, 2),
            scale=(.4, .6),
            origin=(-.5, 0),
            position=(-.5, 0),
            texture='sword',
            texture_scale=(1, 1),
            color=color.rgba(100, 100, 100, 255),
            highlight_color=color.rgba(200, 200, 200, 255),
            on_click=self.update_weapon)

        self.update_health = None

        self.but2 = Button(
            parent=self,
            model=Quad(.1, 16, 2),
            scale=(.4, .6),
            origin=(.5, 0),
            position=(.5, 0),
            texture='gem',
            texture_scale=(1, 1),
            color=color.rgba(200, 100, 100, 255),
            highlight_color=color.rgba(255, 0, 0, 255),
            on_click=self.update_health)

        self.update_weapon = None
        self.update_health = None


        self.enabled = False

    @property
    def update_weapon(self):
        return self._update_weapon

    @update_weapon.setter
    def update_weapon(self, value):
        self._update_weapon = value
        destroy(self.but)
        self.but = Button(
            parent=self,
            model=Quad(.1, 16, 2),
            scale=(.4, .6),
            origin=(-.5, 0),
            position=(-.5, 0),
            texture='sword',
            texture_scale=(1, 1),
            color=color.rgba(100, 100, 100, 255),
            highlight_color=color.rgba(250, 255, 255, 255),
            on_click=value)

    @property
    def update_health(self):
        return self._update_weapon

    @update_health.setter
    def update_health(self, value):
        self._update_weapon = value
        destroy(self.but2)
        self.but2 = Button(
            parent=self,
            model=Quad(.1, 16, 2),
            scale=(.4, .6),
            origin=(.5, 0),
            position=(.5, 0),
            texture='gem',
            texture_scale=(1, 1),
            color=color.rgba(100, 100, 100, 255),
            highlight_color=color.rgba(255, 0, 0, 255),
            on_click=value)


if __name__ == '__main__':
    app = Ursina()
    Sky()
    EditorCamera()
    inventory = Inventory()


    def input(key):
        if key == 'tab':
            inventory.enabled = not inventory.enabled


    app.run()
