import base64


def download_message_attachment(service, message, user_id: str, store_dir: str, file_type: str):
    """
    https://stackoverflow.com/a/27335699
    changed path = '/'.join([store_dir, part['filename']])
    """
    parts = [message['payload']]
    while parts:
        part = parts.pop()
        file_data = None
        if part.get('parts'):
            parts.extend(part['parts'])
        if part.get('filename'):
            if file_type in part['filename']:
                if 'data' in part['body']:
                    file_data = base64.urlsafe_b64decode(part['body']['data'].encode('UTF-8'))
                elif 'attachmentId' in part['body']:
                    attachment = service.users().messages().attachments().get(
                        userId=user_id, messageId=message['id'], id=part['body']['attachmentId']
                    ).execute()
                    file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
        if file_data:
            # do some stuff, e.g.
            path = '/'.join([store_dir, part['filename']])
            with open(path, 'wb') as f:
                f.write(file_data)
