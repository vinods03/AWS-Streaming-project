import logging
import boto3
import json
import time
import sys
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
    logging.info(f"Starting to write into Kinesis data stream {stream_name}")

    while True:

        order = make_order()
        try:
            response = kinesis.put_record(
                                          StreamName = stream_name,
                                          Data = json.dumps(order).encode('utf-8'),
                                          PartitionKey = order['order_id']
                                          )
            logging.info(f'Successfully transferred order into kinesis data stream {stream_name}')
            logging.info(f'The order published into kinesis data stream is {order}')
            # logging.info(f'The response is {response}')
            logging.info(f"The order is published in shard {response['ShardId']} with sequence number {response['SequenceNumber']}")
        except Exception as e:
            logging.error(f'Failed to transfer order into kinesis data stream {stream_name}')

        time.sleep(3)

if __name__ == '__main__':
    main(sys.argv)