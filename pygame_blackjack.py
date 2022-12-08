# black jack in python with pygame
# import modules needed
import copy
import random

import pygame

# game variables initialized here
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 1
WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')
fps = 60
timer = pygame.time.Clock()
active = False
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
initial_deal = False
reveal_dealer = False
player_score = 0
dealer_score = 0
hand_active = False
records = [0, 0, 0]
outcome = 0
add_score = False
results = ['', 'PLAYER BUSTED! o_O', 'PLAYER WINS :)', 'DEALER WINS :(', 'TIE GAME...']


# when function is asked to add a card to a deck, randomly select a card, add to hand, and remove from deck
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card - 1])
    current_deck.pop(card - 1)
    print(current_hand, current_deck)
    return current_hand, current_deck


# function to calculate and score of player and dealer
def calculate_score(hand):
    # calculate hand score fresh every loop, check how many aces the hand is holding
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        # for 2,3,4,5,6,7,8,9 just add the number
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        # for 10 and all face cards add ten
        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        # for aces, start by adding 11, we'll handle picking between 11 or 1 later
        elif hand[i] == 'A':
            hand_score += 11
    # determine how many aces need to be 1s to reduce score below 21 if possible
    if hand_score > 21 and aces_count > 0:
        for i in range(1, aces_count + 1):
            if hand_score > 21:
                hand_score -= 10

    return hand_score


# show player and dealer hand totals
def draw_scores(player, dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (350, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'), (350, 100))


# pygame commands for displaying key gameplay items
def draw_game(active_hand, record, result):
    button_list = []
    # initially on game startup, only give the player a deal button
    if not active_hand:
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 20, 300, 100], 3, 5)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (165, 50))
        button_list.append(deal)
    # once game has started, show the hit and stand buttons, hand scores, and record of games
    else:
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [0, 700, 300, 100], 3, 5)
        screen.blit(font.render('HIT ME', True, 'black'), (55, 735))
        button_list.append(hit)
        stand = pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [300, 700, 300, 100], 3, 5)
        screen.blit(font.render('STAND', True, 'black'), (355, 735))
        button_list.append(stand)
        screen.blit(font.render('Your Hand: ', True, 'white'), (50, 400))
        screen.blit(font.render('Dealer Hand: ', True, 'white'), (50, 100))
        # display records from while the player has been playing record = w,l,d
        score_text = smaller_font.render(f'Wins: {record[0]}     Losses:{record[1]}     Draws:{record[2]}', True,
                                         'white')
        screen.blit(score_text, (15, 840))
        # once there is an outcome from the game, display the status at top of screen, with play again button
        if result != 0:
            screen.blit(font.render(results[result], True, 'white'), (15, 25))
            deal = pygame.draw.rect(screen, 'white', [150, 220, 300, 100], 0, 5)
            pygame.draw.rect(screen, 'green', [150, 220, 300, 100], 3, 5)
            pygame.draw.rect(screen, 'black', [153, 223, 294, 94], 3, 5)
            deal_text = font.render('NEW HAND', True, 'black')
            screen.blit(deal_text, (165, 250))
            button_list.append(deal)

    return button_list


# display player and dealer cards - shift right and down to display several cards as if in hand together
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
        screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 465 + 5 * i))
        screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 635 + 5 * i))
        pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)
    # if player turn hasn't finished, the dealer's second card remains hidden
    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 335 + 5 * i))
        else:
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 335 + 5 * i))
        pygame.draw.rect(screen, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)


#  check for endgame scenarios, then decide what the outcome is and update the scores
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    # check end game scenarios once player has stood, blackjacked or busted
    # result 1 = player busted, 2 = win, 3 = loss, 4 =  push, totals 0 = win, 1 = loss, 2 = draw
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
    return result, totals, add


# main game loop - code that runs repeatedly during game operation goes here
run = True
while run:
    # run game at framerate, fill with bg color
    timer.tick(fps)
    screen.fill('black')

    # for first deal, give player and dealer two cards from fresh game deck
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False
    # once cards are given out, calculate scores, display cards and scores
    if active:
        calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        player_score = calculate_score(my_hand)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)
    # always show buttons, the function handles which ones are active
    buttons = draw_game(active, records, outcome)

    # event handling - if quit button pressed, always end while loop, if deal pressed initially, set game in motion
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    hand_active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    add_score = True
            # put code to handle hit me, stand, and restart buttons while gameplay is active
            else:
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        hand_active = True
                        reveal_dealer = False
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0
    # if player busts, end turn
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True
    # check end game scenarios once player has stood or busted
    # outcome 1 = player busted, 2 = win, 3 = loss, 4 =  push
    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)
    # display everything on screen
    pygame.display.flip()
# end function if while loop exited
pygame.quit()
