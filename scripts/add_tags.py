from uptime_kuma_api import UptimeKumaApi, MonitorType
import click

@click.command()
@click.option('--username', default='admin', help='username for Uptime Kuma login')
@click.option('--password', prompt='Uptime Kuma password', help='password for Uptime Kuma login')
@click.option('--server', prompt='Uptime Kuma server', default='http://localhost:8080/', help='URL for Uptime Kuma server in IP format (e.g. http://127.0.0.1:3001/)')
@click.option('--tag', default='TEST', help="Name of tag to add to Uptime Kuma")
def main(username, password, server, tag):

    if not password:
        raise Exception('Please provide the password used to login to Uptime Kuma.')
  
    # Initialize connection to Uptime Kuma server
    # api = UptimeKumaApi(server)


    with UptimeKumaApi(server) as api:

        # Login to server with username and password
        api.login(username, password) 

        ## Get all monitors
        result = api.get_monitors()
        total = len(result)
        count = 1
        
        print('Login successful. Adding tags to ', total, ' monitors')

        test_tag = api.add_tag(
            name=str(tag),
            color="#ffffff"
        )

        test_tag_id = test_tag['id']

        for monitor in result:
            if monitor['active'] is False and monitor['maintenance'] is False:
                api.add_monitor_tag(test_tag_id, monitor['id'])

if __name__ == "__main__":
    main()
