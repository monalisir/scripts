#! /Users/Cooper/Work/python-env/lershare-env/bin/python
# -*- coding: UTF-8 -*-
import os,Image,sys
import json
import plistlib
from biplist import *
from xml.etree import ElementTree
from xml.etree.ElementTree import ElementTree as ETClass
#from xml.etree.ElementTree import ElementTree,Element 

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

def generateSDPRoot( ccbNode, rate ) :
    sdpNode = ccbNode #ccbNode.value()
    # create root node ---SkeletonParts
    SkeletonParts = ElementTree.Element('SkeletonParts', attrib = {'version':'1.0'} )

    # create SkeletonTree
    SkeletonTree = ElementTree.SubElement(SkeletonParts, 'SkeletonTree', attrib = {'version':'1.0'})

    # create SkeletonAction
    SkeletonAction = ElementTree.SubElement(SkeletonParts, 'SkeletonAction', attrib = {'version':'1.0', 'TotalFrame':"16", 'Rate' : str(rate)})

    # create SkeletonSkin
    SkeletonSkin = ElementTree.SubElement(SkeletonParts, 'SkeletonSkin', attrib = {'version':'1.0'})

    totalFrame = 0
    for item in sdpNode :
        p_tag = 0
        p_sprite = ""
        p_anchor = [0.5, 0.5]
        p_opacity = 255
        p_color = [255, 255, 255]
        p_skew = [1, 1]
        for propInfo in item['properties'] :
            propertyName = propInfo['name']
            propertyValue = propInfo['value']
            p_rotation = 0.0
            if propertyName == 'tag' :
                p_tag = int(propertyValue)
            if propertyName == 'displayFrame' :
                p_sprite = propertyValue[1]
            if propertyName == 'anchorPoint' :
                p_anchor = propertyValue
            if propertyName == 'position' :
                p_position = propertyValue
            if propertyName == 'scale' :
                p_scale = propertyValue
            if propertyName == 'rotation' :
                p_rotation = propertyValue
            if propertyName == 'skew' :
                p_skew = propertyValue
            if propertyName == 'opacity' :
                p_opacity = propertyValue
            if propertyName == 'color' :
                p_color = propertyValue


        NodeName = ElementTree.SubElement( SkeletonTree, 'NodeName', attrib = {'Tag':str(p_tag), 'Name':item['displayName']} )

        NodeData = ElementTree.SubElement( SkeletonAction, 'NodeData', attrib = {'Tag':str(p_tag), 'AnchorX':str(p_anchor[0]), 'AnchorY':str(p_anchor[1])} )

        KeyFrameAnim = ElementTree.SubElement( SkeletonSkin, 'KeyFrameAnim', attrib = { 'Tag':str(p_tag) } )

        animationFrames = item['animatedProperties']['0']

        frameInfo = {}
        if animationFrames.has_key('rotation') :
            for r in animationFrames['rotation']['keyframes'] :
                idx = str(r['time'])
                if not frameInfo.has_key(idx) :
                    frameInfo[idx] = {}
                frameInfo[idx]['rotation'] = r['value']
        if animationFrames.has_key('position') :
            for p in animationFrames['position']['keyframes'] :
                idx = str(p['time'])
                if not frameInfo.has_key(idx) :
                    frameInfo[idx] = {}
                frameInfo[idx]['position'] = p['value']
        if animationFrames.has_key('scale') :
            for s in animationFrames['scale']['keyframes'] :
                idx = str(s['time'])
                if not frameInfo.has_key(idx) :
                    frameInfo[idx] = {}
                frameInfo[idx]['scale'] = s['value']
        if animationFrames.has_key('opacity') :
            for o in animationFrames['opacity']['keyframes'] :
                idx = str(o['time'])
                if not frameInfo.has_key(idx) :
                    frameInfo[idx] = {}
                frameInfo[idx]['opacity'] = o['value']
        if animationFrames.has_key('color') :
            for c in animationFrames['color']['keyframes'] :
                idx = str(c['time'])
                if not frameInfo.has_key(idx) :
                    frameInfo[idx] = {}
                frameInfo[idx]['color'] = c['value']
        if animationFrames.has_key('displayFrame') :
            for f in animationFrames['displayFrame']['keyframes'] :
                idx = str(f['time'])
                if not frameInfo.has_key(idx) :
                    frameInfo[idx] = {}
                frameInfo[idx]['displayFrame'] = f['value'][1]
        if animationFrames.has_key('skew') :
            for x in animationFrames['skew']['keyframes'] :
                idx = str(x['time'])
                if not frameInfo.has_key(idx) :
                    frameInfo[idx] = {}
                frameInfo[idx]['skew'] = x['value']

        # convert frame dict to list
        frameList = []
        for frameIdx in sorted(frameInfo.keys()) :
            frameInfo[frameIdx]['Frame'] = frameIdx

            if not 'rotation' in frameInfo[frameIdx] :
                if not frameList :
                    frameInfo[frameIdx]['rotation'] = p_rotation
                else :
                    frameInfo[frameIdx]['rotation'] = frameList[-1]['rotation']

            if not 'position' in frameInfo[frameIdx] :
                if not frameList :
                    frameInfo[frameIdx]['position'] = p_position
                else :
                    frameInfo[frameIdx]['position'] = frameList[-1]['position']
                
            if not 'scale' in frameInfo[frameIdx] :
                if not frameList :
                    frameInfo[frameIdx]['scale'] = p_scale
                else :
                    frameInfo[frameIdx]['scale'] = frameList[-1]['scale']

            if not 'opacity' in frameInfo[frameIdx] :
                if not frameList :
                    frameInfo[frameIdx]['opacity'] = p_opacity
                else :
                    frameInfo[frameIdx]['opacity'] = frameList[-1]['opacity']

            if not 'color' in frameInfo[frameIdx] :
                if not frameList :
                    frameInfo[frameIdx]['color'] = p_color
                else :
                    frameInfo[frameIdx]['color'] = frameList[-1]['color']

            if not 'skew' in frameInfo[frameIdx] :
                if not frameList :
                    frameInfo[frameIdx]['skew'] = p_skew
                else :
                    frameInfo[frameIdx]['skew'] = frameList[-1]['skew']

            if not 'displayFrame' in frameInfo[frameIdx] :
                if not frameList :
                    frameInfo[frameIdx]['displayFrame'] = p_sprite
                elif ( frameList[-1].has_key('displayFrame') ) and ( 'displayFrame' in frameInfo[frameIdx] ):
                    if (frameInfo[frameIdx]['displayFrame'] != frameList[-1]['displayFrame']) :
                        frameInfo[frameIdx]['displayFrame'] = frameList[-1]['displayFrame']
                elif 'displayFrame' in frameInfo[frameIdx]:
                    del frameInfo[frameIdx]['displayFrame']
                                                                                            
            frameList.append(frameInfo[frameIdx])
        
            data = frameList[-1]
            i = int(float(data['Frame']) * rate)
            if ( totalFrame < i ) :
                totalFrame = i
            strColor = "r=%d; g=%d; b=%d" %(data['color'][0], data['color'][1], data['color'][2])
            FrameData = ElementTree.SubElement( NodeData, 'FrameData', attrib = {'Frame'  : str(i), 
                                                                                 'PosX'   : str(list(data['position'])[0]),
                                                                                 'PosY'   : str(list(data['position'])[1]),
                                                                                 'ScaleX' : str(list(data['scale'])[0]),
                                                                                 'ScaleY' : str(list(data['scale'])[1]),
                                                                                 'SkewX'  : str(list(data['skew'])[0]),
                                                                                 'SkewY'  : str(list(data['skew'])[1]),
                                                                                 'Rot'    : str(data['rotation']),
                                                                                 'Color'  : strColor,
                                                                                 'Opacity': str(data['opacity']),
                                                                                 'Visible': '1' } )


            if 'displayFrame' in data :
                FrameData = ElementTree.SubElement( KeyFrameAnim, 'FrameData', attrib = {'Frame'  : str(i), 'Name' :data['displayFrame'] } )

        SkeletonAction.attrib['TotalFrame'] = str(totalFrame)

    xmlRoot = ETClass(SkeletonParts)

    return xmlRoot

filenames=os.listdir(os.getcwd())
for filename in filenames:
    if (filename.rfind(".ccb") < 0):
        continue

    # make temp sdp folder
    sdpFolder = 'sdp'
    if not os.path.isdir(sdpFolder):
        os.makedirs(sdpFolder)

    sdpFile = sdpFolder + '/' + filename.replace(".ccb", ".sdp")

    try:
        # get root element
        ccbRoot = readPlist( filename )
        sdpNodeList = {}
        for child in ccbRoot['nodeGraph']['children']:
            if child['displayName'].find('SDP_') != -1 :
                act_name = child['displayName']
                act_name = act_name.replace('SDP_', '')
                sdpNodeList[act_name] = child['children']

        length = ccbRoot['sequences'][0]['length']
        rate = ccbRoot['sequences'][0]['resolution']

        for sdp in sdpNodeList.keys() :
            sdpNode = sdpNodeList[sdp]
            xmlRoot = generateSDPRoot(sdpNode, rate)
            fn = sdpFolder + '/' + sdp + '.sdp'
            xmlRoot.write(fn, encoding="utf-8", xml_declaration=True)
            fn = sdpFolder + '/' + sdp + '.xml'
            xmlRoot.write(fn, encoding="utf-8", xml_declaration=True)

    except InvalidPlistException, e:
        print "Not a Plist or Plist Invalid:", e



