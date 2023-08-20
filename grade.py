#Import the Image and ImageFilter classes from PIL (Pillow)
from PIL import Image
from PIL import ImageFilter
import sys
import random
import numpy as np



im = Image.open(sys.argv[1])

output_file = sys.argv[2]

# Dimensions of the image
print("Image is %s pixels wide." % im.width)
print("Image is %s pixels high." % im.height)
print("Image mode is %s." % im.mode)

# Here I've used Sobel filters for vertical and horizontal to perform the edge detection

# vertical filter
filter_v = [[-1,-2,-1], [0,0,0], [1,2,1]]

#horizontal filter
filter_h = [[-1,0,1], [-2,0,2], [-1,0,1]]

# Converting the input image to grayscale value
gray_im = im.convert("L")

# Create a new blank color image the same size as the input
color_im = Image.new("RGB", (im.width, im.height), color=0)

# A copy of the original image is taken to change to values that will given after edge detection
edges_img = np.array(gray_im.copy())

image_array = np.array(gray_im)

# Two dictionaries are initialized to get the x and y line coordinates along with edge strength
dict_y = {}

dict_x = {}

# Performing edge detection
for x in range(3, im.height-2):
    
    x_sum = 0
    
    for y in range(3,im.width-2):

        # Patch from the image is parsed for applying filter
        parse_win = image_array[x-1:x+2, y-1:y+2]
        
        # Vertical filter applied
        trans_v = filter_v*parse_win

        value_v = trans_v.sum()/4
        
        # Horizontal filter applied
        trans_h = filter_h*parse_win

        value_h = trans_h.sum()/4

        edge_value = np.sqrt(value_v**2 + value_h**2)
        
        # The edge values are calculated and stored
        edges_img[x, y] = edge_value*10
        
        x_sum += edge_value*10

        # The y line coordinte along with the pixel strength is captured
        if y in dict_y.keys():

            dict_y[y] += edge_value*10

        else:

            dict_y[y] = edge_value*10
            
    # The x line coordinate along with the pixel strength is captured
    dict_x[x] = x_sum



# Function to find the vertical lines in the image for the answer boxes

def find_lines(item, num, dist):
    
    count = 0
    
    axis_list = [sys.maxsize]
    
    # Looping through the line coordinates
    for axis in item.keys():
        
        inner_count = 0
        
        for each_axis in axis_list:
            
            # Keeping a check on the distance between each vertical line 
            if(abs(each_axis - axis) < dist):
                
                inner_count += 1

                break

        # If the distance between 2 lines satisfies then append it to the final list
        if(inner_count == 0):
            
            axis_list.append(axis)

            count+=1

        # Check to find the relevant number of vertical lines for the image answer boxes
        if count>100 or len(axis_list) == num:
        
            break
    
    return axis_list[1:]


# Function to find the horizontal lines in the image for the answer boxes

def x_lines_func(x_line,dist_1,dist_2,y_line):
    
    y_line.sort()
    
    x_line.sort()
    
    final = []
    
    # Looping through each horizontal line
    for each_index_1 in range(0,len(x_line)):
        
        if(x_line[each_index_1] > 560):
            
            # Check to find if it contains the number before to assume as a answer box
            
            x = edges_img[x_line[each_index_1]+6:x_line[each_index_1]+29,y_line[0]-50:y_line[0]].sum()
                        
            if(x > 20000):
            
                final.append(x_line[each_index_1])

                index = each_index_1

                break
                
    # Check if the lines are separated with a threshold distance
    
    for each_index in range(index+1,len(x_line)):
        
        # Lines for the answer box
        
        if(len(final)%2 !=0 ):

            if(abs(x_line[each_index] - final[-1]) > dist_1):

                final.append(x_line[each_index])

        # Lines for the distance beteween the answer box
        else:

            if(abs(x_line[each_index] - final[-1]) > dist_2):

                final.append(x_line[each_index])
                
    return final


# Sort the vertical and horizontal lines based on the edge strength 

y_axis = dict(sorted(dict_y.items(), key=lambda x:x[1], reverse = True))
x_axis = dict(sorted(dict_x.items(), key=lambda x:x[1], reverse = True))


# To find all the correct vertical lines

y_line = find_lines(y_axis,31,25)

# To find all the correct horizontal lines

x_all = find_lines(x_axis,200,12)
x_line = x_lines_func(x_all,25,10,y_line)


pil_image=Image.fromarray(edges_img)
       
#pil_image.save("result.png")


x_value = []
y_value = []

# Plot the vertical and horizontal lines that are captured onto to edge detected image

for x in range(pil_image.width):
    for y in range(pil_image.height):
        p = pil_image.getpixel((x,y))
        # Range is provided to get only the Answer box lines
        if (x in y_line or y in x_line) and (560 < y < 2090) :
            (R,G,B) = (255,255,0)
            color_im.putpixel((x,y), (R,G,B))
        else:
            color_im.putpixel((x,y), (p,p,p))


# Show the image with the lines
color_im.show()
color_im.save("result.png")


# Function to couple the intersecting coordinates of the horizontal and vertical line

indexes = []

x_line.sort()
y_line.sort()

for i in x_line:
    
    for j in y_line:
        
        # Threshold to only capture the Answer boxes
        if(i > 560):
        
            indexes.append((i,j))


# Function to extract the correct answers from the answer boxes.

answer_strength = []

sub_list = []

count = 1

count_index = 0

# Loop through the intersecting coordinates to find the answer boxes

for i in range(0,len(indexes),2):
    
    if(i%30 == 0):
        
        count_index+=1
    
    if(count_index%2!=0):
        
        # Check to see if any student has written the answer 
        # to the left of the question by calculaing pixel strength within a frame
        
        if(count == 1):
            
            cor_ans = (image_array[indexes[i][0]+6:indexes[i][0]+29,indexes[i][1]-110:indexes[i][1]-50] < 100).sum()
        
        # Calculate the pixel strength of eacjh of the options
        
        sub_array = image_array[indexes[i][0]:indexes[i][0]+37,indexes[i][1]:indexes[i][1]+35]
        sub_list.append((sub_array > 200).sum())
        
        # See the 5 options and add to the list 
        
        if(count == 5):
            
            if(cor_ans > 50):
            
                answer_strength.append((sub_list,True))
            else:
                answer_strength.append((sub_list,False))
            count = 0
            sub_list = []

        count+=1


# Dictionary to store answer for each question
answers = {}

# All the answer options
ans = ['A','B','C','D','E']

# The column starting numbers
column = [1,30,59]

ques = 1
part = 0

for i in answer_strength[:-3]:
    
    # Zip the Answer option and its pixel strength
    sol = list(zip(ans,i[0]))
    
    m = max(i[0])
    
    answers[column[part]] = []
    
    # Identify the correct answer using a threshold
    
    for j in sol:
        if abs(j[1] - m) > 150:
            answers[column[part]].append(j[0])
            
    # If True then append x
    
    if i[1]:
        answers[column[part]].append("x")
        
    column[part] = column[part]+1
            
    if(part == 2):
        part = 0
    else:
        part += 1

# Pop the last blank boxes

if(86 in answers.keys()):
    answers.pop(86)
if(87 in answers.keys()):
    answers.pop(87)  
if(88 in answers.keys()):
    answers.pop(88)

output = dict(sorted(answers.items(), key=lambda x:x[0]))  


# Writing question and the answers to the output file. 

with open(output_file, 'w') as f: 
    for key, value in output.items(): 
        if("x" in value):
            value = value[:-1]
            anss = ''.join(value)
            f.write('%s %s x\n' % (key,anss))
        else:
            anss = ''.join(value)
            f.write('%s %s\n' % (key,anss))
