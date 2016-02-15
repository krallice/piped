#!/bin/python

# Imports:
import yaml
from lxml import html
import requests

# Class definition for our pipe object:
class Pipe(object):

  def __init__(self, url, description):
    self.url = url
    self.description = description

  def get_url(self):
    return self.url

  def get_description(self):
    return self.description

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
    newDescriptions = parentTree.xpath('//span[@class="new"]/following-sibling::a/text()')

    pipeList = []

    for i in range(len(newURLs)):
      pipe = Pipe(newURLs[i], newDescriptions[i])
      print pipe.get_url()

# Call pipedMain on program entry:
if __name__ == "__main__":
  pipedMain()
