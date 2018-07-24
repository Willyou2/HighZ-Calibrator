# HighZ-Calibrator
IMPORTANT NOTES:
1. Please do not edit or change the excel file named 1.xslx! This is used to generate a theoretical polynomial fit for the noise source, whose power values depend on our experiment. 


USAGE:
1. To run the program, open up the calibratorUI.py file and edit the line near the top that says 'direc = "XXXXXXXXXXXXXXXXXXX"' and set the stuff in the "" equal to the path of the home directory that contains the data_70MHz and switch_data folders. Be sure to change all the '\' to '/' as python reads '\' as an escape sequence.
2. Next, run the python file, either through the terminal (or command prompt for windows users). Alternatively, using a built-in method such as the build (ctrl + B) that sublime text3 has works as well.