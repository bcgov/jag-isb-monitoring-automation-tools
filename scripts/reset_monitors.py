# Tested on Python 3.11.9

import csv
import pandas as pd

from uptime_kuma_api import UptimeKumaApi, MonitorType
import click

@click.command()
@click.option('--username', default='admin', help='username for Uptime Kuma login')
@click.option('--password', prompt='Uptime Kuma password', help='password for Uptime Kuma login')
@click.option('--server', prompt='Uptime Kuma server', default='http://localhost:8080/', help='URL for Uptime Kuma server in IP format (e.g. http://127.0.0.1:3001/)')
@click.option('--monitor_list', default='', type=click.Path() )
# TODO: Make the list for monitors to DO the resetting or NOT to do the resetting. 
def main(username, password, server, monitor_list):

    
    if not password:
        raise Exception('Please provide the password used to login to Uptime Kuma.')
  
    # Initialize connection to Uptime Kuma server
    with UptimeKumaApi(server) as api:

        # Login to server with username and password
        api.login(username, password) 

        ## Get all monitors
        result = api.get_monitors()
        total = len(result)
        count = 1
        
        if monitor_list == '':
            print('Login successful. Resetting ', total, ' monitors')
            reset_default_monitors(api, result, count, total)
        else:
            print('Login successful. Parsing file list')
            file_list = parse_csv(monitor_list)
            result = create_sub_dict(file_list, result)
            total = len(result)
            print('Resetting ', total, ' monitors from list')
            reset_monitors_from_list(api, result, count, total)


def parse_csv(monitor_list):
    df = pd.read_csv(monitor_list, delimiter=',')
    tuples = [tuple(x) for x in df.values]
    # print(tuples)
    return tuples


def create_sub_dict(file_list, result):

    new_result = []
    
    for index, tuple in enumerate(file_list):
        # print(index, tuple)
        for monitor in result:
        
            if str(monitor['url']) == tuple[index]:
                new_result.append(monitor) 

    print(new_result)
    return new_result


def reset_monitors_from_list(api, result, count, total):
    for monitor in result:
        reset(api, monitor, total)
        print('Reset complete for ', count, ' out of ', total, ' monitors.')
        count += 1

        
def reset_default_monitors(api, result, count, total):
    for monitor in result:
        reset_monitor = reset_criteria(monitor)        
        if reset_monitor:
            reset(api, monitor, total)
            print('Reset complete for ', count, ' out of ', total, ' monitors.')
            count += 1
        else:
            print('Monitor ineligible for reset, skipping.')
            count += 1


def reset(api, monitor, total):
    p = api.pause_monitor(monitor['id'])
    print(monitor['name'], p)
    r = api.resume_monitor(monitor['id'])
    print(monitor['name'], r)
    

def reset_criteria(monitor):

    # Do not reset monitors that are disabled from needing credentials - April 16th 2024
    if '[need creds]' in monitor['name']:
        return False

    # Do not reset monitors in maintenance mode. This will remove them from maintenance mode. 
    if monitor.get('maintenance') == True:
        return False

    for tag in monitor['tags']:
        if tag['name'] == 'DO NOT RESET' or tag['name'] == 'TEST':
            return False
    return True
    

if __name__ == "__main__":
    main()
