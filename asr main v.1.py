import speech_recognition as sr 
import pyttsx3  
import pyautogui as pg
import time
  
# Initialize the recognizer  
r = sr.Recognizer()  
  
# Function to convert text to 
# speech 
def SpeakText(command): 
      
    # Initialize the engine 
    engine = pyttsx3.init() 
    engine.say(command)  
    engine.runAndWait() 
      
      
# Loop infinitely for user to 
# speak 


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
              
            #listens for the user's input  
            audio2 = r.listen(source2) 
              
            # Using ggogle to recognize audio 
            MyText = r.recognize_google(audio2) 
            MyText = MyText.lower() 

            if MyText == 'go' or 'go' in MyText:
                print('next')
                pg.press('right')
                SpeakText('Next slide')
                continue

            elif MyText == 'back' or 'back' in MyText:
                print('back')
                pg.press('left')
                SpeakText('Back Slide')
                continue

            elif MyText == 'white':
                pg.press('w')
                continue

            elif MyText == 'finish':
                print('Finished Loop')
                SpeakText('Thank you for your attention')

                break

            elif MyText == 'start':

                print('Powerpoint timer have started')

                #print("Did you say "+MyText) 
                #Sext(MyText) peakT
              
    except sr.RequestError as e: 
        print("Could not request results; {0}".format(e)) 
          
    except sr.UnknownValueError: 
        print("unknown error occured")