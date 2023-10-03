"""
Exports issues from a list of repositories to individual csv files.
Uses basic authentication (Github username + password) to retrieve issues
from a repository that username has access to. Supports Github API v3.
Forked from: unbracketed/export_repo_issues_to_csv.py
"""
import argparse
import csv
import re
import json
from addict import Dict
from getpass import getpass
from collections import Counter
import requests
import os

auth = None
state = 'open' 

# def write_issues(r, csvout, label, descurl,wcagsort, name, rating):
def write_issues(r, csvout, label, descurl,wcagsort, name, rating):
    """Parses JSON response and writes to CSV."""
    if r.status_code != 200:
        raise Exception(r.status_code)

    for issue in r.json():
        if 'pull_request' not in issue:            
            if 'closed' not in issue['state']:

                if any(project in s['name'] for s in issue['labels']):
                    # print(issue['url'])

                    if wcagsort == 1:
                        if 'id' not in label:    
                            if re.match(r'[0-9]*\.', label) is not None:   
                                csvout.writelines(["# WCAG " + label + "\n" ])
                    wcag = []
                    severity = []
                    platform = []
                    location = []

                    for label in issue['labels']:
                            if re.match(r'[0-9]*\.', label['name']) is not None: 
                                wcag.append(label['name'])
                            elif re.match(r'[A-Z]$', label['name']) is not None:
                                severity.append(label['name'])
                            elif re.match(r'Desktop', label['name']) is not None:
                                platform.append(label['name'])
                            elif re.match(r'Mobile', label['name']) is not None:
                                platform.append(label['name'])
                            elif re.match(r'Tablet', label['name']) is not None:
                                platform.append(label['name'])
                            elif re.match(r'iPad', label['name']) is not None:
                                platform.append(label['name'])
                            elif re.match(r'iOS', label['name']) is not None:
                                platform.append(label['name'])
                            elif re.match(r'Android', label['name']) is not None:
                                platform.append(label['name'])
                            elif re.match(r'IE', label['name']) is not None:
                                platform.append(label['name'])
                            elif re.match(r'Chrome', label['name']) is not None:
                                platform.append(label['name'])
                            elif re.match(r'Firefox', label['name']) is not None:
                                platform.append(label['name'])
                            elif re.match(r'Safari', label['name']) is not None:
                                platform.append(label['name'])
                            elif re.match(r'Automated', label['name']) is not None:
                                platform.append(label['name'])
                            elif re.match(r'Automated findings', label['name']) is not None:
                                platform.append(label['name'])
                            elif re.match(r'NVDA', label['name']) is not None:
                                platform.append(label['name'])
                            elif re.match(r'JAWS', label['name']) is not None:
                                platform.append(label['name'])
                            elif re.match(r'iPhone', label['name']) is not None:
                                platform.append(label['name'])
                            elif re.match(r'Persistent Issue', label['name']) is not None:
                                platform.append(label['name'])
                            elif re.match(r'Landing Page', label['name']) is not None:
                                platform.append(label['name'])
                            elif re.match(r'Content Page', label['name']) is not None:
                                platform.append(label['name'])
                            else: 
                                if project not in label['name']:
                                    location.append(label['name'])

                    criteria = []
                    if wcag:
                        for criterion in wcag:

                            criteria.append( "[" + criterion + " (" + wcagdict[criterion]['Level']+ ")]" + "(" + wcagdict[criterion]['Reference'] + ")" )
                            
                        wcaglabels = ', '.join([l for l in criteria])
                        wcaglabels =  "WCAG " + wcaglabels + " - " 
                    else:
                        wcaglabels = ""      


                    if severity:
                        sevlabels = ', '.join([l for l in severity])
                        sevlabels = ' (' + sevlabels + ')'
                    else:
                        sevlabels = ""
                    
                    if platform:
                        platformlabels = ', '.join([l for l in platform])
                        platformlabels =  platformlabels
                    else:
                        platformlabels = ""        

                    if location:
                        locations = []
                        for label in location:
                            url = 'https://api.github.com/repos/{}/labels/{}'.format(name, label)
                            if get_description(url):

                                if re.match(r'https', get_description(url)) is not None:
                                
                                    descurl = "- [" + label + "](" + get_description(url) + ")"
                                    
                                else:
                                    descurl = ""
                            else:
                                descurl = ""
                            locations.append(descurl)
                        locationlabels = '\n'.join([l for l in locations])
                        location =  locationlabels
                    else:
                        location = ""
                    
                    paddedBody = issue['body'].replace("[image]", "[]")


                    if re.match(r'^#[ ]', paddedBody) is not None:

                            for link in re.findall(r'[ ^]#(\d{1,} |[A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})', paddedBody):
                                # Check link
                                
                                poshex = re.match(r'([A-Fa-f0-9]{6})', link)

                                if poshex is None:
                                    issuelink = get_issue(link)
                                    ## If this fails uncomment the line below to find out where the issue originates
                                    #print(link) 
                                    paddedBody = paddedBody.replace(" #" + link, " [" + issuelink +"] ")
                                    
                                    
                            Body1 = paddedBody

                            newh1 = re.search(r'\n## (.*)', Body1)
                            if newh1:
                                newh1 = re.sub(r'\.', "", newh1.group(1))
                                
                                if wcaglabels:
                                    Body2 = re.sub(r"\n## (.*)",  "\n### " + wcaglabels + platformlabels + "\n" + descurl + "\n" + location + "\n", Body1)
                                else:
                                    Body2 = re.sub(r"\n## (.*)",  "\n### " + r"\1" , Body1)

                                Body2 = re.sub(r"^(# )(.*)\n",  "# " + newh1 , Body2)
                            
                                Body2 = re.sub(r"(^##[ ].*)", r"\1", Body2)
                            else:   
                                Body2 = Body1
                            
                            
                            rBody = re.sub(r"^#[ ]([A-Za-z0-9,. -_ `<>]*)", "\n\n## " + r"\1" + sevlabels +  "\n", Body2)

                            rBody = re.sub(r"\!\[([-a-zA-Z0-9()@:%_\+.~#?'`&\/=_, ]*)\]\(([\w\W]+?)\)", '```{r, fig.cap="' + r"\1" + '", fig.alt="' + r"\1" + '", fig.align="center", out.width="90%", echo=FALSE}\ninclude_image("' + r"\2" + '", img_dir = "images")\n```', rBody)

                    else: 
                        for link in re.findall(r'[ ^]#(\d{1,} |[A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})', paddedBody):
                            # Check link
                            poshex = re.match(r'([A-Fa-f0-9]{6})', link)

                            if poshex is None:
                                issuelink = get_issue(link)
                                paddedBody = paddedBody.replace(" #" + link, " [" + issuelink +"] ")                        
                        rBody = paddedBody

                    rBody = re.sub(r"Recommendation\:", "Recommendation" , rBody)
                    rBody = re.sub(r"Recommendations\:", "Recommendation" , rBody)
                    rBody = re.sub(r'<img width="([0-9]*)" [\w\W]+? src="([\w\W]+?)">', "![](" + r"\2" + ")" , rBody)

                    rBody = re.sub(r"\!\[([-a-zA-Z0-9()@:%_\+.~#?$£€&\/=_,; '`‘’]*)\]\(([\w\W]+?)\)", '```{r, fig.cap="' + r"\1" + '", fig.alt="' + r"\1" + '", fig.align="center" , echo=FALSE}\ninclude_image("' + r"\2" + '", img_dir = "images")\n```', rBody)
                    
                    # rBody = re.sub(r'<img width=\"([0-9]*)\" [\w\W]+? src=\"([\w\W]+?)\">', '```{r, out.width="' + r"\1" + 'px", echo=FALSE}\n include_image("' + r"\2" + '", img_dir = "images")\n```', Body2)

                    csvout.writelines([rBody + "\n\n" + "---" + "\n\n" ])

                    # csvout.writelines(["`r pagebreak()`"])



def get_issue(issue):
    url = 'https://api.github.com/repos/{}/issues/{}'.format(repository, issue)

    r = requests.get(url, auth=auth)
    if r.status_code != 200:
        raise Exception(r.status_code)

    wcag = []
    severity = []
    platform = []
    location = []
    issue = r.json()
    
    for label in issue['labels']:
        if re.match(r'[0-9]*\.', label['name']) is not None: 
            wcag.append(label['name'])
        elif re.match(r'[A-Z]$', label['name']) is not None:
            severity.append(label['name'])
        elif re.match(r'Desktop', label['name']) is not None:
            platform.append(label['name'])
        elif re.match(r'Mobile', label['name']) is not None:
            platform.append(label['name'])
        elif re.match(r'Tablet', label['name']) is not None:
            platform.append(label['name'])
        elif re.match(r'iPad', label['name']) is not None:
            platform.append(label['name'])
        elif re.match(r'iOS', label['name']) is not None:
            platform.append(label['name'])
        elif re.match(r'Android', label['name']) is not None:
            platform.append(label['name'])
        elif re.match(r'IE', label['name']) is not None:
            platform.append(label['name'])
        elif re.match(r'Chrome', label['name']) is not None:
            platform.append(label['name'])
        elif re.match(r'Firefox', label['name']) is not None:
            platform.append(label['name'])
        elif re.match(r'Safari', label['name']) is not None:
            platform.append(label['name'])
        elif re.match(r'Automated findings', label['name']) is not None:
            platform.append(label['name'])
        elif re.match(r'NVDA', label['name']) is not None:
            platform.append(label['name'])
        elif re.match(r'JAWS', label['name']) is not None:
            platform.append(label['name'])
        elif re.match(r'iPhone', label['name']) is not None:
            platform.append(label['name'])
        elif re.match(r'Persistent Issue', label['name']) is not None:
            platform.append(label['name'])
        elif re.match(r'Landing Page', label['name']) is not None:
            platform.append(label['name'])
        elif re.match(r'Content Page', label['name']) is not None:
            platform.append(label['name'])
        else: 
            if project not in label['name']:
                location.append(label['name'])
    
    if wcag:
        wcaglabels = ', '.join([l for l in wcag])
        wcaglabels =  "WCAG " + wcaglabels + " - " 
    else:
        wcaglabels = ""      

    sevlabels = ', '.join([l for l in severity])
    
    if platform:
        platformlabels = ', '.join([l for l in platform])
        platformlabels =  platformlabels
    else:
        platformlabels = ""        

    if location:
        locationlabels = ', '.join([l for l in location])
        location =  "\n- Location - " + locationlabels
    else:
        location = ""

    fixedBody = issue['body'].replace("[image]", "[]")
    paddedBody = fixedBody.replace("# ", "# ")
   
    Body1 = re.sub(r"(^#[ ].*)", r"\1" + "\n:::::::::::::: {.columns}\n::: {.column}", paddedBody)
    Body2 = re.sub(r"\n##[ ]([A-Za-z0-9,.` -_]*)", "\n:::\n::: {.column}\n## " + r"\1", Body1)
    newh1 = re.search(r'\n## (.*)', Body2)
    if newh1:
        newh1 = re.sub(r'\.', "", newh1.group(1))
        Body2 = re.sub(r"\n## (.*)",  "\n### " + wcaglabels + platformlabels + "\n", Body2)
        Body2 = re.sub(r"^(# )(.*)\n",  "# " + newh1, Body2)
    Body2 = re.sub(r"(^#[ ].*)", r"\1", Body2)
    rBody = re.sub(r"^#[ ]([A-Za-z0-9,. -_]*)", "\n\n## " + r"\1" + " (" + sevlabels + ")" "\n", Body2)
    title = re.search(r'\n## (.*)', rBody)
    if title:
        return title.group(1)

    if re.match(r'^#[ ]', paddedBody) is not None:
    # print(re.findall(r' #(\d{1,})', paddedBody))

        # print(paddedBody)
        Body1 = re.sub(r"(^#[ ].*)", r"\1" + "\n:::::::::::::: {.columns}\n::: {.column}", paddedBody)
        Body2 = re.sub(r"\n##[ ]([A-Za-z0-9,.` -_]*)", "\n:::\n::: {.column}\n## " + r"\1", Body1)
        newh1 = re.search(r'\n## (.*)', Body2)
        if newh1:
            newh1 = re.sub(r'\.', "", newh1.group(1))
            Body2 = re.sub(r"\n## (.*)",  "\n### " + wcaglabels + platformlabels + "\n", Body2)
            Body2 = re.sub(r"^(# )(.*)\n",  "# " + newh1, Body2)
        Body2 = re.sub(r"(^#[ ].*)", r"\1", Body2)
        rBody = re.sub(r"^#[ ]([A-Za-z0-9,. -_]*)", "\n\n## " + r"\1" + " (" + sevlabels + ")" "\n", Body2)
        title = re.search(r'\n## (.*)', rBody)
        if title:
            return title.group(1)
        else: 
            return issue['title'].title()
    else:
        # print(issue['body'])
        # print(issue['title'])
        return issue['title'].title()

def get_description(url):
    headers = {'Accept': 'application/vnd.github.symmetra-preview+json'}
    r = requests.get(url, auth=auth, headers=headers)

    if r.status_code != 200:
        return ""
    label = r.json()
    return label['description']


def get_issues(name, project, state, count):
    """Requests issues from GitHub API and writes to CSV file."""
    
    ratings = ["P", "H", "M", "L", "O"]
    platforms = ["Desktop", "iPhone", "Tablet", "iOS",  "IE", "iPad", "Android", "Firefox", "Chrome", "Safari", "Automated", "Automated findings", "NVDA", "JAWS"]

    csvfilename = '05-issues-' + str(count).zfill(2) + '.Rmd'.format(name.replace('/', '-'))

    with open(csvfilename, 'w') as csvfile:
        csvout = csvfile
        url = 'https://api.github.com/repos/{}/labels/{}'.format(name, project)

        if get_description(url):
            descurl = get_description(url)
        else:
            descurl = ""

        label = project

        project = project.replace("-", " ").replace("_", " - ")
        projectlabel = re.sub(r"UV[0-9 -]*", "", project)
        
        if re.match(r'\(WRAP\)', descurl) is not None: 
            
            splitdesc = re.sub(r"\(WRAP\) ", "",descurl)

            csvout.writelines(["# (PART) " + splitdesc + "\n" ])
            csvout.writelines(["# " + splitdesc + " - WCAG Rating\n" ])


            get_ratings(name, label, state, csvout)

      
            # descurl = "**[" + descurl + "](" + descurl + ")**"
            descurl = "**" + descurl + "**"
            wcagsort = 0
            


        else:

            splitdesc = re.sub(r"\(h", "\n(h",descurl)
            splitdesc = re.sub(r"\\n ", "\n",splitdesc)

            csvout.writelines(["# " + splitdesc + "\n" ])

      
            # descurl = "**[" + descurl + "](" + descurl + ")**"
            descurl = "**" + descurl + "**"
            wcagsort = 0
            

            for rating in ratings:
                # url = 'https://api.github.com/search/issues?q=repo:{}+state:{}+label:{}+label:{}'.format(name, state, label, criterion)
                # url = 'https://api.github.com/repos/{}/issues?state={}&labels={}'.format(name, state, label)
                url = 'https://api.github.com/repos/{}/issues?state={}&labels={},{}&sort=created&direction=asc'.format(name, state, label, rating)
                
                r = requests.get(url, auth=auth)
                if r.status_code != 200:
                    raise Exception(r.status_code)
                else:
                    write_issues(r, csvout, label, descurl, wcagsort, name, rating)

                # Multiple requests are required if response is paged
                if 'link' in r.headers:
                    pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                            (link.split(';') for link in
                            r.headers['link'].split(','))}
                    while 'last' in pages and 'next' in pages:
                        pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                                (link.split(';') for link in
                                r.headers['link'].split(','))}
                        r = requests.get(pages['next'], auth=auth)
                        write_issues(r, csvout, "",descurl, wcagsort, name, rating)
                        if pages['next'] == pages['last']:
                            break

            # else:            




def locate_issues(r, project):
    """Parses JSON response and writes to CSV."""
    if r.status_code != 200:
        raise Exception(r.status_code)
    # print(project)
    for issue in r.json():
        if 'pull_request' not in issue:
            if 'closed' not in issue['state']:
                for s in issue['labels']:

                    if project == s['name']:
                        wcag = []
                        severity = []
                        platform = []
                        location = []
                        # print(s)

                        for label in issue['labels']:
                            
                            if re.match(r'[0-9.]', label['name']) is not None: 
                                failedLabels.append(label['name'])
                                # print(failedLabels)



# def get_ratings(name, project, state,csvout):
#     """Requests issues from GitHub API and writes to CSV file."""
#     # print(project)
#     ratings = ["H", "M", "L"]

#     for rating in ratings:
        
#         url = 'https://api.github.com/repos/{}/issues?state={}&labels={},{}'.format(name, state, project, rating)

#         # print(url)
#         r = requests.get(url, auth=auth)
#         locate_issues(r, project)


#         # Multiple requests are required if response is paged
#         if 'link' in r.headers:
#             pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
#                     (link.split(';') for link in
#                     r.headers['link'].split(','))}
#             while 'last' in pages and 'next' in pages:
#                 pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
#                         (link.split(';') for link in
#                         r.headers['link'].split(','))}
#                 r = requests.get(pages['next'], auth=auth)
#                 locate_issues(r, project)
#                 if pages['next'] == pages['last']:
#                     break

#     wcaglabels = failedLabels.sort()
#     # print(wcaglabels)
#     wcaglist = '\n'.join([l for l in failedLabels])
#     mylist = []
#     principlelist = []
#     criterialist = []

#     for l in failedLabels:
#         mylist.append(l)
#         principlelist.append(l[:3])
#         criterialist.append(l)
#     #   print(criterialist)
    

    # a = 30
    # aa = 50
    # aaa = 78
    # for criterion in wcagdict:
    #     if criterion in criterialist:
    #         if wcagdict[criterion]['Level'] == "A":
    #             a = a - 1
    #             aa = aa - 1
    #             aaa = aaa - 1
    #         elif wcagdict[criterion]['Level'] == "AA":
    #             aa = aa - 1
    #             aaa = aaa - 1
    #         elif wcagdict[criterion]['Level'] == "AAA":
    #             aaa = aaa - 1
    
    # aPass = a
    # aFail = 30-a
    # aaPass = aa
    # aaFail = 50-aa
    # aaaPass = aaa
    # aaaFail = 78-aaa

    # # donut = '\n(ref:wcag'+ str(count) +') WCAG 2.1 Compliance - '+ str(round(aPass/30*100)) +'% Level A, '+ str(round(aaPass/50*100)) +'% Level AA, '+ str(round(aaaPass/78*100)) +'% Level AAA   \n\n(ref:wcag'+ str(count+1) +') WCAG 2.1 Compliance - '+ str(round(aPass/30*100)) +'% Level A, '+ str(round(aaPass/50*100)) +'% Level AA, '+ str(round(aaaPass/78*100)) +'% Level AAA   \n\n```{r,  fig.cap="(ref:wcag'+ str(count) +')",  fig.alt="(ref:wcag'+ str(count+1) +')", fig.align="center", echo=FALSE}\nlibrary(ggplot2)\nlibrary(gridExtra)\nlibrary(grid)\nblank_theme <- theme_minimal()+\n  theme(\n    axis.title.x = element_blank(),\n    axis.title.y = element_blank(),\n    panel.border = element_blank(),\n    panel.grid=element_blank(),\n    axis.ticks = element_blank(),\n    plot.title=element_text(size=13, face="bold"),\n  )\ndat = data.frame(count=c('+str(aPass)+', '+str(aFail)+'), category=c("Pass", "Fail"))\ndat$fraction = dat$count / sum(dat$count)\ndat$ymax = cumsum(dat$fraction)\ndat$ymin = c(0, head(dat$ymax, n=-1))\ndat$category <- factor(dat$category, levels = c("Pass", "Fail"))\np1 = ggplot(dat, aes(fill=category, ymax=ymax, ymin=ymin, xmax=4, xmin=3)) +\n  geom_rect(color="white") +\n  coord_polar(theta="y") +\n  xlim(c(2, 4))\nedu<-p1 + scale_fill_brewer("Level A",palette = "Dark2") + blank_theme + \n  theme(axis.text.x=element_blank()) + theme(legend.position=c(.5, .5)) + ggtitle("") +\n  theme(panel.grid=element_blank()) +\n  theme(axis.text=element_blank()) +\n  theme(axis.ticks=element_blank()) +\n  theme(legend.title = element_text(size=10, face="bold")) +\n  theme(legend.text = element_text(size = 11, face = "bold"))\nedu +  geom_label(aes(label=paste(round(fraction*100, digits = 0),"%"), x=3.5,y=(ymin+ymax)/2), inherit.aes = TRUE, show.legend = FALSE,label.size = 0, color="white") -> p4\ndat = data.frame(count=c('+str(aaPass)+', '+str(aaFail)+'), category=c("Pass", "Fail"))\ndat$fraction = dat$count / sum(dat$count)\ndat$ymax = cumsum(dat$fraction)\ndat$ymin = c(0, head(dat$ymax, n=-1))\ndat$category <- factor(dat$category, levels = c("Pass", "Fail"))\np2 = ggplot(dat, aes(fill=category, ymax=ymax, ymin=ymin, xmax=4, xmin=3)) +\n  geom_rect(color="white") +\n  coord_polar(theta="y") +\n  xlim(c(2, 4))\nedu<-p2 + scale_fill_brewer("Level AA",palette = "Dark2") + blank_theme + \n  theme(axis.text.x=element_blank()) + theme(legend.position=c(.5, .5)) + ggtitle("") +\n  theme(panel.grid=element_blank()) +\n  theme(axis.text=element_blank()) +\n  theme(axis.ticks=element_blank()) +\n  theme(legend.title = element_text(size=13, face="bold")) +\n  theme(legend.text = element_text(size = 11, face = "bold"))\nedu +  geom_label(aes(label=paste(round(fraction*100, digits = 0),"%"), x=3.5,y=(ymin+ymax)/2), inherit.aes = TRUE, show.legend = FALSE,label.size = 0, color="white") -> p5\ndat = data.frame(count=c('+str(aaaPass)+', '+str(aaaFail)+'), category=c("Pass", "Fail"))\ndat$fraction = dat$count / sum(dat$count)\ndat$ymax = cumsum(dat$fraction)\ndat$ymin = c(0, head(dat$ymax, n=-1))\ndat$category <- factor(dat$category, levels = c("Pass", "Fail"))\np3 = ggplot(dat, aes(fill=category, ymax=ymax, ymin=ymin, xmax=4, xmin=3)) +\n  geom_rect(color="white") +\n  coord_polar(theta="y") +\n  xlim(c(2, 4))\nedu<-p3 + scale_fill_brewer("Level AAA",palette = "Dark2") + blank_theme + \n  theme(axis.text.x=element_blank()) + theme(legend.position=c(.5, .5)) + ggtitle("") +\n  theme(panel.grid=element_blank()) +\n  theme(axis.text=element_blank()) +\n  theme(axis.ticks=element_blank()) +\n  theme(legend.title = element_text(size=13, face="bold")) +\n  theme(legend.text = element_text(size = 11, face = "bold"))\nedu +  geom_label(aes(label=paste(round(fraction*100, digits = 0),"%"), x=3.5,y=(ymin+ymax)/2), inherit.aes = TRUE, show.legend = FALSE,label.size = 0, color="white") -> p6\n\ngrid.arrange(p4, p5, p6, ncol = 2, nrow = 2)\n```\n\n'

    # donut1 = '\n(ref:wcag'+ str(count) +') WCAG 2.1 Compliance - '+ str(round(aPass/30*100)) +'% Level A, '+ str(round(aaPass/50*100)) +'% Level AA   \n\n(ref:wcag'+ str(count+1) +') WCAG 2.1 Compliance - '+ str(round(aPass/30*100)) +'% Level A, '+ str(round(aaPass/50*100)) +'% Level AA   \n\n```{r,  fig.cap="(ref:wcag'+ str(count) +')",  fig.alt="(ref:wcag'+ str(count+1) +')", fig.align="center", echo=FALSE}\n\nlibrary(ggplot2)\nlibrary(gridExtra)\nlibrary(grid)\nblank_theme <- theme_minimal()+\n  theme(\n    axis.title.x = element_blank(),\n    axis.title.y = element_blank(),\n    panel.border = element_blank(),\n    panel.grid=element_blank(),\n    axis.ticks = element_blank(),\n    plot.title=element_text(size=16, face="bold"),\n  )\ndat = data.frame(count=c('+str(aPass)+', '+str(aFail)+'), category=c("Pass", "Fail"))\ndat$fraction = dat$count / sum(dat$count)\ndat$ymax = cumsum(dat$fraction)\ndat$ymin = c(0, head(dat$ymax, n=-1))\ndat$category <- factor(dat$category, levels = c("Pass", "Fail"))\np1 = ggplot(dat, aes(fill=category, ymax=ymax, ymin=ymin, xmax=4, xmin=3)) +\n  geom_rect(color="white") +\n  coord_polar(theta="y") +\n  xlim(c(2, 4))\nedu<-p1 + scale_fill_brewer("Level A",palette = "Dark2") + blank_theme + \n  theme(axis.text.x=element_blank()) + theme(legend.position=c(.5, .5)) + ggtitle("") +\n  theme(panel.grid=element_blank()) +\n  theme(axis.text=element_blank()) +\n  theme(axis.ticks=element_blank()) +\n  theme(legend.title = element_text(size=16, face="bold")) +\n  theme(legend.text = element_text(size = 14, face = "bold"))\nedu +  geom_label(aes(label=paste(round(fraction*100, digits = 0),"%"), x=3.5,y=(ymin+ymax)/2), inherit.aes = TRUE, show.legend = FALSE,label.size = 0, color="white") -> p3\ndat = data.frame(count=c('+str(aaPass)+', '+str(aaFail)+'), category=c("Pass", "Fail"))\ndat$fraction = dat$count / sum(dat$count)\ndat$ymax = cumsum(dat$fraction)\ndat$ymin = c(0, head(dat$ymax, n=-1))\ndat$category <- factor(dat$category, levels = c("Pass", "Fail"))\np2 = ggplot(dat, aes(fill=category, ymax=ymax, ymin=ymin, xmax=4, xmin=3)) +\n  geom_rect(color="white") +\n  coord_polar(theta="y") +\n  xlim(c(2, 4))\nedu<-p2 + scale_fill_brewer("Level AA",palette = "Dark2") + blank_theme + \n  theme(axis.text.x=element_blank()) + theme(legend.position=c(.5, .5)) + ggtitle("") +\n  theme(panel.grid=element_blank()) +\n  theme(axis.text=element_blank()) +\n  theme(axis.ticks=element_blank()) +\n  theme(legend.title = element_text(size=16, face="bold")) +\n  theme(legend.text = element_text(size = 14, face = "bold"))\nedu +  geom_label(aes(label=paste(round(fraction*100, digits = 0),"%"), x=3.5,y=(ymin+ymax)/2), inherit.aes = TRUE, show.legend = FALSE,label.size = 0, color="white") -> p4\ngrid.arrange(p3, p4, ncol = 2)\n```\n\n'

      
    # # donut2 = '\n(ref:wcag'+ str(count+2) +') WCAG 2.1 Compliance - '+ str(round(aaaPass/78*100)) +'% Level AAA   \n\n(ref:wcag'+ str(count+3) +') WCAG 2.1 Compliance - '+ str(round(aaaPass/78*100)) +'% Level AAA   \n\n```{r,  fig.cap="(ref:wcag'+ str(count+2) +')",  fig.alt="(ref:wcag'+ str(count+3) +')", fig.align="center", echo=FALSE}\nlibrary(ggplot2)\nlibrary(gridExtra)\nlibrary(grid)\nblank_theme <- theme_minimal()+\n  theme(\n    axis.title.x = element_blank(),\n    axis.title.y = element_blank(),\n    panel.border = element_blank(),\n    panel.grid=element_blank(),\n    axis.ticks = element_blank(),\n    plot.title=element_text(size=13, face="bold"),\n  )\ndat = data.frame(count=c('+str(aaaPass)+', '+str(aaaFail)+'), category=c("Pass", "Fail"))\ndat$fraction = dat$count / sum(dat$count)\ndat$ymax = cumsum(dat$fraction)\ndat$ymin = c(0, head(dat$ymax, n=-1))\ndat$category <- factor(dat$category, levels = c("Pass", "Fail"))\np3 = ggplot(dat, aes(fill=category, ymax=ymax, ymin=ymin, xmax=4, xmin=3)) +\n  geom_rect(color="white") +\n  coord_polar(theta="y") +\n  xlim(c(2, 4))\nedu<-p3 + scale_fill_brewer("Level AAA",palette = "Dark2") + blank_theme + \n  theme(axis.text.x=element_blank()) + theme(legend.position=c(.5, .5)) + ggtitle("") +\n  theme(panel.grid=element_blank()) +\n  theme(axis.text=element_blank()) +\n  theme(axis.ticks=element_blank()) +\n  theme(legend.title = element_text(size=13, face="bold")) +\n  theme(legend.text = element_text(size = 11, face = "bold"))\nedu +  geom_label(aes(label=paste(round(fraction*100, digits = 0),"%"), x=3.5,y=(ymin+ymax)/2), inherit.aes = TRUE, show.legend = FALSE,label.size = 0, color="white") -> p6\n\ngrid.arrange(p6, ncol = 1)\n```\n\n'

    # # print(aaPass)
    # if aaPass != 50:
    #     csvout.writelines(donut1)
    #     # csvout.writelines(donut2)

    #     criteria = []
    #     csvout.writelines("This table shows an overview of the WCAG principles that have been successfully attained. \n\n| **Principle**|**Description**| **Result**|\n|:------------:|:--------------:|:---------:|\n")

    #     for principle in wcagprinciples:
    #         if principle in Counter(principlelist).keys():
    #             line = "|" + principle + "|" + wcagprinciples[principle]['Principle'] + "| Fail|" + "\n"
    #         else:
    #             line = "|" + principle + "|" + wcagprinciples[principle]['Principle'] + "| **Pass** |" + "\n"
    #         csvout.writelines(line)


    #     mylist = list(dict.fromkeys(mylist))
    #     wcaglabels = ', '.join([l for l in mylist])
    #     # print(wcaglabels)
    #     failedLabels.clear()


def write_ratings(name, parent, state,count):
    """Requests issues from GitHub API and writes to CSV file."""
    # print(project)
    ratings = ["H", "M", "L"]
    csvfilename = '02.2-wcag-overview.Rmd'
    with open(csvfilename, 'w') as csvfile:
        csvout = csvfile
        # csvout.writelines(["WCAG\n" ])
        for rating in ratings:

            url = 'https://api.github.com/repos/{}/issues?state={}&labels={}'.format(name, state, rating)
            # print(parent)
            r = requests.get(url, auth=auth)
            locate_issues(r, parent)

            # Multiple requests are required if response is paged
            if 'link' in r.headers:
                pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                        (link.split(';') for link in
                        r.headers['link'].split(','))}
                while 'last' in pages and 'next' in pages:
                    pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                            (link.split(';') for link in
                            r.headers['link'].split(','))}
                    r = requests.get(pages['next'], auth=auth)
                    locate_issues(r, parent)
                    if pages['next'] == pages['last']:
                        break
        wcaglabels = failedLabels.sort()
        wcaglist = '\n'.join([l for l in failedLabels])
        mylist = []
        principlelist = []
        criterialist = []

        for l in failedLabels:
            mylist.append(l)
            principlelist.append(l[:3])
            criterialist.append(l)
        # print(Counter(principlelist).keys())
        # print(Counter(mylist).keys())
        # print(Counter(mylist).values())
        # csvout.writelines('### WCAG 2.1 Compliance {-}\n')

        # a = 30
        # aa = 50
        # aaa = 78
        # for criterion in wcagdict:
        #     if criterion in criterialist:
        #         if wcagdict[criterion]['Level'] == "A":
        #             a = a - 1
        #             aa = aa - 1
        #             aaa = aaa - 1
        #         elif wcagdict[criterion]['Level'] == "AA":
        #             aa = aa - 1
        #             aaa = aaa - 1
        #         elif wcagdict[criterion]['Level'] == "AAA":
        #             aaa = aaa - 1
        
        # aPass = a
        # aFail = 30-a
        # aaPass = aa
        # aaFail = 50-aa
        # aaaPass = aaa
        # aaaFail = 78-aaa
        # print(aaaPass)

        # # donut = '\n(ref:wcag'+ str(count) +') WCAG 2.1 Compliance - '+ str(round(aPass/30*100)) +'% Level A, '+ str(round(aaPass/50*100)) +'% Level AA, '+ str(round(aaaPass/78*100)) +'% Level AAA   \n\n(ref:wcag'+ str(count+1) +') WCAG 2.1 Compliance - '+ str(round(aPass/30*100)) +'% Level A, '+ str(round(aaPass/50*100)) +'% Level AA, '+ str(round(aaaPass/78*100)) +'% Level AAA   \n\n```{r,  fig.cap="(ref:wcag'+ str(count) +')",  fig.alt="(ref:wcag'+ str(count+1) +')", fig.align="center", echo=FALSE}\nlibrary(ggplot2)\nlibrary(gridExtra)\nlibrary(grid)\nblank_theme <- theme_minimal()+\n  theme(\n    axis.title.x = element_blank(),\n    axis.title.y = element_blank(),\n    panel.border = element_blank(),\n    panel.grid=element_blank(),\n    axis.ticks = element_blank(),\n    plot.title=element_text(size=13, face="bold"),\n  )\ndat = data.frame(count=c('+str(aPass)+', '+str(aFail)+'), category=c("Pass", "Fail"))\ndat$fraction = dat$count / sum(dat$count)\ndat$ymax = cumsum(dat$fraction)\ndat$ymin = c(0, head(dat$ymax, n=-1))\ndat$category <- factor(dat$category, levels = c("Pass", "Fail"))\np1 = ggplot(dat, aes(fill=category, ymax=ymax, ymin=ymin, xmax=4, xmin=3)) +\n  geom_rect(color="white") +\n  coord_polar(theta="y") +\n  xlim(c(2, 4))\nedu<-p1 + scale_fill_brewer("Level A",palette = "Dark2") + blank_theme + \n  theme(axis.text.x=element_blank()) + theme(legend.position=c(.5, .5)) + ggtitle("") +\n  theme(panel.grid=element_blank()) +\n  theme(axis.text=element_blank()) +\n  theme(axis.ticks=element_blank()) +\n  theme(legend.title = element_text(size=10, face="bold")) +\n  theme(legend.text = element_text(size = 11, face = "bold"))\nedu +  geom_label(aes(label=paste(round(fraction*100, digits = 0),"%"), x=3.5,y=(ymin+ymax)/2), inherit.aes = TRUE, show.legend = FALSE,label.size = 0, color="white") -> p4\ndat = data.frame(count=c('+str(aaPass)+', '+str(aaFail)+'), category=c("Pass", "Fail"))\ndat$fraction = dat$count / sum(dat$count)\ndat$ymax = cumsum(dat$fraction)\ndat$ymin = c(0, head(dat$ymax, n=-1))\ndat$category <- factor(dat$category, levels = c("Pass", "Fail"))\np2 = ggplot(dat, aes(fill=category, ymax=ymax, ymin=ymin, xmax=4, xmin=3)) +\n  geom_rect(color="white") +\n  coord_polar(theta="y") +\n  xlim(c(2, 4))\nedu<-p2 + scale_fill_brewer("Level AA",palette = "Dark2") + blank_theme + \n  theme(axis.text.x=element_blank()) + theme(legend.position=c(.5, .5)) + ggtitle("") +\n  theme(panel.grid=element_blank()) +\n  theme(axis.text=element_blank()) +\n  theme(axis.ticks=element_blank()) +\n  theme(legend.title = element_text(size=13, face="bold")) +\n  theme(legend.text = element_text(size = 11, face = "bold"))\nedu +  geom_label(aes(label=paste(round(fraction*100, digits = 0),"%"), x=3.5,y=(ymin+ymax)/2), inherit.aes = TRUE, show.legend = FALSE,label.size = 0, color="white") -> p5\ndat = data.frame(count=c('+str(aaaPass)+', '+str(aaaFail)+'), category=c("Pass", "Fail"))\ndat$fraction = dat$count / sum(dat$count)\ndat$ymax = cumsum(dat$fraction)\ndat$ymin = c(0, head(dat$ymax, n=-1))\ndat$category <- factor(dat$category, levels = c("Pass", "Fail"))\np3 = ggplot(dat, aes(fill=category, ymax=ymax, ymin=ymin, xmax=4, xmin=3)) +\n  geom_rect(color="white") +\n  coord_polar(theta="y") +\n  xlim(c(2, 4))\nedu<-p3 + scale_fill_brewer("Level AAA",palette = "Dark2") + blank_theme + \n  theme(axis.text.x=element_blank()) + theme(legend.position=c(.5, .5)) + ggtitle("") +\n  theme(panel.grid=element_blank()) +\n  theme(axis.text=element_blank()) +\n  theme(axis.ticks=element_blank()) +\n  theme(legend.title = element_text(size=13, face="bold")) +\n  theme(legend.text = element_text(size = 11, face = "bold"))\nedu +  geom_label(aes(label=paste(round(fraction*100, digits = 0),"%"), x=3.5,y=(ymin+ymax)/2), inherit.aes = TRUE, show.legend = FALSE,label.size = 0, color="white") -> p6\n\ngrid.arrange(p4, p5, p6, ncol = 2, nrow = 2)\n```\n\n'

        # donut1 = '\n(ref:wcag'+ str(count) +') WCAG 2.1 Compliance - '+ str(round(aPass/30*100)) +'% Level A, '+ str(round(aaPass/50*100)) +'% Level AA   \n\n(ref:wcag'+ str(count+1) +') WCAG 2.1 Compliance - '+ str(round(aPass/30*100)) +'% Level A, '+ str(round(aaPass/50*100)) +'% Level AA   \n\n```{r,  fig.cap="(ref:wcag'+ str(count) +')",  fig.alt="(ref:wcag'+ str(count+1) +')", fig.align="center", echo=FALSE}\n\nlibrary(ggplot2)\nlibrary(gridExtra)\nlibrary(grid)\nblank_theme <- theme_minimal()+\n  theme(\n    axis.title.x = element_blank(),\n    axis.title.y = element_blank(),\n    panel.border = element_blank(),\n    panel.grid=element_blank(),\n    axis.ticks = element_blank(),\n    plot.title=element_text(size=16, face="bold"),\n  )\ndat = data.frame(count=c('+str(aPass)+', '+str(aFail)+'), category=c("Pass", "Fail"))\ndat$fraction = dat$count / sum(dat$count)\ndat$ymax = cumsum(dat$fraction)\ndat$ymin = c(0, head(dat$ymax, n=-1))\ndat$category <- factor(dat$category, levels = c("Pass", "Fail"))\np1 = ggplot(dat, aes(fill=category, ymax=ymax, ymin=ymin, xmax=4, xmin=3)) +\n  geom_rect(color="white") +\n  coord_polar(theta="y") +\n  xlim(c(2, 4))\nedu<-p1 + scale_fill_brewer("Level A",palette = "Dark2") + blank_theme + \n  theme(axis.text.x=element_blank()) + theme(legend.position=c(.5, .5)) + ggtitle("") +\n  theme(panel.grid=element_blank()) +\n  theme(axis.text=element_blank()) +\n  theme(axis.ticks=element_blank()) +\n  theme(legend.title = element_text(size=16, face="bold")) +\n  theme(legend.text = element_text(size = 14, face = "bold"))\nedu +  geom_label(aes(label=paste(round(fraction*100, digits = 0),"%"), x=3.5,y=(ymin+ymax)/2), inherit.aes = TRUE, show.legend = FALSE,label.size = 0, color="white") -> p3\ndat = data.frame(count=c('+str(aaPass)+', '+str(aaFail)+'), category=c("Pass", "Fail"))\ndat$fraction = dat$count / sum(dat$count)\ndat$ymax = cumsum(dat$fraction)\ndat$ymin = c(0, head(dat$ymax, n=-1))\ndat$category <- factor(dat$category, levels = c("Pass", "Fail"))\np2 = ggplot(dat, aes(fill=category, ymax=ymax, ymin=ymin, xmax=4, xmin=3)) +\n  geom_rect(color="white") +\n  coord_polar(theta="y") +\n  xlim(c(2, 4))\nedu<-p2 + scale_fill_brewer("Level AA",palette = "Dark2") + blank_theme + \n  theme(axis.text.x=element_blank()) + theme(legend.position=c(.5, .5)) + ggtitle("") +\n  theme(panel.grid=element_blank()) +\n  theme(axis.text=element_blank()) +\n  theme(axis.ticks=element_blank()) +\n  theme(legend.title = element_text(size=16, face="bold")) +\n  theme(legend.text = element_text(size = 14, face = "bold"))\nedu +  geom_label(aes(label=paste(round(fraction*100, digits = 0),"%"), x=3.5,y=(ymin+ymax)/2), inherit.aes = TRUE, show.legend = FALSE,label.size = 0, color="white") -> p4\ngrid.arrange(p3, p4, ncol = 2)\n```\n\n'

      
        # # donut2 = '\n(ref:wcag'+ str(count+2) +') WCAG 2.1 Compliance - '+ str(round(aaaPass/78*100)) +'% Level AAA   \n\n(ref:wcag'+ str(count+3) +') WCAG 2.1 Compliance - '+ str(round(aaaPass/78*100)) +'% Level AAA   \n\n```{r,  fig.cap="(ref:wcag'+ str(count+2) +')",  fig.alt="(ref:wcag'+ str(count+3) +')", fig.align="center", echo=FALSE}\nlibrary(ggplot2)\nlibrary(gridExtra)\nlibrary(grid)\nblank_theme <- theme_minimal()+\n  theme(\n    axis.title.x = element_blank(),\n    axis.title.y = element_blank(),\n    panel.border = element_blank(),\n    panel.grid=element_blank(),\n    axis.ticks = element_blank(),\n    plot.title=element_text(size=13, face="bold"),\n  )\ndat = data.frame(count=c('+str(aaaPass)+', '+str(aaaFail)+'), category=c("Pass", "Fail"))\ndat$fraction = dat$count / sum(dat$count)\ndat$ymax = cumsum(dat$fraction)\ndat$ymin = c(0, head(dat$ymax, n=-1))\ndat$category <- factor(dat$category, levels = c("Pass", "Fail"))\np3 = ggplot(dat, aes(fill=category, ymax=ymax, ymin=ymin, xmax=4, xmin=3)) +\n  geom_rect(color="white") +\n  coord_polar(theta="y") +\n  xlim(c(2, 4))\nedu<-p3 + scale_fill_brewer("Level AAA",palette = "Dark2") + blank_theme + \n  theme(axis.text.x=element_blank()) + theme(legend.position=c(.5, .5)) + ggtitle("") +\n  theme(panel.grid=element_blank()) +\n  theme(axis.text=element_blank()) +\n  theme(axis.ticks=element_blank()) +\n  theme(legend.title = element_text(size=13, face="bold")) +\n  theme(legend.text = element_text(size = 11, face = "bold"))\nedu +  geom_label(aes(label=paste(round(fraction*100, digits = 0),"%"), x=3.5,y=(ymin+ymax)/2), inherit.aes = TRUE, show.legend = FALSE,label.size = 0, color="white") -> p6\n\ngrid.arrange(p6, ncol = 1)\n```\n\n'
    
        # # This stops the donut generating 
        # csvout.writelines(donut1)
        # # csvout.writelines(donut2)

        # criteria = []
        # csvout.writelines("This table shows an overview of the WCAG principles that have been successfully attained.\n\n| **Principle**|**Description**| **Result**|\n|:------------:|:--------------:|:---------:|\n")



        # for principle in wcagprinciples:
        #     if principle in Counter(principlelist).keys():
        #         line = "|" + principle + "|" + wcagprinciples[principle]['Principle'] + "| Fail|" + "\n"
        #     else:
        #         line = "|" + principle + "|" + wcagprinciples[principle]['Principle'] + "| **Pass** |" + "\n"
        #     csvout.writelines(line)


        # mylist = list(dict.fromkeys(mylist))
        # wcaglabels = ', '.join([l for l in mylist])
        # # print(wcaglabels)


parser = argparse.ArgumentParser(description="Write GitHub repository issues "
                                             "to CSV file.")
parser.add_argument('projects', nargs='+', help="Project names")
parser.add_argument('parent', help="Parent label")
parser.add_argument('repository', help="Repository names, "
                    "formatted as 'username/repo'")
parser.add_argument('username', help="Username")
parser.add_argument('token', help="GitHub Token")
parser.add_argument('--wcag',  action='store_true', help="Sort by WCAG")
parser.add_argument('--all', action='store_true', help="Returns both open "
                    "and closed issues.")
args = parser.parse_args()

if args.all:
    state = 'all'

count = 1
projects = args.projects
repository = args.repository
parent = args.parent
username = args.username
password = args.token
auth = (username, password)

failedLabels = []

wcagpath = os.getcwd() + "/utils/wcag21.json"
wcagpath2 = os.getcwd() + "/utils/wcagprinciples.json"
wcagdict = {}
wcagprinciples = {}

with open(wcagpath2, "r") as config_file:
    wcagprinciples = json.load(config_file)

with open(wcagpath, "r") as config_file:
    wcagdict = json.load(config_file)

if args.wcag:
    for project in args.projects:
        get_issues_bywcag(repository, project, state, count)
        count = count + 1
else:
    for project in args.projects:
        get_issues(repository, project, state, count)
        count = count + 1
    write_ratings(repository, parent, state, count)