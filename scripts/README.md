# Docs

These scripts are for use with the unofficial Uptime Kuma API


### Pre-requisities

- Python 3.11. This was the version these scripts were made with. I would recommend sticking to as close to this version as possible.
- pip package manager: https://pip.pypa.io/en/stable/installation/
- virtualenv to create a virtual environment for managing Python package installations.     

--Refer to this guide for information on virtual environments: https://virtualenv.pypa.io/en/stable/installation 
-- Refer to this guide for installation instructions for Windows https://mothergeo-py.readthedocs.io/en/latest/development/how-to/venv-win.html 

- using pip to install the requirements.txt file:
    pip install -r requirements. txt

### Scripts

#### reset_monitors.py - this file is used to reset monitors on a backup/restore process. 

To run the script, run the following command:

`python3 .\reset_monitors.py --username admin --password <uptime_kuma_password> --monitor_list <optional_list_of_monitors>`

The monitor list is optional if you want to specify which monitors to reset. Otherwise, it will reset all monitors that do not have the 'TEST' or 'DO NOT RESET' tags. Maintenance monitors will be reset, so you will need to specify a tag to avoid them from being reset and taken out of maintenance. 

#### add_tags.py -
This file is used to add tags to PAUSED monitors. This can be used to prevent paused monitors from being reset. 

Run the following command to run this script:

`python3 .\add_tags.py --username admin --password <uptime_kuma_password> --tag <optional_name_for_tag>`


You can specify a tag with the --tag parameter. The default value will be TEST, which will allow it to be ignored by the reset monitors script. 


#### create_csv_file.py 

This script is used to generate a csv list of all monitors. Currently, this is a way to get a list to be used with reset_monitors.py. 

`python3 .\create_csv_file.py --username admin --password <uptime_kuma_password>`