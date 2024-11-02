import RPi.GPIO as g
import time
from time import sleep
import tm1637
import serial
import pynmea2



#setup
g.setmode(g.BCM)
g.setwarnings(False)
displayClk= 25
displayDio= 8

trigPin =2
echoPin =3
TRIGGER_TIME = 0.00001
MAX_TIME = 0.4

g.setup(trigPin,g.OUT)
g.setup(echoPin, g.IN,pull_up_down=g.PUD_UP)
g.output(trigPin, False)


cdisplay =tm1637.TM1637(clk = displayClk, dio = displayDio)

speedW = 1482
speedS = 343

def getDepth():

    g.output(trigPin, True)
    time.sleep(TRIGGER_TIME)
    g.output(trigPin, False)

    start = time.time()
    timeout = start + MAX_TIME

    while g.input(echoPin) == 0 and start <= timeout:
        start = time.time()

    if(start > timeout):
        return -1

    stop = time.time()
    timeout = stop + MAX_TIME

    while g.input(echoPin) == 1 and stop <= timeout:
        stop = time.time()

    if(stop <= timeout):
        elapsed = stop-start
        distance = float(elapsed * speedW)/2.0
    else:
        return -1
    return distance


#port setup
port="/dev/ttyAMA0"
ser=serial.Serial(port, baudrate=9600, timeout=1)
dataout = pynmea2.NMEAStreamReader()

while True:
    try:
        newdata=ser.readline().decode('utf-8').strip()


        if newdata[:6] == "$GPRMC":

            dis = getDepth()
            print(dis)
            discm=dis-(int(dis))
            if dis  < 10:
                cdisplay.numbers(0+int(dis),int(100*discm))
            else:cdisplay.numbers(int(dis),int(100*discm))
            
            newmsg=pynmea2.parse(newdata)
            lat=newmsg.latitude
            lng=newmsg.longitude
            # gps = "Latitude= " + str(lat) + " Longitude= " + str(lng)
            # print(gps)
            # print("hlbka: ",dis)

            if (lat != 0 or lng !=0) and (dis != 0 or dis != -1):
                    with open('/media/kiko/SUB/sonarOutput.txt', 'a') as out:
                        out.write(f"{float(lat)},{float(lng)},{float(dis)}")
                        out.write("\n")
                        out.close()    
                    # cdisplay.show("done")
    except: 
        pass



