from flask import *
from twilio.rest import Client
import random

app = Flask(__name__)
app.secret_key = 'otp' #Very very secret

@app.route('/') #URL Pattern
def home():
    return render_template('login.html')

@app.route('/getOTP', methods = ['POST'])
def getOTP():

    number = request.form['number']
    val = getOTPApi(number)
    if val:
        return render_template('enterOTP.html')

@app.route('/validateOTP',methods = ['POST'])
def validateOTP():
    otp = request.form['otp']
    if 'response' in session:
        s = session['response']
        session.pop('response',None)
        if s == otp:
            return 'OTP VERIFIED'
        else:
            return 'INCORRECT OTP '

def generateOTP():
    return random.randrange(100000,999999)

def getOTPApi(number):
    account_sid = 'ACffcf2ddea75997740f01ec7d238f3b44'
    auth_token = '53b87011cdc8e2bf232b3453929fd0ba'
    client = Client(account_sid, auth_token)
    otp = generateOTP()
    session['response'] = str(otp)
    body = 'Your OTP is ' + str(otp)
    session['response'] = str(otp)
    message = client.messages.create(
                              from_='+18624200141',
                              body=body,
                              to=number
                          )
    if message.sid:
        return True
    else:
        False

if __name__ == '__main__':
    app.run(debug = True)