#!/bin/python

# Imports:
import yaml

# Our load config function:
def loadConfig():
  with open("config.yaml", "r") as f:
    config = yaml.load(f)
    return config

def pipedMain():

  # Load up our config variable
  config = loadConfig()

  for brand in config["pipeBrands"]:
    parentURL = config["baseURL"] + brand + "/"
    print parentURL

# Call pipedMain on program entry:
if __name__ == "__main__":
  pipedMain()
