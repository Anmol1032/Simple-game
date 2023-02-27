from perlin_noise import PerlinNoise
from ursina import *



def main():
    """"""


    sky_parent = Entity(model=Mesh(vertices=[], uvs=[]))
    alfa = 10
    scale = 70
    while alfa < 440:
        sky = Sky(color=color.rgba(20, 100, 255, alfa), scale=scale)
        scale += 3
        alfa += 50      # Less alfa increase fog like effect but somewhat less FPS and more loading in while start.
        sky_parent.combine().vertices.extend(sky.combine().vertices)




    level_parent = Entity(model=Mesh(vertices=[], uvs=[]))

    noise = PerlinNoise(octaves=3, seed=1032)
    for z in range(0, 2048, 128):
        for x in range(0, 2048, 128):
            # height = round(GeneratedNoiseMap(z, x, 20) * 20)

            y = noise([x * .15, z * .15])
            y = math.floor(y * 7.5)
            block = Entity(position=(x, y, z), model='cube', collider='box',
                           scale=(128, 128, 128), texture='files/img.png', color=color.rgb(20, 100, 255),
                           texture_scale=(2, 2, 2))
            # level_parent.combine().vertices.extend(block.combine().vertices)        # Uncomment this to increase FPS but it take much loading while start.

    level_parent.collider = 'mesh'


if __name__ == '__main__':
    import player
    app = Ursina()

    main()

    player_ = player.FPC(x=0, z=0, y=200)
    player_.camera_pivot.y += 1

    app.run()
