# Author: Christoph Häußer <christoph.haeusser@gmail.com>

"""
Readme, Changelog:
20260605, 17:26 h: Changed bb size on 5. Jun 2026, 17:23 h to 10 mm
"""

"""
@article{Kerns2023, doi = {10.21105/joss.06001}, url = {https://doi.org/10.21105/joss.06001},
year = {2023}, publisher = {The Open Journal}, volume = {8}, number = {92}, pages = {6001},
author = {James R. Kerns}, title = {Pylinac: Image analysis for routine quality assurance in radiotherapy},
journal = {Journal of Open Source Software} }
"""

"""The Winston-Lutz module loads and processes EPID images that have acquired Winston-Lutz type images.

Features:

* **Couch shift instructions** - After running a WL test, get immediate feedback on how to shift the couch.
  Couch values can also be passed in and the new couch values will be presented so you don't have to do that pesky conversion.
  "Do I subtract that number or add it?"
* **Automatic field & BB positioning** - When an image or directory is loaded, the field CAX and the BB
  are automatically found, along with the vector and scalar distance between them.
* **Isocenter size determination** - Using backprojections of the EPID images, the 3D gantry isocenter size
  and position can be determined *independent of the BB position*. Additionally, the 2D planar isocenter size
  of the collimator and couch can also be determined.
* **Image plotting** - WL images can be plotted separately or together, each of which shows the field CAX, BB and
  scalar distance from BB to CAX.
* **Axis deviation plots** - Plot the variation of the gantry, collimator, couch, and EPID in each plane
  as well as RMS variation.
* **File name interpretation** - Rename DICOM filenames to include axis information for linacs that don't include
  such information in the DICOM tags. E.g. "myWL_gantry45_coll0_couch315.dcm".
"""


import os
from tkinter import filedialog
from tkinter.constants import TRUE

from pydicom import dcmread
from pylinac import WinstonLutz, image

#######################################################################################################################################

# Data input

print("")
print("Changelog: 5. Jun 2026, 17:25 h: changed bb size from 5 to 10 mm")
print("")
print("Warning! Make sure that the field is about the center of the imager!")
print("")

print("Please enter notes, if you like. Max 10 charactersp: ")
notes = input()
notes_str = str(notes)

#######################################################################################################################################
folder_tkinter_in = filedialog.askdirectory(
    initialdir="/home/christoph/data_medphy/input"
)
print("")
print(folder_tkinter_in)
print("")
#######################################################################################################################################
# counting files

"""
https://pynative.com/python-count-number-of-files-in-a-directory/

The scandir() function of an os module returns an iterator of os.DirEntry objects corresponding to the entries in the directory.

Use the os.scandir() function to get the names of both directories and files present in a given directory.
Next, iterate the result returned by the scandir() function using a for loop
Next, In each iteration of a loop, use the isfile() function to check if it is a file or directory. if yes increment the counter by 1
Note: If you need file attribute information along with the count, using the scandir() instead of listdir() can significantly
increase code performance because os.DirEntry objects expose this information if the operating system provides it when scanning a directory.

"""
count = 0

for file_path in os.scandir(folder_tkinter_in):
    if file_path.is_file():
        count += 1

print("file count:", count)
print("")

#######################################################################################################################################

# list file names in an array variable

file_names = []  # array variable

# Iterate directory
for file_path in os.listdir(folder_tkinter_in):
    # check if current file_path is a file
    if os.path.isfile(os.path.join(folder_tkinter_in, file_path)):
        # add filename to list
        file_names.append(file_path)

#######################################################################################################################################

# Get data from a single DICOM File
path_to_image_1 = folder_tkinter_in + "/" + file_names[0]
iviewData = dcmread(path_to_image_1)
# print(iviewData)

PatientID = str(iviewData[0x0010, 0x0020].value)
Linac_str = PatientID

StationName = str(iviewData[0x0008, 0x1010].value)
print(StationName)
print("")

Date_imaging_str = str(iviewData[0x0008, 0x0023].value)
Time_imaging_str_init = str(iviewData[0x0008, 0x0033].value)
Time_imaging_str = Time_imaging_str_init
Modality = str(iviewData[0x0008, 0x0060].value)
Manufacturer = str(iviewData[0x0008, 0x0070].value)
RT_Image_Label = str(iviewData[0x3002, 0x0002].value)
Study_ID = str(iviewData[0x0020, 0x0010].value)

print(
    "Linac Name: "
    + Linac_str
    + ", "
    + "Date of imaging: "
    + Date_imaging_str
    + ", "
    + "Time of imaging: "
    + Time_imaging_str
)
print("")
#######################################################################################################################################
# print file names and their metadata
# and plot images

for x in range(count):
    path_to_file_x = folder_tkinter_in + "/" + file_names[x]
    image_data = dcmread(path_to_file_x)
    gantryAngleInit = image_data[0x300A, 0x011E].value
    gantryAngleTrunc = "%.1f" % gantryAngleInit
    gantryAngle = str(gantryAngleTrunc)
    colliAngleInit = image_data[0x300A, 0x0120].value
    colliAnlgeTrunc = "%.1f" % colliAngleInit
    colliAngle = str(colliAnlgeTrunc)
    couchAngleInit = image_data[0x300A, 0x0122].value
    couchAnlgeTrunc = "%.1f" % couchAngleInit
    couchAngle = str(couchAnlgeTrunc)
    rtImageLabel = str(image_data[0x3002, 0x0002].value)
    print(
        file_names[x]
        + "\t"
        + " Gantry Angle: "
        + gantryAngle
        + "\t"
        + " Colli Angle: "
        + colliAngle
        + "\t"
        + " Couch Angle: "
        + couchAngle
        + "\t"
        + " RTImageLabel: "
        + rtImageLabel
    )

# Program code

# wl = WinstonLutz(folder_tkinter_in, axis_mapping=mapping, sid=1000)
wl = WinstonLutz(folder_tkinter_in, sid=1000)

wl.analyze(bb_size_mm=10)

#######################################################################################################################################

# Data output

# folder_tkinter_out = filedialog.askdirectory(initialdir="/home/christoph/Dropbox/Tech_IT_Medphy_Coding_Skripte/Databases/Linacs_AK_St_Georg/Reports_Linacs_AK_St_Georg")

# folder_tkinter_out_file = folder_tkinter_out+"/"+Linac_str+"_"+Study_ID+".pdf"
# folder_tkinter_out_file = "/home/christoph/Dropbox/Tech_IT_Medphy_Coding_Skripte/Databases/Linacs_AK_St_Georg/Reports_Linacs_AK_St_Georg"+"/"+Linac_str+"_"+Study_ID+"_"+Date_imaging_str+"_"+Time_imaging_str+".pdf"

folder_out = filedialog.askdirectory(
    initialdir="/home/christoph/data_medphy/output_asklepios"
)

folder_tkinter_out_file = (
    folder_out
    + "/"
    # + Linac_str
    # + "_sn_"
    + StationName
    + "_WL_"
    + Date_imaging_str
    + "_"
    + Time_imaging_str
    + ".pdf"
)

wl.publish_pdf(
    folder_tkinter_out_file,
    open_file=TRUE,
    metadata={
        "Patient": Linac_str,
        "stn": StationName,
        "Image Type": Modality,
        # "Mfct": Manufacturer,
        "Date of Imaging": Date_imaging_str,
        "Time of Imaging": Time_imaging_str,
        "Notes": notes_str,
    },
)
