# Rosetta Code Problem 2

import random
import matplotlib.pyplot as plt

# Index of each Card = Drawer number
# Value of each Card = Corresponding prisoner number
def genCards(N):
    L_cards = list(range(N))
    random.shuffle(L_cards)
    return L_cards

def successfulRandTurn(N, L_cards, prisoner_num):
    drawers_to_search = {i for i in range(N)}

    drawers_searched = random.sample(drawers_to_search, N//2)

    for drawer in drawers_searched:
        if L_cards[drawer] == prisoner_num:
            return True
    
    return False

def successfulOptTurn(N, L_cards, prisoner_num):
    drawer = prisoner_num # Start by opening draw of same number as prisoner's own number
    for _ in range(N//2):
        number_drawn = L_cards[drawer]
        if number_drawn == prisoner_num:
            return True
        else:
            drawer = number_drawn
    
    return False

def successfulTrial(N, strategy):
    L_cards = genCards(N)

    for prisoner_num in range(N):
        if strategy == "rand":
            if not successfulRandTurn(N, L_cards, prisoner_num):
                return False
            
        elif strategy =="opt":
            if not successfulOptTurn(N, L_cards, prisoner_num):
                return False
    
    return True

# N : number of prisoners
def simulate(N, trials=2000):
    num_rand_successful = 0
    num_opt_successful = 0
    
    for _ in range(trials):
        if successfulTrial(N, strategy = "rand"):
            num_rand_successful += 1
        if successfulTrial(N, strategy = "opt"):
            num_opt_successful += 1
    
    percRandSuccess = num_rand_successful/trials * 100
    percOptSuccess = num_opt_successful/trials * 100

    return (percRandSuccess, percOptSuccess)

T_results = simulate(100)

print(f"Proportion of Trials with Random Strategy Successful = {T_results[0]} %\nProportion of Trials with Optimum Strategy Successful = {T_results[1]} %")

# Taking further now to explore different N of prisoners

# Plotting success rates for each strategy as N of prisoners varies

N_values = list(range(3, 10, 1)) + list(range(10, 201, 10))
rand_results = []
opt_results = []

for N in N_values:
    r, o = simulate(N, trials=200000//N) # Trying to maximise no of trials for smaller N to minimise noise
    rand_results.append(r)
    opt_results.append(o)

plt.plot(N_values, rand_results, label="Random Strategy")
plt.plot(N_values, opt_results, label="Optimal Strategy")

plt.xlabel("Number of Prisoners (N)")
plt.ylabel("Probability of Success")
plt.title("100 Prisoners Problem: Success Probability vs N")
plt.legend()

plt.show()
# Think noise is due to number of attempts given to prisoners being determined by N//2 
# Therfore small even numbers have a serious advantage over small odd numbers