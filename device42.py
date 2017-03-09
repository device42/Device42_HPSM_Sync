import base64
import urllib2
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


class Device42Doql:
    def __init__(self, config, options):
        self.username = config['username']
        self.password = config['password'] if config['password'] else ''
        self.host = config['host']
        self.debug = options['debug']
        self.dry_run = options['dry_run']

    def _getter(self, url):
        request = urllib2.Request(url)
        base64string = base64.b64encode('%s:%s' % (self.username, self.password))
        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header("Content-Type", "application/json")
        r = urllib2.urlopen(request, context=ctx)
        body = r.read()
        r.close()

        if self.debug:
            msg1 = 'Status code: %s' % str(r.code)
            msg2 = str(r.msg.encode('utf-8'))

            print '\n\t----------- GET FUNCTION -----------'
            print '\t' + url
            print '\t' + msg1
            print '\t' + msg2
            print '\t------- END OF GET FUNCTION -------\n'

        return body

    def get_devices(self):
        url = 'https://%s/services/data/v1.0/query/?query=SELECT ' \
              'device_pk, name, type, in_service, service_level, virtual_host, ' \
              'hard_disk_size, network_device, ' \
              'asset_no, serial_no, notes, os_version_no, os_fk, hardware_fk ' \
              'FROM view_device_v1&header=yes' % self.host
        msg = '\tGet request to %s ' % url
        if not self.dry_run:
            print msg
        return self._getter(url)

    def get_hardware(self, value):
        url = "https://%s/services/data/v1.0/query/?query=SELECT " \
              "name, vendor_fk " \
              "FROM view_hardware_v1 " \
              "WHERE hardware_pk='%s'&header=yes" \
              % (self.host, value)
        msg = '\tGet request to %s ' % url
        if not self.dry_run:
            print msg
        return self._getter(url)

    def get_vendor(self, value):
        url = "https://%s/services/data/v1.0/query/?query=SELECT " \
              "name " \
              "FROM view_vendor_v1 " \
              "WHERE vendor_pk='%s'&header=yes" \
              % (self.host, value)
        msg = '\tGet request to %s ' % url
        if not self.dry_run:
            print msg

        return self._getter(url)

    def get_os(self, value):
        url = "https://%s/services/data/v1.0/query/?query=SELECT " \
              "name, vendor_fk " \
              "FROM view_os_v1 " \
              "WHERE os_pk='%s'&header=yes" \
              % (self.host, value)
        msg = '\tGet request to %s ' % url
        if not self.dry_run:
            print msg
        return self._getter(url)

    def get_subnet(self, value):
        url = "https://%s/services/data/v1.0/query/?query=SELECT " \
              "name " \
              "FROM view_subnet_v1 " \
              "WHERE subnet_pk='%s'&header=yes" \
              % (self.host, value)
        msg = '\tGet request to %s ' % url
        if not self.dry_run:
            print msg
        return self._getter(url)

    def get_macs(self, value):
        url = "https://%s/services/data/v1.0/query/?query=SELECT " \
              "hwaddress " \
              "FROM view_netport_v1 " \
              "WHERE device_fk='%s' and hwaddress != ''&header=yes" \
              % (self.host, value)
        msg = '\tGet request to %s ' % url
        if not self.dry_run:
            print msg
        return self._getter(url)

    def get_ips(self, value):
        url = "https://%s/services/data/v1.0/query/?query=SELECT " \
              "ip_address, subnet_fk " \
              "FROM view_ipaddress_v1 " \
              "WHERE device_fk='%s'&header=yes" \
              % (self.host, value)
        msg = '\tGet request to %s ' % url
        if not self.dry_run:
            print msg
        return self._getter(url)



