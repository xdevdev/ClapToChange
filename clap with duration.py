import pyaudio
import struct
import math
import pyautogui as pg
import time
import pyttsx3  
from datetime import datetime

INITIAL_TAP_THRESHOLD = 0.010
FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 2
RATE = 44100  
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
# if we get this many noisy blocks in a row, increase the threshold
OVERSENSITIVE = 15.0/INPUT_BLOCK_TIME                    
# if we get this many quiet blocks in a row, decrease the threshold
UNDERSENSITIVE = 120.0/INPUT_BLOCK_TIME 
# if the noise was longer than this many blocks, it's not a 'tap'
MAX_TAP_BLOCKS = 0.15/INPUT_BLOCK_TIME

next_slide = 'next'
back_slide = 'back'

def SpeakText(command): 
      
    engine = pyttsx3.init() 
    engine.say(command)  
    engine.runAndWait() 

def get_rms( block ):
    # RMS amplitude is defined as the square root of the 
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768. 
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    #Vrms
    #return math.sqrt( sum_squares / count )

    #Vavg
    #return math.sqrt( sum_squares / count ) / 1.1107

    #Vpeak
    #return math.sqrt( sum_squares / count ) / 0.707

    #Vpeak to peak
    return math.sqrt( sum_squares / count ) * 2.828

class TapTester(object):
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
        self.tap_threshold = INITIAL_TAP_THRESHOLD
        self.noisycount = MAX_TAP_BLOCKS+1 
        self.quietcount = 0 
        self.errorcount = 0

    def stop(self):
        self.stream.close()

    def find_input_device(self):
        device_index = None            
        for i in range( self.pa.get_device_count() ):     
            devinfo = self.pa.get_device_info_by_index(i)   
            print( "Device %d: %s"%(i,devinfo["name"]) )

            for keyword in ["mic","input"]:
                if keyword in devinfo["name"].lower():
                    print( "Found an input: device %d - %s"%(i,devinfo["name"]) )
                    device_index = i
                    return device_index

        if device_index == None:
            print( "No preferred input found; using default input device." )

        return device_index

    def open_mic_stream( self ):
        device_index = self.find_input_device()

        stream = self.pa.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = device_index,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        return stream

    def tapDetected(self):
        print("Tap!")
        #pg.press('right')
        
        


    def listen(self):
        
        clap_count = 0

        resetstarttime = True

        starttime = time.time()

        #starttime = time.time()

        while True:

            #now = datetime.now()
            

            try:
                block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
            except IOError as e:
                # dammit. 
                self.errorcount += 1
                print( "(%d) Error recording: %s"%(self.errorcount,e) )
                self.noisycount = 1
                return

            amplitude = get_rms( block )
            if amplitude > self.tap_threshold:
                # noisy block
                self.quietcount = 0
                self.noisycount += 1
                if self.noisycount > OVERSENSITIVE:
                    # turn down the sensitivity
                    self.tap_threshold *= 1.1 
            else:            
                # quiet block.

                if 1 <= self.noisycount <= MAX_TAP_BLOCKS:
                    self.tapDetected()
                    clap_count += 1
                    
                    if resetstarttime == True:
                        starttime = time.time()
                        resetstarttime = False
                    

                self.noisycount = 0
                self.quietcount += 1

                if self.quietcount > UNDERSENSITIVE:
                    # turn up the sensitivity
                    self.tap_threshold *= 0.9

            current_time = time.time()
           
            
            
            if int(current_time) - int(starttime) >= 1.5:
                #print(clap_count)

                #if clap_count > 0:
                 #   print(clap_count)
                #clap_count = 0
                #resetstarttime = True

                if clap_count == 1:
                    resetstarttime = True
                    clap_count = 0
                    #print('1 claps *************************************')

                elif clap_count == 2:
                    clap_count = 0
                    pg.press('right')
                    SpeakText(next_slide)
                    resetstarttime = True

                elif clap_count == 3:
                    clap_count = 0
                    pg.press('left')
                    SpeakText(back_slide)
                    resetstarttime = True
                else:
                    clap_count = 0
                    resetstarttime = True
                    
               # elif clap_count == 3:
               #     print('3 claps')
               #     clap_count = 0
                #    resetstarttime = True
               #else:
                    #clap_count = 0
                    #resetstarttime = True
                    #print('You are two claps already')

            #else:
                #resetstarttime = True
                #print(current_time - starttime)
                #clap_count = 0


if __name__ == "__main__":
    tt = TapTester()

    for i in range(1000):
        tt.listen()