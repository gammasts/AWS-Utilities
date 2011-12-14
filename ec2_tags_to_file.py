#!/usr/bin/env python

# Gets instance metadata and ec2 tags and writes them out to a sourceable bash file and ini file for reading elsewhere
import urllib
from boto.ec2.connection import EC2Connection

# Use what ever you want to fill in the AWS info (envar, import, plaintext)
conn = EC2Connection("AWS_ACCESS_KEY", "AWS_SECRET_KEY")
reservations = conn.get_all_instances()
# Get all of our instances
instances = [i for r in reservations for i in r.instances]

# Get the current instance id
instance_id = urllib.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read()

print("%s" % instance_id)

f_bash = open('/tmp/instance-metadata', 'w')
f_config = open('/tmp/metadata-config.ini', 'w')

f_config.write("[EC2_TAGS]\n")

# Loop through until we find the instance we are currently on
for i in instances:
    if i.id == instance_id:
        tags = i.tags
        for k, v in tags.items():
            f_bash.write("export EC2_%s=%s\n" % (k.upper(), v))
            f_config.write("%s: %s\n" % (k, v))

f_bash.close()
f_config.close()
