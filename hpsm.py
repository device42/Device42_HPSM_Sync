import requests
from requests.auth import HTTPBasicAuth
import json


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
        if self.dry_run == 'True':
            print('--------- Dry Run ---------')
            print('\t Insert item %s/%s ' % (self.api_url, name))
            print('\t %s ' % data)
        elif self.dry_run == 'False':
            try:
                headers = {
                    'Content-Type': 'application/json'
                }

                r = requests.post('%s/%s' % (self.api_url, name), auth=HTTPBasicAuth(self.username, self.password),
                                  headers=headers, payload=json.dumps(data))
                body = r.text
                json_object = json.loads(body)

                if self.debug == "True":
                    print(json_object)
            except Exception as e:
                print(e)
                self.update_item(data, root, name)

    def update_item(self, data, root, name):
        logical_name = data[root]['logical.name'].replace(' ', '%20')
        if self.dry_run == 'True':
            print('\t Update item %s/%s/%s ' % (self.api_url, name, logical_name))
            print('\t %s ' % data)
        elif self.dry_run == 'False':
            headers = {
                'Content-Type': 'application/json'
            }

            r = requests.put('%s/%s/%s' % (self.api_url, name, logical_name),
                             auth=HTTPBasicAuth(self.username, self.password), headers=headers, payload=json.dumps(data))
            body = r.text
            json_object = json.loads(body)

            if self.debug == "True":
                print(json_object)

    def get_d42_items(self, obj_type, name):
        if self.debug == 'True':
            print('\t Get Device42 Items %s/%s ' % (self.api_url, name))

        headers = {
            'Content-Type': 'application/json'
        }

        r = requests.get('%s/%s/?type=%s&view=expand' % (self.api_url, obj_type, name), auth=HTTPBasicAuth(self.username, self.password), headers=headers, verify=False)

        body = r.text
        json_object = json.loads(body)

        if self.debug == "True":
            print(json_object)

        return json_object


