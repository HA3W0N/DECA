#!/bin/bash
urle () { [[ "${1}" ]] || return 1; local LANG=C i x; for (( i = 0; i < ${#1}; i++ )); do x="${1:i:1}"; [[ "${x}" == [a-zA-Z0-9.~-] ]] && echo -n "${x}" || printf '%%%02X' "'${x}"; done; echo; }

echo -e "\nDownloading deca_model..."

FILEID=1rp8kdyLPvErw2dTmqtjISRVvQLj6Yzje
# FILEID=1Vgt4tuzDz67eZf0F35CgkjM9V9ShFBEy
FILENAME=./data/deca_model.tar
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id='1rp8kdyLPvErw2dTmqtjISRVvQLj6Yzje -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1rp8kdyLPvErw2dTmqtjISRVvQLj6Yzje" -O ./data/deca_model.tar && rm -rf /tmp/cookies.txt
