import speech_recognition as sr 
import pyttsx3  
import pyautogui as pg
import time
from datetime import datetime

#----------------------------------------------------------------------#
#time Developer

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

#----------------------------------------------------------------------#

# Initialize the recognizer  
r = sr.Recognizer()  
r.dynamic_energy_threshold = True  
  
# Function to convert text to 
# speech 

#----------------------------------------------------------------------#

def SpeakText(command): 
      
    # Initialize the engine 
    engine = pyttsx3.init() 
    engine.say(command)  
    engine.runAndWait() 
      
      
# Loop infinitely for user to 
# speak 

#----------------------------------------------------------------------#

slide_number = 1

#----------------------------------------------------------------------#

while True:     
      
    # Exception handling to handle 
    # exceptions at the runtime 
    try: 
          
        # use the microphone as source for input. 
        with sr.Microphone() as source2: 
              
            # wait for a second to let the recognizer 
            # adjust the energy threshold based on 
            # the surrounding noise level  
            r.adjust_for_ambient_noise(source2, duration=0.2) 
            r.dynamic_energy_threshold = True  
              
            #listens for the user's input  
            audio2 = r.listen(source2) 
              
            # Using ggogle to recognize audio 
            MyText = r.recognize_google(audio2 , language='th-TH') 
            MyText = MyText.lower() 

            if MyText == 'ต่อไป' or 'ต่อ' in MyText:
                print('next')
                pg.press('right')
                slide_number += 1
                SpeakText('Slide ' + str(slide_number))
                

            elif MyText == 'ย้อนกลับ' or 'ย้อน' in MyText:
                print('back')
                pg.press('left')

                if slide_number <= 1:
                    slide_number = 1
                    SpeakText('Slide ' + str(slide_number))
                else:
                    slide_number -= 1
                    SpeakText('Slide ' + str(slide_number))

            elif MyText == 'ทดสอบ':
                print('I am ready')
                SpeakText('i am ready')

            elif MyText == 'ว่าง':
                SpeakText('Blank')
                pg.press('w')

            elif MyText == 'เวลา':
                print('Current Time Speaked')
                SpeakText(current_time)
                
                

            elif MyText == 'จบการนำเสนอ':
                print('Finished Loop')
                pg.press('esc')
                SpeakText('Thank you for your attention')

                break

            elif MyText == 'เริ่ม':

                print('Powerpoint timer have started')

                #print("Did you say "+MyText) 
                #Sext(MyText) peakT

              
    except sr.RequestError as e: 
        print("Could not request results; {0}".format(e)) 
          
    except sr.UnknownValueError: 
        print("unknown error occured")

'''

Different from V.1(9/1/64)
- Change the Language from English(Main) to Thai
- Add Number slide's teller loop

'''