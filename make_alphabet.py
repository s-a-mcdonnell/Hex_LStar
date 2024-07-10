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

                f.write(next_letter + "\n")
    
    f.close()

write_alphabet()