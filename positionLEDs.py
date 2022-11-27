#!/usr/bin/env python
import os
import re

os.system('cp DFTBoard.kicad_pcb DFTBoard.kicad_pcb2')
f = open("DFTBoard.kicad_pcb2", "r")
flines = f.readlines()

trigString = [ \
#"\(fp_text reference D* \(at 0 0\) \(layer F\.SilkS\)", \
'(fp_text reference D', \
'(fp_text reference U',\
'(fp_text reference C',\
'(fp_text reference R',\
'(fp_text reference H']
targetOffset = [-2, -5, -5, -5, -5]
spacing    = [3.0   , 3.0*8, 3.0*4, 3.0*8, 3.0*8]
LEDSPERSIDE = 22*8

    
for j, line in enumerate(flines):
    for i, trigStr in enumerate(trigString):
        if trigStr in line:
            # find the designator number,
            # mulitply by spacing
            ChangePos = False
            
            desigLine = flines[j]
            print(desigLine)
            designator= desigLine.split()[2]
            desigNumber=  designator[1:]
            print(designator)
            print(desigNumber)
            desigLetter=  designator[:1]
            desigNumberInt = int(eval(desigNumber))
            
            # THE LEDS
            if desigLetter == "D":
                ChangePos = True   
                #print(eval(line.split()[2][1:]))
                ledno = int(eval(line.split()[2][1:]))
                if ledno <= LEDSPERSIDE:
                    xpos = ledno * spacing[i] - 111.6
                    ypos = 110
                    rot = 90
                else:
                    xpos = (ledno-LEDSPERSIDE) * spacing[i] - 111.6
                    ypos = 110
                    rot = 270
                    
                    
            elif desigLetter == "U":
                if desigNumberInt in range(11, 33):
                    ChangePos = True   
                    driverno = desigNumberInt-11
                    rot = 0
                    xpos = driverno * spacing[i] - 98.1
                    ypos = 104.3
                elif desigNumberInt in range(33,55):
                    ChangePos = True   
                    driverno = desigNumberInt-33
                    rot  = 0
                    xpos = driverno * spacing[i] - 98.1
                    ypos = 115.6
                elif desigNumberInt in range(56,62):
                    ChangePos = True   
                    driverno = desigNumberInt-56
                    rot  = 270
                    xpos = driverno * 3.0*8*3 -33.25
                    if desigNumberInt >= 59:
                        xpos = xpos + 3.0*8
                    ypos = 102.55
                elif desigNumberInt in range(62,68):
                    ChangePos = True   
                    driverno = desigNumberInt-62
                    rot  = 90
                    xpos = driverno * 3.0*8*3 -33.25
                    if desigNumberInt >= 65:
                        xpos = xpos + 3.0*8
                    ypos = 117.45


            elif desigLetter == 'R':
                rot = 0
                if desigNumberInt in range(29, 51):
                    ChangePos = True    
                    driverno = desigNumberInt-29
                    ypos = 102.5
                    xpos = driverno * spacing[i] - 93.9
                elif desigNumberInt in range(51,73):
                    ChangePos = True   
                    driverno = (desigNumberInt-51)
                    ypos = 117.5
                    xpos = driverno * spacing[i] - 93.9
                #else:
                #    ChangePos = True   
                #    driverno = desigNumberInt
                #    ypos = 80
                #    xpos = driverno * spacing[i] - 93.9

            elif desigLetter == 'C':
                driverno = (desigNumberInt-1)
                rot = 0
                if desigNumberInt in range(18, 62):
                    ChangePos = True   
                    driverno = desigNumberInt -18
                    ypos = 102.5
                    xpos = driverno * spacing[i] - 92
                    if desigNumberInt%2 != 0:
                        rot = 270
                        xpos = xpos-4
                elif desigNumberInt in range(62, 106):
                    ChangePos = True   
                    driverno = desigNumberInt - 62
                    ypos = 117.5
                    xpos = driverno * spacing[i] - 92
                    if desigNumberInt%2 != 0:
                        rot = 90
                        xpos = xpos-4  
                #else:
                #    ChangePos = True   
                #    driverno = desigNumberInt
                #    ypos = 80
                #    xpos = driverno * spacing[i] - 93.9
                
                
            elif desigLetter == 'H':
                rot = 0
                if desigNumberInt in range(1, 6):
                    ChangePos = True    
                    driverno = desigNumberInt-1
                    ypos = 102.5
                    xpos = driverno * spacing[i] + 105
                elif desigNumberInt in range(6,12):
                    ChangePos = True   
                    driverno = (desigNumberInt-6)
                    ypos = 117.5
                    xpos = driverno * spacing[i] + 105
                    
            print(j)
            if ChangePos:
                k = 0
                while not flines[j+k].strip().startswith("(at "):    
                    k-=1
                outStr = "(at %f %f %d)\n" % (xpos, ypos, rot)
                flines[j+k] = outStr
            

g = open("DFTBoard.kicad_pcb", "w+")
for line in flines:
    g.write(line)
g.close()
f.close()
