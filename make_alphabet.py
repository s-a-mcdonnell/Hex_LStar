
def check_validity(input):
    '''
    Check the validity of a specified character based on programmer-specified conditions 
    (often the size of the environment being tested)
    '''
    # Empty strings are invalid
    if len(input) == 0:
        return False

    # splice the three character string into three one-character chunks
    info = int(input[0], 16)
    x = int(input[1], 16)
    y = int(input[2], 16)

    # all 16 forms of info are valid

    # invalid if the second two coordinate 4-bit strings are outside of the walls
    # x needs to be... greater than zero, and less than 13
    if (x <= 5) or (x >= 11):
        return False
    
    if (y <= 5) or (y >= 11):
        return False
    
    '''The below commented out code is for a full hexgrid as seen in our HexSimulator repository'''

    # y needs to be... greater than 6 - i...
    # and less than 15 - i if x is odd, but less than 14 - i if x is even

    # if x % 2 == 0:
    #     # if x is even, i = x - 2 / 2
    #     i = (x - 2) / 2
    #     if (y <= 6 - i) or (y >= 14 - i):
    #         return False
        
    # # if x is odd...
    # else:
    #     i = (x - 1)/2
    #     if (y <= 6 - i) or (y >= 15 - i):
    #         return False

    return True


def write_alphabet():
    '''
    Write all valid letters of the alphabet into a text file for easy access by DFAs
    Currently, each "character" in our alphabet is made up of three hexadecimal characters:
    First character represents the ident, and second two represent the graph hex position of the ident
    '''
    # Writing to a text file according to this tutorial: https://www.w3schools.com/python/python_file_write.asp

    # Overwrite text in alphabet file with the empty string
    # "w" (write only) access mode createts a new file in the folder if it does not already exist (if it already exists, the file gets overwritten)
    f = open("alphabet.txt", "w")
    f.write("")
    f.close()

    # Re-open file to append text
    f = open("alphabet.txt", "a")
    sub_alpha = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]

    # Write all combinations of three four-bit strings to the file
    for i in range(16):
        for j in range(16):
            for k in range(16):
                next_letter = sub_alpha[i] + sub_alpha[j] + sub_alpha[k]

                # check if a 12 bit character is valid (ie, inside the walls of hex world), and if not, don't add it
                if check_validity(next_letter):
                    f.write(next_letter + "\n")
    
    f.close()

# MAIN
write_alphabet()