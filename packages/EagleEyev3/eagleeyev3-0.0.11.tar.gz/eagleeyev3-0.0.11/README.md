# EagleEyev3 #

## Summary ##
This is a python package for working with the Eagle Eye Networks APIv3.  It takes some liberties with the API to make it more pythonic.  There is plenty of sugar sprinkled in to make it a little easier to use.

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
