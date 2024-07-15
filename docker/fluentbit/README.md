# Deployment instructions 


## Manual 



### `docker build -t fluentbit-splunk -f .\Dockerfile.ci .`
### `docker tag fluentbit-splunk:latest <image_registry>/<tools-namespace>/fluentbit-splunk:latest`
### `docker push <image_registry>/<tools-namespace>/fluentbit-splunk:latest`


## "Automated"

Go to the Actions panel in Github, select the workflow you wish to run. Click the Run workflow dropdown and select the branch you want to run the workflow on. 