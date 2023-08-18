# EagleEyev3 #

## Summary ##
This is a python package for working with the Eagle Eye Networks APIv3.  It takes some liberties with the API to make it more pythonic.  There is plenty of sugar sprinkled in to make it a little easier to use.

## Getting Started ##


Start by import the package and the config from settings (see the Settings File section below)

```
from EagleEyev3 import *
from settings import config
```

Make a new instance

```
een = EagleEyev3(config)
```


If you are going to use the Oauth2 login flow, construct the login url

```
base_url     =  "https://auth.eagleeyenetworks.com/oauth2/authorize"
path_url     =  f"?client_id={een.client_id}&response_type=code&scope=vms.all&redirect_uri={een.redirect_uri}"
login_url    =  f"{base_url}{path_url}"  }
``` 

Handle the callback from Oauth2 including the code, proceed to get access and refresh tokens

```
oauth_object = een.login_tokens(code)
```

You'll probably want to get a list of cameras

```
een.get_list_of_cameras()
```

There are helpers to get online cameras

```
[i for i in een.cameras if i.is_online()]
```

and offline

```
[i for i in een.cameras if i.is_offline()]
```

You can get a live preview image

```
camera.get_live_preview()
```

You can get a list of all feeds
```
een.get_list_of_feeds()
```



## Settings File ##
There is file `settings.py` that is needed to run.  It should look similar to this:

```
config = {

	# Set up your application and get client id/secrete first
	# https://developerv3.eagleeyenetworks.com/page/my-application
	"client_id": "",
	"client_secret": "",

	# you will need to add approved redirect_uris in your application
	# this examples assumes you've added http://127.0.0.1:3333/login_callback
	# change the following variables if you did something different
	# Note: do not use localhost for server_host, use 127.0.0.1 instead
	"server_protocol": "http",
	"server_host": "127.0.0.1", 
	"server_port": "3333",
	"server_path": "login_callback",
}
```

You can create your application and setup credentials at: [https://developerv3.eagleeyenetworks.com/page/my-application-html](my applications).  You can also reach out to api_support@een.com for help.
