import urllib2, sys, sets
import json


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

def get_userids(usernames):
    batches = split_list_by(usernames, MAX_TERM_ALLOWED)
    userids = []
    for batch in batches:
        url = URL+','.join(batch)
        print url
        f = urllib2.urlopen(url)
        j = json.loads(f.read())
        userids = userids + map(lambda x:x['id'] ,j)
        found = sets.Set(map(lambda x:x['screen_name'].lower(), j))
        print "missing" + str(sets.Set(map(lambda x:x.lower(), batch)) - found)
        f.close()
    print userids
    return userids

def get_userids_file(infile):
    inh = open(infile,'r')
    unames = []
    for ln in inh:
        s = ln.strip('\r\n"')
        unames.append(s)
    inh.close()
    uids = get_userids(unames)
    return uids


def get_terms_file(infile):
    inh = open(infile,'r')
    terms = []
    for ln in inh:
        s = ln.strip('\r\n"')
        terms.append(s.lower())
    inh.close()
    return terms


def split_list_by(l,n):
    rounds = len(l) / n
    result = []
    for i in range(0,rounds+1):
        if i*n < len(l):
            result.append(l[i*n:(i+1)*n])
    return result
