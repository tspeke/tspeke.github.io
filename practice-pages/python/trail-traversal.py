def navigate_trail(map):
    grid = gen_grid(map)
    grid_h = len(grid[0])
    grid_w = len(grid)

    start_coord = find_start(grid)
    
    if start_coord: # Checking C acc exists on map
        x,y = start_coord
        S_moves = ""
        moving = True
        path_coord = []
        
        ref_grid = grid # Going to change each visited tile --> "-" value

        while moving:
            ref_grid[x][y] = "-" # Ensures wont revisit the same spot again
            path_coord.append((x,y))

            if x+1 < grid_w: # Preventing from error occuring from checking off the map
                if ref_grid[x+1][y] != "-":
                    S_moves = S_moves + "R"
                    x = x+1
                    continue
            if y+1 < grid_h:
                if ref_grid[x][y+1] != "-":
                    S_moves = S_moves + "D"
                    y = y+1
                    continue
            if x-1 >= 0:
                if ref_grid[x-1][y] != "-":
                    S_moves = S_moves + "L"
                    x = x-1
                    continue
            if y-1 >= 0:
                if ref_grid[x][y-1] != "-":
                    S_moves = S_moves + "U"
                    y = y-1
                    continue

            # Assumes if no continuation tiles found => must be at goal
            # Would be skipped if any of the above satisfied
            moving = False
        
    return S_moves

# Converting list of strings map input --> 2D array
def gen_grid(map):
    grid = []

    for i in range(len(map[0])):
        column = []
        
        for j in range(len(map)):
            column.append(map[j][i])
        
        grid.append(column)

    return grid

def find_start(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "C":
                return (i,j)
    
    return None

L_test_maps = [
    [
        "-CT--", 
        "--T--", 
        "--TT-", 
        "---T-", 
        "---G-"],
    [
        "-----", 
        "--TTG", 
        "--T--", 
        "--T--", 
        "CTT--"],
    [
        "-C----", 
        "TT----", 
        "T-----", 
        "TTTTT-", 
        "----G-"],
    [
        "--------", 
        "-CTTT---", 
        "----T---", 
        "---GT---", 
        "--------"],
    [
        "TTTTTTT-", 
        "T-----T-", 
        "T-----T-", 
        "TTTT--TG", 
        "---C----"]]

for test_map in L_test_maps:
    print(test_map)
    print(navigate_trail(test_map))