import boto3
import logging
import json
import sys
import time
from order_generator import make_order

kinesis = boto3.client('kinesis')

logging.basicConfig(
  format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S',
  level=logging.INFO,
  handlers=[
      logging.FileHandler("producer.log"),
      logging.StreamHandler(sys.stdout)
  ]
)

def main(args):

    stream_name = args[1]
    logging.info(f'Publishing records into the kinesis data stream {stream_name}')

    shard_sequence_num_details = {}

    while True:

        # Note that we are using seller_id and not order_id as the partition key here
        # This is because, we want to see that for the same partition key, when the record is loaded into the same shard, sequencing is maintained
        # order_id is a running number and we will not be able to test the "same partition key" concept
        # All records with same partition key go into the same shard
       
        order = make_order()
        partition_key = order['seller_id']


        # Note that we create a dict, update the dict with another key only if the record with the same partition key is already available in the shard_sequence_num_details
        # and then use the dict in the put_record api. Without this approach, if we try to insert like in 1. Publish individual records, the program will fail
        # because sequence number is not present for the initial records

        kwargs = dict(
                      StreamName = stream_name,
                      Data = json.dumps(order).encode('utf-8'),
                      PartitionKey = order['order_id']
                    )

        if partition_key in shard_sequence_num_details:
            seq_num = shard_sequence_num_details.get(partition_key)
            kwargs.update(SequenceNumberForOrdering = seq_num)

        try:
            
            response = kinesis.put_record(**kwargs)

            logging.info(f"Successfully published order {order['order_id']} into the kinesis stream {stream_name}")
            logging.info(f"The order details are: {order}")
            logging.info(f"The partition key is {partition_key} and the record is published into Shard {response['ShardId']} with sequence number as {response['SequenceNumber']}")

            shard_sequence_num_details[partition_key] = response['SequenceNumber']
            logging.info(f'{shard_sequence_num_details}')
        
        except Exception as e:

            logging.error(f"Failed to publish order {order['order_id']} into the kinesis stream {stream_name}. The exception is {e}")

        # time.sleep(6)

if __name__ == '__main__':
    main(sys.argv)

