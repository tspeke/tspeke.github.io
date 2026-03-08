def shift_matrix(M_input, shift):
    
    height = len(M_input)
    width = len(M_input[0])
    size = width * height

    M_shifted = [[0]*width for _ in range(height)]
    
    for j in range(height):
        for i in range(width):
            # "Flatten" the matrix into single index parameter
            index = j*width + i
            shifted_index = (index + shift) % size
            shifted_i = shifted_index % width
            shifted_j = shifted_index // width
            M_shifted[shifted_j][shifted_i] = M_input[j][i]

    return M_shifted

L_test_M = [
    [[1, 2, 3], 
     [4, 5, 6]],
    
    [[1, 2, 3], 
     [4, 5, 6]],

    [[1, 2, 3], 
     [4, 5, 6], 
     [7, 8, 9]],

    [[1, 2, 3], 
     [4, 5, 6], 
     [7, 8, 9]],

    [[1, 2, 3, 4], 
     [5, 6, 7, 8], 
     [9, 10, 11, 12], 
     [13, 14, 15, 16]],

    [[1, 2, 3, 4], 
     [5, 6, 7, 8], 
     [9, 10, 11, 12], 
     [13, 14, 15, 16]]
     
]

L_test_shifts = [1, -1, 5, -6, 7, -54]

for i in range(len(L_test_M)):
    test_M = L_test_M[i]
    test_shift = L_test_shifts[i]
    print(f"\nInitial Matrix: {test_M}")
    print(f"Shift: {test_shift}")
    print(f"Shifted Matrix: {shift_matrix(test_M, L_test_shifts[i])}")