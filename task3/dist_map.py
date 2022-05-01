import hazelcast

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

# Standard Put and Get
for idx in range(1000):
    my_map.put(f"key-{idx}", f"value-{idx}")

# Shutdown this Hazelcast Client
client.shutdown()
