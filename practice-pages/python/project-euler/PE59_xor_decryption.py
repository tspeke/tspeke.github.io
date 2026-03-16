import os

script_dir = os.path.dirname(__file__)
path = os.path.join(script_dir, "59-cipher.txt") # finding the path between python script --> txt file

with open(path) as f:
    L_code = f.read().split(",")

for i in range(len(L_code)):
    L_code[i] = int(L_code[i])

# ord() converts Character --> ASCII code
# chr() converts ASCII code --> Character

# "L_code" is a list of integers corresponding to the encoded message
# "key" is 3 lower case characters
def xor_decrypt(L_code, key):
    
    # L_binary_code = [bin(number)[2:] for number in L_code] # "[2:]" necessary since binary values have "0b" prefix to code to indicate type
    
    # NB "^" operator acts on DECIMAL INTEGERS anyway!

    # Converting string key --> integer
    L_number_key = [ord(character) for character in key]

    L_decoded = []

    for i, number_code in enumerate(L_code):
        
        number_key = L_number_key[i % len(L_number_key)] # Happen to know length of binary_code is 3 but this is futureproofing

        number_decoded = number_code ^ number_key # "^" operator performs XOR on two Binary variables
    
        character_decoded = chr(number_decoded)

        L_decoded.append(character_decoded)
    
    return "".join(L_decoded)

def crack_code(L_code, key_length):
    # going to cycle through each key character to finds one with maximum number of " " ~ SPACE characters
    
    L_max_counts = [0 for _ in range(key_length)]
    L_best_ascii = [0 for _ in range(key_length)]
    
    for ascii_code in range(0, 128):
        
        L_current_counts = [0 for _ in range(key_length)]
        for i, code in enumerate(L_code):
            
            # Tests whether performing XOR on code with key results in --> SPACE key
            if (code ^ ascii_code) == 32:
                L_current_counts[i%key_length] += 1
        
        for j in range(key_length):
            if L_current_counts[j] > L_max_counts[j]:
                L_max_counts[j] = L_current_counts[j]
                L_best_ascii[j] = ascii_code
        
    # Now assuming most common character is the space character can infer key value...   
    key = ""
    for i in range(key_length):
        ascii_key = L_best_ascii[i] # 32 = ASCII character of the SPACE key
        char_key = chr(ascii_key)
        key = key + char_key
    
    return key

key = crack_code(L_code, 3)

decoded_message = xor_decrypt(L_code, key)

# Problem wants the sum of message ASCII values
message_sum = 0
for char in decoded_message:
    message_sum += ord(char)

print(f"\nKey: {key}")
print(f"\nSum of ASCII values of decoded message: {message_sum}")
print(f"\nDecrypted message:\n{decoded_message}")