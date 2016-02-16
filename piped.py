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
    self.newPipe = True

  def get_url(self):
    return self.url

  def get_description(self):
    return self.description

  def get_newStatus(self):
    return self.newStatus

  def set_oldPipe(self):
    self.newStatus = False

# Our load config function:
def loadConfig():

  with open("config.yaml", "r") as f:
    config = yaml.load(f)
    return config

# Our Main Function:
def pipedMain():

  debugMode = 1

  config = loadConfig()
  pipeList = []

  # Loop over each pipe brand, and populate our Pipe class:
  for brand in config["pipeBrands"]:

    parentURL = config["baseURL"] + brand + "/"
    if debugMode == 1:
      print "Fetching " + parentURL
    parentHTML = requests.get(parentURL)
    parentTree = html.fromstring(parentHTML.content)

    # Locate the 'NEW' spans:
    newURLs = parentTree.xpath('//span[@class="new"]/following-sibling::a/@href')
    newDescriptions = parentTree.xpath('//span[@class="new"]/following-sibling::a/text()')

    # Populate the Pipe class:
    for i in range(len(newURLs)):
      pipe = Pipe(newURLs[i], newDescriptions[i])
      pipeList.append(pipe)
      print pipe.get_url()

  # Open our cache file for reading:
  with open(config["cacheFile"], "a+") as cf:

    if debugMode == 1:
      print "Reading Cache File"

    # Read file into string (scaling should be ok):
    cache = cf.readlines()

    # Compare our cache with our pipeList:
    for pipe in pipeList:
      for line in cache:
        if pipe.get_url() == line.rstrip():
          pipe.set_oldPipe()   
          if debugMode == 1:
            print "Pipe " + pipe.get_description() + " is OLD!"

    # Generate Notification of new pipes + update our cache:
    if debugMode == 1:
      print "Generating Email now and updating cache:"
    for pipe in pipeList:
      if pipe.get_newStatus() == True:
      # todo: generate notification + update cache 

# Call pipedMain on program entry:
if __name__ == "__main__":
  pipedMain()
