# piped
pipe deamon -- email based python webscraper for tobacco pipes of manhood
new and improved formula -- now a systemd service unit!
---

### Install:

Given that you satisfy the following python module requirements:
+ python-requests
+ python-lxml; and
+ pyyaml

As root run the included ./deploy.sh install script (wont automatically satisfy the python module deps)
to deploy to your local system.

Modify the YAML value for destinationEmails in file /usr/local/etc/piped-private.conf to set your recipients in the following format:
destinationEmails: "user1@example.com, user2@example.com"

Optionally, tune the scrape interval key/value pair called sleepTime in file /usr/local/etc/piped.conf

Enable and start the piped daemon:

```
systemctl enable piped.service
systemctl start piped.service
```

peruse dem pipes kind sir
---
