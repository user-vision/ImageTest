#!/bin/bash
#set -ev
#python utils/github_issues_to_md.py $@
#Rscript -e "rmarkdown::render_site(output_format = 'md_document', encoding = 'UTF-8')"
#Rscript -e "bookdown::render_book('index.Rmd', 'bookdown::gitbook')"
#Rscript -e "rmarkdown::render_site(output_format = 'bookdown::pdf_book', encoding = 'UTF-8')"
#tail -n +2 _main.md > _main.tmp
#cat index.Rmd _main.tmp > accessibility_audit.md
rm _main.*
rm 02.2*
rm 05*
rm -rf public
#rm _main.tmp
#Rscript -e 'rmarkdown::render("accessibility_audit.md", output_format = "powerpoint_presentation", output_dir = "public", output_file = "accessibility_audit.pptx")'
#rm accessibility_audit.md
docker run --rm -v "$(pwd)":/app -e 'REPO=user-vision/template-report' -e 'BRANCHES=chapter-labels' -e 'AUTH='$1'' -e 'PARENT=UVXXXX' uservision/uv-python; 
docker run --rm -v "$(pwd)":/app uservision/uv-a11yreport:latest 
docker run --rm -v "$(pwd)":/app uservision/uv-pdf:pandoc 