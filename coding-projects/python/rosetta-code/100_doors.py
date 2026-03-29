# Rosetta Code Problem 1

def passDoors(L_doors, interval):
    for i in range(interval-1, len(L_doors), interval):
        L_doors[i] = not L_doors[i]
    
    return L_doors

# True = Door Open
# False = Door Closed
def getFinalOpenedDoors(N):
    L_doors = [False for _ in range(1,N+1)]
    for i in range(1,N+1):
        L_doors = passDoors(L_doors, i)
    
    return L_doors

finalDoorStates = getFinalOpenedDoors(100)
print(finalDoorStates)
print([i+1 for i, state in enumerate(finalDoorStates) if state])