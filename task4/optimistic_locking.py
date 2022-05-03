import logging
import time

import hazelcast

# Configure the logging
logging.basicConfig(level=logging.INFO)

# Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
client = hazelcast.HazelcastClient(cluster_name="dev",
                                   cluster_members=[
                                       "127.0.0.1:5701",
                                       "127.0.0.1:5702",
                                       "127.0.0.1:5703"
                                   ])
print("Connected to cluster")

# Get the Distributed Map from Cluster.
my_map = client.get_map("my-distributed-map").blocking()

key = "1"
value = "0"
my_map.put_if_absent(key, value)

# Standard Put and Get
for i in range(1000):
    while True:
        old_value = value = my_map.get(key)
        new_value = int(old_value)
        time.sleep(0.01)
        new_value += 1
        if my_map.replace_if_same(key, old_value, str(new_value)):
            break

print(f"Finished: Result = {my_map.get(key)}")

# Shutdown this Hazelcast Client
client.shutdown()
