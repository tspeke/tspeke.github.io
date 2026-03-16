import math

# Returns Boolean output equating to whether the given number, n, can be written as the sum of a prime number and 2 x square number
def satisfies_goldbach(n, L_primes):
    for prime in L_primes:
        
        if prime <= n-2:
            residue = n - prime

            i = 1
            while 2*(i**2) <= residue:
                if residue == twice_square:
                    return True

                i += 1

        else:
            return False

### Adapted from Problem 10 which adapted from Problem 7 ###
def prime_generator(X): # X is now the stop value ie. subroutine returns L of primes below X
	l_of_primes = [2]

	for i in range(2, X):
		i += 1
		i_is_prime = True

		for prime in l_of_primes: # Can refine since know candidate factor must be less than half of i
			if prime > math.sqrt(i)+1:
				break
			if i%prime == 0:
				i_is_prime = False
				break

		if i_is_prime:
			l_of_primes.append(i)

	return l_of_primes
######################################

# Checks whether numbers up to N satisfy goldbach
def check_goldbach(N):
    L_primes = prime_generator(N)
    
    for odd in range(3, N+1, 2): # Taking steps of 2 => Checking only odd numbers
        is_prime = False
        for prime in L_primes:
            if prime == odd:
                is_prime = True
                break
            elif prime > odd:
                break
        
        if not is_prime:
            if satisfies_goldbach(odd, L_primes) == False:
                return odd
			
print(check_goldbach(1000000))