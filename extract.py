from PIL import Image
from random import randrange
import numpy as np
import inject
import sys
def read_barcode(file_path):
    # Read in image and convert it to an array
    im = Image.open(file_path)
    barcode = np.array(im)
    values = []
    values1 = []
    values2 = []

    cur_index = [555,657]

    for i in range(cur_index[1], cur_index[1]+569):

        val_string = ''
        cur_index[0] = 555

        while cur_index[0] < 583:

            # Check pixel values to determine what binary representation they are
            if barcode[cur_index[1]][cur_index[0]] == 0:
                val_string+='1'

                # Since we have found a pixel, skip ahead 3 since each bit is represented in a 3 pixel x 3 pixel domain
                cur_index[0]+=3

            elif barcode[cur_index[1]][cur_index[0]] == 255:
                val_string+='0'

                # Since we have found a pixel, skip ahead 3 since each bit is represented in a 3 pixel x 3 pixel domain
                cur_index[0]+=3

            else:

                # We didn't find a matching binary representation (most likely an edge or noise), so just increment the loop as normal
                cur_index[0]+=1

        # If our value string was an actual binary representation (i.e. not a null character), add it to our values
        if val_string != '':
            values.append(val_string)

            # Since we found a row that had a binary representation, skip down 3 rows since each bit is represented in a 3 pixel x 3 pixel domain
            cur_index[1]+=3

        else:

            # We didn't find a valid binary string (i.e. a null character), so just increment the loop as normal
            cur_index[1]+=1

    cur_index = [555,657]

    for i in range(cur_index[1], cur_index[1]+569):
        val_string = ''
        cur_index[0] = 1004

        while cur_index[0] < 1032:
            # Check pixel values to determine what binary representation they are
            if barcode[cur_index[1]][cur_index[0]] == 0:
                val_string+='1'

                # Since we have found a pixel, skip ahead 3 since each bit is represented in a 3 pixel x 3 pixel domain
                cur_index[0]+=3

            elif barcode[cur_index[1]][cur_index[0]] == 255:
                val_string+='0'

                # Since we have found a pixel, skip ahead 3 since each bit is represented in a 3 pixel x 3 pixel domain
                cur_index[0]+=3

            else:

                # We didn't find a matching binary representation (most likely an edge or noise), so just increment the loop as normal
                cur_index[0]+=1

        # If our value string was an actual binary representation (i.e. not a null character), add it to our values
        if val_string != '':
            values1.append(val_string)

            # Since we found a row that had a binary representation, skip down 3 rows since each bit is represented in a 3 pixel x 3 pixel domain
            cur_index[1]+=3

        else:

            # We didn't find a valid binary string (i.e. a null character), so just increment the loop as normal
            cur_index[1]+=1

    cur_index = [555,657]

    for i in range(cur_index[1], cur_index[1]+562):

        val_string = ''
        cur_index[0] = 1453

        while cur_index[0] < 1481:

            # Check pixel values to determine what binary representation they are
            if barcode[cur_index[1]][cur_index[0]] == 0:
                val_string+='1'

                # Since we have found a pixel, skip ahead 3 since each bit is represented in a 3 pixel x 3 pixel domain
                cur_index[0]+=3

            elif barcode[cur_index[1]][cur_index[0]] == 255:
                val_string+='0'

                # Since we have found a pixel, skip ahead 3 since each bit is represented in a 3 pixel x 3 pixel domain
                cur_index[0]+=3

            else:

                # We didn't find a matching binary representation (most likely an edge or noise), so just increment the loop as normal
                cur_index[0]+=1

        # If our value string was an actual binary representation (i.e. not a null character), add it to our values
        if val_string != '':
            values2.append(val_string)

            # Since we found a row that had a binary representation, skip down 3 rows since each bit is represented in a 3 pixel x 3 pixel domain
            cur_index[1]+=3

        else:

            # We didn't find a valid binary string (i.e. a null character), so just increment the loop as normal
            cur_index[1]+=1


    # Code below taken from: https://www.kite.com/python/answers/how-to-convert-binary-to-string-in-python
    # and adapted to fit our use case
    ascii_string = ""
    a = [values,values1,values2]
    for component in a:
        for value in component:

            # Convert the value from base 2 to an integer
            ac = int(value, 2)

            # Convert the integer representation of a character to an actual character
            ac = chr(ac)

            # Revert '-' to spaces
            if ac == "-":
                ascii_string+=" "
            else:
                ascii_string+=ac



    return ascii_string
if __name__ == '__main__':
    # Enter the file location of injected image
    a = read_barcode(sys.argv[1])
    s = ""
    for i in a:
        if i.isdigit():
            s = s+i
        if i == " ":
            s = s + " "
        if i.isalpha():
            s = s + i + " "

    text_file = open(sys.argv[2], "w")
    n = text_file.write(s)
    text_file.close()
    print(s)
