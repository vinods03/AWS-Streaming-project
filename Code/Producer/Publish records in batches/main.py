import boto3
import json
import sys
import logging
import time

from order_generator import make_order

logging.basicConfig(
  format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S',
  level=logging.INFO,
  handlers=[
      logging.FileHandler("producer.log"),
      logging.StreamHandler(sys.stdout)
  ]
)

kinesis = boto3.client('kinesis')

def main(args):

    stream_name = args[1]
    logging.info(f'Started publishing messages into the kinesis data stream {stream_name}')

    orders = []
    batch_number = 1

    while True:

        order = make_order()
        order_for_kinesis_put = dict(Data = json.dumps(order).encode('utf-8'), PartitionKey = order['order_id'])
        orders.append(order_for_kinesis_put)
        
        if len(orders) > 20:

            try:
                response = kinesis.put_records(StreamName = stream_name, Records = orders)
                logging.info(f'Successfully published batch number {batch_number} records into the kinesis data stream {stream_name}')
                # logging.info(f'The response is {response}')

                for i, record_response in enumerate(response['Records']):
                    error_code = record_response.get('ErrorCode')
                    if error_code:
                        error_message = record_response.get('ErrorMessage')
                        logging.error(f"Failed to publish order  {orders[i]['Data']}. The error is {error_message}")
                    else:
                        logging.info(f'Order number {i} published for batch number {batch_number}')
                        logging.info(f"The order {orders[i]['Data']} is published into Shard {record_response['ShardId']} with Sequence number {record_response['SequenceNumber']}")

            except Exception as e:
                logging.error(f'Failed to publish with exception {e}')
                break

            orders = []
            batch_number = batch_number + 1
            time.sleep(20)

if __name__ == '__main__':
    main(sys.argv)