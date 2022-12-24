import json
import requests
import sys
import time
from os import system
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

posted=[]
ver="1.11"
Home="DBO6"
system("title "+"InBound Notifier")
x=0
with open('WEBHOOK-LINK.txt','r') as f:
    file=f.read()

##grab related URLs as actionable variables
#Grab webhook URL from file
WEBHOOK_URI=file
if file=='placeholder':
    print("You Did Not setup the Webhook! Please enter your webhook URL into WEBHOOK-LINK.txt to continue")
    time.sleep(10)
    # with open('Error Log.txt', 'r+') as file:  
    #     file.seek(0, 0) 
    #     file.write('\n' + 'Webhook not provided'+time.asctime()) 
    sys.exit('Webhook Not Provided')
elif "https://hooks.chime.aws/incomingwebhooks" is not file:
    print("Provided Webhook link is Invalid")
    time.sleep(10)
    sys.exit('Invalid Webhook')

#testing webhook
#WEBHOOK_URI = 'https://hooks.chime.aws/incomingwebhooks/9be51f5c-cf60-4f5a-bfe5-869f54fa9b11?token=QnBTOTZFY0R8MXx6MllJZEtPU2ZGeVg3Z0xGQmtVX2NYV18xc1lXNEYyOWt2cVVXVzQyQ19V'
IBURL= 'https://trans-logistics.amazon.com/ssp/dock/ib/'

##posting setup message
##Connect to webhook
print("Connecting to Webhook")
def post_message(msg):
    response = None
    try:
        response = requests.post(
            url=WEBHOOK_URI,
            json={"Content": msg})
        return json.loads(response.text)
    except:
        return "Fix your webhook loser"

##Load webpage to scrape
response=requests.get(IBURL, verify=False)
#print(response.text)
print("connected")

## Get the message to send as a parameter
message = "INBOUND BOT Initiated\nVer."+ver+"\nScript will now process through any current manifests\nChecks will happen in 5 minute increments and will run until host systems VPN expires\nStarted @ "+time.asctime()

## Post the message
print("Posting")
req_res = post_message(message)

##Main Loop
while True:
    t= time.time()


    ##reset vars for this loop
    system('cls')
    print()
    print("INBOUND NOTIFIER")
    print("Developed by Zac Garbos( garbosz)")
    print("VER."+ver)
    print("Origin Station: "+Home)

    ##selenium loads data from page
    print("selecting URL")
    driver=webdriver.Chrome('/Downloads/chromedriver_win32/chromedriver')
    #print("opening URL")
    driver.get(IBURL)
    time.sleep(4)
    print("finding table in xpath")
    try:
        trailers=driver.find_element("xpath",'//*[@id="dashboard"]')
        print("content loaded")
        print("parsing data")
        parsed = trailers.text.split()
    except:
        trailers=[]
        message="VPN DISCONNECTED\nPlease re submit VPN and restart script to continue"
        parsed=""
        req_res = post_message(message)
        sys.exit('VPN Expired')
    #print(parsed)
    driver.close()

    ##Process Data
    #set up array
    VRID=[]
    MANI=[]
    #data=[]
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
            print("end of file")
            break

    ##fix non numerical manifests
    print("Repairing Non Numerical Manifests")
    for x in range(0,len(MANI)):
        if MANI[x].isnumeric():
            print("MANI ok")
        else:
            print("Not a Number setting to 0")
            MANI[x]='0'

    ##testing spot print array of VRID AND MANI
    print("Found VRIDs/Manifests")
    for x in range(0,len(VRID)):
        print(VRID[x]+": "+MANI[x])
    

        
    ##See which trailers are manifested
    print("CHECKING MANIFESTS")
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
        
    print("---MESSAGE---")
    print(chimeout)
    print("---MESSAGE---")

    ##Load webpage to scrape
    response=requests.get(IBURL, verify=False)
    #print(response.text)
    print("connected")

    ## Get the message to send as a parameter
    message = chimeout

    ## Post the message
    print("Posting")
    req_res = post_message(message)
    #print(json.dumps(req_res, indent=2))
    #limit length of posted Vrids to 16 to keep memory in check
    if (len(posted)>=17):
        posted.pop(0)
    print("Message posted")
    print("---POSTED VRIDS---")
    print(posted)
    print("---POSTED VRIDS---")

    ##Restart the loop
    print(time.asctime())
    print("waiting 5 minutes from last update")
    t= time.time()-t
    time.sleep(300-t)