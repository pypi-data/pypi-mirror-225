# queue-local-python-package

## Usage:

Install: `pip install queue-local`  
(Preferable you add queue-local to requirements.txt)  

Use the `DatabaseQueue`:
```py
from queue_local.database_queue import DatabaseQueue

q = DatabaseQueue()
q.push({"item": "test 1", "action_id": 1})
result = q.peek()  # "test 1" is still in the queue
result = q.get()   # "test 1" is no longer in the queue
result = q.get_by_action_ids(action_ids=(1, ))  # action_ids must be tuple


```
Inherit from our abstract queue:
```py
from queue_local.our_queue import OurQueue

class YourClass(OurQueue):
    def __init__(self):
        pass
    
    def push(self, item):
        """push to the queue"""
        pass

    def get(self):
        """get from the queue (and delete)"""
        pass

    def peek(self):
        """get the head of the queue (without deleting)"""
        pass
    # add whatever functions you like, like is_empty()
```