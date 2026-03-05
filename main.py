import arcade
import math
import random

from settings import *
from player import Player


class Game(arcade.Window):

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.scene = None
        self.player = None
        self.camera = None
        self.physics_engine = None

        self.level = 1
        self.max_level = 5

        self.spawn_position = None
        self.finish_position = None

        self.game_started = False
        self.paused = False
        self.game_won = False

        self.show_instruction = False
        self.instruction_shown = False

        self.on_ladder = False

        self.coins = 0
        self.total_coins = 0

        self.level_buttons = []

        self.step_sounds = [
            arcade.load_sound("game_data/assets/sounds/step1.mp3"),
            arcade.load_sound("game_data/assets/sounds/step2.mp3"),
            arcade.load_sound("game_data/assets/sounds/step3.mp3"),
            arcade.load_sound("game_data/assets/sounds/step4.mp3")
        ]

        self.coin_sound = arcade.load_sound("game_data/assets/sounds/coin.mp3")

        self.step_timer = 0

        self.create_level_buttons()

    def create_level_buttons(self):

        gap = 120
        start_x = SCREEN_WIDTH / 2 - gap * 2
        y = SCREEN_HEIGHT / 2

        for i in range(5):

            x = start_x + i * gap
            self.level_buttons.append((i + 1, x, y))

    def setup(self):

        if not self.game_started:
            return

        if self.level == 4 and not self.instruction_shown:
            self.show_instruction = True
            return

        map_name = f"game_data/maps/level_{self.level:02}.tmx"

        tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)

        self.scene = arcade.Scene.from_tilemap(tile_map)

        self.player = Player()

        self.coins = 0

        if "Coins" in self.scene:
            self.total_coins = len(self.scene["Coins"])
        else:
            self.total_coins = 0

        objects = tile_map.object_lists["Objects"]

        for obj in objects:

            if obj.name == "player_spawn":

                self.spawn_position = (
                    obj.shape[0][0],
                    obj.shape[0][1]
                )

                self.player.center_x = self.spawn_position[0]
                self.player.center_y = self.spawn_position[1]

            if obj.name == "finish":

                self.finish_position = (
                    obj.shape[0][0],
                    obj.shape[0][1]
                )

        self.scene.add_sprite("Player", self.player)

        self.camera = arcade.camera.Camera2D()

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            walls=self.scene["Platforms"],
            gravity_constant=GRAVITY
        )

    def play_step_sound(self):

        sound = random.choice(self.step_sounds)
        arcade.play_sound(sound)

    def on_draw(self):

        self.clear(arcade.color.SKY_BLUE)

        if self.game_won:

            arcade.draw_text(
                "YOU WIN!",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2 + 40,
                arcade.color.GOLD,
                60,
                anchor_x="center"
            )

            arcade.draw_text(
                "Press SPACE to return to menu",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2 - 20,
                arcade.color.YELLOW,
                24,
                anchor_x="center"
            )

            return

        if not self.game_started:

            arcade.draw_text(
                "SELECT LEVEL",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT - 120,
                arcade.color.WHITE,
                30,
                anchor_x="center"
            )

            for level, x, y in self.level_buttons:

                arcade.draw_text(
                    str(level),
                    x,
                    y,
                    arcade.color.WHITE,
                    40,
                    anchor_x="center",
                    anchor_y="center"
                )

            return

        if self.show_instruction:

            arcade.draw_text(
                "LEVEL 4",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2 + 80,
                arcade.color.GOLD,
                40,
                anchor_x="center"
            )

            arcade.draw_text(
                "Collect all coins to finish the level",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.YELLOW,
                24,
                anchor_x="center"
            )

            arcade.draw_text(
                "Press SPACE to start",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2 - 60,
                arcade.color.WHITE,
                20,
                anchor_x="center"
            )

            return

        with self.camera.activate():
            self.scene.draw()

        arcade.draw_text(
            f"Coins: {self.coins}/{self.total_coins}",
            SCREEN_WIDTH - 170,
            SCREEN_HEIGHT - 40,
            arcade.color.GOLD,
            20
        )

        if self.paused:

            arcade.draw_lbwh_rectangle_filled(
                0,
                0,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                (0, 0, 0, 150)
            )

            arcade.draw_text(
                "PAUSE",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2 + 40,
                arcade.color.GOLD,
                50,
                anchor_x="center"
            )

            arcade.draw_text(
                "ESC - Continue",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.YELLOW,
                22,
                anchor_x="center"
            )

            arcade.draw_text(
                "M - Main Menu",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2 - 40,
                arcade.color.YELLOW,
                22,
                anchor_x="center"
            )

    def on_mouse_press(self, x, y, button, modifiers):

        if not self.game_started:

            for level, bx, by in self.level_buttons:

                if bx - 40 < x < bx + 40 and by - 40 < y < by + 40:

                    self.level = level
                    self.game_started = True
                    self.setup()

    def on_key_press(self, key, modifiers):

        if self.game_won:

            if key == arcade.key.SPACE:

                self.game_won = False
                self.game_started = False
                self.level = 1

            return

        if not self.game_started:

            if arcade.key.KEY_1 <= key <= arcade.key.KEY_5:

                self.level = key - arcade.key.KEY_0
                self.game_started = True
                self.setup()

            return

        if key == arcade.key.ESCAPE:
            self.paused = not self.paused
            return

        if self.paused:

            if key == arcade.key.M:
                self.paused = False
                self.game_started = False
                self.level = 1

            return

        if self.show_instruction:

            if key == arcade.key.SPACE:
                self.show_instruction = False
                self.instruction_shown = True
                self.setup()

            return

        if key == arcade.key.A:
            self.player.change_x = -PLAYER_SPEED

        if key == arcade.key.D:
            self.player.change_x = PLAYER_SPEED

        if key == arcade.key.W and self.on_ladder:
            self.player.change_y = PLAYER_SPEED

        if key == arcade.key.S and self.on_ladder:
            self.player.change_y = -PLAYER_SPEED

        if key == arcade.key.SPACE and not self.on_ladder:

            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP

    def on_key_release(self, key, modifiers):

        if key == arcade.key.A or key == arcade.key.D:
            self.player.change_x = 0

        if key == arcade.key.W or key == arcade.key.S:
            if self.on_ladder:
                self.player.change_y = 0

    def on_update(self, delta_time):

        if not self.game_started or self.paused or self.show_instruction:
            return

        self.check_ladder()

        self.physics_engine.update()

        self.player.update_animation()

        if abs(self.player.change_x) > 0 and not self.on_ladder:

            self.step_timer += delta_time

            if self.step_timer > 0.35:

                self.play_step_sound()
                self.step_timer = 0

        self.check_finish()
        self.check_coins()
        self.check_spikes()
        self.check_fall()

        self.camera.position = (
            self.player.center_x,
            self.player.center_y
        )

    def check_ladder(self):

        if "Ladders" not in self.scene:
            self.on_ladder = False
            self.physics_engine.gravity_constant = GRAVITY
            return

        ladders = arcade.check_for_collision_with_list(
            self.player,
            self.scene["Ladders"]
        )

        if ladders:

            self.on_ladder = True
            self.physics_engine.gravity_constant = 0

        else:

            self.on_ladder = False
            self.physics_engine.gravity_constant = GRAVITY

    def check_finish(self):

        if self.finish_position:

            distance = math.sqrt(
                (self.player.center_x - self.finish_position[0]) ** 2 +
                (self.player.center_y - self.finish_position[1]) ** 2
            )

            if distance < 40 and self.coins == self.total_coins:

                if self.level == self.max_level:

                    self.game_won = True
                    self.game_started = False
                    return

                self.level += 1
                self.setup()

    def check_spikes(self):

        if "Spikes" in self.scene:

            spikes = arcade.check_for_collision_with_list(
                self.player,
                self.scene["Spikes"]
            )

            if spikes:
                self.respawn()

    def check_fall(self):

        if self.player.center_y < -200:
            self.respawn()

    def check_coins(self):

        if "Coins" in self.scene:

            coins = arcade.check_for_collision_with_list(
                self.player,
                self.scene["Coins"]
            )

            for coin in coins:

                coin.remove_from_sprite_lists()

                arcade.play_sound(self.coin_sound)

                self.coins += 1

    def respawn(self):

        self.player.center_x = self.spawn_position[0]
        self.player.center_y = self.spawn_position[1]

        self.player.change_x = 0
        self.player.change_y = 0


def main():

    game = Game()
    arcade.run()


if __name__ == "__main__":
    main()