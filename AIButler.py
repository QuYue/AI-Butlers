from flask import Flask, request
from Butlers import Butler_Alfred, Butler_WatchDog, Butler_Lucius

Butler_ID={'$:LWCP_v1:$aQhMTAtIgfqDOZ+Y6qsX1hkbm8To5fEd':'Alfred',
           '$:LWCP_v1:$YAVkoEiOgUnV0Gxcho4GJ8UoNh8J7t3x':'看门狗',
           '$:LWCP_v1:$P7hd6Cxkr3W29qYtgC8s+VRClrkPyY4r':'Lucius'}

Alfred = Butler_Alfred()
WatchDog = Butler_WatchDog()
Lucius = Butler_Lucius()

def Butler_name(ID):
    if ID in Butler_ID:
        pass
    else:
        Butler_ID[ID]='Strange Butler'
    return Butler_ID[ID]

app = Flask(__name__)

@app.route('/', methods=['POST'])
def register():
    # print('1:',request.headers)
    # print( request.json)
    sender = request.json['senderNick']
    butler = Butler_name(request.json['chatbotUserId'])
    # print(butler)
    content = request.json['text']['content']
    print(f"{sender}: {content}.")
    if butler == 'Alfred':
        reply = Alfred.implement(content, sender)  
        Alfred.response(reply)
    elif butler == '看门狗':
        reply = WatchDog.implement(content, sender)  
        WatchDog.response(reply)
    elif butler == 'Lucius':
        reply = Lucius.implement(content, sender)  
        Lucius.response(reply)
    elif butler == 'Strange Butler':
        print('Sorry, you are a stranger\n', request.json)
    else:
        print('System: 404 error')
    
    print(f"{butler}: {reply}")
    return 'OK.'



if __name__ == '__main__':
    app.run(port=8000,debug=True)