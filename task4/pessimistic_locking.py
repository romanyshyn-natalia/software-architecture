import hazelcast
import logging
import time

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
    my_map.lock(key)
    try:
        value = my_map.get(key)
        time.sleep(0.01)
        value = str(int(value) + 1)
        my_map.put(key, value)
    finally:
        my_map.unlock(key)

print(f"Finished: Result = {my_map.get(key)}")

# Shutdown this Hazelcast Client
client.shutdown()
