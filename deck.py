import random
from card import Card

def create_deck():
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def draw_luck_card(luck, current_score):
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suits = ["hearts", "diamonds", "clubs", "spades"]
    
    # We create a list of weights, starting with 1 for every card
    weights = [1.0] * len(ranks)

    # If luck is high, we help the player avoid busting!
    if luck > 5:
        # Calculate how much room we have before 21
        room = 21 - current_score
        
        for i, rank in enumerate(ranks):
            # Get the numerical value of this rank
            val = 11 if rank == "A" else (10 if rank in "JQK" else int(rank))
            
            # If this card would make the player hit exactly 21, 
            # increase the weight based on luck!
            if current_score + val == 21:
                weights[i] += (luck - 5) * 2 
            
            # If this card would make the player bust (> 21),
            # decrease the weight significantly based on luck
            elif current_score + val > 21:
                # High luck makes it very unlikely to draw a 'bust' card
                weights[i] /= (luck - 4)

    # Select a rank based on our calculated weights
    chosen_rank = random.choices(ranks, weights=weights, k=1)[0]
    # Suit usually remains purely random in Blackjack
    chosen_suit = random.choice(suits)
    
    return chosen_rank, chosen_suit

def deal_initial_cards(player_hand, dealer_hand, luck):
    # Standard Blackjack opening: 2 for player, 2 for dealer
    # We use a loop or manual sequence
    
    # 1. Player's first card
    p1_rank, p1_suit = draw_luck_card(luck, 0)
    p1_sprite = Card(p1_rank, p1_suit, (1100, 100), (100, 500))
    player_hand.add_card(p1_sprite)
    p1_sprite.flip() # Player's cards are usually dealt face-up
    
    # 2. Dealer's first card (Face Down)
    d1_rank, d1_suit = draw_luck_card(5, 0) # Dealer doesn't get "Luck"
    d1_sprite = Card(d1_rank, d1_suit, (1100, 100), (100, 150), should_flip=False)
    dealer_hand.add_card(d1_sprite)
    # Note: We do NOT call flip() yet! It stays as the back image.
    
    # 3. Player's second card
    p2_rank, p2_suit = draw_luck_card(luck, player_hand.value)
    p2_sprite = Card(p2_rank, p2_suit, (1100, 100), (180, 500))
    player_hand.add_card(p2_sprite)
    p2_sprite.flip()
    
    # 4. Dealer's second card (Face Up)
    d2_rank, d2_suit = draw_luck_card(5, dealer_hand.value)
    d2_sprite = Card(d2_rank, d2_suit, (1100, 100), (180, 150), should_flip=True)
    dealer_hand.add_card(d2_sprite)
    d2_sprite.flip()

def run_dealer_turn(dealer_hand, player_hand, luck):
    # 1. First, reveal the hidden card!
    for card_sprite in dealer_hand.cards:
        if not card_sprite.face_up:
            card_sprite.flip()
            
    # 2. If the player hasn't busted, the dealer must play
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            # Dealer draws a card (usually not luck-based)
            rank, suit = draw_luck_card(5, dealer_hand.value)
            # Position it next in the dealer's row
            target_x = 100 + (len(dealer_hand.cards) * 80)
            target_y = 150
            new_card = Card(rank, suit, (1100, 100), (target_x, target_y))
            dealer_hand.add_card(new_card)
            new_card.flip() # Dealer cards are always visible now

    # 3. Finally, decide the winner and update winnings!
    resolve_hand(player_hand, dealer_hand)

def resolve_hand(player_hand, dealer_hand):
    global winnings # If you have a global winnings or pass it as an argument
    
    p_val = player_hand.value
    d_val = dealer_hand.value
    
    if p_val > 21:
     # Already handled in the bust check, but good for safety
        return "Bust!"
    elif d_val > 21 or p_val > d_val:
            # Player wins!
        return "Win!"
    elif p_val < d_val:
            # Dealer wins!
        return "Loss!"
    else:
            # Push! (A tie)
        return "Push!"

def calculate_winnings(player_value, dealer_value, bet):
    if player_value > 21:
        return -bet  # Loss
    if dealer_value > 21:
        return bet   # Dealer bust, player wins
    if player_value > dealer_value:
        return bet   # Player higher, player wins
    if player_value < dealer_value:
        return -bet  # Dealer higher, player loss
    return 0         # Push (Tie)