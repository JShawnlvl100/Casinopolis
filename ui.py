import pygame

def draw_start_screen(screen):
    font = pygame.font.SysFont("Arial", 48)
    title_font = pygame.font.SysFont("Arial", 72)
    
    # Render text
    title_surface = title_font.render("CASINOPOLIS", True, "gold")
    start_surface = font.render("Press SPACE to Deal", True, "white")
    
    # Position text
    title_rect = title_surface.get_rect(center=(640, 200))
    start_rect = start_surface.get_rect(center=(640, 400))
    
    screen.blit(title_surface, title_rect)
    screen.blit(start_surface, start_rect)

def draw_game_over_screen(screen):
    font = pygame.font.SysFont("Arial", 48)
    
    msg_surface = font.render("GAME OVER", True, "red")
    retry_surface = font.render("Press R to Restart or Q to Quit", True, "white")
    
    msg_rect = msg_surface.get_rect(center=(640, 300))
    retry_rect = retry_surface.get_rect(center=(640, 400))
    
    screen.blit(msg_surface, msg_rect)
    screen.blit(retry_surface, retry_rect)