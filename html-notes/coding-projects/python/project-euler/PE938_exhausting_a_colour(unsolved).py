import random

def turn(T_deck):
    red, black = T_deck

    # True if red
    # False if black
    x = random.random() # Random float between 0.0 and 1.0
    card1 = (x <= red / (red + black))
    
    if card1:
        temp_red = red - 1
        temp_black = black
    else:
        temp_red = red
        temp_black = black - 1

    x = random.random()
    card2 = (x <= temp_red / (temp_red + temp_black))
    
    if card1 == card2:
        if card1: # both red
            red -= 2
        else: # both black
            pass
    else:
        black -= 1
    
    return (red, black)

def play_game(T_init_deck):
    c_red, c_black = T_init_deck

    playing = True
    while playing:
        
        # Check for game conclusion condition
        if c_red == 0:
            return True # All remaining cards in deck are black
        elif c_black == 0:
            return False
        
        c_red, c_black = turn((c_red, c_black))

# no_games gives the number of games that should be evaluated to arrive at the estimate
def estimate_p(T_init_deck, no_games):
    
    no_black_wins = 0
    for _ in range(no_games):
        if play_game(T_init_deck):
            no_black_wins += 1
    
    return no_black_wins / no_games

# print(estimate_p((2,2), int(1E6)))

# print(estimate_p((24690, 12345), int(1000)))

from collections import defaultdict

def prob_black_win(R0, B0, tol=1e-14):

    states = {(R0,B0): 1.0}
    black_win = 0.0

    while states:
        new_states = defaultdict(float)

        for (r,b), p in states.items():

            if r == 0:
                black_win += p
                continue

            if b == 0:
                continue

            n = r + b

            p_rr = r*(r-1)/(n*(n-1))
            p_bb = b*(b-1)/(n*(n-1))
            p_rb = 1 - p_rr - p_bb

            denom = 1 - p_bb

            p_rr /= denom
            p_rb /= denom

            pr = p * p_rr
            pb = p * p_rb

            if pr > tol:
                new_states[(r-2,b)] += pr

            if pb > tol:
                new_states[(r,b-1)] += pb

        states = new_states

    return black_win

P = prob_black_win(24690,12345)
print(P)
print(round(P, 10))