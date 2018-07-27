# HighZ-Calibrator
IMPORTANT NOTES:
1. Please do not edit or change the excel file named 1.xslx! This is used to generate a theoretical polynomial fit for the noise source, whose power values depend on our experiment. 
2. The program is not made as efficient as possible due to the lack of knowledge of numpy arrays (so basically all arrays were converted to lists)
3. Make sure there is no text file in the root directory already called "expData.txt".


USAGE:
1. To run the program, open up the calibratorUI.py file and edit the line near the top that says 'direc = "XXXXXXXXXXXXXXXXXXX"' and set the stuff in the "" equal to the path of the home directory that contains the data_70MHz and switch_data folders. Be sure to change all the '\' to '/' as python reads '\' as an escape sequence.
2. Next, run the python file, either through the terminal (or command prompt for windows users). Alternatively, using a built-in method such as the build (ctrl + B) that sublime text3 has works as well.
3. The program is designed to take in your data and spit out the calibrated data compiled into a single text file. Every value in each column is separated by commas and each new row corresponds to a new line. This can be easily plotted, since it is a single file that contains the calibrated data for the entire set of data fed in.
