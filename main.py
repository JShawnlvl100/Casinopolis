import pygame
import sys
import platform
import os
from winnings import *
from sounds import sounds
from constants import *
from resources import load_card_assets, CARD_IMAGES
from card import Card
from hand import Hand
from deck import *
import ui


RESOLUTIONS = [
    (1280, 720),
    (1920,1080),
]

def main():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    if platform.system() == "Windows":
        os.environ['SDL_AUDIODRIVER'] = 'directsound'
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init() 
    resolution_index = 0
    SCREEN_WIDTH, SCREEN_HEIGHT = RESOLUTIONS[resolution_index]
    state = "START"
    is_paused = False
    font = pygame.font.SysFont("Arial", 36)
    pause_text = font.render(f"PAUSED", True, (255, 255, 255))
    cards = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Card.containers = (updatable, drawable)
    clock = pygame.time.Clock()
    dt = 0
    val_dict = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
            "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11
        }
    player_hand = Hand()
    dealer_hand = Hand()
    winnings = 1000
    luck = 1
    hand_active = True
    result_text = ""

    print(f"Starting Casinopolis with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    load_card_assets()
    sounds.load_assets()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if state == "START":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    import constants
                    resolution_index = (resolution_index + 1) % len(RESOLUTIONS)
                    SCREEN_WIDTH, SCREEN_HEIGHT = RESOLUTIONS[resolution_index]
                    pygame.display.quit()
                    os.environ["SDL_VIDEO_CENTERED"] = "1"
                    pygame.display.init()
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    constants.SCREEN_WIDTH = SCREEN_WIDTH
                    constants.SCREEN_HEIGHT = SCREEN_HEIGHT
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player_hand = Hand()
                    dealer_hand = Hand()
                    for sprite in updatable:
                        sprite.kill()
                    deal_initial_cards(player_hand, dealer_hand, luck)
                    state = "PLAYING"
                    hand_active = True
                    if player_hand.value == 21:
                        hand_active = False
                        if dealer_hand.value != 21:
                            winnings += 150
                            result_text = "BLACKJACK! (3:2 Payout)"
                        else:
                            result_text = "PUSH (DOUBLE BLACKJACK)"
                        for card_spite in dealer_hand.cards:
                            card_spite.flip()
            elif state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if hand_active:
                        if event.key == pygame.K_l:
                            luck += 1
                            print(f"Luck boosted! Luck is now {luck}")
                        if event.key == pygame.K_h:
                            # 1. Get a lucky card based on current score
                            rank, suit = draw_luck_card(luck, player_hand.value)
                            target_x = 100 + (len(player_hand.cards) * 80)
                            target_y = 500                
                            new_card_sprite = Card(rank, suit, (1100, 100), (target_x, target_y))
                            player_hand.add_card(new_card_sprite)
                            if player_hand.value > 21:
                                hand_active = False
                                outcome = calculate_winnings(player_hand.value, dealer_hand.value, 100)
                                winnings += outcome
                                if outcome > 0:
                                    result_text = "YOU WIN!"
                                elif outcome < 0:
                                    result_text = "YOU LOSE!"
                                else:
                                    result_text = "PUSH"
                                for card_sprite in dealer_hand.cards:
                                    card_sprite.flip()
                            elif player_hand.value == 21:
                                hand_active = False
                                run_dealer_turn(dealer_hand, player_hand, luck)
                                outcome = calculate_winnings(player_hand.value, dealer_hand.value, 100)
                                winnings += outcome
                                if outcome > 0:
                                    result_text = "YOU WIN!"
                                elif outcome < 0:
                                    result_text = "YOU LOSE!"
                                else:
                                    result_text = "PUSH"
                        if event.key == pygame.K_s:
                            hand_active = False
                            run_dealer_turn(dealer_hand, player_hand, luck)
                            outcome = calculate_winnings(player_hand.value, dealer_hand.value, 100)
                            winnings += outcome
                            if outcome > 0:
                                result_text = "YOU WIN!"
                            elif outcome < 0:
                                result_text = "YOU LOSE!"
                            else:
                                result_text = "PUSH"
                    else:
                        if event.key == pygame.K_SPACE:
                            if winnings <= 0:
                                state = "GAME_OVER"
                        else:   
                            # Reset the table
                            for sprite in updatable:
                                sprite.kill()
                            player_hand = Hand()
                            dealer_hand = Hand()

                            deal_initial_cards(player_hand, dealer_hand, luck)
                            hand_active = True 
                            result_text = ""
                            if player_hand.value == 21:
                                hand_active = False
                                if dealer_hand.value != 21:
                                    winnings += 150
                                    result_text = "BLACKJACK! (3:2 Payout)"
                                else:
                                    result_text = "PUSH (DOUBLE BLACKJACK)"
                                for card_spite in dealer_hand.cards:
                                    card_spite.flip()
            elif state == "GAME_OVER":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: # 'R' to Restart
                        state = "START"
                    elif event.key == pygame.K_q: # 'Q' to Quit
                        return
        dt_ms = clock.tick(60)
        dt = dt_ms / 1000
        screen.fill("black")
        if state == "START":
            ui.draw_start_screen(screen)
        elif state == "PLAYING":
            if hand_active:
                visible_value = sum([val_dict[c.rank] for c in dealer_hand.cards if c.face_up])
                dealer_text = font.render(f"Dealer: {visible_value} + ?", True, (255, 255, 255))
            else:
                dealer_text = font.render(f"Dealer: {dealer_hand.value}", True, (255, 255, 255))
            winnings_surface = font.render(f"Winnings: {winnings}", True, (255, 255, 255))
            hand_value_surface = font.render(f"Hand: {player_hand.value}", True, (255, 255, 255))
            results_surface = font.render(f"{result_text}", True, (255, 255, 255))
            deck_image = CARD_IMAGES["back"]
            screen.blit(deck_image, (1100, 100))
            screen.blit(winnings_surface, (10, 10))
            screen.blit(hand_value_surface, (10, 640))
            screen.blit(dealer_text, (10, 40))
            screen.blit(results_surface, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            for draw in drawable:
                draw.draw(screen)
            if not is_paused:
                updatable.update(dt)
                
                
            else:
                text_rect = pause_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                screen.blit(pause_text, text_rect)
            

        elif state == "GAME_OVER":
            ui.draw_game_over_screen(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
