cloudflare-lb
=============

Use cloudflare as a load balancer!!! This is a very simple roundrobin load balancer using the cloudflre api to add and remove nodes from a pool. This code base does support a healthcheck to make sure the node is avaiable but your milage may varr depending on the type of aviaablity checking you need.

Requirments
===========
* A domain name on cloudflare.com
* A cloudflare api key (comes with the account)
* More then 1 ip address pointing to ur site.
* Linux host with python (2.7+ tested 2.5+ should work, sorry i dont think python 3 will work)

Setup
=====
```python
HOSTS    = [
            ['127.0.0.1', 'A'], 
            ['127.0.0.2', 'A'], 
            ['127.0.0.3', 'A'], 
            ['127.0.0.4', 'A'], 
            ['127.0.0.5', 'A']
           ] # Your A/AAAA value, i.e. 192.168.1.10
PROTO    = 'http'                 # http or https
PORT     = 80                     #Defaults to port 80
API      = ''                     # Your CloudFlare client API key found at https://www.cloudflare.com/my-account
EMAIL    = 'example@example.com'  # Your CloudFlare email address
RECORD   = 'lb'                   # where you want the load balancer
DOMAIN   = 'example.com'          # Use DOMAIN if this is for the root domain
TTL      = 1                      # Set TTL
RECS     = []                     # RECORDS
INTERVAL = 60                     #how long we wait between runs
```
* Simple add all the A or AAAA records for the backend servers you want cloudflare to point a record to.
* Select which protocol and port you want the health check to run on http or https.
* Provide your cloudflare api key and email address of that cloudflare account.
* By default its going to try to add your load balancer to lb.example.com you may change this. If you want it to be the root domain use '@'.
* Select the ttl you want the records to have I dont know if this needs to be anything but 1 ince its going to be cloudflre orange cloud meaning cloudflare will proxy it. If you wanna know more about that visit the cloudflare client api.
* The RECS variable should be left blank.
* INTERVAL is how often you want the script to run. I found 60 seconds pretty safe number depending on your needs you may want it faster or slower but not sure if cloudflre will rate limit your api access if you go overboard.

Running
=======
$ python cloudflare-lb.py

That will kick the script off it does log things to stdout. You may wanna just point it to /dev/null if you dont care or a file or something for your records. It does not run as a service but if you use a processes manaager like supervsor. If you want to run this in crontab. Set INTERVAL = 0. This will cause the program to not run in a loop.

Issues
======
* In the event that all of your nodes are marked unreachable the record would be removed from cloudflare and if gone long enough it would not point to cloudflare at all meaning when adding the records in again it will need to proigate. 
