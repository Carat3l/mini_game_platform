import arcade

from settings import PLAYER_SCALING


class Player(arcade.Sprite):

    def __init__(self):

        super().__init__()

        self.walk_textures = [
            arcade.load_texture("game_data/assets/player/character_green_walk_a.png"),
            arcade.load_texture("game_data/assets/player/character_green_walk_b.png")
        ]

        self.jump_texture = arcade.load_texture(
            "game_data/assets/player/character_green_jump.png"
        )

        self.texture = self.walk_textures[0]

        self.scale = PLAYER_SCALING

        self.walk_index = 0
        self.animation_timer = 0

    def update_animation(self, delta_time=1/60):

        if self.change_y != 0:
            self.texture = self.jump_texture
            return

        if abs(self.change_x) > 0:

            self.animation_timer += 1

            if self.animation_timer > 10:
                self.walk_index += 1
                self.walk_index %= 2
                self.texture = self.walk_textures[self.walk_index]
                self.animation_timer = 0

        else:
            self.texture = self.walk_textures[0]