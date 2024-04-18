from uptime_kuma_api import UptimeKumaApi, MonitorType
import click
import pandas as pd
import csv
import time 

@click.command()
@click.option('--username', default='admin', help='username for Uptime Kuma login')
@click.option('--password', prompt='Uptime Kuma password', help='password for Uptime Kuma login')
@click.option('--server', prompt='Uptime Kuma server', default='http://localhost:8080/', help='URL for Uptime Kuma server in IP format (e.g. http://127.0.0.1:3001/)')
def main(username, password, server):

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
        
        print('Login successful. Parsing data for ', total, ' monitors')

        tuples = parse_monitors_list(result)
        write_tuples_to_csv(tuples)


def parse_monitors_list(result):
    tuples = []
    for monitor in result:
        tuples.append((monitor['url'], monitor['name']))
    return tuples


def write_tuples_to_csv(tuples):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = 'monitor_list' + timestr + '.csv'
    with open(filename, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['url', 'friendly_name'])
        for tup in tuples:
            writer.writerow(tup)


if __name__ == "__main__":
    main()
