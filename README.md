[![CircleCI](https://circleci.com/gh/yamsergey/pyautoproxy.svg?style=svg&circle-token=a3ff3d7f5da08b8af00e14b5f704d375855f5685)](https://circleci.com/gh/yamsergey/pyautoproxy) [![PyPI version](https://badge.fury.io/py/pyautoproxy.svg)](https://badge.fury.io/py/pyautoproxy)

## State 
In active development. It's in experiment state now

# Python AutoProxy

`pyautoproxy` helps to configure your proxy for developemnt purpose.
When you work with some proxy and have to validate traffic quite often it really annoying to reconfigure a device to use proxy when needed and when not to.

To make life a bit easier we can use Proxy [Auto-Config](https://en.wikipedia.org/wiki/Proxy_auto-config). But problem with it is that most of http clients expect it to be on some server and response from that server should have proper headers, hence we can't use just a file on local machine.  Also Different devices require different proxy config time by time.

This app can solve the issue above. It's simple http server which now start serve on specified port and return correct `Auto-Config` based on query parameters.

### Usge 

Install
```
pip install pyautoproxy
```

Run the server:
```
pyautoproxy --port 8081
```

For exanple, request to [http://localhost:8081?host=localhost&port=8080](http://localhost:8081/?host=localhost&port=8080) will return
```
function FindProxyForURL(url, host)
{
    return "PROXY localhost:8080; DIRECT";
}

```

Which means that when proxy on `localhost:8080` is available a client will try use it, but when you turn it off it will bypass proxy and use direct connections.

### iOS simulator

iOS simulator requires configure your Mac OS to use the proxy, which really annoying. But when you start `pyautoproxy` as
```
pyautoproxy -s
``` 

It will filter all requests except requests from iOS, hence all you machine traffic won't go through the proxy.  
#### Configure for Android Emulator
From emulator you can always refer to host machine with ip `10.0.2.2`. Usual link for `Auto-Proxy` config on Android will looks like `http://10.0.2.2:8081/?host=10.0.2.2&port=8080` 


### Configure proxy type

By default, proxy corresponding to the protocol of the original request, be it http, https, or ftp, is used.

If you want to change it, just add `proxy` parameter to the Auto-Config URL e.g.:
```
http://localhost:8081/?host=localhost&port=8080&proxy=SOCKS5

// Will return

function FindProxyForURL(url, host)
{
    return "SOCKS5 localhost:8080; DIRECT";
}
```