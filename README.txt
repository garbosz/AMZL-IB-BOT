developed by Zac Garbos (Garbosz)
# INBOUND BOT

inbound bot is a script that will Post newly manifested trailers using data from the AMZL IB page 
it will loop on 5 minute increments and run until host VPN expires

## Installation

follow these steps for first time setup on any computer, after this follow usage instructions for general use of the bot

Step one:
	Creat Webhook for target chime room(https://docs.aws.amazon.com/chime/latest/ug/webhooks.html for instructions on how to do this)
	Copy and paste the webhooks URL into the text file named WEBHOOK-LINK.txt, the link should be the ONLY text in this file
Step two:
	Open Amazon Software center
	Search for "Python"
	click install
step three:
	Double click on SETUP.bat
	click run anyway if windows gives a security warning(its because of file type not because of the content inside, IT can verify that the scripts are safe if necessary)
	once the CMD windows closes the script is now ready to run, follue usage instructions for general use of the bot


## Usage

VPN Computer 

Double click IBnotifier.py to launch script

Webhook should post a message to confirm its working

enjoy!

## Feedback and support

Please Chime @garbosz with any questions comments or concerns
i will respond as soon as i see the message im usually online
WIKI https://w.amazon.com/bin/view/Users/garbosz/Inbound-Bot/

## License

MIT License

Copyright (c) [2022] [Zachary S. Garbos (Garbosz)]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.