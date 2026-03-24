def sum_of_factorial(n):

    # Want to find numbers which can make 10 since x10 adds exactly zero to digit sum
    current_factorial = 1
    for i in range(1, n+1):
        
        if i % 10 == 0: # Bug was removing the number COMPLETELY - e.g. x40 will still impart x4
            current_factorial *= (i // 10)

        elif i % 5 == 0: # Since more even numbers than multiples of 5 => x5 always makes a new factor of 10
            current_factorial //= 2
            current_factorial *= (i // 5)
            continue

        else:
            current_factorial *= i
        
        print(i)

    print(current_factorial)

    sum_of_digits = 0
    for pos in range(len(str(current_factorial))):
        sum_of_digits += int(str(current_factorial)[pos])
    
    return sum_of_digits

print(sum_of_factorial(100))