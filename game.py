import raylibpy as rl
import random
import time

# Constants
WIDTH = 480
HEIGHT = 640
FPS = 30
CAR_SPEED = 2
DX = 4

# Sprite class
class Sprite:
    def __init__(self, texture, x, y):
        self.texture = texture
        self.pos = rl.Vector2(x, y)

def main():
    # Initialize window and audio device
    rl.init_window(WIDTH, HEIGHT, "Python Car Racing")
    rl.init_audio_device()  # Initialize audio system
    rl.set_target_fps(FPS)

    # Load car texture
    car_texture = rl.load_texture("res/car.png")
    car = Sprite(car_texture, WIDTH / 2 - car_texture.width / 2, HEIGHT * 3 / 5)

    # Load trees
    ttrees = rl.load_texture("res/trees.png")
    srect = [rl.Rectangle(i * 48, 0, 48, 48) for i in range(3)]
    
    # Randomize tree positions
    trees_num = random.randint(10, 18)
    trees_pos = [rl.Vector2() for _ in range(trees_num)]
    for i in range(trees_num):
        if i < trees_num // 2:
            trees_pos[i].x = random.randint(1, WIDTH // 3)
        else:
            trees_pos[i].x = random.randint(2 * WIDTH // 3, WIDTH)
        trees_pos[i].y = random.randint(0, HEIGHT)
    
    # Load cars and randomize positions
    tcars = rl.load_texture("res/cars.png")
    srect_cars = [rl.Rectangle(i * 16, 0, 16, 24) for i in range(6)]
    cars_pos = [rl.Vector2() for _ in range(6)]
    cars_speed = [random.randint(6, 10) for _ in range(6)]
    
    for i in range(6):
        lane = random.randint(1, 3)
        if lane == 1:
            cars_pos[i].x = WIDTH / 3 + WIDTH / 18 - tcars.width / 12
        elif lane == 2:
            cars_pos[i].x = WIDTH / 2 - tcars.width / 12
        else:
            cars_pos[i].x = WIDTH * 2 / 3 - WIDTH / 18 - tcars.width / 12
        cars_pos[i].y = random.randint(0, HEIGHT)

    # Load sound files
    collision_sound = rl.load_sound("res/collision_sound.wav")
    background_music = rl.load_music_stream("res/background_music.wav")

    # Play background music (looping)
    rl.play_music_stream(background_music)
    rl.set_music_volume(background_music, 0.5)  # Set volume level (optional)

    # Game state variables
    lives = 3
    score = 0
    time_elapsed = 0
    vulnerable_time = 0
    vulnerable = True
    game_over = False
    game_won = False

    # Game loop
    while not rl.window_should_close():
        if not game_over:
            # Update the background music stream
            rl.update_music_stream(background_music)

            # Input handling
            if rl.is_key_down(rl.KEY_A) or rl.is_key_down(rl.KEY_LEFT):
                car.pos.x -= CAR_SPEED
            if rl.is_key_down(rl.KEY_D) or rl.is_key_down(rl.KEY_RIGHT):
                car.pos.x += CAR_SPEED
            if rl.is_key_down(rl.KEY_W) or rl.is_key_down(rl.KEY_UP):
                car.pos.y -= CAR_SPEED
            if rl.is_key_down(rl.KEY_S) or rl.is_key_down(rl.KEY_DOWN):
                car.pos.y += CAR_SPEED

            # Update tree positions
            for i in range(trees_num):
                trees_pos[i].y += CAR_SPEED
                if trees_pos[i].y > HEIGHT:
                    trees_pos[i].y = -ttrees.height

            # Update car positions and check for collisions
            for i in range(6):
                cars_pos[i].y += cars_speed[i]
                if cars_pos[i].y > HEIGHT:
                    cars_pos[i].y = -tcars.height
                    lane = random.randint(1, 3)
                    if lane == 1:
                        cars_pos[i].x = WIDTH / 3 + WIDTH / 18 - tcars.width / 12
                    elif lane == 2:
                        cars_pos[i].x = WIDTH / 2 - tcars.width / 12
                    else:
                        cars_pos[i].x = WIDTH * 2 / 3 - WIDTH / 18 - tcars.width / 12
                    cars_speed[i] = random.randint(6, 10)

                # Collision detection
                rec1 = rl.Rectangle(car.pos.x, car.pos.y, car.texture.width, car.texture.height)
                rec2 = rl.Rectangle(cars_pos[i].x, cars_pos[i].y, tcars.width / 6, tcars.height)
                if rl.check_collision_recs(rec1, rec2):
                    if vulnerable:
                        lives -= 1
                        vulnerable = False
                        rl.play_sound(collision_sound)  # Play collision sound
                    car.pos.y -= car.texture.height - 10

            # Vulnerability timing
            if not vulnerable:
                vulnerable_time += rl.get_frame_time()
                if vulnerable_time > 1:
                    vulnerable = True
                    vulnerable_time = 0

            # Check game over or won
            if lives < 0:
                game_over = True
            if score > 999:
                game_won = True
                game_over = True

            # Update score
            time_elapsed += rl.get_frame_time()
            if time_elapsed > 1:
                score += 1
                time_elapsed = 0

        # Drawing section
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        # Draw background
        rl.draw_rectangle(0, 0, WIDTH // 3, HEIGHT, rl.GREEN)
        rl.draw_rectangle(2 * WIDTH // 3, 0, WIDTH // 3, HEIGHT, rl.GREEN)
        rl.draw_rectangle(WIDTH // 3, 0, WIDTH // 3, HEIGHT, rl.GRAY)
        rl.draw_rectangle(WIDTH // 3 + WIDTH // 9 - 1, 0, 2, HEIGHT, rl.BLACK)
        rl.draw_rectangle(WIDTH // 3 + 2 * WIDTH // 9 - 1, 0, 2, HEIGHT, rl.BLACK)

        # Draw car
        if vulnerable:
            rl.draw_texture(car.texture, int(car.pos.x), int(car.pos.y), rl.WHITE)
        else:
            rl.draw_texture(car.texture, int(car.pos.x), int(car.pos.y), rl.Color(0, 0, 0, 100))

        # Draw other cars
        for i in range(6):
            rl.draw_texture_rec(tcars, srect_cars[i], cars_pos[i], rl.WHITE)

        # Draw trees
        for i in range(trees_num):
            rl.draw_texture_rec(ttrees, srect[i % 3], trees_pos[i], rl.WHITE)

        # Draw score and lives
        rl.draw_text(f"Score: {score}", 10, 10, 20, rl.WHITE)
        rl.draw_text(f"Lives: {lives}", WIDTH - 100, 10, 20, rl.WHITE)

        # Draw game over screen
        if game_over:
            rl.draw_rectangle(0, 0, WIDTH, HEIGHT, rl.Color(0, 0, 0, 180))
            if game_won:
                rl.draw_text("You Won!", WIDTH // 5, HEIGHT // 3, 50, rl.WHITE)
            else:
                rl.draw_text("Game Over!", WIDTH // 5, HEIGHT // 3, 50, rl.WHITE)

        rl.end_drawing()

    # Clean up
    rl.stop_music_stream(background_music)
    rl.unload_sound(collision_sound)
    rl.unload_music_stream(background_music)
    rl.unload_texture(tcars)
    rl.unload_texture(ttrees)
    rl.unload_texture(car.texture)
    rl.close_audio_device()  # Close audio device
    rl.close_window()

if __name__ == "__main__":
    main()

