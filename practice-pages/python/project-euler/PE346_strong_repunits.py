# N is maximum number in decimal repunits should be searched below for
def gen_repunits(N):
    L_repunits = []
    
    b = 2
    while True:

        lowest_repunit = repunit_to_dec(b, 3)
        if lowest_repunit > N:
            break
        
        k = 3
        while True:
            new_repunit = repunit_to_dec(b, k)
            
            if new_repunit > N:
                break
            
            L_repunits.append(new_repunit)
            k += 1
        
        b += 1
    
    L_repunits.append(1) # Append since our algorithm only considers k >= 3
    
    L_unique_repunits = set(L_repunits)

    return L_unique_repunits

# b is base of repunit
# k is length of repunit string
def repunit_to_dec(b, k):
    sum = 0
    for i in range(k):
        sum += b**i

    return sum

set_of_repunits = gen_repunits(1E12)
#print(gen_repunits(1E12))
print(sum(set_of_repunits))