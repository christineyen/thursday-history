#!/bin/bash
while read past
do
  curl -s $past | grep 'street-address' | sed -e 's/.*address">//' -e 's/<\/span.*$//'
done < <(cat past.txt)
