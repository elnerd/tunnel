A raw tcp forwarded to debug issues with Outflank Agent via webshells.

Usage:



1. ./server.py 127.0.0.1 4242 

Listen on 127.0.0.1:4242 for client.py to connect to it

2./client.py 127.0.0.1 9999 127.0.0.1 4242 94.130.221.94 23

Listens on 127.0.0.1:9999, will connect to 127.0.0.1:4242 and instruct it to connect to 94.130.221.94 on port 23
All data will now be proxied through the server.py.

3. telnet 127.0.0.1 9999

You should not be able to reach 94.130.221.94 on port 23 via the server.py proxy.




