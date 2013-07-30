# Python S60 dice roller

from appuifw import *
import e32, random
random.seed()

# Standard dice roll total
def total_roll(sides, rolls):
	total = 0
	for i in range(rolls):
		total += random.randint(1, sides)
	return total
	
# Exalted success count
def exalt_roll(rolls):
	successes = 0
	botches = 0
	for i in range(rolls):
		die = random.randint(1, 10)
		if die >= 7 and die < 10:
			successes += 1
		elif die == 10:
			successes += 2
		elif die ==  1:
			botches += 1
	return successes, botches

# D20 +/- modifier roll
def d20_roll(mod, modtype):
	crit = 0 # -1 = crit fail, 1 = crit succcess
	die = random.randint(1, 20)
	if die == 20:
		crit = 1
	elif die == 1:
		crit = -1
	if modtype == 0:
		die += mod
	else:
		die -= mod
	return die, crit

# Setup screen
app.screen="normal"
app.title = u"5d60 Dice Roller"

# Determine which option from the list was chosen, prompt
# for number, then roll and display
def list_handler():
	# Total roll: rolls T number of dS, sums the result
	if list_menu.current() == 0:
		sides = query(u"Number of sides:", "number")
		number = query(u"Number of dice rolled:", "number")
		result = total_roll(sides, number)
		note("Total: " + unicode(result))
	
	# Exalted: counts successes (7, 8, 9 = 1, 10 = 2)
	elif list_menu.current() == 1:
		number = query(u"Number of dice rolled:", "number")
		result = exalt_roll(number)
		if result[0] > 0:
			note("Successes: " + unicode(result[0]))
		elif result[1] > 0 and result [0] == 0:
			note("Botches: " + unicode(result[1]))
		else:
			note(u"Roll was a failure.")
	
	# D20 system with modifiers
	elif list_menu.current() == 2:
		modlist = [u"+ mod", u"- mod"]
		modtype = popup_menu(modlist, u"Positive or negative modifier?")
		mod = query(u"Enter modifier:", "number")
		result = d20_roll(mod, modtype)
		crit_text = ""
		if result[1] == 1:
			crit_text = "Natural 20!"
		elif result[1] == -1:
			crit_text = "Natural 1..."
		note("Rolled: " + unicode(result[0]) + "\n" + crit_text)
		
	else:
		note(u"Something went wrong with the list callback, oh noes!", "error")

# Create list of options
entries = [u"Roll dice, total result", u"Exalted, successes", u"D20 with modifiers"]

# Put list into UI element Listbox and set as main element
list_menu = Listbox(entries, list_handler)
app.body = list_menu
about_text = Text()

# Option menu functions
def ver_python():
	note(unicode(e32.pys60_version))

def ver_s60():
	note(unicode(e32.s60_version_info))
	
def ver_5d60():
	note(u"1.0")
	
def app_main():
	app.body = list_menu
	app.exit_key_handler = app_exit
	app.menu = [(u"About", app_about),
	(u"Version",
		((u"Python version", ver_python),
		(u"S60 version", ver_s60))),
	(u"Exit", app_exit)]

def app_about():
	about_text.set(u"""5d60, a dice roller for Python S60.
	
Copyright (C) 2013 James Wright

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.""")
	about_text.set_pos(0)
	app.body = about_text
	app.menu = [(u"Dice roller", app_main),
	(u"Version",
		((u"Python version", ver_python),
		(u"S60 version", ver_s60))),
	(u"Exit", app_exit)]
	app.exit_key_handler = app_main

def app_exit():
	app_lock.signal()

# Option menu of left softkey
app.menu = [(u"About", app_about),
(u"Version",
	((u"Python version", ver_python),
	(u"S60 version", ver_s60))),
(u"Exit", app_exit)]
		
app_lock = e32.Ao_lock()
app.exit_key_handler = app_exit
app_lock.wait()