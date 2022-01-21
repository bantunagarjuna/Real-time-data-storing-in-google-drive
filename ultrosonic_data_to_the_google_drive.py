#Libraries
import RPi.GPIO as GPIO
import time

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Rename the downloaded JSON file to client_secrets.json which downloaded from the googleapi
# The client_secrets.json file needs to be in the same directory as the script.
gauth = GoogleAuth()
gauth.LocalWebserverAuth() 
drive = GoogleDrive(gauth)

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
#string name
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance

if __name__ == '__main__':
    while True:
        try:
            while True:
                dist = distance()
                print ("Measured Distance = %.1f cm" % dist)
                
                if(dist<10):
                    print("you are close to Nagarjuna")
                    #name="closer to Nagarjuna"
                    
                    time.sleep(1)
                    # Reset by pressing CTRL + C
                dis =  str(dist) #{0:4d}
                #cop = str(name)
                 #{1:3}%".format (adcout, percent)
                reporttime = (time.strftime("%H:%M:%S"))
                csvresult = open("paste the path of the folder where code was saved/Ultrosonic_data22.csv","a")
                #csvresult.write(dis + ","+ closer +" , " + reporttime + "\n")
                csvresult.write(dis + ","+ reporttime + "\n")
                csvresult.close
                # # Upload files to your Google Drive
                upload_file_list = ["Ultrosonic_data22.csv"]
                for upload_file in upload_file_list:
                    gfile = drive.CreateFile({'parents': [{'id': 'google folder id where you want to store'}]})
                    # Read file and set it as a content of this instance.
                    gfile.SetContentFile(upload_file)
                    gfile.Upload() # Upload the file.
        except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()
