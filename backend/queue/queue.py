import uuid
from collections import deque

class MessageQueue:
    def __init__(self):
        self.queue = deque()

    
    def publish(self, payload) -> str:
        task_id = str(uuid.uuid4())
        self.queue.append((task_id, payload))
        return task_id

    
    def consume(self):
        if self.queue:
            task_id, _ = self.queue.popleft()
            return task_id
        return None

    
# Example usage
if __name__ == "__main__":
    mq = MessageQueue()
    id1 = mq.publish({"type": "email", "to": "user@example.com"})
    id2 = mq.publish({"type": "sms", "to": "+1234567890"})
    print("Consumed task:", mq.consume())
    print("Consumed task:", mq.consume())
    print("Nothing left:", mq.consume())
