# ThinClient
The thinclient is the heart of Linux Admin in the way that it is what sits on every pc that Linux admin controls, we have little control over this code except for the ability to introduce an auto-update functionality that can be used to replace it. Even then mistakes in this code will likely lead to downtime and bigger problems upstream. 

We plan to distribute using apt-repo's and bash scripts. This gives up finer control over the installation process. We absolutely do not wish to rely on people using a simple python script for this purpose. The initial setup and registration of the device should be made by an api call to the django endpoint that will create a db object and root password for the  system.

## Registration

### Implementation
1. Variables needed for API call are
- We're using a token password based implementation that can be created in the frontend, since tokens will be org specific
and their passwords will be auto generated it's a secure way to register device. 
- In return the server will send over a root password, device id, organization id, and kafka topic authentication.


### TODO
1. Design Bash script to pull down the bash script. Through a linuxadmin.mustansirg.in/thinclient/download endpoint. 
2. Design registration process, and make sure that the frontend has the capability to generate things such as a registration code/token that can be verified with an api call by the thinclient. 

## Build Notes
1. Always obfuscate code with pyarmor before pushing to git. Any pull requests to the main branch will run an automatic action with github workflows to publish the package to PYPI.

## DEV Notes
1. Poetry maintains development dependencies and package dependencies. 
2. Package dependencies are also to be kept in setup.cfg. Since we're shipping as a python package

## Command for obfuscation
```bash
pyarmor obfuscate --recursive --output src/thinclient code/thinclient/__init__.py
```
