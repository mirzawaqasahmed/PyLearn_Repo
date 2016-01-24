hostnames = ('SLL-316-115-C3500-ACC-1', 'SLL-316-115-C3500-ACC-2',
             'SLL-311-003-C3500-ACC-5', 'SLL-311-003-C3500-ACC-6',
             'SLL-311-003-C3500-ACC-7', 'SLL-311-056-C3500-ACC-9',
             'SLL-311-056-C3500-ACC-10', 'SLL-314-007-C3500-ACC-12',
             'SLL-314-007-C3500-ACC-13')

def get_device_info(hostname):
    info = {}
    info['Location'] = hostname.split('-')[0]
    info['Building'] = hostname.split('-')[1]
    info['IT Room'] = hostname.split('-')[2]
    info['Model'] = hostname.split('-')[3]
    info['Role'] = hostname.split('-')[4]
    info['# of Switch'] = hostname.split('-')[5]
#    print info
    return info

for h in hostnames:
    info = get_device_info(h)
    print "Hostname = %s" % h
    print "Location =  %s" % info['Location']
    print "Building =  %s" % info['Building']
    print "IT Room =  %s" % info['IT Room']
    print "Model =  %s" % info['Model']
    print "Role =  %s" % info['Role']
    print "# of Switch =  %s" % info['# of Switch']
