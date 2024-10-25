import json
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

def verify_signature(event):
    """Verify that the request came from Discord"""
    try:
        PUBLIC_KEY = 'YOUR_DISCORD_PUBLIC_KEY'

        headers = {k.lower(): v for k, v in event['headers'].items()}
        signature = headers.get('x-signature-ed25519')
        timestamp = headers.get('x-signature-timestamp')
        body = event.get('body', '')

        verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
        verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
        return True
    except:
        return False

def lambda_handler(event, context):
    """Handle incoming Discord interactions"""
    if not verify_signature(event):
        return {
            'statusCode': 401,
            'body': json.dumps('invalid request signature')
        }

    body = json.loads(event['body'])

    if body['type'] == 1:  # PING
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'type': 1})
        }

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'type': 4,
            'data': {
                'content': 'Command received'
            }
        })
    }