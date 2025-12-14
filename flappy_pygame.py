import pygame
import random

# --- Inisialisasi Pygame ---
pygame.init()

# --- Konstanta Game ---
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird Pygame')

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (112, 197, 206)
YELLOW = (255, 255, 0)
GREEN = (0, 150, 0)
RED = (255, 0, 0)

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
jump_power = -7

# --- Variabel Pipa ---
pipe_width = 50
pipe_gap = 130
pipe_speed = 3
pipes = []
score = 0
pipe_spawn_time = 1800  # Waktu dalam milidetik
last_pipe_time = pygame.time.get_ticks()

# --- Status Game ---
game_over = False
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 64)

# --- Fungsi Pipa ---
def create_pipe():
    # Tinggi pipa atas secara acak
    min_height = 100
    max_height = SCREEN_HEIGHT - pipe_gap - 100
    top_height = random.randint(min_height, max_height)
    
    # Buat Rects untuk pipa atas dan bawah
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
        pipe['top'].x -= pipe_speed
        pipe['bottom'].x -= pipe_speed
        
        # Cek Skor
        if pipe['top'].right < bird_x and not pipe['passed']:
            score += 1
            pipe['passed'] = True
            
    # Hapus pipa yang sudah keluar layar
    pipes[:] = [pipe for pipe in pipes if pipe['top'].right > 0]

# --- Fungsi Burung ---
def draw_bird():
    pygame.draw.rect(SCREEN, YELLOW, bird_rect)

def jump():
    global velocity
    velocity = jump_power

# --- Fungsi Tabrakan ---
def check_collision():
    # Cek Batas Atas/Bawah
    if bird_rect.bottom >= SCREEN_HEIGHT or bird_rect.top <= 0:
        return True
    
    # Cek Pipa
    for pipe in pipes:
        if bird_rect.colliderect(pipe['top']) or bird_rect.colliderect(pipe['bottom']):
            return True
            
    return False

# --- Fungsi Game Over ---
def game_over_screen():
    text = big_font.render("GAME OVER", True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    SCREEN.blit(text, text_rect)
    
    restart_text = font.render("Tekan SPACE untuk Restart", True, BLACK)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
    SCREEN.blit(restart_text, restart_rect)

def reset_game():
    global bird_y, velocity, pipes, score, game_over, bird_rect
    bird_y = int(SCREEN_HEIGHT / 2)
    velocity = 0
    pipes = []
    score = 0
    game_over = False
    bird_rect = pygame.Rect(bird_x, bird_y, bird_size, bird_size)

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

    # --- Logika Update (Jika Game Belum Berakhir) ---
    if not game_over:
        # 1. Update Fisika Burung
        velocity += gravity
        bird_y += velocity
        bird_rect.y = bird_y
        
        # 2. Spawn Pipa Baru
        if current_time - last_pipe_time > pipe_spawn_time:
            create_pipe()
            last_pipe_time = current_time
            
        # 3. Gerakkan Pipa
        move_pipes()
        
        # 4. Cek Tabrakan
        game_over = check_collision()
        
    # --- Rendering (Menggambar) ---
    SCREEN.fill(SKY_BLUE) # Latar Belakang

    draw_pipes()
    draw_bird()

    # Tampilkan Skor
    score_text = font.render(f"Score: {score}", True, BLACK)
    SCREEN.blit(score_text, (10, 10))

    if game_over:
        game_over_screen()
        
    # Update Layar dan Kontrol Kecepatan
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()