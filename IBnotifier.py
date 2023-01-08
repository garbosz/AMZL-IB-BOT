import json
import requests
import sys
import time
import atexit
import keyboard
from os import system
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

posted=[]
ver="1.15.3"
Home="DBO6"
system("title "+"InBound Notifier")
x=0
with open('WEBHOOK-LINK.txt','r') as f:
    file=f.read()

##post some welcome stuff for setup
print("INBOUND NOTIFIER")
print("Developed by Zac Garbos( garbosz)")
print("VER."+ver)
print("Origin Station: "+Home)
print("\nRunning Setup...")

##handle when user presses X button
def on_exit():
    with open('errorLog.txt', 'a+') as error:  
        error.seek(0, 0) 
        error.write('\n' + 'Script Closed: '+time.asctime()) 

atexit.register(on_exit)

##verify Webhook from webhook link file, as well as defining IB link
print("Verifying WEBHOOK-LINK.txt")
WEBHOOK_URI=file
if file=='placeholder':
    print("You Did Not setup the Webhook! Please enter your webhook URL into WEBHOOK-LINK.txt to continue")
    with open('errorLog.txt', 'a+') as error:  
        error.seek(0, 0) 
        error.write('\n' + 'Webhook not provided: '+time.asctime()) 
    time.sleep(10)
    sys.exit('Webhook Not Provided')
elif "https://hooks.chime.aws/incomingwebhooks" in file:
    print("Webhook Link Valid...Continuing")
else:
    print("Provided Webhook link is Invalid")
    with open('errorLog.txt', 'a+') as error:  
        error.seek(0, 0) 
        error.write('\n' + 'Invalid Webhook: '+time.asctime()) 
    time.sleep(10)
    sys.exit('Invalid Webhook')

IBURL= 'https://trans-logistics.amazon.com/ssp/dock/ib/'

##check whether alt key is pressed to determing backup mode or normal operation
start_time = time.time()
while True:
    # Check if a key has been pressed
    if keyboard.is_pressed("alt"):
        backup = True
        break
    
    # Wait for 0.1 seconds before checking again
    time.sleep(0.1)
    
    # If no key has been pressed for 5 seconds, set key_pressed to False
    if time.time() - start_time > 3:
        backup = False
        break

##post to webhook function
def post_message(msg):
    response = None
    try:
        response = requests.post(
            url=WEBHOOK_URI,
            json={"Content": msg})
        return json.loads(response.text)
    except:
        with open('errorLog.txt', 'a+') as error:  
            error.seek(0, 0) 
            error.write('\n' + 'Unable to connect to Webhook: '+time.asctime()) 
        return "Fix your webhook loser"

##Load webpage to scrape
print("Loading IB")
response=requests.get(IBURL, verify=False)


##Load Initiation post, based on status of backup mode 
if backup==True:
    message = "INBOUND BOT Initiated\nVer."+ver+"\nPrimary Bot has failed, Backup Bot initiated\nChecks will happen in 5 minute increments and will run until host systems VPN expires\nStarted @ "+time.asctime()
else:
    message = "INBOUND BOT Initiated\nVer."+ver+"\nScript will now process through any current manifests\nChecks will happen in 5 minute increments and will run until host systems VPN expires\nStarted @ "+time.asctime()

## Post the message
print("Posting Initiation to Chime")
req_res = post_message(message)

##asks user for previously posted VRIDs to mitigate duplicate posting
if backup==True:
    # ask the user to input a list of strings, separated by commas
    input_string = input("Enter a list of posted VRIDs, separated by commas: ")

    # split the input string into a list of strings
    input_list = input_string.split(',')

    # iterate over the input list, stripping any leading/trailing whitespace
    for item in input_list:
        posted.append(item.strip())

##Main Loop
print("Entering Main Process Loop")
while True:
    t= time.time()


    ##reset cmd window for current loop
    #system('cls')
    print()
    print("INBOUND NOTIFIER")
    print("Developed by Zac Garbos( garbosz)")
    print("VER."+ver)
    print("Origin Station: "+Home)

    ##selenium loads data from page
    print("Booting Webdriver")
    driver=webdriver.Chrome('/Downloads/chromedriver_win32/chromedriver')
    driver.implicitly_wait(10)
    print("Loading IB Page")
    try:
        driver.get(IBURL)
        time.sleep(3)
    except:
        print("Unable to load chrome! Check if its installed and using the latest version")
        with open('errorLog.txt', 'a+') as error:  
            error.seek(0, 0) 
            error.write('\n' + 'Chrome Error: '+time.asctime()) 
        time.sleep(10)
        sys.exit('Chrome Error')
    print("finding table in xpath")
    try:
        trailers=driver.find_element("xpath",'//*[@id="dashboard"]')
        print("content found")
        parsed = trailers.text.split()
    except:
        print("FAILED TO FIND DATA ON PAGE")
        trailers=[]
        message="VPN DISCONNECTED\nPlease re submit VPN and restart script to continue"
        parsed=""
        req_res = post_message(message)
        with open('errorLog.txt', 'a+') as error:  
            error.seek(0, 0) 
            error.write('\n' + 'VPN Expired: '+time.asctime()) 
        sys.exit('VPN Expired')
    driver.close()

    ##Process Data Pulled from selenium
    print("Parsing Data from IB")
    #set up array
    VRID=[]
    MANI=[]
    pointer=20
    i=20
    for x in parsed:
        pointer=i
        i=i+1

        try:
            if parsed[pointer]=='Fifty':
                pointer=pointer-1
                VRID.append(parsed[pointer])
                if parsed[pointer+7]=="AZNG":
                    MANI.append(parsed[pointer+9])
                elif parsed[pointer+7]=="[ATS_DEDICATED]":
                    MANI.append(parsed[pointer+8])
                elif parsed[pointer+7].isnumeric():
                    MANI.append(parsed[pointer+7])
                else:
                    MANI.append("Volume Not Found")

            elif parsed[pointer]=='Twenty':
                pointer=pointer-1
                VRID.append(parsed[pointer])
                if parsed[pointer+7]=="AZNG":
                    MANI.append(parsed[pointer+9])
                elif parsed[pointer+7]=="[ATS_DEDICATED]":
                    MANI.append(parsed[pointer+8])
                elif parsed[pointer+7].isnumeric():
                    MANI.append(parsed[pointer+7])
                else:
                    MANI.append("Volume Not Found")

            else:
                i=i
        except:
            print("Done...")
            break

    ##fix non numerical manifests
    print("Repairing Non Numerical Manifests")
    for x in range(0,len(MANI)):
        if MANI[x].isnumeric():
            print("MANI ok")
        else:
            print("Not a Number setting to 0")
            MANI[x]='0'

    ##print array of VRID AND MANI
    print("Parsed VRIDs/Manifests")
    for x in range(0,len(VRID)):
        print(VRID[x]+": "+MANI[x])
    

        
    ##See which trailers are manifested
    print("CHECKING FOR MANIFESTS")
    chimeout=""
    tempmsg=""
    for x in range(0,len(VRID)):
        try:
            print("Checking "+VRID[x])
            if MANI[x]!='0':
                if (VRID[x] in posted):
                    print("Already Notified")
                else:
                    chimeout="New Manifest!"+"\n"+"VRID:"+VRID[x]+"\n"+"Volume:"+MANI[x]
                    posted.append(VRID[x])
                    print("added "+VRID[x]+" To posted list")
                    break
            else:
                print("Not manifested")
        except:
            print("Reached end of list")
        
    ##sample of the current message being posted, if its blank then no message was posted
    print("---MESSAGE---")
    print(chimeout)
    print("---MESSAGE---")

    ## Get the message to send as a parameter
    message = chimeout

    ## Post the message
    print("Posting to Chime")
    req_res = post_message(message)

    #limit length of posted Vrids to 16 to keep memory in check
    if (len(posted)>=17):
        posted.pop(0)
    print("Message posted")
    print("---POSTED VRIDS---")
    print(posted)
    print("---POSTED VRIDS---")

    ##Restart the loop
    lastCheck=time.time()
    print("Time of last Update: "+time.asctime())
    print("waiting 5 minutes")
    t= time.time()-t
    time.sleep(300-t)