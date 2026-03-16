import _3_largest_prime_factor as PE3

# N gives the maximum value any element of the chain may have
def gen_amicable_chains(N):
    L_chains = []

    to_check = set(range(1, int(1E6 + 1)))

    while True:
        
        start_n = to_check.pop()
        n = start_n
        chain = []
        valid_chain = True
        
        while True:
            chain.append(n)
            n = sum(PE3.prime_factors(n)) + 1 + n
            to_check.discard(n)
            
            if n >= N:
                valid_chain = False
            
            if n == start_n:
                
                if valid_chain:
                    L_chains.append(chain)
                
                break
        
        if len(to_check) == 0:
            break
    
    return L_chains

print(gen_amicable_chains(10000))

#####################################################################################################