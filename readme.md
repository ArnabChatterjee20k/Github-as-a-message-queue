# Idea
## Producer-Consumer Strategy:
### Producer:
* The producer is the entity or process responsible for creating messages (or tasks) and placing them in a message queue (or buffer).
* The queue acts as a temporary storage area that holds messages until a consumer can process them.
* Producers do not need to know how or when the consumers will process the messages; their primary task is to generate and enqueue messages in queue order (typically FIFO: First In, First Out).

### Consumer:
* The consumer is the entity or process that retrieves messages from the message queue and processes them.
* It operates independently of the producer and consumes messages in the order they were placed in the queue (if FIFO is being used).
* Consumers usually pull messages from the queue, ensuring no message is left unprocessed.

## How github fits here?
1. Issue = Payload:

* Each issue represents a message payload.
* The issue's description contains the body of the message payload.
* Additional metadata (e.g., priority, type, etc.) can be added as labels or custom fields.

2. Queue Management:

* GitHub issues inherently act as a queue because they are sequentially created.
* Sorting by creation date or assigning priority labels can determine processing order.

3. Consumer Scripts:

* Scripts are consumers that poll GitHub for new issues or are triggered by GitHub webhooks.
* Scripts parse the issue description and execute the necessary workflows or actions.

4. Trigger via API:
* Use GitHub's REST or GraphQL API to create issues programmatically. This makes it easy to integrate with other systems.


### Steps
1. add github access token to the package
2. generate labels
3. map labels to consumer script and create the lables in the github
4. generate the github actions script
5. ask the user to create a empty github repo. And tell him to copy the http url
6. use the http url and publish the urls to the repo online using github of the user

### TODO
[] Also copy the requirements.txt to the repo along with the consumers
[] Preparing some app to showcase
[] turn the label in the action to array to call multiple files in order for having a multiple consumer type thingy
[] clearing the message or the issue