import math

### Initially taken from Problem 7 ###
def prime_generator(X): # Instead of X being the xth prime, X is now the stop value ie. subroutine returns L of primes below X
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

def sum_of_L(List):
	running_total = 0

	for number in List:
		running_total += number

	return running_total

### Results

print(sum_of_L(prime_generator(X=2000000)))