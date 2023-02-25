Both DynamoDB and S3 have data at the order level i.e. one record per order.  
However DynamoDB has the details/value of every product in the order whereas S3 has total value per order.

Refer Architecture diagram for the flow.

Below files have important concepts:

8. Enhanced fan-out consumers
9a. Kinesis firehose - dynamic partitioning
10. Lambda transformation on delivery stream
6. DynamoDB table
