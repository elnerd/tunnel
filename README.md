# Tunnel

An experimental setup to test out forwarding TCP socket over a HTTP webshell.

Usage:


1. Start flask_server. It will by default listen on port 5000

```
python3 webshell/flask_server.py
```

2. Start the client. It will by default listen on port 9999

```
python3 client/client.py

```

3. Connect to the client listener on port 9999

```
telnet 127.0.0.1 9999
```

How it works:

     ┌─────────────────┐                                                        
     │application      │                                                        
     │                 │                                                        
     │                 │  TCP   ┌───────────┐HTTP┌────────────┐ TCP┌────────┐   
     │                 │        │client     │    │ webshell   │    │Target  │   
     │                 │ ─────► │LISTEN 9999│ ──►│ LISTEN 5000├───►│        │   
     │                 │        │           │    │            │    │        │   
     │                 │        └───────────┘    └────────────┘    └────────┘   
     │                 │                                                        
     │                 │                                                        
     │                 │                                                        
     └─────────────────┘                                                        

# TODO

The purpose of this project is to make a reference implementation that works really well.

A flask server is not particularly useful webshell.

- [ ] Create ASPX and ASHX webshell compatible with `client.py`