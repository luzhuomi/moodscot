import urllib2, sys, sets
import json
#from mongomodel.crawl.twitter.models import ScreenNameCache,init
#import pymongo

from twython import Twython, TwythonError


MAX_TERM_ALLOWED = 75


def read_cred(file):
    in_handle = open(file,'r')
    cred = {}
    for ln in in_handle:
        data = ln.strip('\r\n').split('=')
        if len(data) > 1:
            key = data[0].strip(' ').lower()
            value = data[1].strip(' ')
            cred[key] = value
        else:
            print "error in parsing credentials file"
    return cred

URL = "https://api.twitter.com/1/users/lookup.json?include_entities=true&screen_name="
'''
def get_userids(cred,usernames):
    print "usernames" + str(usernames)
    batches = split_list_by(usernames, MAX_TERM_ALLOWED)
    userids = []
    notfound = []
    for batch in batches:
        #url = URL+','.join(batch)
        #print url
        try:
            #f = urllib2.urlopen(url)
            #j = json.loads(f.read())
            twitter = Twython(cred['consumer_key'], cred['consumer_secret'],
                              cred['access_token_key'], cred['access_token_secret'])
            j = twitter.lookup_user(screen_name=batch)
            userids = userids + map(lambda x:x['id'] ,j)
            found = sets.Set(map(lambda x:x['screen_name'].lower(), j))
            for x in j:
                print "caching"
                print ((x['screen_name'], x['id']))
                cache_userid(x['screen_name'], x['id'])
            # f.close()
        except Exception as e:
            print "connection refused" + str(e)
            found = sets.Set([])
        notfound_this_round = sets.Set(map(lambda x:x.lower(), batch)) - found
        print "missing" + str(notfound_this_round)
        notfound = notfound + list(notfound_this_round)
    print userids
    return (userids, notfound)

def get_cached_userids(usernames):
    found = []
    not_found = []
    for n in usernames:
        cs = ScreenNameCache.objects.filter(screenname = n)
        if len(cs) > 0:
            c = cs[0]
            found.append(c.tid)
        else:
            not_found.append(n)
    return { 'found' : found, 'not_found' : not_found }

def cache_userid(name,id):
    c = ScreenNameCache(screenname = name, tid = id)
    c.save()

def get_userids_file(cred,infile):
    inh = open(infile,'r')
    unames = []
    for ln in inh:
        s = ln.strip('\r\n"').replace(' ','%20')
        unames.append(s)
    inh.close()
    db = init()
    cache_result = get_cached_userids(unames)
    found = cache_result['found']
    not_found = cache_result['not_found']
    print "found %d in cache" % (len(found))
    print "looking for %d from API" % (len(not_found))
    (uids,not_found_still) = get_userids(cred,not_found)
    ofh = open(infile + '.notfound', 'w')
    for n in not_found_still:
        print >> ofh, n
    ofh.close()
    if hasattr(db,'disconnect'):
        db.disconnect()
    else:
        db.connection.disconnect()
    return (found+uids)
'''

def split_list_by(l,n):
    rounds = len(l) / n
    result = []
    for i in range(0,rounds+1):
        if i*n < len(l):
            result.append(l[i*n:(i+1)*n])
    return result

