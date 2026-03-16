import os

value_map = {
    '2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13,'A':14
}
L_suits = ['S', 'H', 'D', 'C']

script_dir = os.path.dirname(__file__)
path = os.path.join(script_dir, "54-poker.txt") # finding the path between python script --> txt file

with open(path) as f:
    for line in f:
        cards = line.split() # Default is to split on Whitespace e.g. spaces, tabs, new lines

        h1 = cards[:5]
        h2 = cards[5:]

        if p1_wins(h1, h2):
            wins += 1

# Compares h1 and h2 and returns True is h1 is better than h2
def p1_wins(hand1, hand2):
    return score_hand(hand1) > score_hand(hand2) 
    
def score_hand(hand):
    # Extracting hand info
    values = sorted([value_map[c[0]] for c in hand], reverse=True) # For the kickers
    suits = [c[1] for c in hand]

print(count_p1_wins(L_hands))