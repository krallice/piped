#!/bin/python

# Imports:
import os
import re
import yaml
import requests
from lxml import html

# Class definition for our pipe object:
class Pipe(object):

  def __init__(self, url, brand, description, img, price):
    self.url = url
    self.brand = brand
    self.description = description
    self.img = img
    self.price = price
    self.newPipe = True

  def get_url(self):
    return self.url

  def get_brand(self):
    return self.brand

  def get_pretty_brand(self):
    return self.brand.title()

  def get_description(self):
    return self.description

  def get_img(self):
    return self.img

  def get_price(self):
    return self.price

  def get_newStatus(self):
    return self.newPipe

  def set_oldPipe(self):
    self.newPipe = False

# Our load config function:
def loadConfig():

  with open("config.yaml", "r") as f:
    openConfig = yaml.load(f)
  with open("privateconfig.yaml", "r") as f:
    privateConfig = yaml.load(f)

  config = openConfig.copy()
  config.update(privateConfig)
  return config

# Send Basic Email via sendmail, perhaps oneday replace 
# with a nice MIME templated email:
def sendBasicMail(newPipes, senderAddress, destinationEmails, domainTop):

  # Leverage sendmail binary:
  sendmail_location = "/usr/sbin/sendmail"
  p = os.popen("%s -t" % sendmail_location, "w")
  p.write("From: %s\n" % senderAddress)
  p.write("To: %s\n" % destinationEmails)
  p.write("Subject: New Pipes!\n")
  p.write("Content-Type: text/html")
  p.write("\n") # blank line separating headers from body
  p.write("<h3>%s freshly baked pipes for your gentlemanly perusal ...</h3>" % len(newPipes)) # blank line separating headers from body
  p.write("<table border=1>")
  for pipe in newPipes:
    fullPath=domainTop + pipe.get_url()
    p.write("<tr>")
    p.write("<td><a href='%s'>%s</a></td>\n" % ( fullPath, pipe.get_description() ))
    p.write("<td>%s</td>\n" % pipe.get_pretty_brand())
    p.write("<td><a href='%s'><img src='%s'></a></td>\n" % ( fullPath, pipe.get_img() ))
    p.write("<td>%s</td>\n" % pipe.get_price())
    p.write("</tr>")
  p.write("</table>")
  status = p.close()

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
    newImgs = parentTree.xpath('//span[@class="new"]/../preceding-sibling::div/a/img/@src')
    newPrices = parentTree.xpath('//span[@class="new"]/../../following-sibling::div/div/following-sibling::div/div/sup/following-sibling::text()')

    # Populate the Pipe class:
    for i in range(len(newURLs)):
      # Strip out the strange whitespace out of our prices:
      newPrices[i] = re.sub('[\n\t\r]', '', newPrices[i])
      pipe = Pipe(newURLs[i], brand, newDescriptions[i], newImgs[i], newPrices[i])
      pipeList.append(pipe)
      print pipe.get_url()

  # Open our cache file:
  with open(config["cacheFile"], "a+") as cf:

    if debugMode == 1:
      print "Reading Cache File"

    # Read file into string (scaling should be ok):
    cache = cf.readlines()

    newPipes = []

    # Compare our cache with our pipeList:
    for pipe in pipeList:
      for line in cache:
        if pipe.get_url() == line.rstrip():
          pipe.set_oldPipe()   
          if debugMode == 1:
            print "Pipe " + pipe.get_description() + " is OLD!"
      # Our pipe is new?
      if pipe.get_newStatus() == True:
        # Update our cache:
        cf.write(pipe.get_url() + "\n")
        newPipes.append(pipe)

    # Check if we actually have new pipes:
    if len(newPipes) > 1:
      if debugMode == 1:
        print "New Pipes Exist -- Sending Email"
      sendBasicMail(newPipes, config["senderAddress"], config["destinationEmails"], config["domainTop"])

# Call pipedMain on program entry:
if __name__ == "__main__":
  pipedMain()
