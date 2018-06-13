import sys
import subprocess
import DOGProtocol as DOG
import RPi.GPIO as GPIO
import threading

GPIO.setwarnings(False)
started = False
file_name = ""


MAN = {"help":"Call 'help <command>' to see information about the command.\nCommands:\n\t-display\n\t-help\n\t-send\n\t-start",
	"start":"Help for 'start':\nStarts listening to the ports connected (hopefully) to the VEX Cortex. Enters the received data to a file.",
	"exit":"Help for 'exit':\nCloses this server.",
	"display":"Help for 'display':\nDisplays the data requested. Data options:\n\t-all (default): shows all data collected",
	"send":"Help for 'send':\nSends the following string using DOGProtocol. Transmission ports are defined in DOGProtocol.py.",
	"write":"Help for 'write':\nWrites the following string directly to the output file.",

	}

def help(args):
	if len(args) == 1:
		print(MAN.get("help"))
	elif len(args) == 2:
		print(MAN.get(args[1]))

def send(data):
	data = data[1:]
	global started
	if not started:
		print("You must start the server first!")
		return
	print(data)
	data_string = ""
	for s in data:
		data_string += s + " "
	DOG.send(data_string)

def rec_loop():
	global file_name
	while(True):
		with open(file_name, 'a') as f:
			f.write(DOG.receive())
			f.write("\n")

def write(args):
	global started
	global file_name
	if not started:
		print("You must start the server first!")
		return
	with open(file_name, 'a') as f:
		for st in args[1:]:
			f.write(st)
			f.write(" ")
		f.write("\n")

def start(args):
	global started
	if started:
		print("Server has already been started.")
		return
	if len(args) == 1:
		print("You must specify a file name!")
		return
	global file_name
	file_name = args[1]
	output_file = open(args[1], "a+")
	output_file.close()
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	started = True
	rec_thread = threading.Thread(target=rec_loop,name='Receive Thread')
	rec_thread.start()

def display(args):
	global started
	if not started:
		print("You must start the server first!")
		return
	global file_name
	if len(args) == 1:
		with open(file_name) as f:
			print(f.read())

def ex(args):
	print("Session closing.")
	GPIO.cleanup()
	exit()

COMMAND_LIST = {"help": help, "start": start, "display":display, "exit":ex, "send":send, "write":write}

def runserver():
	global started
	while True:
		command = input("JAYES@ROVER53:\t")

		#if command.split()[0] not in COMMAND_LIST:
		#	print("Unknown command. Try 'help'")
		#elif command.split()[0] == "exit":
	#		ex()
#		elif command.split()[0] == "help":
		#	help(command.split())
		#elif command.split()[0] == "start":
		#	start(command.split())
		#elif command.split()[0] == "send":
		#	send(command.split()[1:])
		#elif command.split()[0] == "display":
		#	display(command.split())
		args = command.split()
		COMMAND_LIST.get(args[0], lambda _: print("Unknown command. Try 'help'"))(command.split())

try:
	runserver()
except KeyboardInterrupt:
	print("\nKeyboardInterrupt")
	runserver()
