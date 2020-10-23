# -*- coding:utf-8 -*-
import configparser
import csv
from io import StringIO
from hpsm import HpsmApi
from device42 import Device42Doql

config = configparser.ConfigParser()
config.read('conf.cfg')

device42 = {
    'host': config["Device42"]["d42_host"],
    'username': config["Device42"]["d42_username"],
    'password': config["Device42"]["d42_password"],
    'verify_ssl': config["Device42"].getboolean("d42_verify_ssl")
}

hpsm = {
    'host': config["HPSM"]["hpsm_host"],
    'protocol': config["HPSM"]["hpsm_protocol"],
    'port': config["HPSM"]["hpsm_port"],
    'username': config["HPSM"]["hpsm_username"],
    'password': config["HPSM"]["hpsm_password"],
    'api_version': config["HPSM"]["hpsm_api_version"],
    'verify_ssl': config["HPSM"].getboolean("hpsm_verify_ssl")
}

options = {
    'debug': config["OPTIONS"].getboolean("opt_debug"),
    'dry_run': config["OPTIONS"].getboolean("opt_dry_run")
}

hpsm_rest = HpsmApi(hpsm, options)
device42_doql = Device42Doql(device42, options)


class Integration:

    def __init__(self):
        pass

    @staticmethod
    def get_d42_devices():
        f = StringIO(device42_doql.get_devices())
        devices = []
        for item in csv.DictReader(f, delimiter=','):
            devices.append(item)
        return devices

    @staticmethod
    def get_d42_hardware(hw_id):
        f = StringIO(device42_doql.get_hardware(hw_id))
        for item in csv.DictReader(f, delimiter=','):
            return item

    @staticmethod
    def get_d42_vendor(vn_id):
        f = StringIO(device42_doql.get_vendor(vn_id))
        for item in csv.DictReader(f, delimiter=','):
            return item

    @staticmethod
    def get_d42_os(os_id):
        f = StringIO(device42_doql.get_os(os_id))
        for item in csv.DictReader(f, delimiter=','):
            return item

    @staticmethod
    def get_d42_subnet(subnet_id):
        f = StringIO(device42_doql.get_subnet(subnet_id))
        for item in csv.DictReader(f, delimiter=','):
            return item

    @staticmethod
    def get_d42_macs(device_id):
        f = StringIO(device42_doql.get_macs(device_id))
        macs = []
        for item in csv.DictReader(f, delimiter=','):
            macs.append(item)

        return macs

    @staticmethod
    def get_d42_ips(device_id):
        f = StringIO(device42_doql.get_ips(device_id))
        ips = []
        for item in csv.DictReader(f, delimiter=','):
            ips.append(item)

        return ips


def main():
    integration = Integration()
    devices = integration.get_d42_devices()

    hpsm_computers = hpsm_rest.get_d42_items('computers', 'computer')
    hpsm_networkdevices = hpsm_rest.get_d42_items('networkdevices', 'networkcomponents')

    hpsm_d42_computers = []
    hpsm_d42_networkdevices = []

    if 'content' in hpsm_computers:
        hpsm_computers = hpsm_computers['content']
        hpsm_d42_computers = {str(x['Computer']['device42.id']): x['Computer'] for x
                              in hpsm_computers if 'device42.id' in x['Computer']}
    else:
        hpsm_computers = []

    if 'content' in hpsm_networkdevices:
        hpsm_networkdevices = hpsm_networkdevices['content']
        hpsm_d42_networkdevices = {str(x['NetworkDevice']['device42.id']): x['NetworkDevice'] for x
                                   in hpsm_networkdevices if 'device42.id' in x['NetworkDevice']}
    else:
        hpsm_networkdevices = []

    for device in devices:
        hardware = integration.get_d42_hardware(device['hardware_fk']) if device['hardware_fk'] else None
        vendor = integration.get_d42_vendor(hardware['vendor_fk']) if hardware and hardware['vendor_fk'] else None
        os = integration.get_d42_os(device['os_fk']) if device['os_fk'] else None
        os_vendor = integration.get_d42_vendor(os['vendor_fk']) if os and os['vendor_fk'] else None
        macs = integration.get_d42_macs(device['device_pk'])
        ips = integration.get_d42_ips(device['device_pk'])

        if device['network_device'] == 't':
            root = 'NetworkDevice'
            endpoint = 'networkdevices'
            ctype = 'networkcomponents'
            hpsm_mapping = hpsm_d42_networkdevices
            hpsm_devices = hpsm_networkdevices
        else:
            root = 'Computer'
            endpoint = 'computers'
            ctype = 'computer'
            hpsm_mapping = hpsm_d42_computers
            hpsm_devices = hpsm_computers

        # check locked
        if len(hpsm_mapping) > 0 and device['device_pk'] in hpsm_mapping:
            device['name'] = hpsm_mapping[device['device_pk']]['logical.name']
        else:
            # check by serial if not locked
            for hpsm_device in hpsm_devices:
                hpsm_device = hpsm_device[root]
                if 'serial.no.' in hpsm_device and hpsm_device['serial.no.'] == device['serial_no']:
                    device['name'] = hpsm_device['logical.name']
                    break

        device['name'] = device['name'].replace('/', '_')

        hpsm_rest.insert_item({
            root: {
                'logical.name': device['name'],
                'machine.name': device['name'],
                'istatus': 'In Service' if device['in_service'] == 't' else 'Missing',
                'type': ctype,
                'subtype': device['type'].upper(),
                'assignment': 'Hardware',
                'environment': device['service_level'],
                'asset.tag': device['asset_no'],
                'manufacturer': vendor['name'] if vendor and 'name' in vendor else '',
                'model': hardware['name'] if hardware and 'name' in hardware else '',
                'serial.no.': device['serial_no'],
                'description': device['notes'],
                'os.name': os['name'] if os else '',
                'os.version': device['os_version_no'],
                'os.manufacturer': os_vendor['name'] if os_vendor and 'name' in os_vendor else '',
                'physical.mem.total': float(device['hard_disk_size']) * 1048576 if device['hard_disk_size'] else '',
                'mac.address': macs[0]['hwaddress'] if len(macs) > 0 else '',
                'ip.address': ips[0]['ip_address'] if len(ips) > 0 else '',
                'network.name': integration.get_d42_subnet(ips[0]['subnet_fk'])['name'] if len(ips) > 0 else '',
                'device42.id': device['device_pk']
            }
        }, root, endpoint)

        if len(macs) > 1:
            hpsm_rest.update_item({
                root: {
                    'logical.name': device['name'],
                    'addlMacAddress': macs[1]['hwaddress']
                }
            }, root, endpoint)

        if len(ips) > 1:
            hpsm_rest.update_item({
                root: {
                    'logical.name': device['name'],
                    'addlIPAddr': [{
                        'addlIPAddress': x['ip_address'],
                        'addlSubnet': integration.get_d42_subnet(x['subnet_fk'])['name']
                    } for x in ips[1:]]
                }
            }, root, endpoint)


if __name__ == '__main__':
    main()
    print('\n Finished')
