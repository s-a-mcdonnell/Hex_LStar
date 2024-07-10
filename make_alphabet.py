def check_validity(input):

    # splice the twelve character string into three four character chunks
    info = input[0:4]
    x = int(input[4:8], 2)
    y = int(input[8:],2)

    # all 16 forms of input are valid

    # invalid if the second two coordinate 4-bit strings are outside of the walls
    # x needs to be... greater than zero, and less than 13
    if (x <= 0) or (x >= 13):
        return False
    
    # y needs to be... greater than 6 - i...
    # and less than 15 - i if x is odd, but less than 14 - i if x is even

    if x % 2 == 0:
        # if x is even, i = x - 2 / 2
        i = (x - 2) / 2
        if (y <= 6 - i) or (y >= 14 - i):
            return False
        
    # if x is odd...
    else:
        i = (x - 1)/2
        if (y <= 6 - i) or (y >= 15 - i):
            return False

    return True

def write_alphabet():
    # Writing to a text file according to this tutorial: https://www.w3schools.com/python/python_file_write.asp

    # Overwrite text in alphabet file with the empty string
    # TODO: Deal with case where file doesn't exist
    f = open("alphabet.txt", "w")
    f.write("")
    f.close()

    # Re-open file to append text
    f = open("alphabet.txt", "a")
    four_bits = ["0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111", "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"]

    # Write all combinations of three four-bit strings to the file
    for i in range(16):
        for j in range(16):
            for k in range(16):
                next_letter = four_bits[i] + four_bits[j] + four_bits[k]

                # check if a 12 bit character is valid (ie, inside the walls of hex world), and if not, don't add it
                if check_validity(next_letter):
                    f.write(next_letter + "\n")
    
    f.close()

write_alphabet()