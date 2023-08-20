# Image Processing and Recognition 

## Task 1: Extracting the Answers that Students have marked in Answer Sheet

This part was completely designed and implemented by Kowshik Selvam.

### Part 1 : Brainstorming

When I read the question for the task to extract the answers that the students have marked in the answer sheet, I straight away started thinking of various techniques using which I could find the boundaries of the Answer options (A, B, C, D, E) for each question. Since all the answer option in the answer sheet should follow a straight line, as in all the starting and ending line of the answer option box should fall in a straight line, I first thought of ways to get the straight lines along the boxes. Then once I get all the straight lines, I thought of extracting the correct option marked from the boxes which are covered by the lines. 

### Idea 1:

The first idea that I implemented for Hough Transform. I did non maximum suppression to makes sure it forms only one line instead of various lines coupling together at a single point ( in our case the horizontal and vertical line of the box. Then I implemented Hough transform from scratch and first it took 19 min to give few lines along the answer options. It gave somewhat good result but it took a lot of time. So I tried optimizing the code to check for lines in only desired places and then I managed to get lines along horizontally and vertically in 7 min but the result was not quite good as there were many overlapping lines and I was not able to get any useful insights from the lines to further develop on it. I performed various pre processing on the image to get the lines by performing hough transform but I was able to get the desired output.

### Idea 2:

Since I believed obtaining lines was one of the easiest and computationally faster way to extract the answers marked by students, I started to brainstorm on various possibilities to get the lines around the boxes. I assumed since this answer sheet would be distributed among the students for them to mark, the lines of the boxes should almost follow 90 degrees (not perfect 90 but almost a 90), I thought of calculating the edge strength along the horizontal axis and vertical axis to get the boundary of the boxes.

### Development on Idea 2:

First I did edge detection on the image to get brighter box boundaries. I used sobel filter to perform the edge detection and multiplied the edge value by 10. Then I calculated the pixel value along every row and column. Since we assumed the answer boxes to follow almost a straight + or - 90 degree scale, obviously we can say that the rows and columns having the answer box pixels will be the highest because we performed edge detection to detect the edges which makes it brighter. Then I sorted the horizontal and vertical lines with the highest pixel sum value in decreasing. From this by neglecting close lines I formed all the vertical lines around the box lines as we know the lines along the box lines will be having the highest pixel sum value. Now taking these vertical lines as reference I found the rest of the horizontal lines around the boxes.


![Answer box frame length](/report-images/frame.png)

As seen from the above image I approximated the dimension of the answer box to plot the lines. Now after finding the horizontal and vertical lines for the image that represents the boundary of the boxes, I couple the horizontal and vertical lines to found the coordinates of the intersection points and plotted to lines to check if it is along the boundary of the answer boxes.

This below image with the line boundaries will be shown while running the program.

![Answer box frame length](/report-images/result.png)

From the above image we can see the lines formed by the predicted lines. Since it’s along the boundary of the boxes now we can loop through each intersecting coordinates to find the frame which we need to parse to get the answer.

Now in the original image these coordinate points of the boxes are used to get the answer box frame and a threshold is given to count the pixel sum lesser than some range. This way I predicted the correct answer from the boxes. Same way to obtain anything that is written by the student near to the question number a separate frame is used along a threshold value and if the sum of pixel value is below a range in the frame then it is considered to be “x” in the output file.

As a result the extracted answers are appended in a text file along with the question number and “x” if some other answer is marked by the student near the question number.

 
### Shortcomings

Though the above logic works most of the times correctly on images with answer boxes, if the boxes are very much slanting, that is if the pixel doesn’t follow almost 90 degrees for the lines along the boxes then the logic may not work that properly but still it should do some descent job. I carried out this particular logical implementation just because just type of answer sheet will always follow a straight line.

The outputs are accurate to all the files except for the a-27.png file as the thresholds needs to be modified to make it more accurate to work with a-27.png which can be done by pixel level calculation to make it robust across all the images.
