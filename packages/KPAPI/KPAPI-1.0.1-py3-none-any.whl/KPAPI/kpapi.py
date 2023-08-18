import requests
import json


class KPAPI:
    def __init__(self, token:str, sender_id:str):
        self.token = token
        self.sender_id = sender_id

    def seen(self):
        params = {"access_token": self.token}
        headers = {"Content-Type": "application/json"}
        data = json.dumps({
            "recipient": {
                "id": self.sender_id
            },
            "sender_action": "mark_seen"
        })

        return requests.post("https://graph.facebook.com/v3.0/me/messages", params=params, headers=headers, data=data).json()

    def sendMessage(self,message:str):
        params = {
            "access_token": self.token
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": self.sender_id
            },
            "message": {
                "text": message
            }
        })
        return requests.post("https://graph.facebook.com/v3.0/me/messages", params=params, headers=headers, data=data).json()

    def sendMedia(self,type:str,url:str):
        params = {"access_token": self.token}
        headers = {"Content-Type": "application/json"}
        data = json.dumps({
            "recipient": {
                "id": self.sender_id
            },
            "message": {
                "attachment": {
                    "type": type,
                    "payload": {
                        "is_reusable": True,
                        "url": url
                    }
                }
            }
        })

        return requests.post("https://graph.facebook.com/v3.0/me/messages",
                             params=params,
                             headers=headers,
                             data=data).json()
    def typingon(self):
        params = {"access_token": self.token}
        headers = {"Content-Type": "application/json"}
        data = json.dumps({
            "recipient": {
            "id": self.sender_id
        },
            "sender_action": "typing_on"
        })

        return requests.post("https://graph.facebook.com/v3.0/me/messages", params=params, headers=headers, data=data).json()
    def typingoff(self):
        params = {"access_token": self.token}
        headers = {"Content-Type": "application/json"}
        data = json.dumps({
            "recipient": {
            "id": self.sender_id
        },
            "sender_action": "typing_off"
        })

        return requests.post("https://graph.facebook.com/v3.0/me/messages", params=params, headers=headers, data=data).json()