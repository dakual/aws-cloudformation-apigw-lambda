import logging, boto3, json, datetime

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

dynamodb = boto3.client('dynamodb')

CONNECTIONS_TABLE = "connections"
MESSAGES_TABLE    = "messages"

def handler(event, context):
    logger.debug(event)

    status_code   = 200
    route_key     = event["requestContext"]["routeKey"]
    connection_id = event["requestContext"]["connectionId"]
    
    if route_key == "$connect":
        dynamodb.put_item(
            TableName = CONNECTIONS_TABLE,
            Item = {
                "connectionId": { "S": str(connection_id) }
            }
        )
    elif route_key == "$disconnect":
        dynamodb.delete_item(
            TableName = CONNECTIONS_TABLE,
            Key = {
                "connectionId": { "S": str(connection_id) }
            }
        )
    elif route_key == "$default":
        message_id = event["requestContext"]["messageId"]
        timestamp  = datetime.datetime.now()
        timestamp  = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        content    = event["body"] if "body" in event else 'Null'

        sendMessage(connection_id, {"messages": content}, event)

        dynamodb.put_item(
            TableName = MESSAGES_TABLE,
            Item = {
                "messageId": { "S": str(message_id) },
                "timestamp": { "S": str(timestamp) },
                "content": { "S": str(content) },
            }
        )
    else:
        # Unknown route key
        status_code = 400
    
    return {
        "statusCode": status_code,
        "body": ""
    }

def sendMessage(connection_id, data, event):
    gatewayapi = boto3.client("apigatewaymanagementapi",
            endpoint_url = "https://" + event["requestContext"]["domainName"] +
                    "/" + event["requestContext"]["stage"])

    return gatewayapi.post_to_connection(ConnectionId=connection_id,
                Data=json.dumps(data).encode('utf-8'))