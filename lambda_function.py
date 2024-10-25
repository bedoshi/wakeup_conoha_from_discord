import json
import os
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

def verify_signature(event):
    """Verify that the request came from Discord"""
    PUBLIC_KEY = os.environ['DISCORD_PUBLIC_KEY']

    # ヘッダーからの取得を小文字に統一（API Gatewayの仕様に対応）
    headers = {k.lower(): v for k, v in event['headers'].items()}

    signature = headers.get('x-signature-ed25519')
    timestamp = headers.get('x-signature-timestamp')
    body = event.get('body', '')

    if not signature or not timestamp:
        return False

    try:
        verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
        verify_key.verify(
            f'{timestamp}{body}'.encode(),
            bytes.fromhex(signature)
        )
        return True
    except (BadSignatureError, ValueError, TypeError):
        return False

def lambda_handler(event, context):
    """Handle incoming Discord interactions"""
    print("Received event:", json.dumps(event))  # デバッグ用ログ

    # 署名検証
    if not verify_signature(event):
        print("Signature verification failed")  # デバッグ用ログ
        return {
            'statusCode': 401,
            'body': json.dumps('invalid request signature')
        }

    # リクエストボディの解析
    try:
        body = json.loads(event['body'])
    except json.JSONDecodeError:
        print("Failed to parse request body")  # デバッグ用ログ
        return {
            'statusCode': 400,
            'body': json.dumps('invalid request body')
        }

    # PINGリクエストの処理
    if body['type'] == 1:  # PING
        print("Responding to PING")  # デバッグ用ログ
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'type': 1  # PONG
            })
        }

    # その他のコマンド処理
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'type': 4,
            'data': {
                'content': 'Command received'
            }
        })
    }