from collections import Counter

import PE7_10001st_prime as PE7

# N gives the maximum value any element of the chain may have
def gen_amicable_chains(N):
    L_primes = PE7.prime_generator(N)
    L_chains = []

    to_check = set(range(1, int(1E6 + 1)))

    while True:
        
        start_n = to_check.pop()
        n = start_n
        chain = []
        valid_chain = True
        
        while True:
            chain.append(n)
            n = sum(proper_divisors(n, L_primes)) + 1 + n
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

def prime_factors(n, L_primes):
    L_factors = []
    for prime in L_primes:
        if n%prime == 0:
            while n%prime == 0:
                L_factors.append(prime)
                n = n//prime
    
    return L_factors

def proper_divisors(n, L_primes):
    factors = Counter(prime_factors(n, L_primes))
    
    divisors = [1]
    
    for prime, power in factors.items():
        new_divisors = []
        for d in divisors:
            for exp in range(1, power + 1):
                new_divisors.append(d * (prime ** exp))
        divisors += new_divisors
    
    divisors.remove(n)
    return divisors


#####################################################################################################

print(gen_amicable_chains(10000))