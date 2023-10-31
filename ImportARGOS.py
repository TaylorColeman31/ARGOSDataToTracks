##---------------------------------------------------------------------
## ImportARGOS.py
##
## Description: Read in ARGOS formatted tracking data and create a line
##    feature class from the [filtered] tracking points
##
## Usage: ImportArgos <ARGOS folder> <Output feature class> 
##
## Created: Fall 2023
## Author: John.Fay@duke.edu (for ENV859)
##---------------------------------------------------------------------

# Import modules
import sys, os, arcpy

#Allowing output to be overwritten
arcpy.env.overwriteOutput = True

# Set input variables (Hard-wired)
inputFile = 'V:/ARGOSTracking/Data/ARGOSData/1997dg.txt'
outputFC = "V:/ARGOSTracking/Scratch/ARGOStrack.shp"
outputSR = arcpy.SpatialReference(54002)

## Prepare a new feature class to which we'll add tracking points
# Create an empty feature class; requires the path and name as separate parameters
outPath,outName = os.path.split(outputFC) #Splits outputFC into 2 items (path and file)
arcpy.CreateFeatureclass_management(outPath, outName, "POINT","","","", outputSR)

# Add TagID, LC, and Date fields to the output feature class
arcpy.AddField_management(outputFC,"TagID","LONG")
arcpy.AddField_management(outputFC,"LC","TEXT")
arcpy.AddField_management(outputFC,"Date","DATE")

# Construct a while loop and iterate through all lines in the data file
# Open the ARGOS data file
inputFileObj = open(inputFile,'r')

# Get the first line of data, so we can use the while loop
lineString = inputFileObj.readline()

# Start the while loop
while lineString:
    
    # Set code to run only if the line contains the string "Date: "
    if ("Date :" in lineString):
        
        # Parse the line into a list
        lineData = lineString.split()
        
        # Extract attributes from the datum header line
        tagID = lineData[0]
        
        # Extract location info from the next line
        line2String = inputFileObj.readline()
        
        # Parse the line into a list
        line2Data = line2String.split()
        
        # Extract the date we need to variables
        obsLat = line2Data[2]
        obsLon= line2Data[5]
                    
        # Extract the date, time, and LC values
        obsDate = lineData[3]
        obsTime = lineData[4]
        obsLC   = lineData[7]
        
        #Try to convert coordinates to numbers
        try:

            # Print results to see how we're doing
            print (tagID,"Lat:"+obsLat,"Long:"+obsLon, obsLC, obsDate, obsTime)

            # Convert raw coordinate strings to numbers
            if obsLat[-1] == 'N': #If last character ends in 'N',
                obsLat = float(obsLat[:-1])
            else:
                obsLat = float(obsLat[:-1]) * -1 #Use this to convert S coords to negative values!
            if obsLon[-1] == 'E':
                obsLon = float(obsLon[:-1])
            else:
                obsLon = float(obsLon[:-1]) * -1 #Doing the same thing with W coords (-)

            # Construct a point object from the feature class
            obsPoint = arcpy.Point()
            obsPoint.X = obsLon
            obsPoint.Y = obsLat
        
        #Handle any error
        except Exception as e:
            print(f"Error adding record {tagID} to the output: {e}")

        
    # Move to the next line so the while loop progresses
    lineString = inputFileObj.readline()
    
#Close the file object
inputFileObj.close()