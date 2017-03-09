import urllib2
import base64
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


class HpsmApi:

    def __init__(self, config, options):
        self.username = config['username']
        self.password = config['password']
        self.host = config['host']
        self.protocol = config['protocol']
        self.port = config['port']
        self.api_version = config['api_version']
        self.debug = options['debug']
        self.dry_run = options['dry_run']
        self.api_url = '%s://%s:%s/SM/%s/rest' % (self.protocol, self.host, self.port, self.api_version)

    def insert_item(self, data, root, name):
        if not self.dry_run:
            print '\t Insert item %s/%s ' % (self.api_url, name)

        request = urllib2.Request('%s/%s' % (self.api_url, name), json.dumps(data))
        base64string = base64.b64encode('%s:%s' % (self.username, self.password))
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header("Content-Type", "application/json")
        try:
            r = urllib2.urlopen(request, context=ctx)
            body = r.read()
            r.close()
            json_object = json.loads(body)

            if self.debug:
                print json_object
        except urllib2.HTTPError:
            self.update_item(data, root, name)

    def update_item(self, data, root, name):
        logical_name = data[root]['logical.name'].replace(' ', '%20')
        if not self.dry_run:
            print '\t Update item %s/%s/%s ' % (self.api_url, name, logical_name)

        request = urllib2.Request('%s/%s/%s' % (self.api_url, name, logical_name), json.dumps(data))
        base64string = base64.b64encode('%s:%s' % (self.username, self.password))
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'PUT'
        r = urllib2.urlopen(request, context=ctx)
        body = r.read()
        r.close()
        json_object = json.loads(body)

        if self.debug:
            print json_object

    def get_d42_items(self, obj_type, name):
        if not self.dry_run:
            print '\t Get Device42 Items %s/%s ' % (self.api_url, name)

        request = urllib2.Request('%s/%s/?type=%s&view=expand' % (self.api_url, obj_type, name))
        base64string = base64.b64encode('%s:%s' % (self.username, self.password))
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header("Content-Type", "application/json")
        r = urllib2.urlopen(request, context=ctx)
        body = r.read()
        r.close()
        json_object = json.loads(body)

        if self.debug:
            print json_object

        return json_object


