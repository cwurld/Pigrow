#!/usr/bin/python
import os
import sys

###  Requires MPV to be installed, use - sudo apt install mpv

#default user settings
time_skip = 1 #when making timelapse uses every Nth frame so 4 is 4x faster
darksize =75000   #all smaller files are removed assumed to be useless 75000 is a good value
outfps = 10       #10 is a good value, between 2 and 60 is acceptable
capsdir = "/home/pragmo/camcaps/"
listfile = "/home/pragmo/ffTL.txt"
outfile = "/home/pragmo/timelapse16.mkv" #directory to save output
file_type = "jpg"
outvidc = "libx264"
inpoint=0
outpoint=0 #use -10 to end at ten befor the end, 0 to show the whole thign and 10 to shopw only ten frames
#end of user settings

for argu in sys.argv:
    thearg = str(argu).split('=')[0]
    if  thearg == 'caps':
        capsdir = str(argu).split('=')[1]
    elif thearg == "of":
        outfile = str(argu).split('=')[1]
    elif thearg == "fps":
        outfps = str(argu).split('=')[1]
    elif thearg == "darksize" or thearg == 'ds':
        darksize = int(str(argu).split('=')[1])
    elif thearg == "ts" or thearg == 'timeskip':
        time_skip = int(str(argu).split('=')[1])
    elif thearg == "ft" or thearg == 'filetype':
        file_type = str(argu).split('=')[1]
    elif thearg == "ovc" or thearg == 'outvidc':
        outvidc = str(argu).split('=')[1]
    elif thearg == "inp" or thearg == 'inpoint':
        inpoint = int(str(argu).split('=')[1])
    elif thearg == "op" or thearg == 'outpoint':
        outpoint = int(str(argu).split('=')[1])

filelist = []
no_dark = []
faster = []
fcounter = 0

#grab all the files in /caps directory
if outpoint == 0:
    outpoint = len(os.listdir(capsdir))
for filefound in os.listdir(capsdir):
    if filefound.endswith(file_type):
        fcounter = fcounter + 1
        filelist.append(filefound)
print "Starting with; " + str(fcounter)
filelist.sort()
print "Filelist is now:" + str(len(filelist))
#make list ignoring the small image assuming they're the datk ones
for x in filelist[inpoint:outpoint]:
    statinfo = os.stat(capsdir + x)
    if statinfo.st_size >= darksize: #increase or decrese as needed, 75000 works well for most
        no_dark.append(x)
print("There are - " + str(len(no_dark)) + " entries in no_dark")
#make list every Nth file
for x in range(0, len(no_dark), time_skip):
    faster.append(no_dark[x])
#writes the file-list for mpv video encoder to use
os.chdir(capsdir)
ffTL = open(listfile, "w")
for x in faster: #can also be no_dark: or to include dark images change to filelist:
    ffTL.write(x + "\n")
ffTL.close()
print "we have " + str(len(faster)) + " files in the faster version..."
#runs the video encouder
print "making you a timelapse video..."
os.system("mpv mf://@"+listfile+" -mf-fps="+str(outfps)+" -o "+outfile) # --ovc "+outvidc+" --ovcopts=bitrate=1200:threads=2 --ovc 'gif' --ovcopts=bitrate=1200:threads=2 
if os.path.isfile(outfile) == True:
    print "there you go; "+outfile+" ready to roll.."
else:
    print "for some reason the file wasn't created, sorry..."
