#!/bin/python

baseURL = "https://www.smokingpipes.com/pipes/new/"
pipeBrands = [ "neerup", "nording" ]

for brand in pipeBrands:
  parentURL = baseURL + brand + "/"
  print parentURL
