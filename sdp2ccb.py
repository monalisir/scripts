#! /Users/Cooper/Work/python-env/lershare-env/bin/python
# -*- coding: UTF-8 -*-
import os,Image,sys
import json
import plistlib
from biplist import *
from xml.etree import ElementTree

'''
    How to use this:
    1. open all png file , export it to PNG file with alpha option
    2. use this to crop png files.
'''

DEF_ROTATION_TYPE = 2
DEF_POSITION_TYPE = 3
DEF_SCALE_TYPE = 4
DEF_OPACITY_TYPE = 5
DEF_COLOR_TYPE = 6
DEF_SPRITFRAME_TYPE = 7
DEF_SKEW_TYPE = 8

kCCBKeyframeEasingInstant = 0
kCCBKeyframeEasingLinear = 1
kCCBKeyframeEasingCubicIn = 2
kCCBKeyframeEasingCubicOut = 3
kCCBKeyframeEasingCubicInOut = 4
kCCBKeyframeEasingElasticIn = 5
kCCBKeyframeEasingElasticOut = 6
kCCBKeyframeEasingElasticInOut = 7
kCCBKeyframeEasingBounceIn = 8
kCCBKeyframeEasingBounceOut = 9
kCCBKeyframeEasingBounceInOut = 10
kCCBKeyframeEasingBackIn = 11
kCCBKeyframeEasingBackOut = 12
kCCBKeyframeEasingBackInOut = 13


def convertSDP2CCB(data, totalframes, rate, ccbfile):
    children = []

    timesec = float(1.0 / rate)

    for item in data:
        timeline = {}
        timeline['color'] = {}
        timeline['color']['name'] = 'color'
        timeline['color']['type'] = DEF_COLOR_TYPE

        timeline['opacity'] = {}
        timeline['opacity']['name'] = 'opacity'
        timeline['opacity']['type'] = DEF_OPACITY_TYPE

        timeline['position'] = {}
        timeline['position']['name'] = 'position'
        timeline['position']['type'] = DEF_POSITION_TYPE

        timeline['rotation'] = {}
        timeline['rotation']['name'] = 'rotation'
        timeline['rotation']['type'] = DEF_ROTATION_TYPE

        timeline['skew'] = {}
        timeline['skew']['name'] = 'skew'
        timeline['skew']['type'] = DEF_SKEW_TYPE

        timeline['scale'] = {}
        timeline['scale']['name'] = 'scale'
        timeline['scale']['type'] = DEF_SCALE_TYPE

        timeline['displayFrame'] = {}
        timeline['displayFrame']['name'] = 'displayFrame'
        timeline['displayFrame']['type'] = DEF_SPRITFRAME_TYPE

        timeline['color']['keyframes'] = []
        timeline['opacity']['keyframes'] = []
        timeline['position']['keyframes'] = []
        timeline['rotation']['keyframes'] = []
        timeline['skew']['keyframes'] = []
        timeline['scale']['keyframes'] = []

        color = {}
        opacity = {}
        position = {}
        rotation = {}
        skew = {}
        scale = {}
        spriteFrames = {}

        color['keyframes'] = []
        opacity['keyframes'] = []
        position['keyframes'] = []
        rotation['keyframes'] = []
        skew['keyframes'] = []
        scale['keyframes'] = []
        spriteFrames['keyframes'] = []

        for frame in item['frames'] :
            #color property
            time = frame['index'] * timesec

            cProperty = {}
            cProperty['easing'] = {}
            cProperty['easing']['type'] = kCCBKeyframeEasingLinear
            cProperty['name'] = 'color'
            cProperty['time'] = time
            cProperty['type'] = DEF_COLOR_TYPE
            cProperty['value'] = frame['color']
            if (not color['keyframes']) or color['keyframes'][-1]['value'] != frame['color'] :
                color['keyframes'].append(cProperty)

            #opacity property
            oProperty = {}
            oProperty['easing'] = {}
            oProperty['easing']['type'] = kCCBKeyframeEasingLinear
            oProperty['name'] = 'opacity'
            oProperty['time'] = time
            oProperty['type'] = DEF_OPACITY_TYPE
            oProperty['value'] = frame['opacity']
            if ( not opacity['keyframes'] ) or opacity['keyframes'][-1]['value'] != frame['opacity'] :
                opacity['keyframes'].append(oProperty)

            #position property
            p = {}
            p['easing'] = {}
            p['easing']['type'] = kCCBKeyframeEasingLinear
            p['name'] = 'position'
            p['time'] = time
            p['type'] = DEF_POSITION_TYPE
            p['value'] = frame['position']
            if (not position['keyframes']) or (position['keyframes'][-1]['value'] != p['value']) :
                position['keyframes'].append(p)

            #rotation property
            #if ( last['rotation'] != frame['rotation'] ) or ( next['rotation'] != frame['rotation'] ) or i == 0 :
            r = {}
            r['easing'] = {}
            r['easing']['type'] = kCCBKeyframeEasingLinear
            r['name'] = 'rotation'
            r['time'] = time
            r['type'] = DEF_ROTATION_TYPE
            r['value'] = frame['rotation']
            if ( not rotation['keyframes'] ) or (rotation['keyframes'][-1]['value'] != frame['rotation']) :
                rotation['keyframes'].append(r)

            #skew property
            s = {}
            s['easing'] = {}
            s['easing']['type'] = kCCBKeyframeEasingLinear
            s['name'] = 'skew'
            s['time'] = time
            s['type'] = DEF_SKEW_TYPE
            s['value'] = frame['skew']
            if ( not skew['keyframes'] ) or (skew['keyframes'][-1]['value'] != frame['skew']) :
                skew['keyframes'].append(s)

            #scale property
            l = {}
            l['easing'] = {}
            l['easing']['type'] = kCCBKeyframeEasingLinear
            l['name'] = 'scale'
            l['time'] = time
            l['type'] = DEF_SCALE_TYPE
            l['value'] = frame['scale']
            if (not scale['keyframes']) or (scale['keyframes'][-1]['value'] != frame['scale']) :
                scale['keyframes'].append(l)

            if frame.has_key('spriteFrame') :
                df = {}
                df['easing'] = {}
                df['easing']['type'] = kCCBKeyframeEasingInstant
                df['name'] = 'displayFrame'
                df['time'] = float(time)
                df['type'] = DEF_SPRITFRAME_TYPE
                sframe = frame['spriteFrame']
                if sframe.find('/') != -1:
                    fileList = sframe.split('/')
                    df['value'] = (fileList[0], fileList[1])
                else:
                    df['value'] = ("", sframe)
                if (not spriteFrames['keyframes']) or (spriteFrames['keyframes'][-1]['value'] != df['value']) :
                    spriteFrames['keyframes'].append(df)

        if len(color['keyframes']) > 1 :
            timeline['color']['keyframes'] = color['keyframes']
        else :
            del timeline['color']

        if len(opacity['keyframes']) > 1 :
            timeline['opacity']['keyframes'] = opacity['keyframes']
        else :
            del timeline['opacity']

        if len(position['keyframes']) > 1 :
            timeline['position']['keyframes'] = position['keyframes']
        else :
            del timeline['position']

        if len(rotation['keyframes']) > 1 :
            timeline['rotation']['keyframes'] = rotation['keyframes']
        else :
            del timeline['rotation']

        if len(skew['keyframes']) > 1 :  
            timeline['skew']['keyframes'] = skew['keyframes']
        else :
            del timeline['skew']

        if len(scale['keyframes']) > 1 :
            timeline['scale']['keyframes'] = scale['keyframes']
        else :
            del timeline['scale']

        if ( len(spriteFrames['keyframes']) > 1 ):
            timeline['displayFrame']['keyframes'] = spriteFrames['keyframes']
        else :
            del timeline['displayFrame']

        animatedProperties = {}
        animatedProperties['0'] = timeline
        
        spriteNode = {}
        spriteNode['animatedProperties'] = animatedProperties
        spriteNode['baseClass'] = 'CCSprite'
        spriteNode['children'] = []
        spriteNode['customClass'] = ""
        spriteNode['displayName'] = item['displayName']
        spriteNode['memberVarAssignmentName'] = ""
        spriteNode['memberVarAssignmentType'] = 0
        spriteNode['selected'] = False
        spriteNode['seqExpanded'] = True

        spriteNode['properties'] = []

        #position
        positionSetter = {}
        #positionSetter['baseValue'] = (50, 50)
        positionSetter['name'] = 'position'
        positionSetter['type'] = 'Position'
        _list = list(position['keyframes'][0]['value'])
        _list.append(0)
        a = tuple(_list)
        positionSetter['value'] = a
        spriteNode['properties'].append(positionSetter)

        #anchor point
        anchorPointerSetter = {}
        anchorPointerSetter['name'] = 'anchorPoint'
        anchorPointerSetter['type'] = 'Point'
        anchorPointerSetter['value'] = item['anchor']
        spriteNode['properties'].append(anchorPointerSetter)

        #scale
        scaleSetter = {}
        #scaleSetter['baseValue'] = (1, 1)
        scaleSetter['name'] = 'scale'
        scaleSetter['type'] = 'ScaleLock'
        _list = list(scale['keyframes'][0]['value'])
        _list.append(True)
        _list.append(0)
        a = tuple(_list)
        scaleSetter['value'] = a
        spriteNode['properties'].append(scaleSetter)

        #rotation
        rotationSetter = {}
        #rotationSetter['baseValue'] = 0.0
        rotationSetter['name'] = 'rotation'
        rotationSetter['type'] = 'Degrees'
        rotationSetter['value'] = rotation['keyframes'][0]['value']
        spriteNode['properties'].append(rotationSetter)

        #skew
        skewSetter = {}
        skewSetter['name'] = 'skew'
        skewSetter['type'] = 'FloatXY'
        skewSetter['value'] = skew['keyframes'][0]['value']
        spriteNode['properties'].append(skewSetter)

        #igore anchor point for position
        igoreAPSetter = {}
        igoreAPSetter['name'] = 'ignoreAnchorPointForPosition'
        igoreAPSetter['type'] = 'Check'
        igoreAPSetter['value'] = False
        spriteNode['properties'].append(igoreAPSetter)

        #sprite frame
        if item.has_key('spriteFrame') :
            sfSetter = {}
            sfSetter['name'] = 'displayFrame'
            sfSetter['type'] = 'SpriteFrame'
            sframe = item['spriteFrame']
            if sframe.find('/') != -1:
                fileList = sframe.split('/')
                sfSetter['value'] = (fileList[0], fileList[1])
            else:
                sfSetter['value'] = ("", sframe)
            spriteNode['properties'].append(sfSetter)

        #opcity
        opcitySetter = {}
        opcitySetter['name'] = 'opacity'
        opcitySetter['type'] = 'Byte'
        opcitySetter['value'] = opacity['keyframes'][0]['value']
        spriteNode['properties'].append(opcitySetter)

        #color
        colorSetter = {}
        colorSetter['name'] = 'color'
        colorSetter['type'] = 'Color3'
        colorSetter['value'] = color['keyframes'][0]['value']
        spriteNode['properties'].append(colorSetter)

        children.append(spriteNode)

    # read templates and insert children to templates
    templatesRoot = readPlist( CCBTEMPLATE )
    for child in templatesRoot['nodeGraph']['children']:
        if child['displayName'] == 'SDPNode':
            child['children'] = children

    # set frame length
    length = float(timesec) * float(totalframes) + 0.5
    if length > 10.0 :
        length = 10.0
    templatesRoot['sequences'][0]['length'] = length

    writePlist(templatesRoot, ccbfile)
    writePlist(templatesRoot, ccbfile.replace('.ccb', '.plist'))
    '''
    didOpen = 0
    if isinstance(ccbfile, (str, unicode)):
        pathOrFile = open(ccbfile, "w")
        didOpen = 1
    writer = PlistWriter(ccbfile)
    writer.writeValue(templatesRoot)
    if didOpen:
        ccbfile.close()
    '''

PLUTIL = '/usr/bin/plutil'
TEXTUREPACKER = '/usr/local/bin/TexturePacker'
CCBTEMPLATE = '/Users/cooper/Work/iOS/CocosBuilder-2.1-examples/CocosBuilderExample/CocosBuilderExample/Resources/Tests/sdp_template.ccb'

filenames=os.listdir(os.getcwd())
for filename in filenames:
    if (filename.rfind(".sdp") < 0):
        continue

    # make temp ccb folder
    ccbFolder = 'ccb'
    if os.path.isdir(ccbFolder):
        pass
    else:
        os.makedirs(ccbFolder)

    plstFile = ccbFolder + '/' + filename.replace(".sdp", ".plist")
    ccbFile = ccbFolder + '/' + filename.replace(".sdp", ".ccb")

    try:
        print filename

        # get root element
        root = ElementTree.parse(filename).getroot()
        spriteList = []

        # get SkeletonTree Node
        SkeletonTree = root.find("SkeletonTree")
        NodeNameList = SkeletonTree.findall('NodeName')
        for NodeName in NodeNameList:
            tag = int(NodeName.attrib['Tag'])
            name = NodeName.attrib['Name']
            # dict for sprite
            sprite = {}
            sprite['tag'] = tag
            sprite['displayName'] = name
            spriteList.append(sprite)
            
        # get SkeletonAction Node
        SkeletonAction = root.find('SkeletonAction')
        totalframe = SkeletonAction.attrib['TotalFrame']
        rate = int(SkeletonAction.attrib['Rate'])
        NodeDataList = SkeletonAction.findall('NodeData')
        for NodeData in NodeDataList:
            nodeTag = int(NodeData.attrib['Tag'])
            anchorX = NodeData.attrib['AnchorX']
            anchorY = NodeData.attrib['AnchorY']

            for sprite in spriteList:
                if nodeTag == sprite['tag']:
                    sprite['anchor'] = (float(anchorX), float(anchorY))
                    sprite['frames'] = []

                    FrameData = NodeData.findall('FrameData')
                    for frame in FrameData:
                        index = int(frame.attrib['Frame'])
                        posX = float(frame.attrib['PosX'])
                        posY = float(frame.attrib['PosY'])
                        scaleX = float(frame.attrib['ScaleX'])
                        scaleY = float(frame.attrib['ScaleY'])
                        skewX = float(frame.attrib['SkewX'])
                        skewY = float(frame.attrib['SkewY'])
                        rotate = float(frame.attrib['Rot'])
                        opacity = int(frame.attrib['Opacity'])
                        visible = bool(frame.attrib['Visible'])
                        colorlist = frame.attrib['Color'].replace('r=','').replace('g=','').replace('b=','').replace(' ','').split(';')
                        frame = {}
                        frame['index'] = index
                        frame['position'] = (posX, posY)
                        frame['scale'] = (scaleX, scaleY)
                        frame['skew'] = (skewX, skewY)
                        frame['rotation'] = rotate
                        frame['opacity'] = opacity
                        frame['visible'] = visible
                        frame['color'] = (int(colorlist[0]), int(colorlist[1]), int(colorlist[2]))
                        sprite['frames'].append(frame)
                
#                print "[%d](%f, %f) scale(%f, %f), skew(%f, %f), rotate(%f), opacity(%d), visisble(%d) color(%s)" % (index, posX, posY, scaleX, scaleY, skewX, skewY, rotate, opacity, visible, color)

        # get SkeletonSkin Node
        SkeletonSkin = root.find('SkeletonSkin')
        KeyFrameAnimList = SkeletonSkin.findall('KeyFrameAnim')
        for keyFrameAnim in KeyFrameAnimList:
            kfTag = int(keyFrameAnim.attrib['Tag'])

            for sprite in spriteList:
                if kfTag == sprite['tag']:                    
                    FrameDataList = keyFrameAnim.findall('FrameData')
                    for FrameData in FrameDataList:
                        frameIndex = int(FrameData.attrib['Frame'])
                        idx = 0
                        for frame in sprite['frames']:
                            if idx == 0:
                                sprite['spriteFrame'] = FrameData.attrib['Name']
                            if frame['index'] == frameIndex:
                                frame['spriteFrame'] = FrameData.attrib['Name']
                            idx += 1

        convertSDP2CCB(spriteList, totalframe, rate, ccbFile)
        #print spriteList
        print "\r\n"
        
        #writePlist(spriteList, plstFile)

        continue

        print "totally export %d" %(iFileCount)

    except InvalidPlistException, e:
        print "Not a Plist or Plist Invalid:", e



