#!/usr/bin/env python3
import math
import os
from collections import deque
from gcode_parser import GcodeParser
import datGen
from typing import List

import argparse

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

parser = argparse.ArgumentParser(description='GCODE to KUKA KRL LS Translator v0.9. Copyright by F2 Innovations LLC')
parser.add_argument("--maxpoints", nargs="?", type=int, const=500, default=500,
                    help='Maximum points per .SRC file, default 500')
parser.add_argument("gcode", type=str, default='ABS_Calibration_cube.gcode',
                    help='Source GCODE file')
parser.add_argument("folder", nargs="?", type=str, default=os.path.join(__location__, 'output'),
                    help='Target KRL files folder (default = "output" subfolder in script directory)')
parser.add_argument("--uframe", nargs="?", type=int, const=1, default = 1,
                    help='Target Userframe, default = 1')
parser.add_argument("--utool", nargs="?", type=int, const=1, default = 1,
                    help='Target Toolframe, default = 1')

args = parser.parse_args()
    
machineState = dict(axes=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], direction=[0.0,0.0,0.0], feedrate = 0.0, nextAngle = 0.0, weaveposition = 0.0, isExtruding = False, isMoving = False, extrusion=dict(position = 0.0,amount = 0.0, speed = 0.0), moveModes=dict(toolMoveMode='Absolute',extrusionMode='Absolute'))    
currentMovement = dict(axes=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], direction=[0.0,0.0,0.0], feedrate = 0.0, nextAngle = 0.0, weaveposition = 0.0, isExtruding = False, isMoving = False, extrusion=dict(position = 0.0,amount = 0.0, speed = 0.0), moveModes=dict(toolMoveMode='Absolute',extrusionMode='Absolute'))    

isMovementCommand = False

movequeue = deque([],maxlen=3)

weaveStep = (math.pi/2)
weavePosition = 0.0
commandlimit = args.maxpoints

f2 = open(os.path.join(args.folder,"kuka_commands.tmp"), "w")
kuka_call = open(os.path.join(args.folder,"addstart.src"), "w")

gcodefilename = args.gcode

pointnumber = 0
programnumber = 0

header_template ='''&ACCESS RVP
&REL 65
&PARAM DISKPATH = KRC:\R1\Program
DEF '''
header_template2_start = ''' ( )   
   ;FOLD INI;%{PE}
     ;FOLD BASISTECH INI
       GLOBAL INTERRUPT DECL 3 WHEN $STOPMESS==TRUE DO IR_STOPM ( )
       INTERRUPT ON 3 
       BAS (#INITMOV,0 )
     ;ENDFOLD (BASISTECH INI)
     ;FOLD USER INI
       ;Make your modifications here
     ;ENDFOLD (USER INI)
   ;ENDFOLD (INI)

   BAS (#VEL_PTP, 0020.0000)
   BAS (#ACC_PTP, 0020.0000)
   
   ;-----SET LIN AND ARC MOTION VARIABLES-----
   $VEL.ORI1 = 0350.0000
   $VEL.ORI2 = 0350.0000
   
   $ACC.CP = 0005.0000
   $ACC.ORI1 = 1000.0000
   $ACC.ORI2 = 1000.0000
   
   ;-----APPROXIMATION-----
   $APO.CVEL = 0100
   $APO.CPTP = 0100
   $APO.CDIS = 0006.0000
   $APO.CORI = 0090.0000

   BAS (#BASE, 1) ;Positioner
   BAS (#TOOL, 1) ;Vrashatel

   BAS(#VEL_PTP,15)                         ;;Set PTP Axis Velocity
   BAS(#ACC_PTP,50)                         ;;Set PTP Axis Acceleration
   PTP{A1 -92,A2 -133,A3 132,A4 7,A5 50,A6 -10}
'''
header_template2 = ''' ( )
  ;FOLD PTP P1 Vel=50 % PDAT1 Tool[1]:cmttorch Base[1]:vrashatel ;%{PE} 
;FOLD Parameters ;%{h} 
;Params IlfProvider=kukaroboter.basistech.inlineforms.movement.old; Kuka.IsGlobalPoint=False; Kuka.PointName=P1; Kuka.BlendingEnabled=False; Kuka.MoveDataPtpName=PDAT1; Kuka.VelocityPtp=50; Kuka.CurrentCDSetIndex=0; Kuka.MovementParameterFieldEnabled=True; IlfCommand=PTP 
;ENDFOLD 
$BWDSTART = FALSE 
PDAT_ACT = PPDAT1 
FDAT_ACT = FP1 
BAS(#PTP_PARAMS, 50.0) 
SET_CD_PARAMS (0) 
PTP XP1 
;ENDFOLD
  
'''

footer_template_start = '''

END
'''

footer_template = '''

END
'''

arcOn_template = '''
;FOLD ARCON WDAT1 LIN P3 Vel=0.5 m/s CPDAT1 Tool[1]:cmttorch Base[1]:vrashatel ;%{PE}
  ;FOLD Parameters ;%{h}
    ;Params IlfProvider=kukaroboter.arctech.arconlin; Kuka.IsGlobalPoint=False; Kuka.PointName=P3; Kuka.BlendingEnabled=False; Kuka.MoveDataName=CPDAT1; Kuka.VelocityPath=0.5; Kuka.CurrentCDSetIndex=0; Kuka.MovementParameterFieldEnabled=True; ArcTech.WdatVarName=WDAT1; ArcTech.Basic=3.4.3.1264
  ;ENDFOLD
  $BWDSTART = FALSE
  LDAT_ACT = LCPDAT1
  FDAT_ACT = FP3
  BAS(#CP_PARAMS, 0.5)
  SET_CD_PARAMS (0)
  TRIGGER WHEN DISTANCE = 1 DELAY = ArcGetDelay(#PreDefinition, WDAT1) DO ArcMainNG(#PreDefinition, WDAT1, WP3) PRIO = -1
  TRIGGER WHEN PATH = ArcGetPath(#OnTheFlyArcOn, WDAT1) DELAY = ArcGetDelay(#GasPreflow, WDAT1) DO ArcMainNG(#GasPreflow, WDAT1, WP3) PRIO = -1
  TRIGGER WHEN PATH = ArcGetPath(#OnTheFlyArcOn, WDAT1) DELAY = 0 DO ArcMainNG(#ArcOnMoveStd, WDAT1, WP3) PRIO = -1 
  ArcMainNG(#ArcOnBeforeMoveStd, WDAT1, WP3)
  LIN XP3
  ArcMainNG(#ArcOnAfterMoveStd, WDAT1, WP3)
;ENDFOLD
'''

arcOff_template = '''
;FOLD ARCOFF WDAT2 LIN P4 CPDAT2 Tool[1]:cmttorch Base[1]:vrashatel ;%{PE}
  ;FOLD Parameters ;%{h}
    ;Params IlfProvider=kukaroboter.arctech.arcofflin; Kuka.IsGlobalPoint=False; Kuka.PointName=P4; Kuka.BlendingEnabled=False; Kuka.MoveDataName=CPDAT2; Kuka.VelocityPath=0.01; Kuka.CurrentCDSetIndex=0; Kuka.MovementParameterFieldEnabled=True; ArcTech.WdatVarName=WDAT2; ArcTech.Basic=3.4.3.1264
  ;ENDFOLD
  $BWDSTART = FALSE
  LDAT_ACT = LCPDAT2
  FDAT_ACT = FP4
  BAS(#CP_PARAMS, gArcBasVelDefinition)
  SET_CD_PARAMS (0)
  TRIGGER WHEN PATH = ArcGetPath(#ArcOffBefore, WDAT2) DELAY = 0 DO ArcMainNG(#ArcOffBeforeOffStd, WDAT2, WP4) PRIO = -1
  TRIGGER WHEN PATH = ArcGetPath(#OnTheFlyArcOff, WDAT2) DELAY = 0 DO ArcMainNG(#ArcOffMoveStd, WDAT2, WP4) PRIO = -1 
  ArcMainNG(#ArcOffBeforeMoveStd, WDAT2, WP4)
  LIN XP4
  ArcMainNG(#ArcOffAfterMoveStd, WDAT2, WP4)
;ENDFOLD
'''

prevExtrusion = False;

def kuka_start():  
  kuka_call.write(header_template)
  kuka_call.write('Addstart')
  kuka_call.write(header_template2_start)
  return

def kuka_flush():
  global programnumber
  global pointnumber
  global f2

  name = "ap_" + str(programnumber)
  f4 = open(os.path.join(args.folder,name+".dat"), "w")
  f3 = open(os.path.join(args.folder,name+".src"), "w")
  f3.write(header_template)
  f4.write(datGen.header_template)
  f4.write(name)
  f4.write(datGen.param_template)
  f3.write(name)
  f3.write(header_template2_start)

  f2.close()

  with open(os.path.join(args.folder,"kuka_commands.tmp")) as infile:
    for line in infile:
      f3.write(line)

  f3.write(footer_template)

  kuka_call.write('   '+name+" ( )\n")
  
  f2 = open(os.path.join(args.folder,"kuka_commands.tmp"), "w")

  programnumber += 1
  pointnumber = 1

  return

def outputpoint(point):
  global pointnumber
  global prevExtrusion
  if point['isMoving']:
    pointnumber += 1
  
  if pointnumber > commandlimit:
    kuka_flush()

  if prevExtrusion != point['isExtruding']:
      if point['isExtruding']:
          prevExtrusion = True
          f2.write(arcOn_template)
      else:
          prevExtrusion = False
          f2.write(arcOff_template)
  smooth = 3.0
  extrusion_speed = point["extrusion"]["speed"]
  
  if extrusion_speed < 0:
    extrusion_speed = 65535 + extrusion_speed

  angle = point['nextAngle']

  #f2.write(f'   RET=EKI_Send("F2Connect","<EXTRUSION>{extrusion_speed:.0f}</EXTRUSION>")\n')
  # if point['isExtruding'] and not point['isMoving']:
  #   f2.write(f'   WAIT SEC {point["extrusion"]["time"]:.2f}\n')
  # else:
  if abs(angle) < 95:
      if abs(angle) < 40:
        smooth = 100
      else:
        smooth = 100 - abs(angle)
      f2.write(f'   $VEL.CP = {(point["feedrate"]/60000.0):.3f}\n')
      f2.write('   LIN  {')
      f2.write(f"X {point['axes'][0]:.3f}, Y {point['axes'][1]:.3f}, Z {point['axes'][2]:.3f}, ")
      f2.write(f"A {point['axes'][3]:.3f}, B {point['axes'][4]:.3f}, C {point['axes'][5]:.3f}")
      f2.write('} C_DIS\n')
  else:
      f2.write(f'   $VEL.CP = {(point["feedrate"]/60000.0):.3f}\n')
      f2.write('   LIN  {')
      f2.write(f"X {point['axes'][0]:.3f}, Y {point['axes'][1]:.3f}, Z {point['axes'][2]:.3f}, ")
      f2.write(f"A {point['axes'][3]:.3f}, B {point['axes'][4]:.3f}, C {point['axes'][5]:.3f}")
      f2.write('} C_DIS\n')
  
  return

def activemovement(vectora,vectorb):    
    total = 0.0
    for index,element in enumerate(vectora):
      total += abs(element - vectorb[index])
    return total > 0.0 

def addStatesPosition(state1, state2):
  for index,axis in enumerate(state2['axes']):
    state1[index] += axis
  return state1

def vectoranglebase(a,b):
  denominator = (math.sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2) * math.sqrt(b[0] ** 2 + b[1] ** 2 + b[2] ** 2))
  if denominator != 0.0: return ((a[0] * b[0] + a[1] * b[1] + a[2] * b[2]) / denominator)
  else: return 1.0

def vectorangle3d(first,second,third):
  delta1 = [second[0]-first[0],second[1]-first[1],second[2]-first[2]]
  delta2 = [third[0]-second[0],third[1]-second[1],third[2]-second[2]]
  sinbase = vectoranglebase(delta1,delta2)
  if sinbase > 1.0: return 1.0
  if sinbase < -1.0: return -1.0
  return math.degrees(math.acos(sinbase))

def vectorlength(first,second):
  length = 0.0
  for index in range(len(first)):
    length += (first[index]-second[index]) ** 2
  return math.sqrt(length)

def split3d(start, end, segments):
    x_delta = (end[0] - start[0]) / float(segments)
    y_delta = (end[1] - start[1]) / float(segments)
    z_delta = (end[2] - start[2]) / float(segments)
    points = []
    for i in range(1, segments):
        points.append([start[0] + i * x_delta, start[1] + i * y_delta, start[2] + i * z_delta])
    return points

def splitsize3d(start, end, segment_size):
    x_delta = (end[0] - start[0])
    y_delta = (end[1] - start[1]) 
    z_delta = (end[2] - start[2]) 
    length = math.sqrt(x_delta ** 2 + y_delta ** 2 + z_delta ** 2)
    segments = math.floor(length / segment_size)
    if segments > 0:
      return split3d(start, end, segments)
    else:
      return None

def unitvector(start, end):
    x_delta = (end[0] - start[0])
    y_delta = (end[1] - start[1]) 
    z_delta = (end[2] - start[2])     
    length = math.sqrt(x_delta ** 2 + y_delta ** 2 + z_delta ** 2)
    if length > 0:
      return [x_delta/length, y_delta/length, z_delta/length]
    else:
      return [0.0,0.0,0.0]


def rotatevector(vector,angle):
    an = math.radians(angle)
    cs = math.cos(an)
    sn = math.sin(an);    
    return [vector[0] * cs - vector[1] * sn, vector[0] * sn + vector[1] * cs]

def weave_sine(width,position):
    return math.sin(position)*width/2

def segmentedoutput(segmentsize = 0.0):
  global weavePosition

  rotated = rotatevector(movequeue[0]['direction'][0:2],90)
  #weave = weave_sine(0.2,weavePosition)
  weave = 0.0
  weavePosition += weaveStep
  segmentlist = splitsize3d(movequeue[0]['axes'][0:3],movequeue[1]['axes'][0:3],segmentsize)  
  #print(f"{movequeue[0]['axes'][0]+rotated[0]*weave:.5}\t{movequeue[0]['axes'][1]+rotated[1]*weave:.5}\t{movequeue[0]['axes'][2]:.5}\t{movequeue[0]['direction'][0]*feed}\t{movequeue[0]['direction'][1]*feed}\t{movequeue[0]['direction'][2]*feed}\t{0.0}")
  outputpoint(movequeue[0])
  print(f"G1 X{movequeue[0]['axes'][0]+rotated[0]*weave:.5} Y{movequeue[0]['axes'][1]+rotated[1]*weave:.5} Z{movequeue[0]['axes'][2]:.5} F{movequeue[0]['feedrate']} ; e={movequeue[0]['extrusion']['amount']:.2f} {movequeue[0]['nextAngle']:.2f} {movequeue[0]['direction']}")  
  if segmentlist is not None:
    for segment in segmentlist:
      weave = weave_sine(10,weavePosition)
      #print(f"{segment[0]+rotated[0]*weave:.5}\t{segment[1]+rotated[1]*weave:.5}\t{segment[2]:.5}\t{movequeue[0]['direction'][0]*feed}\t{movequeue[0]['direction'][1]*feed}\t{movequeue[0]['direction'][2]*feed}\t{0.0}")
      print(f"G1 X{segment[0]+rotated[0]*weave:.5} Y{segment[1]+rotated[1]*weave:.5} Z{segment[2]:.5} F{movequeue[0]['feedrate']} ;{0.0} {movequeue[0]['direction']}")
      weavePosition += weaveStep
  return

# open gcode file and store contents as variable
kuka_start()

with open(gcodefilename, 'r') as f:
  gcode = f.read()


for line in GcodeParser(gcode).lines:

    movement = dict(axes=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0], feedrate = 0.0, moveLength = 0.0, nextAngle = 0.0, weaveposition = 0.0, isExtruding = False, isMoving = False, extrusion=dict(position = 0.0,amount = 0.0, speed = 0.0, time=0.0), command = "")
    movement['command'] = line.command[0] + str(line.command[1])
    # G commands processing
    if line.command[0] == 'G':
      if line.command[1] < 3 and line.command[1] >= 0:
        isMovementCommand = True
      else:
        isMovementCommand = False

    if line.command[0] == 'G':
      if line.command[1] == 1 or line.command[1] == 0:
        # Processing linked cartesian axes
        for index, param in enumerate(('X','Y','Z','W','P','R','A','B','C','D')):
          if currentMovement['moveModes']['toolMoveMode'] == 'Absolute':
            currentMovement['axes'][index] = line.get_param(param,float,currentMovement['axes'][index])
          else:
            currentMovement['axes'][index] += line.get_param(param,float,0.0)
        # Processing extrusion axis
        for param in ('E'):
          if currentMovement['moveModes']['extrusionMode'] == 'Absolute':
            currentMovement['extrusion']['position'] = line.get_param(param,float,currentMovement['extrusion']['position'])
          else:
            currentMovement['extrusion']['position'] += line.get_param(param,float,0.0)
        for param in ('F'):
          currentMovement['feedrate'] = line.get_param(param,float,currentMovement['feedrate'])                          
      if line.command[1] == 90:
        currentMovement['moveModes']['toolMoveMode']='Absolute'
      if line.command[1] == 91:
        currentMovement['moveModes']['toolMoveMode']='Relative'
      if line.command[1] == 92:        
        for index,param in enumerate(('X','Y','Z','W','P','R','A','B','C','D')):
          offset = line.get_param(param,float)
          if offset is not None:
            machineState['axes'][index] += currentMovement['axes'][index]
            machineState['axes'][index] -= offset
            currentMovement['axes'][index] = offset
        #     Возможно нужно
        # extrusionOffset = line.get_param('E',float)
        # if extrusionOffset is not None:
        #   machineState['extrusion']['position'] += currentMovement['extrusion']['position']
        #   machineState['extrusion']['position'] -= extrusionOffset
        #   currentMovement['extrusion']['position'] = extrusionOffset
          

          #currentState[param] = line.get_param(param,float,currentState[param])          
    # M commands processing
    if line.command[0] == 'M':
      if line.command[1] == 82:
        currentMovement['moveModes']['extrusionMode']='Absolute'
      if line.command[1] == 83:
        currentMovement['moveModes']['extrusionMode']='Relative'
    #Process States comparison    

    for index,axisitem in enumerate(currentMovement['axes']):
      movement['axes'][index] = axisitem
    for index,moveitem in enumerate(machineState['axes']):
      movement['axes'][index] += axisitem
    movement['feedrate'] = currentMovement['feedrate']
    movement['extrusion']['position'] = currentMovement['extrusion']['position'] + machineState['extrusion']['position']

    if isMovementCommand:      
      if len(movequeue) > 0:
        if activemovement(movement['axes'],movequeue[-1]['axes']) or activemovement([movement['extrusion']['position']],[movequeue[-1]['extrusion']['position']]):
          
          movement['extrusion']['amount'] = movement['extrusion']['position'] - movequeue[-1]['extrusion']['position']
          
          if activemovement(movement['axes'],movequeue[-1]['axes']):
            movement['isMoving'] = True
          else:
            movement['isMoving'] = False

          if movement['extrusion']['position'] - movequeue[-1]['extrusion']['position'] > 0:
            movement['isExtruding'] = True
          else:
            movement['isExtruding'] = False
          
          movement['moveLength'] = vectorlength(movement['axes'][0:3],movequeue[-1]['axes'][0:3]) 
          
          if movement['isExtruding']:
            if movement['isMoving']:
              movement['extrusion']['speed'] = movement['extrusion']['amount'] / movement['moveLength'] * movement['feedrate']
              movement['extrusion']['time'] = abs(movement['moveLength'] / (movement['extrusion']['speed'] / 60.0))
            else:
              movement['extrusion']['speed'] = math.copysign(movement['feedrate'],movement['extrusion']['amount'])
              movement['extrusion']['time'] = abs(movement['extrusion']['amount'] / (movement['extrusion']['speed'] / 60.0))
          
          if movement['isExtruding'] and movement['isMoving']:
            weavePosition += weaveStep

          movequeue.append(movement)
      else:
        movequeue.append(movement)
      if len(movequeue) > 2:
          movequeue[1]['nextAngle'] = vectorangle3d(movequeue[0]['axes'],movequeue[1]['axes'],movequeue[2]['axes'])
          movequeue[0]['direction'] = unitvector(movequeue[0]['axes'][0:3],movequeue[1]['axes'][0:3])

          if movequeue[0]['isExtruding'] or movequeue[0]['isMoving']:
            outputpoint(movequeue[0])
          #  print(f"G1 X{movequeue[0]['axes'][0]:.3f} Y{movequeue[0]['axes'][1]:.3f} Z{movequeue[0]['axes'][2]:.3f} F{movequeue[0]['feedrate']} E{movequeue[0]['extrusion']['amount']:.3f}; e={movequeue[0]['isExtruding']} m={movequeue[0]['isMoving']} a={movequeue[0]['nextAngle']:.0f}")
          #print(movequeue[0])
          #segmentedoutput(400)
#f2.write(": PR[10]=LPOS    ;\n")
kuka_flush()
kuka_call.write(footer_template_start)
kuka_call.close()
f2.close()

os.remove(os.path.join(args.folder,"kuka_commands.tmp"))
