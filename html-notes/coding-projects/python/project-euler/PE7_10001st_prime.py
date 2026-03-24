def prime_generator(x):
	l_of_primes = [2]

	i = 2
	finding_primes = True
	while finding_primes:
		i += 1
		i_is_prime = True

		for prime in l_of_primes:
			if i%prime == 0:
				i_is_prime = False
				break

		if i_is_prime:
			l_of_primes.append(i)

			if len(l_of_primes) == x:
				finding_primes = False

	return l_of_primes

### Result

# print(prime_generator(10001)[-1])