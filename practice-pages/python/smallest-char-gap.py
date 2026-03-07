def smallest_gap(s):
    L_letters = unique_characters(s)

    # For each unique character now find the length of each gap between same character (if any)
    smallest_gap = len(s)
    smallest_gap_str = None
    smallest_gap_pos = len(s)
    
    for letter in L_letters:
        
        L_letter_pos = []

        for i, char in enumerate(s):
            
            if char == letter:
                L_letter_pos.append(i)

        if len(L_letter_pos) >= 2: # Otherwise no gap => not interested
        
            prev_letter_pos = None
            for letter_pos in L_letter_pos:
                if prev_letter_pos != None:
                    gap_size = letter_pos - prev_letter_pos - 1
                    if gap_size < smallest_gap or (gap_size == smallest_gap and prev_letter_pos < smallest_gap_pos): # Choosing the gap that comes first when have gaps of equal size
                        smallest_gap = gap_size
                        smallest_gap_pos = prev_letter_pos
                        smallest_gap_str = s[prev_letter_pos+1:letter_pos]
                
                prev_letter_pos = letter_pos

    return smallest_gap_str

# Returns a list of all unique characters in a string
def unique_characters(s):
    L_letters = []

    L_letters.append(s[0]) # Just so that list is no longer empty

    for char in s:
        
        is_new_char = True
        for letter in L_letters:
            if char == letter:
                is_new_char = False
        
        if is_new_char:
            L_letters.append(char)
    
    return L_letters

L_test_str = [
    "ABCDAC",
    "racecar",
    "A{5e^SD*F4i!o#q6e&rkf(po8|we9+kr-2!3}=4",
    "Hello World",
    "The quick brown fox jumps over the lazy dog."
]

for test_str in L_test_str:
    print()
    print(test_str)
    print(smallest_gap(test_str))