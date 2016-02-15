#!/bin/python

# Imports:
import yaml
from lxml import html
import requests

# Our load config function:
def loadConfig():

  with open("config.yaml", "r") as f:
    config = yaml.load(f)
    return config

def pipedMain():

  debugMode = 1
  config = loadConfig()

  # Loop over each pipe brand:
  for brand in config["pipeBrands"]:

    parentURL = config["baseURL"] + brand + "/"
    if debugMode == 1:
      print "Fetching " + parentURL
    parentHTML = requests.get(parentURL)
    parentTree = html.fromstring(parentHTML.content)

    # Locate the 'NEW' spans:
    newURLs = parentTree.xpath('//span[@class="new"]/following-sibling::a/@href')
    newNames = parentTree.xpath('//span[@class="new"]/following-sibling::a/text()')
    print newURLs
    print newNames

# Call pipedMain on program entry:
if __name__ == "__main__":
  pipedMain()
