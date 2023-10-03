# User Vision Report Template

Log into your device via the localadmin account 

To run builds locally ensure that you have installed and signed into **Docker** from https://www.docker.com

When installing Docker for the first time, uncheck the WSL-2 Hyper-V box 

**On Windows Docker must be given permission to map local directories as volumes**
  - Open Docker Dashboard
  - Navigate to Settings>Resources>File Sharing 
  - Add the parent directory that contains your report repositories (Github folder)
  - Click "Apply and Restart"

Go to **Github Desktop** and open the current repository and branch and select 'Fetch Origin'. Then select the option to **Open the repository in 
Visual Studio (VS) Code** editor. 

# STEP 1
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
  
### Example
  `docker run --rm -v ${pwd}:/app -e 'REPO=user-vision/Omron' -e 'BRANCHES=UV2783-00 UV2783-01 UV2783-02 UV2783-03 UV2783-04 UV2783-05' -e ‘AUTH= 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' -e 'PARENT= UV2783' uservision/uv-python;`
 
# STEP 2  
## Build Report
- To generate an html format report, run the following:
    `docker run --rm -v ${pwd}:/app uservision/uv-a11yreport:latest`  
    
 
# STEP 3

On VSCode:

**Open each issue file in a new tab, idk why this works but it does**

(Using the search icon in the menu on the left) 
Search: `https://github.com/user-vision/REPO/assets`
(Replace REPO with repository name)

Example: Search for `https://github.com/user-vision/Ministry-of-Justice/assets`


**Replace**: `https://github.com/assets`

Then hit Replace All (icon to the right of the Replace text input)


# STEP 4 
## Configure Report
- Edit author and client information in index.Rmd, as well as updating any other necessary .Rmd files
- Update:
  - **01 Executive Summary**: Add client logo, client name, and what was tested 
  - **02 Summary**: Insert platform, number of issues, and list of top findings
  - **03 Project Background**: Update client name and background 
  - **08 Backmatter**: Edit team and contact details
  - **Index.rmd**: Edit title, authors, and footer (add client name) 


#### Common compiling errors:
- Special symbols in image captions
- Missing `<h1>` elements 
- Unrecognised symbols in write-ups

Try to identify the error based on the debug issue and edit the corresponding issues-0X file 

### To update to WCAG 2.2
Edit:
- github-to-md.py 
- 02-Summary.Rmd (title and comment)

#### To add labels that don't already exist 
_utils> github.issues.to_md.py_
Edit lines around 70, 208, and 289 (follow the syntax from the adjacent lines)  


# STEP 5

## Build Report (yes, again, A11y babies)

`docker run --rm -v ${pwd}:/app uservision/uv-a11yreport:latest`

## Build PDF
`docker run --rm -v ${pwd}:/app uservision/uv-pdf:pandoc`

To access the PDF report, go to the accessibility_audit.pdf file in the Public folder, right click on the file and select 'Reveal in file explorer'. 
  

  
# STEP 6
  
## Update image files  
Go into Command Prompt (NOT Powershell) 

![image](https://github.com/user-vision/template-report/assets/65059425/a8662a79-4540-48b7-b736-0827c5156017)

Type: `cd images`, then hit Enter

Type: `ren * *.png` , then hit Enter

Ignore the errors and continue.

# STEP 7

In the 'images' folder, check that all images have a .png extension

Delete the main.Rmd file. Then, in Powershell run this command **again**:
`docker run --rm -v ${pwd}:/app uservision/uv-pdf:pandoc`
  
# STEP 8

## To change the contrast of heading elements

In VS Code, navigate to _public>libs>gitbook-2.6.7>css>style.css_

Within the code search for the code snippet (using Ctrl+F):
`.book .book-summary ul.summary li span{cursor:not-allowed;opacity:.3;filter:alpha(opacity=30)}.book`

Change the opacity from 0.3 to 0.9 

# STEP 9
  
## To change the focus indicator
Search for `a:focus{outline:dotted thin}`

Change to `a:focus{outline:dashed black}`

# STEP 10

## Add Docker Command into the README file

At the end of each build, add the Docker command to the ReadMe file. In the event that the report needs updated/rebuilt, the command will be there for ease.

e.g. `docker run --rm -v ${pwd}:/app -e 'REPO=user-vision/Ministry-of-Justice' -e 'BRANCHES=UV2924-Manage-Incentives-00 UV2924-Manage-Incentives-01 UV2924-Manage-Incentives-02 UV2924-Manage-Incentives-03' -e ‘AUTH=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' -e 'PARENT=UV2924-Manage-Incentives' uservision/uv-python;`

Once the command is added, save the changes. 

# STEP 11

## Push changes to Github

Within the 'Summary' field on GitHub Desktop, add a 'Summary', e.g 'Report built'.

Select 'Commit to UVXXXX' button.

Select 'Push' to ensure all changes are updated within GitHub.


# STEP 12

##  Creating a web-version of the report via AWS
 
Go to https://aws.amazon.com/amplify/ and log in.

Login details: Username: hello@uservision.co.uk Password: kyv7RZW2fde*qau2xdz

Select the ‘Sign in to the console’ link and then select AWS Amplify.

**Upload it to AWS Amplify Console**
-	From the ‘New App’ dropdown select ‘Host web app’ 
-	Select ‘Deploy without Git provider’
-	Create App name- UVcode-Client Name
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

## Creating a web-version of the report via Netlify
- Go to https://app.netlify.com/ and log in.
- Select to login with ‘Email’
- Login details: 
- Username: hello@uservision.co.uk 
- Password: Uservision55!

- From the dashboard top navigation, select ‘Sites’ 
- From the ‘Add new sites’ drop down, select ‘Deploy manually’
- Drag and drop the Public folder
- A link will automatically be generated 

**Create a custom domain in Bitly**
- Go to https://bitly.com/ and log in
- Select ‘Create new’
- Select ‘link’
- Paste the link generated from Netlify into the ‘Destination’
- Press Enter
- Once the link is generated, select ‘Edit link’
- In the ‘Customise back-half’ field add a new subdomain (UVCode-Client name-Project Name-Accessibility-Audit) and select 'Save'



## Generating CSV and JSON files
https://colab.research.google.com/drive/1aKVCeBM_8MCMwcfOF5XXzpjB190JGS-y?usp=sharing 

- In the first cell, update the **parent_label** and **REPO**
- Run the cells by pressing the `(>)`button on the left of each cell (or keep pressing Shift + Enter)
- Press the File icon on the left menu to expand the list of files 
- Download Issues_Analysis_Spreadsheet, CSV_Version, JSON_Version
