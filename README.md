# HW 2: Deployment and work with distributed in-memory data structures based on Hazelcast: Distributed Map

Task results:
### Task 1
We installed Hazelcast.

### Task 2
3 nodes:
![3 nodes](images/3nodes.png)

### Task 3
Code in [task3/dist_map.py](task3/dist_map.py).

Data in nodes before deleting 3rd node:
![3 nodes map](images/3nodes_map.png)

After deleting 3rd node:
![2 nodes](images/2nodes_map.png)

### Task 4
Code in [task4/](task4).

No locks:
![map browser](images/map_browser_1.png)

Pessimistic locking:
![map browser](images/map_browser_2.png)

Optimistic locking:
![map browser](images/map_browser_3.png)

### Task 5
Into Hazelcast config file (hazelcast.xml) for bounding we added following lines:
```
<queue name="my-distributed-queue">
        <max-size>10</max-size>
</queue>
```

When we only have writing into queue (we bounded it by 10), we see such results:
![queue](images/queue_only_write1.png)

We used blocking queue, so it did not stop, it was just waiting for free spots in the queue.

After we started two reading clients, they took out all the values (they took different values, no data races and such) 
and writer could write all the 1000 values into queue. After readers took all the values, queue became empty.
Reader 1:
![reader](images/reader1.png)

Reader 2: 
![reader](images/reader2.png)
