import uuid
from collections import deque

class MessageQueue:
    def __init__(self):
        self.queue = deque()
        self.task_ids = set()

    def publish(self, task_id, payload) -> bool:
        """Publish a task if not already present."""
        if task_id in self.task_ids:
            print(f"Task {task_id} already exists. Skipping duplicate.")
            return False
        self.queue.append((task_id, payload))
        self.task_ids.add(task_id)
        print(f"Task {task_id} submitted.")
        return True

    def has_task(self, task_id: str) -> bool:
        """Check if a task_id is already in the queue."""
        return task_id in self.task_ids

    def consume(self):
        if self.queue:
            task_id, payload = self.queue.popleft()
            self.task_ids.remove(task_id)
            return task_id, payload
        return None
    
queue = MessageQueue()

    
# # Example usage
# if __name__ == "__main__":
#     mq = MessageQueue()
#     id1 = mq.publish({"type": "email", "to": "user@example.com"})
#     id2 = mq.publish({"type": "sms", "to": "+1234567890"})
#     print("Consumed task:", mq.consume())
#     print("Consumed task:", mq.consume())
#     print("Nothing left:", mq.consume())
