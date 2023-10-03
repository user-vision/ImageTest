# User Vision Report Template

To run builds locally ensure that you have installed **Docker** from https://www.docker.com

**On Windows Docker must be given permission to map local directories as volumes**
  - Open Docker Dashboard
  - Navigate to Settings>Resources>File Sharing 
  - Add the parent directory that contains your report repositories
  - Click "Apply and Restart"

The following commands expect to be run from a terminal with scope of the installed docker instance and from within the project directory eg `~/Development/template-report`

## Pull issues

- Replace the REPO, BRANCHES and AUTH variables with your own and run on the commandline from within your local clone of the project repo.

  - Mac   
  `docker run --rm -v ${PWD}:/app -e 'REPO=user-vision/template-report' -e 'BRANCHES=accessibility_audit' -e 'AUTH=****' 'PARENT=accessibility_audit'uservision/uv-python`
  - Windows Command Line    
  `docker run --rm -v %cd%:/app -e 'REPO=user-vision/template-report' -e 'BRANCHES=accessibility_audit' -e 'AUTH=****' 'PARENT=accessibility_audit'uservision/uv-python`
  - Windows Powershell    
  `docker run --rm -v ${pwd}:/app -e 'REPO=user-vision/template report' -e 'BRANCHES=accessibility_audit' -e ‘AUTH=****' -e 'PARENT=accessibility_audit' uservision/uv-python;`
  
  
## Configure Report
- Edit author and client information in index.Rmd, as well as updating any other necessary .Rmd files
- Change any .GIF files to .gif otherwise the PDF builder will break.

## Build Report
- To generate an html format report, run the folling (adjusting the volume path as necessary):
    `docker run --rm -v ${pwd}:/app uservision/uv-a11yreport:latest`  
- The generated report will be created in a new directory called 'public'

## Deploy to Zeit
- To deploy the contents of the 'public' directory to the web, run the following: 

  `docker run --rm -v ${PWD}:/uv-accessibility-audit uservision/uv-now:latest /bin/sh -c 'now --token **** -c deploy /uv-accessibility-audit'`

Here's an example from a previous deployment
  `docker run --rm -v ${PWD}/public:/uv2544-nhs-digital-antigen-testing-accessibility-audit uservision/uv-now:latest /bin/sh -c 'now --prod --token pUW6DmQJOzfFDj1CVlccuVYg -c deploy /uv2544-nhs-digital-antigen-testing-accessibility-audit'`
