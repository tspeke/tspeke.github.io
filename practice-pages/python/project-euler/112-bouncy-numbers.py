def is_bouncy(n):
    L_digits = [int(char) for char in str(n)]
    
    is_increasing = None
    for i in range(len(L_digits) - 1):
        if (L_digits[i] < L_digits[i+1]):
            is_increasing = True
            break
        elif (L_digits[i] > L_digits[i+1]):
            is_increasing = False
            break
    
    if is_increasing == None:
        return False # Flat number!! e.g. 11
    
    for i in range(len(L_digits) - 1): # Compring each digit with its next
        if is_increasing and (L_digits[i] > L_digits[i+1]):
            return True
        elif not is_increasing and (L_digits[i] < L_digits[i+1]):
            return True
    
    return False

# Calculates the percent of numbers up to (and including) N which are bouncy
def percent_bouncy(N):
    no_bouncy = 0
    for i in range(N+1):
        if is_bouncy(i):
            no_bouncy += 1
    
    return (no_bouncy / N) * 100

# Returns the number at which the percentage of numbers which are bouncy fist exceeds t_percent
def number_for_prop_bouncy(t_percent):
    percent_bouncy = 0
    no_bouncy = 0
    i = 0
    while percent_bouncy < t_percent:
        
        i += 1
        
        if is_bouncy(i):
            no_bouncy += 1

        percent_bouncy = (no_bouncy / i) * 100
    
    return i

print(percent_bouncy(538))

print(number_for_prop_bouncy(90))

print(number_for_prop_bouncy(99))