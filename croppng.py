#! /Users/Cooper/Work/python-env/lershare-env/bin/python
import os,Image,sys
import json
from biplist import *

'''
    How to use this:
    1. open all png file , export it to PNG file with alpha option
    2. use this to crop png files.
'''

PLUTIL = '/usr/bin/plutil'
TEXTUREPACKER = '/usr/local/bin/TexturePacker'

filenames=os.listdir(os.getcwd())
for filename in filenames:
    if (filename.rfind(".plist") < 0):
        continue

    try:
        PListFile = filename
        pngFile = filename.replace(".plist", ".png")
        if (not os.path.exists(pngFile)):
        	continue
        	
        imageFolder = 'temp/' + filename.replace(".plist", "")
        jsonFile = filename.replace(".plist", ".json")
        
        #convert png to readable PNG file
        os.system('$for i in *.png; do sips -s format png $i --out ./$i; done')
        os.system('%s -convert json %s -o %s' % ( PLUTIL, PListFile, jsonFile ) )
        #os.system('%s --quiet --disable-rotation --max-width 4096 --max-height 4096 --no-trim --padding 0 --shape-padding 0 --border-padding 0 --inner-padding 0 %s --sheet %s --data /dev/null' % (TEXTUREPACKER, CCZFile, pngFile) )
        
        jsonH = file(jsonFile)
        metadata = json.load(jsonH)

        try:
            image=Image.open(pngFile)  #open image
        except e:
            print e
            continue
        
        if os.path.isdir(imageFolder):
            os.system('rm -rf %s' %(imageFolder))
        
        os.makedirs(imageFolder)

        for item in metadata['frames']:
            print 'from ' ,pngFile, ' load ', item
            frame = metadata['frames'][item]['frame']
            rotate = metadata['frames'][item]['rotated']
            rectlist = frame.replace('{','').replace('}','').split(',')
            x = int(rectlist[0])
            y = int(rectlist[1])
            #width = int(rectlist[2])
            width = int( rectlist[3] if rotate else rectlist[2] )
            #height = int(rectlist[3])
            height = int( rectlist[2] if rotate else rectlist[3] )
            box = (x, y, x+width, y+height)
            print box
            img = image.crop(box)
            outfile=imageFolder + '/' + item
            print "Write Image to file :", outfile, box
            img.save(outfile)

        os.system('rm -f %s' %(jsonFile) )
        #os.system('rm -f %s' %(pngFile) )
						
        continue


        print "totally export %d" %(iFileCount)

    except InvalidPlistException, e:
        print "Not a Plist or Plist Invalid:", e


