import requests 

class Errors:
    def emptyToken(__value):
        if __value == None:
            raise ValueError("The Token cannot be Empty")
        else:pass
        
    def emptyParams(__values : list):
        for _v in __values:
            if _v == None:
                raise ValueError(f"The {_v} cannot be Empty")
            else:pass
            

class TeleCore:
    def __init__(self, BotToken : str, printData : False = None) -> None:
        self.token = str(BotToken)
        self.api = f"https://api.telegram.org/bot{self.token}"
        self.printData = printData
        self.header = {'Content-Type': 'Application/json', 'Accept': 'Application/json'}
        
    def sendMessage(self, text : str = None, chatID : str = None, messageID : str = None, parseMode : str = None):
        Errors.emptyToken(self.token)
        Errors.emptyParams([text , chatID])
        if (self.printData == False or self.printData == None):
            return requests.post(f"{self.api}/sendMessage?chat_id={chatID}&text={text}&reply_to_message_id={messageID if not messageID == None else ''}&parse_mode={parseMode if not parseMode == None else ''}",headers=self.header).json() 
            
        elif self.printData == True:
            print(f"token: {self.token}")
            print(f"api: {self.api}")
            print(f'method: sendMessage')
            print(f"header: {self.header}")
            print(f'text: {text}')
            print(f'chat id: {chatID}')
            print(f'message id: {messageID}')
            print(f'parseMode: {parseMode}')

            return requests.post(f"{self.api}/sendMessage?chat_id={chatID}&text={text}&reply_to_message_id={messageID if not messageID == None else ''}&parse_mode={parseMode if not parseMode == None else ''}", headers=self.header).json()
       
    def getMe(self):
        Errors.emptyToken(self.token)
        if (self.printData == False or self.printData == None):
            while 1:
                try:
                    return requests.post(f"{self.api}/getMe", headers=self.header).json()
                    break
                except Exception as e: 
                    return e
                    break
                
        else:
            print(f"token: {self.token}")
            print(f"api: {self.api}")
            print(f'method: getMe')
            print(f"header: {self.header}")
            while 1:
                try:
                    return requests.post(f"{self.api}/getMe", headers=self.header).json()
                    break
                except Exception as e: 
                    return e
                    break
            
    def forwardMessage(self, chatID : str = None, fromChatID : str = None, messageID : str = None):
        Errors.emptyToken(self.token)
        Errors.emptyParams([chatID, fromChatID, messageID])
        if (self.printData == False or self.printData == None):
            while 1:
                try:
                    return requests.post(f"{self.api}/forwardMessage?chat_id={chatID}&from_chat_id={chatID}&message_id={messageID}", headers=self.header).json()
                    break
                except Exception as e:
                    return e 
                    break
                
        else:
            print(f"token: {self.token}")
            print(f"api: {self.api}")
            print(f'method: forwardMessage')
            print(f"header: {self.header}")
            print(f'chat id: {chatID}')
            print(f'from chat id: {fromChatID}')
            print(f'message id: {messageID}')
            while 1:
                try:
                    Data = {
                        "chat_id" : chatID,
                        'from_chat_id' : fromChatID,
                        'message_id' : messageID
                    }
                    return requests.post(f"{self.api}/forwardMessage", data=Data, headers=self.header).json()
                    break
                except Exception as e:
                    return e 
                    break
                
    def getUpdates(self):
        Errors.emptyToken(self.token)
        if (self.printData == False or self.printData == None):
            while 1:
                try:
                    return requests.post(f"{self.api}/getUpdates", headers=self.header).json()
                    break
                except Exception as e:
                    return e 
                    break
        
        else:
            print(f"token: {self.token}")
            print(f"api: {self.api}")
            print(f'method: getUpdates')
            print(f"header: {self.header}")
            while 1:
                try:
                    return requests.post(f"{self.api}/getUpdates", headers=self.header).json()
                    break
                except Exception as e:
                    return e 
                    break
                
    def sendPhoto(self, pathOfPhotoOrNamePhoto : str = None, chatID : str = None, messageID : str = None, caption : str = None):
        Errors.emptyToken(self.token)
        Errors.emptyParams([chatID, pathOfPhotoOrNamePhoto])
        while 1:
            try:
                return requests.post(f"{self.api}/sendPhoto?file_id={pathOfPhotoOrNamePhoto}&chat_id={chatID}&caption={caption if not caption == None else ''}&reply_to_message_id={messageID if not messageID == None else ''}").json()
            except Exception as er2:
                return er2
            
    
    def sendAudio(self, pathOfAudioOrNameAudio : str = None, chatID : str = None, messageID : str = None, caption : str = None):
        Errors.emptyToken(self.token)
        Errors.emptyParams([pathOfAudioOrNameAudio, chatID])
        while 1:
            try:
                return requests.post(f"{self.api}/sendAudio?file_id={pathOfAudioOrNameAudio}&chat_id={chatID}&caption={caption if not caption == None else ''}&reply_to_message_id={messageID if not messageID == None else ''}").json()
            except Exception as er3:
                return er3 
            
    def sendDocument(self, pathOfDocOrNameOfDoc : str = None, chatID : str = None, messageID : str = None, caption : str = None):
        Errors.emptyToken(self.token)
        Errors.emptyParams([pathOfDocOrNameOfDoc, chatID])
        while 1:
            try:
                return requests.post(f"{self.api}/sendDocument?file_id={pathOfDocOrNameOfDoc}&chat_id={chatID}&caption={caption if not caption == None else ''}&reply_to_message_id={messageID if not messageID == None else ''}").json()
            except Exception as er4:
                return er4 
    
    def sendVideo(self, pathOfVideoOrNameOfVideo : str = None, chatID : str = None, messageID : str = None, caption : str = None):
        Errors.emptyToken(self.token)
        Errors.emptyParams([pathOfVideoOrNameOfVideo, chatID])
        while 1:
            try:
                return requests.post(f"{self.api}/sendVideo?chat_id={chatID}&file_id={pathOfVideoOrNameOfVideo}&reply_to_message_id={messageID if not messageID == None else ''}&caption={caption if not caption == None else ''}").json()
            except Exception as er5:
                return er5
            
    def sendVoice(self, pathOfVoiceOrNameOfVoice : str = None, chatID : str = None, messageID : str = None, caption : str = None):
        Errors.emptyToken(self.token)
        Errors.emptyParams([pathOfVoiceOrNameOfVoice, chatID])
        while 1:
            try:
                return requests.post(f"{self.api}/sendVoice?file_id={pathOfVoiceOrNameOfVoice}&chat_id={chatID}&caption={caption if not caption == None else ''}&reply_to_message_id={messageID if not messageID == None else ''}").json()
            except Exception as er6:
                return er6
            
    
            