# KPAPI

Optimize the use of Facebook API

## Install
```shell
pip install KPAPI
```

### Usage

```python
from KPAPI import KPAPI
kpapi=KPAPI(Access_token,sender_id)

#Send message to users
kpapi.sendMessage("Message")

#Send media
kpapi.sendMedia("audio/video/image",url_media)

#Seen action
kpapi.seen()

#Typing On action
kpapi.typingon()

#Typing Off action
kpapi.typingoff()
```

