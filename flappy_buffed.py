import pygame
import random

# --- Inisialisasi Pygame ---
pygame.init()

# --- Konstanta Game ---
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird Pygame (Complete)')

# Warna
BLACK = (0, 0, 0)
SKY_BLUE = (112, 197, 206)
YELLOW = (255, 255, 0)
GREEN = (0, 150, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255) # Buff Invincibility
PURPLE = (128, 0, 128) # Buff Dash

# Kecepatan Game
FPS = 60
clock = pygame.time.Clock()

# --- Variabel Burung ---
bird_x = 50
bird_y = int(SCREEN_HEIGHT / 2)
bird_size = 20
bird_rect = pygame.Rect(bird_x, bird_y, bird_size, bird_size)

# Fisika
gravity = 0.5
velocity = 0
jump_power = -9

# --- Variabel Pipa & Skor ---
pipe_width = 50
pipe_gap = 120
pipe_speed = 3
pipes = []
score = 0
high_score = 0 

pipe_spawn_time = 1500  # Waktu dalam milidetik
last_pipe_time = pygame.time.get_ticks()

# --- Fitur Baru: Nyawa (Lives) ---
LIVES_START = 3
lives = LIVES_START

# --- Buff Invincibility (Tembus Pipa) ---
is_invincible = False # Menggantikan is_buffed sebelumnya
INVINCIBLE_ACTIVATE_SCORE = 10
INVINCIBLE_END_SCORE = 50

# --- Buff Dash ---
is_dashing = False
dash_distance = 100 # Jarak dash dalam piksel
dash_duration = 100 # Durasi dash dalam milidetik
dash_start_time = 0
DASH_ACTIVATE_SCORE = 15 # DASH aktif pada score ini

# --- Status Game ---
game_over = False
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 64)

# --- Fungsi Pipa (Tidak Berubah Signifikan) ---
def create_pipe():
    min_height = 100
    max_height = SCREEN_HEIGHT - pipe_gap - 100
    top_height = random.randint(min_height, max_height)
    
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, pipe_width, top_height)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, top_height + pipe_gap, pipe_width, SCREEN_HEIGHT - (top_height + pipe_gap))
    
    pipes.append({'top': top_pipe, 'bottom': bottom_pipe, 'passed': False})

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(SCREEN, GREEN, pipe['top'])
        pygame.draw.rect(SCREEN, GREEN, pipe['bottom'])

def move_pipes():
    global score
    for pipe in pipes:
        # Pipa tidak bergerak saat burung melakukan Dash
        if not is_dashing:
            pipe['top'].x -= pipe_speed
            pipe['bottom'].x -= pipe_speed
        
        # Cek Skor
        if pipe['top'].right < bird_x and not pipe['passed']:
            score += 1
            pipe['passed'] = True
            
    pipes[:] = [pipe for pipe in pipes if pipe['top'].right > 0]

# --- Fungsi Burung ---
def draw_bird():
    color = YELLOW
    if is_invincible:
        color = CYAN
    if is_dashing:
        color = PURPLE
        
    pygame.draw.rect(SCREEN, color, bird_rect)
    # Tambahkan batas tipis saat Buffed
    if is_invincible or is_dashing:
         pygame.draw.rect(SCREEN, BLACK, bird_rect, 2)

def jump():
    global velocity
    velocity = jump_power

def dash():
    global is_dashing, dash_start_time, bird_rect, current_time
    
    # Hanya bisa Dash jika Buff Invincible aktif (Score >= 15) dan sedang tidak Dash
    if is_invincible and not is_dashing:
        is_dashing = True
        dash_start_time = current_time # Catat waktu mulai Dash
        
        # Gerakkan burung ke kanan (melewati pipa)
        bird_rect.x += dash_distance
        # Pastikan burung tidak keluar batas kanan
        if bird_rect.right > SCREEN_WIDTH:
            bird_rect.right = SCREEN_WIDTH

# --- Fungsi Tabrakan dan Kehilangan Nyawa ---
def check_collision():
    global lives, game_over
    
    # 1. Cek Batas Atas/Bawah
    if bird_rect.bottom >= SCREEN_HEIGHT or bird_rect.top <= 0:
        if lives > 1:
            lives -= 1
            reset_bird_position()
            return False # Belum Game Over
        else:
            return True # Game Over

    # 2. Cek Pipa
    for pipe in pipes:
        if bird_rect.colliderect(pipe['top']) or bird_rect.colliderect(pipe['bottom']):
            
            if not is_invincible: 
                # Kehilangan Nyawa
                if lives > 1:
                    lives -= 1
                    reset_bird_position()
                    return False # Belum Game Over
                else:
                    return True # Game Over
            # Jika is_invincible=True, tabrakan diabaikan
            
    return False

def reset_bird_position():
    global bird_y, velocity, bird_rect, pipes
    # Set posisi burung ke tengah dan reset kecepatan
    bird_y = int(SCREEN_HEIGHT / 2)
    velocity = 0
    bird_rect.y = bird_y
    
    # Hapus pipa di dekat burung (Memberi waktu pemulihan)
    pipes[:] = [pipe for pipe in pipes if pipe['top'].left > bird_rect.right + 100]

# --- Fungsi Game Over ---
def game_over_screen():
    global high_score

    if score > high_score:
        high_score = score
    
    text = big_font.render("GAME OVER", True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    SCREEN.blit(text, text_rect)
    
    restart_text = font.render(f"Skor Akhir: {score} | HS: {high_score}", True, BLACK)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
    SCREEN.blit(restart_text, restart_rect)
    
    prompt_text = font.render("Tekan SPACE untuk Restart", True, BLACK)
    prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
    SCREEN.blit(prompt_text, prompt_rect)

def reset_game():
    global bird_y, velocity, pipes, score, game_over, bird_rect, is_invincible, lives, is_dashing
    
    bird_y = int(SCREEN_HEIGHT / 2)
    velocity = 0
    pipes = []
    score = 0
    game_over = False
    bird_rect = pygame.Rect(bird_x, bird_y, bird_size, bird_size)
    
    # Reset status Nyawa dan Buff
    lives = LIVES_START
    is_invincible = False
    is_dashing = False

# --- Loop Utama Game ---
running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_over:
                    jump()
                else:
                    reset_game()
            
            # DASH (Tombol C)
            if event.key == pygame.K_c:
                if not game_over:
                    dash()

    # --- Logika Update (Jika Game Belum Berakhir) ---
    if not game_over:
        # 1. Update Fisika Burung (Hanya jika tidak Dash)
        if not is_dashing:
            velocity += gravity
            bird_y += velocity
            bird_rect.y = bird_y
        
        # 2. Logika Buff Invincibility (Tembus Pipa)
        if score >= INVINCIBLE_ACTIVATE_SCORE and score < INVINCIBLE_END_SCORE and not is_invincible:
            is_invincible = True
            print("BUFF TEMBUS PIPA AKTIF!")
        elif score >= INVINCIBLE_END_SCORE and is_invincible:
            is_invincible = False
            print("BUFF TEMBUS PIPA NONAKTIF!")
        
        # 3. Logika Buff Dash
        if is_dashing:
            if current_time - dash_start_time > dash_duration:
                is_dashing = False # Selesaikan Dash
                print("Dash selesai.")
            # Selama Dash, burung mempertahankan posisi Y-nya
        
        # 4. Spawn Pipa Baru
        if current_time - last_pipe_time > pipe_spawn_time:
            create_pipe()
            last_pipe_time = current_time
            
        # 5. Gerakkan Pipa
        move_pipes()
        
        # 6. Cek Tabrakan
        game_over = check_collision()
        
    # --- Rendering (Menggambar) ---
    SCREEN.fill(SKY_BLUE) 

    draw_pipes()
    draw_bird()

    # Tampilkan Skor, Nyawa, dan HS
    score_text = font.render(f"Score: {score}", True, BLACK)
    SCREEN.blit(score_text, (10, 10))
    
    lives_text = font.render(f"Lives: {lives}", True, RED)
    SCREEN.blit(lives_text, (10, 40))
    
    highscore_text = font.render(f"High Score: {high_score}", True, BLACK)
    SCREEN.blit(highscore_text, (SCREEN_WIDTH - highscore_text.get_width() - 10, 10))

    # Tampilkan Status Buff
    if is_invincible:
        status_color = PURPLE if is_dashing else CYAN
        buff_status_text = font.render("BUFF AKTIF! (C = DASH)", True, status_color)
        SCREEN.blit(buff_status_text, (SCREEN_WIDTH // 2 - buff_status_text.get_width() // 2, 40))

    if game_over:
        game_over_screen()
        
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()