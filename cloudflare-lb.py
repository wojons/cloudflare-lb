#!/usr/bin/env python

import json
import urllib
import time
import random

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

def call_api(params):
    go = urllib.urlopen("https://www.cloudflare.com/api_json.html", params)
    return go.read()
    
def get_recs():
    print "\nGetting data from CloudFlare"
    rec = json.loads(call_api(urllib.urlencode({'a': 'rec_load_all', 'tkn': API, 'email': EMAIL, 'z': DOMAIN})))
    if rec['result'] == "success":
        return rec['response']['recs']['objs']
    else:
        return False
        
def del_rec(rec_id, host):
    result = json.loads(call_api(urllib.urlencode({'a': 'rec_delete', 'tkn': API, 'email': EMAIL, 'z': DOMAIN, 'id': rec_id})))
    if result['result'] == 'success':
        print 'Removing:' +host
    else:
        print 'Remove Failed: '+host+'. '+result['msg']
        
def add_rec(rec):
    result_add = json.loads(call_api(urllib.urlencode({'a': 'rec_new', 'tkn': API, 'email': EMAIL, 'z': DOMAIN, 'name': RECORD, 'content': rec[0], 'type': rec[1], 'ttl': 1})))
    if result_add['result'] == 'success':
        result_edit = json.loads(call_api(urllib.urlencode({'a': 'rec_edit', 'tkn': API, 'email': EMAIL, 'z': DOMAIN, 'name': RECORD, 'content': rec[0], 'type': rec[1], 'ttl': 1, 'id': result_add['response']['rec']['obj']['rec_id'], 'service_mode': 1})))
        if result_edit['result'] == 'success':
            print 'Adding: '+rec[0]
            return True
        else:
            del_rec(result_add['response']['rec']['obj']['rec_id'], rec) #faild to orange cloud
            print 'Add Failed: {0}. {1}'.format(rec[0], result_edit['msg'])
            return False
    
    print 'Add Failed: {0}. {1}'.format(rec[0], result_add['msg'])
    return False

def healthcheck(host):
    try:
        run = urllib.urlopen("{0}://{1}:{2}/".format(PROTO, host[0], str(PORT)))
        if get_rec_id(RECORD, host[0]) == False: #needs to be added
            add_rec(host)
        else:
            print host[0]+': Passed'
    except IOError: #we were not able to do what was needed
        rec_id = get_rec_id(RECORD, host[0]) #get the id of the record
        if rec_id is not False:
            print host[0]+': Removing Host'
            del_rec(rec_id, host[0])
        else:
            print host[0]+': Still dead'
            
def get_rec_id(name, host):
    for y in RECS:
        if y['display_name'] == name and y['content'] == host and (y['type'] == "A" or y['type'] == "AAAA"):
            return y['rec_id']
    return False

if __name__=="__main__":
    while True:
        RECS, start_time = get_recs(), time.time()
        random.shuffle(HOSTS)
        
        for host in HOSTS:
            healthcheck(host)
        
        if INTERVAL >= 0:
            lapse = int(time.time() - start_time)
            print "DONE: sleeping for {0} seconds".format(str(INTERVAL-lapse))
            time.sleep(INTERVAL-lapse) #sleep for some set time seconds
        else:
            exit()
