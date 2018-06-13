import RPi.GPIO as GPIO
import threading
import math
import time
import datetime

# note: these values are the BCM numbers, not the physical board numbers
# you must hook them up based on a pinout diagram, using the number that
# follows "GPIO"
data_out = 5
timer_out = 6

data_in = 20
timer_in = 21

START = [1, 0, 1, 1, 1, 1, 1, 1]
END = [1, 1, 1, 1, 1, 1, 1, 1]
BASE = [0, 0, 0, 0, 0, 0, 0, 0]
# first bit signifies if the buffer is a control flow buffer (stop, start, etc)
# following bits are in order of significance

# interprets a list in buffer format, converting it to a character
def buf_to_char(l: list) -> str:
        bin_string = '0b'
        for bit in l:
                bin_string += str(bit)
        val = int(bin_string, 2)
        return chr(val)

# converts an string of length 1 to a list in buffer format
def char_to_buf(val: str) -> list:
        ret = [0, 0, 0, 0, 0, 0, 0, 0]
        binary = bin(ord(val))
        binary = binary[2:]
        while len(binary) < 7:
                binary = '0' + binary
        for i in range(0, 7):
                ret[i + 1] = int(binary[i])
        return ret

def buf_to_str(buf: list) -> str:
        data = ''
        for li in buf:
                if(li == END or li == START):
                        pass
                else:
                        data += buf_to_char(li)
        return data

# converts an ascii string to a list of lists in buffer format
def str_to_buf(val: str) -> list:
        buf = []
        for c in val:
                buf += [char_to_buf(c)]
        return buf

# sends a string over the data protocol. translates to list of buffers, sends that way
def send(out: str):
        # setup the GPIO pins to send data
        GPIO.setup(data_out, GPIO.OUT, initial=0)
        GPIO.setup(timer_out, GPIO.OUT, initial=0)

        # convert the string to a list of lists in buffer format
        send = str_to_buf(out) + [list(END)]

        for buf in send:
                for bit in buf:
                        # set the timer to 0, prepare the receiver to read input
                        # change the data wire, prepare for the data to be read
                        # set timer to 1, data should be read at this point
                        GPIO.output(timer_out, 0)
                        if bit == 1:
                                GPIO.output(data_out, 1)
                        else:
                                GPIO.output(data_out, 0)
                        time.sleep(.0005)
                        GPIO.output(timer_out, 1)
                        time.sleep(.0005) # wait to ensure data is read
                time.sleep(.0005)
        GPIO.output(timer_out, 0)


# loop to receive input from the GPIO ports
def receive() -> list:
        # setup the gpio pins to recieve data
        GPIO.setup(data_in, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(timer_in, GPIO.IN, GPIO.PUD_DOWN)

        buf = [START]
        ans = list(BASE)

        temp = GPIO.input(timer_in)
        while temp == GPIO.input(timer_in):
                pass

        while(buf[-1] != END):
                bit = 0
                for i in range(0, 8):
                        # wait until the timer is 1, read the data from the data port
                        while GPIO.input(timer_in) == 0:
                                pass
                        ans[bit] = GPIO.input(data_in)
                        bit+=1
                        # wait until the timer is zero again
                        while GPIO.input(timer_in) == 1:
                                pass
                # add the received bits to the data
                buf += [list(ans)] # be sure to clone the list
                # reset the buffer to receive again
                ans = list(BASE)
        return buf_to_str(buf)
