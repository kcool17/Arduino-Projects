# Welcome to the Wiimote Base Program!
#
#
# This program reads data from a wii remote, and then converts it into data you can
# actually use! For buttons, it sets a variable specific to each button to "True" or
# "False", indicating whether that button is pressed. For Analog controls, it sets
# variables to the x and y coordinates of the joystick. The accelerometer reasings
# give values to variables for the x, y, and z coordinates of the accelerometer. All
# of this runs in the background, so that as the main program runs, the variables are
# constantly updated to what is needed in the code. Just check if the button's variable
# is true or not, and then you know whether or not the button is pushed.
#
# Author: Kyle Sawicki
#
# Known issues:
#   -So far, the classic controller's analog buttons only output raw data, I don't have
#    another controller to test to make sure the algorithms work.
#
# Notes:
#   -When connecting to the wiimote, it tries to connect for a while before quitting (if no
#    buttons are pressed, it'll take a long time to timeout. I suggest a status LED for
#    feedback). It also only connects to the specified MAC address (if one is given)
#   -For the joysticks, the center is given as soon as the joystick connects, and the position 
#    is found based off of that. This is because the center varies throughout different
#    extensions, but the distance from left to right is about the same, Based off of this, 
#    the Nunchuck's distance between extremes for the X axis and the Y Axis is about 190.
#    The classic controller's left joystick's X axis is about 50, and about 45 for the Y.
#    For the right joystick, it is about 25 for both axis. I'd say that to keep it safe, 
#    assume that the range is 180 for the Nunchuck's Joystick (both axis), about 40 for the
#    classic controller's left joystick, and 20 for the right one. Anything beyond these value  
#    still counts as the extremes. For the centers, it is within 10 in either direction for
#    the nunchuck, and within 2 for the classic controller
#   -Make sure that when connecting the Wiimote, the extensions are plugged in FIRST, and that
#    the joysticks are in their neutral positions. Otherwise, you'll have to restart the
#    program.
#
# Credits:
#   -Abstrakraft, for creating the cwiid library, and the start of this program (the beginning
#    code can be found at http://abstrakraft.org/cwiid/browser/wmdemo/wmdemo.py)
#   -http://www.raspberrypi-spy.co.uk/2013/02/nintendo-wii-remote-python-and-the-raspberry-pi/,
#    for help with detecting button presses
#   -Stack Overflow, because errors.
#   -The Raspberry Pi Foundation, for creating the Raspberry Pi, and Nintendo for creating the
#    wiimotes
#
# Sources for more info:
#   -The two links above
#   -Python.org
#   -Github.com/abstrakraft/cwiid


#!/usr/bin/python
import cwiid
import sys
import os
import time
import threading


#Main debug menu
menu = '''1: toggle LED 1
2: toggle LED 2
3: toggle LED 3
4: toggle LED 4
5: toggle rumble
a: toggle accelerometer reporting
b: toggle button reporting
c: enable motionplus, if connected
e: toggle extension reporting
i: toggle ir reporting
m: toggle messages
p: print this menu
r: request status message ((t) enables callback output)
s: print current state
t: toggle status reporting
x: exit'''

#IMPORTANT: This is the MAC Adress of the Wiimote you want this to connect to only, leave string
#empty to connect to any Wiimote in the vicinity.
wiimote_mac = "00:22:AA:C1:13:13"

#List of main variables (creates all of the main variables, and makes them global)

#Wiimote

button_a = False
button_b = False
button_1 = False
button_2 = False
button_plus = False
button_minus = False
button_home = False
button_up = False
button_down = False
button_left = False
button_right = False

#Nunchuck
nunchuck_c = False
nunchuck_z = False
#Joystick
nunchuck_joystick_x = 0.0
nunchuck_joystick_y = 0.0

#Classic Controller
classic_a = False
classic_b = False
classic_x = False
classic_y = False
classic_l = False
classic_r = False
classic_zl = False
classic_zr = False
classic_plus = False
classic_minus = False
classic_home = False
classic_up = False
classic_down = False
classic_left = False
classic_right = False
#L/R Button analog values
classic_analog_l = 0.0
classic_analog_r = 0.0
#Joysticks
classic_lstick_x = 0.0
classic_lstick_y = 0.0
classic_rstick_x = 0.0
classic_rstick_y = 0.0

#Raw data holders
wiimote_raw_buttons = 0
wiimote_acc_x = 0
wiimote_acc_y = 0
wiimote_acc_z = 0
classic_raw_buttons = 0
classic_raw_lstick = 0
classic_raw_rstick = 0
classic_raw_analog_l = 0
classic_raw_analog_r = 0
nunchuck_raw_joystick = 0
nunchuck_raw_buttons = 0
nunchuck_acc_x = 0
nunchuck_acc_y = 0
nunchuck_acc_z = 0
nunchuck_joystick_raw_x = 0
nunchuck_joystick_raw_y = 0
classic_lstick_raw_x = 0
classic_lstick_raw_y = 0
classic_rstick_raw_x = 0
classic_rstick_raw_y = 0
nunchuck_joystick_center_x = 0
nunchuck_joystick_center_y = 0
classic_lstick_center_x = 0
classic_lstick_center_y = 0
classic_rstick_center_x = 0
classic_rstick_center_y = 0


#Function to connect to wiimote:
def connect_wii():
    global wiimote
    global connect_wii_timeout
    try:
        if len(wiimote_mac) > 1:
            wiimote = cwiid.Wiimote(wiimote_mac)
        else:
            wiimote = cwiid.Wiimote()
    except RuntimeError:
        connect_wii_timeout += 1
        if connect_wii_timeout < 600:
            print "Trying again"
            connect_wii()
        else:
            print "Failure opening Wiimote Connection"
#What starts and connects to Wiimote
def startUp():
    global rumble
    led = 0
    rpt_mode = 0
    rumble = 0
    mesg = False

    #Connects to Wiimote
    print 'Put Wiimote in discoverable mode now (press 1+2)...'
    global connect_wii_timeout
    connect_wii_timeout = 0
    connect_wii()
    wiimote.mesg_callback = callback
    
    #Activates button/extension/Accelerometer reporting
    rpt_mode ^= cwiid.RPT_BTN
    wiimote.rpt_mode = rpt_mode
    rpt_mode ^= cwiid.RPT_EXT
    wiimote.rpt_mode = rpt_mode
    rpt_mode ^= cwiid.RPT_ACC
    wiimote.rpt_mode = rpt_mode

    #Toggles LEDs (Just comment out some lines to pick which LEDS are on/off)
    led ^= cwiid.LED1_ON
    wiimote.led = led
    led ^= cwiid.LED2_ON
    wiimote.led = led
    led ^= cwiid.LED3_ON
    wiimote.led = led
    led ^= cwiid.LED4_ON
    wiimote.led = led

    #Gives extensions time to initialize
    time.sleep(1)

    #Sets the centers of any extensions attached
    global nunchuck_joystick_center_x
    global nunchuck_joystick_center_y
    global classic_lstick_center_x 
    global classic_lstick_center_y 
    global classic_rstick_center_x 
    global classic_rstick_center_y

    assign_raw(wiimote.state)
    trans_raw_analog()

    if wiimote.state['ext_type'] == cwiid.EXT_CLASSIC:
        classic_lstick_center_x = classic_lstick_raw_x
        classic_lstick_center_y = classic_lstick_raw_y
        classic_rstick_center_x = classic_rstick_raw_x
        classic_rstick_center_y = classic_rstick_raw_y
    elif wiimote.state['ext_type'] == cwiid.EXT_NUNCHUK:
        nunchuck_joystick_center_x = nunchuck_joystick_raw_x
        nunchuck_joystick_center_y = nunchuck_joystick_raw_y
    else:
        return


#Used for debugging, as in printing to console raw data (Button presses, joystick data, etc.)
def debug_menu():
	print menu

	exit = 0
	while not exit:
		c = sys.stdin.read(1)
		if c == '1':
			led ^= cwiid.LED1_ON
			wiimote.led = led
		elif c == '2':
			led ^= cwiid.LED2_ON
			wiimote.led = led
		elif c == '3':
			led ^= cwiid.LED3_ON
			wiimote.led = led
		elif c == '4':
			led ^= cwiid.LED4_ON
			wiimote.led = led
		elif c == '5':
			rumble ^= 1
			wiimote.rumble = rumble
		elif c == 'a':
			rpt_mode ^= cwiid.RPT_ACC
			wiimote.rpt_mode = rpt_mode
		elif c == 'b':
			rpt_mode ^= cwiid.RPT_BTN
			wiimote.rpt_mode = rpt_mode
		elif c == 'c':
			wiimote.enable(cwiid.FLAG_MOTIONPLUS)
		elif c == 'e':
			rpt_mode ^= cwiid.RPT_EXT
			wiimote.rpt_mode = rpt_mode
		elif c == 'i':
			rpt_mode ^= cwiid.RPT_IR
			wiimote.rpt_mode = rpt_mode
		elif c == 'm':
			mesg = not mesg
			if mesg:
				wiimote.enable(cwiid.FLAG_MESG_IFC);
			else:
				wiimote.disable(cwiid.FLAG_MESG_IFC);
		elif c == 'p':
			print menu
		elif c == 'r':
			wiimote.request_status()
		elif c == 's':
			print_state(wiimote.state)
		elif c == 't':
			rpt_mode ^= cwiid.RPT_STATUS
			wiimote.rpt_mode = rpt_mode
		elif c == 'x':
			exit = -1;
		elif c == '\n':
			pass
		else:
			print 'invalid option'

	wiimote.close()

#Used for Debug Menu only
def print_state(state):
	print 'Report Mode:',
	for r in ['STATUS', 'BTN', 'ACC', 'IR', 'NUNCHUK', 'CLASSIC', 'BALANCE', 'MOTIONPLUS']:
		if state['rpt_mode'] & eval('cwiid.RPT_' + r):
			print r,
	print

	print 'Active LEDs:',
	for led in ['1','2','3','4']:
		if state['led'] & eval('cwiid.LED' + led + '_ON'):
			print led,
	print

	print 'Rumble:', state['rumble'] and 'On' or 'Off'

	print 'Battery:', int(100.0 * state['battery'] / cwiid.BATTERY_MAX)

	if 'buttons' in state:
		print 'Buttons:', state['buttons']

	if 'acc' in state:
		print 'Acc: x=%d y=%d z=%d' % (state['acc'][cwiid.X],
		                               state['acc'][cwiid.Y],
		                               state['acc'][cwiid.Z])

	if 'ir_src' in state:
		valid_src = False
		print 'IR:',
		for src in state['ir_src']:
			if src:
				valid_src = True
				print src['pos'],

		if not valid_src:
			print 'no sources detected'
		else:
			print

	if state['ext_type'] == cwiid.EXT_NONE:
		print 'No extension'
	elif state['ext_type'] == cwiid.EXT_UNKNOWN:
		print 'Unknown extension attached'
	elif state['ext_type'] == cwiid.EXT_NUNCHUK:
		if state.has_key('nunchuk'):
			print 'Nunchuk: btns=%.2X stick=%r acc.x=%d acc.y=%d acc.z=%d' % \
			  (state['nunchuk']['buttons'], state['nunchuk']['stick'],
			   state['nunchuk']['acc'][cwiid.X],
			   state['nunchuk']['acc'][cwiid.Y],
			   state['nunchuk']['acc'][cwiid.Z])
	elif state['ext_type'] == cwiid.EXT_CLASSIC:
		if state.has_key('classic'):
			print 'Classic: btns=%.4X l_stick=%r r_stick=%r l=%d r=%d' % \
			  (state['classic']['buttons'],
			   state['classic']['l_stick'], state['classic']['r_stick'],
			   state['classic']['l'], state['classic']['r'])
	elif state['ext_type'] == cwiid.EXT_BALANCE:
		if state.has_key('balance'):
			print 'Balance: right_top=%d right_bottom=%d left_top=%d left_bottom=%d' % \
			  (state['balance']['right_top'], state['balance']['right_bottom'],
			   state['balance']['left_top'], state['balance']['left_bottom'])
	elif state['ext_type'] == cwiid.EXT_MOTIONPLUS:
		if state.has_key('motionplus'):
			print 'MotionPlus: angle_rate=(%d,%d,%d)' % state['motionplus']['angle_rate']

#Not 100% sure what this stuff does
def callback(mesg_list, time):
	print 'time: %f' % time
	for mesg in mesg_list:
		if mesg[0] == cwiid.MESG_STATUS:
			print 'Status Report: battery=%d extension=' % \
			       mesg[1]['battery'],
			if mesg[1]['ext_type'] == cwiid.EXT_NONE:
				print 'none'
			elif mesg[1]['ext_type'] == cwiid.EXT_NUNCHUK:
				print 'Nunchuk'
			elif mesg[1]['ext_type'] == cwiid.EXT_CLASSIC:
				print 'Classic Controller'
			elif mesg[1]['ext_type'] == cwiid.EXT_BALANCE:
				print 'Balance Board'
			elif mesg[1]['ext_type'] == cwiid.EXT_MOTIONPLUS:
				print 'MotionPlus'
			else:
				print 'Unknown Extension'

		elif mesg[0] == cwiid.MESG_BTN:
			print 'Button Report: %.4X' % mesg[1]

		elif mesg[0] == cwiid.MESG_ACC:
			print 'Acc Report: x=%d, y=%d, z=%d' % \
			      (mesg[1][cwiid.X], mesg[1][cwiid.Y], mesg[1][cwiid.Z])

		elif mesg[0] == cwiid.MESG_IR:
			valid_src = False
			print 'IR Report: ',
			for src in mesg[1]:
				if src:
					valid_src = True
					print src['pos'],

			if not valid_src:
				print 'no sources detected'
			else:
				print

		elif mesg[0] == cwiid.MESG_NUNCHUK:
			print ('Nunchuk Report: btns=%.2X stick=%r ' + \
			       'acc.x=%d acc.y=%d acc.z=%d') % \
			      (mesg[1]['buttons'], mesg[1]['stick'],
			       mesg[1]['acc'][cwiid.X], mesg[1]['acc'][cwiid.Y],
			       mesg[1]['acc'][cwiid.Z])
		elif mesg[0] == cwiid.MESG_CLASSIC:
			print ('Classic Report: btns=%.4X l_stick=%r ' + \
			       'r_stick=%r l=%d r=%d') % \
			      (mesg[1]['buttons'], mesg[1]['l_stick'],
			       mesg[1]['r_stick'], mesg[1]['l'], mesg[1]['r'])
		elif mesg[0] ==  cwiid.MESG_BALANCE:
			print ('Balance Report: right_top=%d right_bottom=%d ' + \
			       'left_top=%d left_bottom=%d') % \
			      (mesg[1]['right_top'], mesg[1]['right_bottom'],
			       mesg[1]['left_top'], mesg[1]['left_bottom'])
		elif mesg[0] == cwiid.MESG_MOTIONPLUS:
			print 'MotionPlus Report: angle_rate=(%d,%d,%d)' % \
			      mesg[1]['angle_rate']
		elif mesg[0] ==  cwiid.MESG_ERROR:
			print "Error message received"
			global wiimote
			wiimote.close()
			exit(-1)
		else:
			print 'Unknown Report'

#This function just prints out all of the buttons' variable values for debug purposes
def print_buttons():
    os.system('clear')
    if wiimote.state['ext_type'] == cwiid.EXT_CLASSIC:
        print "Wiimote Raw Buttons: " + str(wiimote_raw_buttons)
        print "Button A: " + str(button_a)
        print "Button B: " + str(button_b)
        print "Button 1: " + str(button_1)
        print "Button 2: " + str(button_2)
        print "Button Plus: " + str(button_plus)
        print "Button Minus: " + str(button_minus)
        print "Button Home: " + str(button_home)
        print "Button Up: " + str(button_up)
        print "Button Down: " + str(button_down)
        print "Button Left: " + str(button_left)
        print "Button Right: " + str(button_right)
        print " "
        print "Classic Raw Buttons: " + str(classic_raw_buttons)
        print "Classic A: " + str(classic_a)
        print "Classic B: " + str(classic_b)
        print "Classic X: " + str(classic_x)
        print "Classic Y: " + str(classic_y)
        print "Classic L: " + str(classic_l)
        print "Classic R: " + str(classic_r)
        print "Classic ZL: " + str(classic_zl)
        print "Classic ZR: " + str(classic_zr)
        print "Classic Plus: " + str(classic_plus)
        print "Classic Minus: " + str(classic_minus)
        print "Classic Home: " + str(classic_home)
        print "Classic Up: " + str(classic_up)
        print "Classic Down: " + str(classic_down)
        print "Classic Left: " + str(classic_left)
        print "Classic Right: " + str(classic_right)
        print " "
    elif wiimote.state['ext_type'] == cwiid.EXT_NUNCHUK:
        print "Wiimote Raw Buttons: " + str(wiimote_raw_buttons)
        print "Button A: " + str(button_a)
        print "Button B: " + str(button_b)
        print "Button 1: " + str(button_1)
        print "Button 2: " + str(button_2)
        print "Button Plus: " + str(button_plus)
        print "Button Minus: " + str(button_minus)
        print "Button Home: " + str(button_home)
        print "Button Up: " + str(button_up)
        print "Button Down: " + str(button_down)
        print "Button Left: " + str(button_left)
        print "Button Right: " + str(button_right)
        print " "
        print "Nunchuck Raw Buttons: " + str(nunchuck_raw_buttons)
        print "Nunchuck C: " + str(nunchuck_c)
        print "Nunchuck Z: " + str(nunchuck_z)
    else:
        print "Wiimote Raw Buttons: " + str(wiimote_raw_buttons)
        print "Button A: " + str(button_a)
        print "Button B: " + str(button_b)
        print "Button 1: " + str(button_1)
        print "Button 2: " + str(button_2)
        print "Button Plus: " + str(button_plus)
        print "Button Minus: " + str(button_minus)
        print "Button Home: " + str(button_home)
        print "Button Up: " + str(button_up)
        print "Button Down: " + str(button_down)
        print "Button Left: " + str(button_left)
        print "Button Right: " + str(button_right)
        print " "

#This function prints out all of the analog variable values for debugging
def print_analog():
    os.system('clear')
    print "Nunchuck Raw Joystick: " + str(nunchuck_raw_joystick)
    print " "
    print "Classic Raw L-Stick: " + str(classic_raw_lstick)
    print "Classic Raw R-Stick: " + str(classic_raw_rstick)
    print "Classic Raw Analog L: " + str(classic_raw_analog_l)
    print "Classic Raw Analog R: " + str(classic_raw_analog_r)
    print " "
    print "CLassic Analog L: " + str(classic_analog_l)
    print "CLassic Analog R: " + str(classic_analog_r)
    print "CLassic L-Stick X: " + str(classic_lstick_x)
    print "CLassic L-Stick Y: " + str(classic_lstick_y)
    print "CLassic R-Stick X: " + str(classic_rstick_x)
    print "CLassic R-Stick Y: " + str(classic_rstick_y)
    print " "
    print "Nunchuck Joystick X: " + str(nunchuck_joystick_x)
    print "Nunchuck Joystick Y: " + str(nunchuck_joystick_y)
    print " "
    print "Nunchuck Center X: " + str(nunchuck_joystick_center_x)
    print "Nunchuck Center Y: " + str(nunchuck_joystick_center_y)
    print "CLassic L-Stick Center X: " + str(classic_lstick_center_x)
    print "CLassic L-Stick Center Y: " + str(classic_lstick_center_y)
    print "CLassic R-Stick Center X: " + str(classic_rstick_center_x)
    print "CLassic R-Stick Center Y: " + str(classic_rstick_center_y)



#This function prints out all of the accelerometer variable values for debugging
def print_acc():
    os.system('clear')
    print "Wiimote Accelerometer X: " + str(wiimote_acc_x)
    print "Wiimote Accelerometer Y: " + str(wiimote_acc_y)
    print "Wiimote Accelerometer Z: " + str(wiimote_acc_z)
    print "Nunchuck Accelerometer X: " + str(nunchuck_acc_x)
    print "Nunchuck Accelerometer Y: " + str(nunchuck_acc_y)
    print "Nunchuck Accelerometer Z: " + str(nunchuck_acc_z)
    

    

#Function assigning raw data to variables
def assign_raw(state):
        #Leftover print_state code (just ignore the commented out part)
        """print 'Report Mode:',
	for r in ['STATUS', 'BTN', 'ACC', 'IR', 'NUNCHUK', 'CLASSIC', 'BALANCE', 'MOTIONPLUS']:
		if state['rpt_mode'] & eval('cwiid.RPT_' + r):
			print r,
	print

	print 'Active LEDs:',
	for led in ['1','2','3','4']:
		if state['led'] & eval('cwiid.LED' + led + '_ON'):
			print led,
	print

	print 'Rumble:', state['rumble'] and 'On' or 'Off'

	print 'Battery:', int(100.0 * state['battery'] / cwiid.BATTERY_MAX)
"""
        #Raw button values
	if 'buttons' in state:
                global wiimote_raw_buttons
		wiimote_raw_buttons = state['buttons']
        #Raw accelerometer values WARNING: Does not work (only nunchuck)
	if 'acc' in state:
                global wiimote_acc_x
                global wiimote_acc_y
                global wiimote_acc_z
		wiimote_acc_x = state['acc'][cwiid.X]
		wiimote_acc_y = state['acc'][cwiid.Y]
		wiimote_acc_z = state['acc'][cwiid.Z]
        #Leftover print_state code for IR (just ignore the commented out part)
	"""if 'ir_src' in state:
		valid_src = False
		print 'IR:',
		for src in state['ir_src']:
			if src:
				valid_src = True
				print src['pos'],

		if not valid_src:
			print 'no sources detected'
		else:
			print
"""     #Extension raw data
	if state['ext_type'] == cwiid.EXT_NONE:
		#print 'No extension'
                var87 = "blah"
	elif state['ext_type'] == cwiid.EXT_UNKNOWN:
		print 'Unknown extension attached'
	#Raw nunchuck values
	elif state['ext_type'] == cwiid.EXT_NUNCHUK:
		if state.has_key('nunchuk'):
                    global nunchuck_raw_buttons
                    global nunchuck_raw_joystick
                    global nunchuck_acc_x
                    global nunchuck_acc_y
                    global nunchuck_acc_z
		    nunchuck_raw_buttons = state['nunchuk']['buttons']
		    nunchuck_raw_joystick = state['nunchuk']['stick']
		    nunchuck_acc_x = state['nunchuk']['acc'][cwiid.X]
		    nunchuck_acc_y = state['nunchuk']['acc'][cwiid.Y]
		    nunchuck_acc_z = state['nunchuk']['acc'][cwiid.Z]
	#Raw classic controller values
	elif state['ext_type'] == cwiid.EXT_CLASSIC:
		if state.has_key('classic'):
                    global classic_raw_buttons
                    global classic_raw_lstick
                    global classic_raw_rstick
                    global classic_raw_analog_l
                    global classic_raw_analog_r
                    classic_raw_buttons = state['classic']['buttons']
		    classic_raw_lstick = state['classic']['l_stick']
		    classic_raw_rstick = state['classic']['r_stick']
		    classic_raw_analog_l = state['classic']['l']
		    classic_raw_analog_r = state['classic']['r']
        #Leftover print_state code for Motion Plus/Balance Board (just ignore the commented out part)
	"""elif state['ext_type'] == cwiid.EXT_BALANCE:
		if state.has_key('balance'):
			print 'Balance: right_top=%d right_bottom=%d left_top=%d left_bottom=%d' % \
			  (state['balance']['right_top'], state['balance']['right_bottom'],
			   state['balance']['left_top'], state['balance']['left_bottom'])
	elif state['ext_type'] == cwiid.EXT_MOTIONPLUS:
		if state.has_key('motionplus'):
			print 'MotionPlus: angle_rate=(%d,%d,%d)' % state['motionplus']['angle_rate']
"""
#Function to use raw data amd find what buttons are pressed for Wiimote
def trans_raw_buttons(buttons):
    button_delay = 0
    global classic_raw_buttons
    classic = classic_raw_buttons
    global nunchuck_raw_buttons
    nunchuck = nunchuck_raw_buttons
    #I have no idea why I need to make these things global, but it doesn't work without it
    #Wiimote
    global button_a 
    global button_b 
    global button_1 
    global button_2 
    global button_plus 
    global button_minus 
    global button_home 
    global button_up 
    global button_down 
    global button_left 
    global button_right
    #Classic Controller
    global classic_a 
    global classic_b 
    global classic_x 
    global classic_y
    global classic_l
    global classic_r
    global classic_zl
    global classic_zr
    global classic_plus 
    global classic_minus 
    global classic_home 
    global classic_up 
    global classic_down 
    global classic_left 
    global classic_right
    #Nunchuck
    global nunchuck_z
    global nunchuck_c

    #Raw button values (Only Classic controller and nunchuck)
    raw_a = 16
    raw_b = 64
    raw_x = 8
    raw_y = 32
    raw_l = 8192
    raw_r = 512
    raw_zl = 128
    raw_zr = 4
    raw_plus = 1024
    raw_minus = 4096
    raw_home = 2048
    raw_up = 1
    raw_down = 16384
    raw_left = 2
    raw_right = 32768
    raw_c = 2
    raw_z = 1

    #Wiimote
    if (buttons & cwiid.BTN_LEFT):
        button_left = True
        time.sleep(button_delay)
    else:
        button_left = False
        time.sleep(button_delay)
 
    if(buttons & cwiid.BTN_RIGHT):
        button_right = True
        time.sleep(button_delay)
    else:
        button_right = False
        time.sleep(button_delay)
 
    if (buttons & cwiid.BTN_UP):
        button_up = True
        time.sleep(button_delay)
    else:
        button_up = False
        time.sleep(button_delay)
 
    if (buttons & cwiid.BTN_DOWN):
        button_down = True
        time.sleep(button_delay)
    else:
        button_down = False
        time.sleep(button_delay)
 
    if (buttons & cwiid.BTN_1):
        button_1 = True
        time.sleep(button_delay)
    else:
        button_1 = False
        time.sleep(button_delay)
 
    if (buttons & cwiid.BTN_2):
        button_2 = True
        time.sleep(button_delay)
    else:
        button_2 = False
        time.sleep(button_delay)
 
    if (buttons & cwiid.BTN_A):
        button_a = True
        time.sleep(button_delay)
    else:
        button_a = False
        time.sleep(button_delay)
 
    if (buttons & cwiid.BTN_B):
        button_b = True
        time.sleep(button_delay)
    else:
        button_b = False
        time.sleep(button_delay)
 
    if (buttons & cwiid.BTN_HOME):
        button_home = True
        time.sleep(button_delay)
    else:
        button_home = False
        time.sleep(button_delay)
 
    if (buttons & cwiid.BTN_MINUS):
        button_minus = True
        time.sleep(button_delay)
    else:
        button_minus = False
        time.sleep(button_delay)
 
    if (buttons & cwiid.BTN_PLUS):
        button_plus = True
        time.sleep(button_delay)
    else:
        button_plus = False
        time.sleep(button_delay)

    #Classic Controller
    if (classic & raw_plus):
        classic_plus = True
        time.sleep(button_delay)
    else:
        classic_plus = False
        time.sleep(button_delay)
        
    if (classic & raw_minus):
        classic_minus = True
        time.sleep(button_delay)
    else:
        classic_minus = False
        time.sleep(button_delay)
        
    if (classic & raw_home):
        classic_home = True
        time.sleep(button_delay)
    else:
        classic_home = False
        time.sleep(button_delay)
        
    if (classic & raw_up):
        classic_up = True
        time.sleep(button_delay)
    else:
        classic_up = False
        time.sleep(button_delay)
        
    if (classic & raw_down):
        classic_down = True
        time.sleep(button_delay)
    else:
        classic_down = False
        time.sleep(button_delay)
        
    if (classic & raw_left):
        classic_left = True
        time.sleep(button_delay)
    else:
        classic_left = False
        time.sleep(button_delay)
        
    if (classic & raw_right):
        classic_right = True
        time.sleep(button_delay)
    else:
        classic_right = False
        time.sleep(button_delay)
        
    if (classic & raw_zl):
        classic_zl = True
        time.sleep(button_delay)
    else:
        classic_zl = False
        time.sleep(button_delay)
        
    if (classic & raw_zr):
        classic_zr = True
        time.sleep(button_delay)
    else:
        classic_zr = False
        time.sleep(button_delay)
        
    if (classic & raw_l):
        classic_l = True
        time.sleep(button_delay)
    else:
        classic_l = False
        time.sleep(button_delay)
        
    if (classic & raw_r):
        classic_r = True
        time.sleep(button_delay)
    else:
        classic_r = False
        time.sleep(button_delay)

    if (classic & raw_a):
        classic_a = True
        time.sleep(button_delay)
    else:
        classic_a = False
        time.sleep(button_delay)

    if (classic & raw_b):
        classic_b = True
        time.sleep(button_delay)
    else:
        classic_b = False
        time.sleep(button_delay)

    if (classic & raw_x):
        classic_x = True
        time.sleep(button_delay)
    else:
        classic_x = False
        time.sleep(button_delay)

    if (classic & raw_y):
        classic_y = True
        time.sleep(button_delay)
    else:
        classic_y = False
        time.sleep(button_delay)
        
    #Nunchuck
    if (nunchuck & raw_c):
        nunchuck_c = True
        time.sleep(button_delay)
    else:
        nunchuck_c = False
        time.sleep(button_delay)

    if (nunchuck & raw_z):
        nunchuck_z = True
        time.sleep(button_delay)
    else:
        nunchuck_z = False
        time.sleep(button_delay)
        
#This function updates the x/y axis of the sticks/analog buttons
def trans_raw_analog():
    global classic_raw_lstick
    global classic_raw_rstick
    global classic_raw_analog_l
    global classic_raw_analog_r
    global nunchuck_raw_joystick
    global classic_analog_l 
    global classic_analog_r
    global classic_lstick_raw_x 
    global classic_lstick_raw_y
    global classic_rstick_raw_x 
    global classic_rstick_raw_y
    global nunchuck_joystick_raw_x
    global nunchuck_joystick_raw_y
    global nunchuck_joystick_x
    global nunchuck_joystick_y
    global classic_lstick_x
    global classic_lstick_y
    global classic_rstick_x
    global classic_rstick_y
    global nunchuck_joystick_center_x
    global nunchuck_joystick_center_y 
    global classic_lstick_center_x 
    global classic_lstick_center_y 
    global classic_rstick_center_x 
    global classic_rstick_center_y 
    #90, 20, 10

    #Sets raw data for X/Y
    if wiimote.state['ext_type'] == cwiid.EXT_CLASSIC:
        classic_lstick_raw_x = classic_raw_lstick[0]
        classic_lstick_raw_y = classic_raw_lstick[1]
        classic_rstick_raw_x = classic_raw_rstick[0]
        classic_rstick_raw_y = classic_raw_rstick[1]
    elif wiimote.state['ext_type'] == cwiid.EXT_NUNCHUK:
        nunchuck_joystick_raw_x = nunchuck_raw_joystick[0]
        nunchuck_joystick_raw_y = nunchuck_raw_joystick[1]
    else:
        return

    #Finds the extremes for X/Y
    if wiimote.state['ext_type'] == cwiid.EXT_CLASSIC:
        classic_lstick_extreme_positive_x = classic_lstick_center_x + 20
        classic_lstick_extreme_positive_y = classic_lstick_center_y + 20
        classic_rstick_extreme_positive_x = classic_rstick_center_x + 10
        classic_rstick_extreme_positive_y = classic_rstick_center_y + 10
        classic_lstick_extreme_negative_x = classic_lstick_center_x - 20
        classic_lstick_extreme_negative_y = classic_lstick_center_y - 20
        classic_rstick_extreme_negative_x = classic_rstick_center_x - 10
        classic_rstick_extreme_negative_y = classic_rstick_center_y - 10
    elif wiimote.state['ext_type'] == cwiid.EXT_NUNCHUK:
        nunchuck_joystick_extreme_positive_x = nunchuck_joystick_center_x + 90
        nunchuck_joystick_extreme_positive_y = nunchuck_joystick_center_y + 90
        nunchuck_joystick_extreme_negative_x = nunchuck_joystick_center_x - 90
        nunchuck_joystick_extreme_negative_y = nunchuck_joystick_center_y - 90
    else:
        return
    
    #Converts the data to a value from -1 to 1
    if wiimote.state['ext_type'] == cwiid.EXT_CLASSIC:
        #L-Stick
        #X Axis
        if classic_lstick_raw_x >= classic_lstick_extreme_positive_x:
            classic_lstick_x = 1.0
        elif classic_lstick_raw_x <= classic_lstick_extreme_negative_x:
            classic_lstick_x = -1.0
        elif abs(classic_lstick_raw_x - classic_lstick_center_x) <= 2.0:
            classic_lstick_x = 0.0
        else:
            classic_lstick_x = abs(float(classic_lstick_raw_x) - float(classic_lstick_center_x)) \
                                  / 20.0
            if classic_lstick_raw_x < classic_lstick_center_x:
                classic_lstick_joystick_x = -1 * classic_lstick_x
        #Y Axis
        if classic_lstick_raw_y >= classic_lstick_extreme_positive_y:
            classic_lstick_y = 1.0
        elif classic_lstick_raw_y <= classic_lstick_extreme_negative_y:
            classic_lstick_y = -1.0
        elif abs(classic_lstick_raw_y - classic_lstick_center_y) <= 2.0:
            classic_lstick_y = 0.0
        else:
            classic_lstick_y = abs(float(classic_lstick_raw_y) - float(classic_lstick_center_y)) \
                                  / 20.0
            if classic_lstick_raw_y < classic_lstick_center_y:
                classic_lstick_joystick_y = -1 * classic_lstick_y

        #R-Stick
        #X Axis
        if classic_rstick_raw_x >= classic_rstick_extreme_positive_x:
            classic_rstick_x = 1.0
        elif classic_rstick_raw_x <= classic_rstick_extreme_negative_x:
            classic_rstick_x = -1.0
        elif abs(classic_rstick_raw_x - classic_rstick_center_x) <= 2.0:
            classic_rstick_x = 0.0
        else:
            classic_rstick_x = abs(float(classic_rstick_raw_x) - float(classic_rstick_center_x)) \
                                  / 10.0
            if classic_rstick_raw_x < classic_rstick_center_x:
                classic_rstick_joystick_x = -1 * classic_rstick_x
        #Y Axis
        if classic_rstick_raw_y >= classic_rstick_extreme_positive_y:
            classic_rstick_y = 1.0
        elif classic_rstick_raw_y <= classic_rstick_extreme_negative_y:
            classic_rstick_y = -1.0
        elif abs(classic_rstick_raw_y - classic_rstick_center_y) <= 2.0:
            classic_rstick_y = 0.0
        else:
            classic_rstick_y = abs(float(classic_rstick_raw_y) - float(classic_rstick_center_y)) \
                                  / 10.0
            if classic_rstick_raw_y < classic_rstick_center_y:
                classic_rstick_joystick_y = -1 * classic_rstick_y
        
    elif wiimote.state['ext_type'] == cwiid.EXT_NUNCHUK:
        #X Axis
        if nunchuck_joystick_raw_x >= nunchuck_joystick_extreme_positive_x:
            nunchuck_joystick_x = 1.0
        elif nunchuck_joystick_raw_x <= nunchuck_joystick_extreme_negative_x:
            nunchuck_joystick_x = -1.0
        elif abs(nunchuck_joystick_raw_x - nunchuck_joystick_center_x) <= 10.0:
            nunchuck_joystick_x = 0.0
        else:
            nunchuck_joystick_x = abs(float(nunchuck_joystick_raw_x) - float(nunchuck_joystick_center_x)) \
                                  / 90.0
            if nunchuck_joystick_raw_x < nunchuck_joystick_center_x:
                nunchuck_joystick_x = -1 * nunchuck_joystick_x
        #Y Axis
        if nunchuck_joystick_raw_y >= nunchuck_joystick_extreme_positive_y:
            nunchuck_joystick_y = 1.0
        elif nunchuck_joystick_raw_y <= nunchuck_joystick_extreme_negative_y:
            nunchuck_joystick_y = -1.0
        elif abs(nunchuck_joystick_raw_y - nunchuck_joystick_center_y) <= 10.0:
            nunchuck_joystick_y = 0.0
        else:
            nunchuck_joystick_y = abs(float(nunchuck_joystick_raw_y) - float(nunchuck_joystick_center_y)) \
                                  / 90.0
            if nunchuck_joystick_raw_y < nunchuck_joystick_center_y:
                nunchuck_joystick_y = -1 * nunchuck_joystick_y
        
        
    else:
        return

#Function to quickly toggle the Wiimote Rumble
def rumbleToggle():
    global rumble
    rumble ^= 1
    wiimote.rumble = rumble


#This function infinitely updates all of the variables for what buttons are pressed when it
#runs. Only run in background!
def button_update():
    y=1
    stopUpdate1=False
    while y==1:
        if stopUpdate1==True:
            y=2
            thread.exit()
        else:
            assign_raw(wiimote.state)
            trans_raw_buttons(wiimote_raw_buttons)
            trans_raw_analog()

#Makes wiimote buttons update in background, start with update_thread.start()
update_thread = threading.Thread(target=button_update)
update_thread.daemon = True




#Main program

#Starts everything and gets it working
startUp()
update_thread.start()

#Code for stuff goes here
x = 1
while x==1:
    print_buttons()
    if button_minus == True and button_home == True:
        rumbleToggle()


#End of code
stopUpdate1 = True
wiimote.close
