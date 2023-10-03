# User Vision Report Template

Log into your device via the localadmin account 

To run builds locally ensure that you have installed and signed into **Docker** from https://www.docker.com

**On Windows Docker must be given permission to map local directories as volumes**
  - Open Docker Dashboard
  - Navigate to Settings>Resources>File Sharing 
  - Add the parent directory that contains your report repositories (Github folder)
  - Click "Apply and Restart"

Go to **Github Desktop** and open the current repository and branch and select 'Fetch Origin'. Then select the option to **Open the repository in 
Visual Studio (VS) Code** editor. 

## Pull issues

- Within VS Code replace the REPO, BRANCHES, PARENT and AUTH variables with your own and run on the commandline from within your local clone of the project repo.

- REPO refers to the project repository name
- BRANCHES refers to the project chapter labels
- PARENT refers to the parent label 
- The AUTH code can be accessed via Github account, go to **Settings**, then **Developer Settings** and select **Personal Access Tokens**. Generate a new token code and copy this into the commandline.

  - Mac   
  `docker run --rm -v ${PWD}:/app -e 'REPO=user-vision/template-report' -e 'BRANCHES=accessibility_audit' -e 'AUTH=****' 'PARENT=accessibility_audit'uservision/uv-python`
  - Windows Command Line    
  `docker run --rm -v %cd%:/app -e 'REPO=user-vision/template-report' -e 'BRANCHES=accessibility_audit' -e 'AUTH=****' 'PARENT=accessibility_audit'uservision/uv-python`
  - Windows Powershell    
  `docker run --rm -v ${pwd}:/app -e 'REPO=user-vision/template report' -e 'BRANCHES=accessibility_audit' -e ‘AUTH=****' -e 'PARENT=accessibility_audit' uservision/uv-python;`
  
Here's an example from a previous deployment
  `docker run --rm -v ${PWD}/public:/uv2544-nhs-digital-antigen-testing-accessibility-audit uservision/uv-now:latest /bin/sh -c 'now --prod --token pUW6DmQJOzfFDj1CVlccuVYg -c deploy /uv2544-nhs-digital-antigen-testing-accessibility-audit'`
  
### Updated Example
  `docker run --rm -v ${pwd}:/app -e 'REPO=user-vision/Omron' -e 'BRANCHES=UV2783-00 UV2783-01 UV2783-02 UV2783-03 UV2783-04 UV2783-05' -e ‘AUTH= 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' -e 'PARENT= UV2783' uservision/uv-python;`
  
## Configure Report
- Edit author and client information in index.Rmd, as well as updating any other necessary .Rmd files
- Update:
  - **01 Executive Summary**: Add client logo, client name, and what was tested 
  - **02 Summary**: Insert platform, number of issues, and list of top findings
  - **03 Project Background**: Update client name and background 
  - **08 Backmatter**: Edit team and contact details
  - **Index.rmd**: Edit title, authors, and footer (add client name) 

- Update Jenkins file with build information
- Change any .GIF files to .gif otherwise the PDF builder will break.

#### Common compiling errors:
- Special symbols in image captions
- Missing `<h1>` elements 
- Unrecognised symbols in write-ups

Try to identify the error based on the debug issue and edit the corresponding issues-0X file 

#### To add labels that don't already exist 
_utils> github.issues.to_md.py_
Edit lines around 70, 208, and 289 (follow the syntax from the adjacent lines)  

## Build Report
- To generate an html format report, run the folling (adjusting the volume path as necessary):
    `docker run --rm -v ${pwd}:/app uservision/uv-a11yreport:latest`  
    
- The generated report will be created in a new directory called 'public'

## Build PDF
`docker run --rm -v ${pwd}:/app uservision/uv-pdf:pandoc`

To access the PDF report, go to the accessibility_audit.pdf file in the Public folder, right click on the file and select 'Reveal in file explorer'. 

## To change the contrast of heading elements

In VS Code, navigate to _public>libs>gitbook-2.6.7>css>style.css_

Within the code search for the code snippet (using Ctrl+F): `.book .book-summary ul.summary li span{cursor:not-allowed;opacity:0.3;filter:alpha(opacity=30)`

Change the opacity from 0.3 to 0.9 

##  Creating a web-version of the report via AWS
 
Go to https://aws.amazon.com/amplify/ and log in.

Login details: Username: hello@uservision.co.uk Password: kyv7RZW2fde*qau2xdz

Select the ‘Sign in to the console’ link and then select AWS Amplify.

**Upload it to AWS Amplify Console**
-	From the ‘New App’ dropdown select ‘Host web app’ 
-	Select ‘Deploy without Git provider’
-	Create App name- UVcode-Client Name- Accessibility Audit
-	Environment name- prod
-	Method- Drag and drop the project folder
-	Select ‘Save and Deploy’

**Create a custom domain in AWS Amplify Console**
- From 'All Apps' select the relevant project
- From 'App Settings' select 'Domain Management' and then select the 'Add a Domain' button
- Whilst on the 'Add domain' page, add the root domain in the search field which is uservisionaccessibility.co.uk and select the 'Configure domain’ button
- Select the 'Exclude root' button so the root domain is not used 
- Add a new subdomain (UVCode-Client name-Project Name-Accessibility-Audit) and select 'Save'
- Now on the 'Status details' page, you should see the domain being created and it should take about 30 minutes to register the new domain. 

- [Video with instructions on how to create a custom domain](https://uservisionltd.sharepoint.com/sites/UserVision/_layouts/15/stream.aspx?id=%2Fsites%2FUserVision%2FShared%20Documents%2FZ%20Drive%20Cloud%20Files%2FAccessibility%2FReporting%20Process%2FAWS%20Amplify%20Custom%20Domain%2Emp4&ga=1)



