def prime_factors(x):
	l_prime_factors = []
	reduced_x = x
	factor_found = True
	largest_prime_checked = 2

	while factor_found == True:
		factor_found = False
		
		for i in range(largest_prime_checked, int(reduced_x**(1/2) + 1)):
			
			if (reduced_x%i) == 0:
				l_prime_factors.append(i)
				largest_prime_checked = i
				reduced_x = reduced_x//i
				factor_found = True
				break

	if reduced_x != x:
		l_prime_factors.append(reduced_x) # Since remainder must also be a prime factor

	return l_prime_factors