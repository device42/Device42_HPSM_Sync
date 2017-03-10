# Device42_HPSM_Sync
Script syncs Device42 (http://www.device42.com) data to HPSM.
This script was tested with HPSM ( 9.40 ) and Device42 ( 12.0.0 )


# Setup
Take the file `conf.sample` and rename it to `conf`. Then change the settings to correct ones.

# HPSM Configuration
1.Open the Database Dictionary and add field (type ‘number, name ‘device42.id’) to both the models ‘computer’ and ‘networkcomponents'


2.Operator should have access to the REST API. The API should allow “Computer” and “NetworkDevice” access, allowing both ‘add’ and ‘save’ actions


3.Both endpoints must allow access to add & update all of the fields listed on this page
```
'logical.name'
'machine.name'
'istatus'
'type'
'subtype'
'assignment'
'environment'
'asset.tag'
'manufacturer'
'model'
'serial.no.'
'description'
'os.name'
'os.version'
'os.manufacturer'
'physical.mem.total'
'mac.address'
'ip.address'
'network.name'
'addlMacAddress'
'addlIPAddr[addlIPAddress]'
'addlIPAddr[addlSubnet]'
'device42.id'
```

4.Unique key for “Computer” and “NetworkDevice” : `logical.name`


# Run
```
python starter.py
```

# How It Works
We check Device42 device serial number and if it exists in HPSM we update HPSM device with the same `serial.no`.
If `serial.no` not exists we check by device name and update HPSM device with the same `logical.name`.
After first sync we lock devices between HPSM and Device42 by Device42 PK. Next updates will only by Device42 PK.
All '/' in device name replacing with '_' because of HPSM REST architecture.
All spaces in device name replacing with '_' because of HPSM REST architecture.

# Information
For now the script supports only devices sync from Device42 to HPSM.
