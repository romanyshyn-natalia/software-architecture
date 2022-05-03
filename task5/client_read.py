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
my_queue = client.get_queue("my-distributed-queue").blocking()

# Standard Take
for idx in range(1000):
    value = my_queue.take()
    print(f"Read: {value}")
    time.sleep(0.01)

# Shutdown this Hazelcast Client
client.shutdown()