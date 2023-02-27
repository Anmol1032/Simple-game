#!C:\Users\abhiv\AppData\Local\Programs\Python\Python311\python.exe

"""Main game"""

from ursina import *
from ursina import curve

import map
import mobs
import player

app = Ursina()

window.borderless = False
window.exit_button.enabled = False
window.cog_button.enabled = False
window.fps_counter.x = 0
window.fps_counter.scale = 2
window.fps_counter.color = color.green

application.development_mode = False

SPLASH = True # make it False to stop splash screen

window.fullscreen = True
sound = Audio('life_is_currency', pitch=random.uniform(.5, 1), loop=True, autoplay=False, volume=1)


def splash_screen():
    sound.play()

    camera.overlay.color = color.blue
    camera.overlay.texture = 'img'
    camera.overlay.scale = 1
    camera.overlay.scale_y *= camera.overlay.texture.height / 100
    camera.overlay.aspect_ratio = camera.overlay.texture.width / camera.overlay.texture.height
    camera.overlay.scale_x = camera.overlay.scale_y * camera.overlay.aspect_ratio

    app.step()

    logo = Sprite(name='ursina_splash', parent=camera.ui, texture='img', world_z=camera.overlay.z - 1, scale=1,
                  color=color.blue)

    logo.animate_rotation((0, 0, 360), duration=6, delay=1, curve=curve.out_expo_boomerang)
    logo.animate_scale(20, duration=6, delay=1, curve=curve.in_out_sine_boomerang)
    logo.animate_x(3, duration=6, delay=1, curve=curve.in_out_sine_boomerang)
    logo.blink(color.clear, duration=2.5, delay=3, curve=curve.in_out_expo_boomerang, loop=False)
    logo.animate_color(color.rgb(20, 100, 255), duration=2, delay=1, curve=curve.in_out_circ_boomerang)
    logo.shake(2, 5, .005, (10, 10), delay=3, )

    logo.animate_color(color.clear, 3, delay=6)

    camera.overlay.animate_color(color.red, duration=1, delay=3.2)
    camera.overlay.animate_color(color.black, duration=1, delay=7)
    camera.overlay.animate_color(color.clear, duration=3, delay=10)

    destroy(logo, delay=10)


if SPLASH:
    window.fps_counter.enabled = False
    splash_screen()
    app.step()

map.main()

player_ = player.FPC(x=100, z=100, y=200)
player_.camera_pivot.y += 1.5

killable = Entity()

if SPLASH:
    player_.enabled = False
    killable.can_summon = False
    invoke(setattr, player_, 'enabled', True, delay=10)
    invoke(setattr, window.fps_counter, 'enabled', True, delay=13.5)
    invoke(setattr, killable, 'can_summon', True, delay=13.5)
    invoke(sound.stop, delay=13.5)
    sound.volume = 0.5
    invoke(sound.play, delay=13.6)
else:
    killable.can_summon = True

seed = random.Random()

# seed.seed(1032)


f = [0.5, 0.25, 0.1, 0.085, 0.07, 0.05] # probablities of summoning of a mob.

f0 = False
f1 = False
f2 = False
f3 = False
f4 = False
f5 = False

stage = 1

player_.inc_prob = True

max_dis = 75
min_dis = 50


def update():
    global f0, f1, f2, f3, f4, f5, f, stage

    if int(window.fps_counter.text) > 40:
        window.fps_counter.color = color.green
        window.fps_counter.scale = 2

    elif int(window.fps_counter.text) > 30:
        window.fps_counter.color = color.yellow
        window.fps_counter.scale = 2.5

    elif int(window.fps_counter.text) > 15:
        window.fps_counter.color = color.orange
        window.fps_counter.scale = 2.7
    else:
        window.fps_counter.color = color.red
        window.fps_counter.scale = 3

    if player_.inc_prob:
        player_.inc_prob = False
        invoke(setattr, player_, 'inc_prob', True, delay=.5)

        for i in range(6):
            exec(f"if f{i}:"
                 f" f[{i}] = round(f[{i}] - 0.0075, 5)",
                 {'f': f, 'i': i, 'f0': f0, 'f1': f1, 'f2': f2, 'f3': f3, 'f4': f4, 'f5': f5})

            exec(f"""
try:
    if not f{i - 1}: 
        f[{i}] = round(f[{i}] - 0.0045, 5)
except:
    pass""", {'f': f, 'i': i, 'f0': f0, 'f1': f1, 'f2': f2, 'f3': f3, 'f4': f4, 'f5': f5})

            if f[i] >= .95:
                f[i] = round(f[i] - 0.0075, 5)
                if i == 0:
                    f0 = True
                elif i == 1:
                    f1 = True
                elif i == 2:
                    f2 = True
                elif i == 3:
                    f3 = True
                elif i == 4:
                    f4 = True
                elif i == 5:
                    f5 = True


            else:
                f[i] = round(f[i] + 0.005, 5)

            exec(f"if f[{i}] <= 0.005:"
                 f" f[{i}] = 0.051",
                 {'f': f, 'i': i})

        if f[5] <= 0.001:
            f0 = False
            f1 = False
            f2 = False
            f3 = False
            f4 = False
            f5 = False
            stage += 1
        print(f, '>>', stage)

    if killable.can_summon:
        killable.can_summon = False
        invoke(setattr, killable, 'can_summon', True, delay=1)  # ************ Increase it to 5

        # karate
        if seed.random() < f[2]:
            if seed.random() < stage / 10:
                pos = Vec3(seed.uniform(-max_dis, max_dis), seed.uniform(25, 29), seed.uniform(-max_dis, max_dis))
                if not (
                        -min_dis < pos.x < min_dis and -min_dis < pos.y < min_dis and -min_dis < pos.z < min_dis) and \
                        not (player_.y + pos.y) <= 10:
                    rare_karate = mobs.karate.Enemy(parent=killable, position=player_.position + pos, max_hp=80,
                                                    color_=color.gold, player=player_)
                    rare_karate.xp_to_give = 35
            else:
                pos = Vec3(seed.uniform(-max_dis, max_dis), seed.uniform(25, 29), seed.uniform(-max_dis, max_dis))

                if not (
                        -min_dis < pos.x < min_dis and -min_dis < pos.y < min_dis and -min_dis < pos.z < min_dis) and \
                        not (player_.y + pos.y) <= 10:
                    karate = mobs.karate.Enemy(parent=killable, position=player_.position + pos, player=player_)

        # -- frank
        elif seed.random() < f[1]:

            if seed.random() < stage / 10:
                pos = Vec3(seed.uniform(-max_dis, max_dis), seed.uniform(25, 29),
                           seed.uniform(-max_dis, max_dis))
                if not (
                        -min_dis < pos.x < min_dis and -min_dis < pos.y < min_dis and -min_dis < pos.z < min_dis) and \
                        not (player_.y + pos.y) <= 10:
                    rare_frank = mobs.frank.Enemy(parent=killable, position=player_.position + pos, max_hp=40,
                                                  color_=color.gold, player=player_)
                    rare_frank.xp_to_give = 20
            else:
                pos = Vec3(seed.uniform(-max_dis, max_dis), seed.uniform(25, 29),
                           seed.uniform(-max_dis, max_dis))

                if not (
                        -min_dis < pos.x < min_dis and -min_dis < pos.y < min_dis and -min_dis < pos.z < min_dis) and \
                        not (player_.y + pos.y) <= 10:
                    frank = mobs.frank.Enemy(parent=killable, position=player_.position + pos, player=player_)


        # -- graper
        elif seed.random() < f[0]:

            if seed.random() < stage / 10:
                pos = Vec3(seed.uniform(-max_dis, max_dis), seed.uniform(25, 29), seed.uniform(-max_dis, max_dis))
                if not (
                        -min_dis < pos.x < min_dis and -min_dis < pos.y < min_dis and -min_dis < pos.z < min_dis) and \
                        not (player_.y + pos.y) <= 10:
                    rare_graper = mobs.graper.Enemy(parent=killable, position=player_.position + pos, max_hp=20,
                                                    color_=color.gold)
                    rare_graper.xp_to_give = 10
            else:
                pos = Vec3(seed.uniform(-max_dis, max_dis), seed.uniform(25, 29), seed.uniform(-max_dis, max_dis))

                if not (
                        -min_dis < pos.x < min_dis and -min_dis < pos.y < min_dis and -min_dis < pos.z < min_dis) and \
                        not (player_.y + pos.y) <= 10:
                    graper = mobs.graper.Enemy(parent=killable, position=player_.position + pos)


mouse.traverse_target = killable


def exitfunc():
    print('\033[32m\nWhy you exit...') #Print when use exit the window


app.exitFunc = exitfunc

app.run()
