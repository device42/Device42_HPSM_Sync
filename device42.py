import requests
from requests.auth import HTTPBasicAuth


class Device42Doql:
    def __init__(self, config, options):
        self.username = config['username']
        self.password = config['password'] if config['password'] else ''
        self.host = config['host']
        self.verify_ssl = config['verify_ssl']
        self.debug = options['debug']
        self.dry_run = options['dry_run']

    def _getter(self, url):
        headers = {
            'Content-Type': "application/json"
        }

        try:
            r = requests.get(url, auth=HTTPBasicAuth(self.username, self.password), headers=headers,
                             verify=self.verify_ssl)
            resp = r.text

            if self.debug:
                msg1 = 'Status code: %s' % str(r.status_code)
                msg2 = str(r.text.encode('utf-8'))

                print('\n\t----------- GET FUNCTION -----------')
                print('\t' + url)
                print('\t' + msg1)
                print('\t' + msg2)
                print('\t------- END OF GET FUNCTION -------\n')

        except Exception as e:
            print(e)
            resp = ""

        return resp

    def get_devices(self):
        url = '%s/services/data/v1.0/query/?query=SELECT ' \
              'device_pk, name, type, in_service, service_level, virtual_host, ' \
              'hard_disk_size, network_device, ' \
              'asset_no, serial_no, notes, os_version_no, os_fk, hardware_fk ' \
              'FROM view_device_v1&header=yes' % self.host
        msg = '\tGet request to %s ' % url
        if self.debug:
            print("----- Get Devices ----- ")
            print(msg)
        return self._getter(url)

    def get_hardware(self, value):
        url = "%s/services/data/v1.0/query/?query=SELECT " \
              "name, vendor_fk " \
              "FROM view_hardware_v1 " \
              "WHERE hardware_pk='%s'&header=yes" \
              % (self.host, value)
        msg = '\tGet request to %s ' % url
        if self.debug:
            print("----- Get Hardware ----- ")
            print(msg)
        return self._getter(url)

    def get_vendor(self, value):
        url = "%s/services/data/v1.0/query/?query=SELECT " \
              "name " \
              "FROM view_vendor_v1 " \
              "WHERE vendor_pk='%s'&header=yes" \
              % (self.host, value)
        msg = '\tGet request to %s ' % url
        if self.debug:
            print("----- Get Vendor ----- ")
            print(msg)

        return self._getter(url)

    def get_os(self, value):
        url = "%s/services/data/v1.0/query/?query=SELECT " \
              "name, vendor_fk " \
              "FROM view_os_v1 " \
              "WHERE os_pk='%s'&header=yes" \
              % (self.host, value)
        msg = '\tGet request to %s ' % url
        if self.debug:
            print("----- Get OS ----- ")
            print(msg)
        return self._getter(url)

    def get_subnet(self, value):
        url = "%s/services/data/v1.0/query/?query=SELECT " \
              "name " \
              "FROM view_subnet_v1 " \
              "WHERE subnet_pk='%s'&header=yes" \
              % (self.host, value)
        msg = '\tGet request to %s ' % url
        if self.debug:
            print("----- Get Subnet Name ----- ")
            print(msg)
        return self._getter(url)

    def get_macs(self, value):
        url = "%s/services/data/v1.0/query/?query=SELECT " \
              "hwaddress " \
              "FROM view_netport_v1 " \
              "WHERE device_fk='%s' and hwaddress != ''&header=yes" \
              % (self.host, value)
        msg = '\tGet request to %s ' % url
        if self.debug:
            print("----- Get MAC ----- ")
            print(msg)
        return self._getter(url)

    def get_ips(self, value):
        url = "%s/services/data/v1.0/query/?query=SELECT " \
              "ip_address, subnet_fk " \
              "FROM view_ipaddress_v1 " \
              "WHERE device_fk='%s'&header=yes" \
              % (self.host, value)
        msg = '\tGet request to %s ' % url
        if self.debug:
            print("----- Get IPS ----- ")
            print(msg)
        return self._getter(url)



