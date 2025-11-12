#!/bin/bash 

echo "INSTALLING AiiDAlab ALC app"
cd "${HOME}"/apps
wget https://github.com/stfc/alc-ux/archive/refs/heads/main.zip 
unzip main.zip 
rm -f main.zip 
cd "${HOME}"/apps/alc-ux-main 
pip install -q . 


cd "${HOME}" 
