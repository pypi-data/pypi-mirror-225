"""Client for api protonmail."""

import asyncio
import pickle
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.parser import Parser
from base64 import b64encode, b64decode
import random
from math import ceil
from threading import Thread
from typing import Optional, Coroutine

import unicodedata
from requests import Session
from requests.models import Response
from aiohttp import ClientSession, TCPConnector
from requests_toolbelt import MultipartEncoder
from tqdm.asyncio import tqdm_asyncio

from .models import Attachment, Message, UserMail, Conversation
from .constants import DEFAULT_HEADERS, urls_api
from .utils.pysrp import User
from .logger import Logger
from .pgp import PGP


class ProtonMail:
    """
    Client for api protonmail.
    """
    def __init__(self, logging_level: int = 2, logging_func: callable = print):
        """
        :param logging_level: logging level 1-4 (DEBUG, INFO, WARNING, ERROR), default 2[INFO].
        :type logging_level: ``int``
        :param logging_func: logging function. default print.
        :type logging_func: ``callable``
        """
        self.logger = Logger(logging_level, logging_func)
        self.pgp = PGP()
        self.user = None
        self.account_id = ''
        self.account_email = ''
        self.account_name = ''

        self.session = Session()
        self.session.headers.update(DEFAULT_HEADERS)

    def login(self, username: str, password: str) -> None:
        """
        Authorization in ProtonMail.

        :param username: your ProtonMail address.
        :type username: ``str``
        :param password: your password.
        :type password: ``str``
        :returns: :py:obj:`None`
        """
        data = {'Username': username}

        info = self.session.post('https://api.protonmail.ch/auth/info', json=data).json()
        client_challenge, client_proof, spr_session = self._parse_info_before_login(info, password)

        auth = self.session.post('https://api.protonmail.ch/auth', json={
            'Username': username,
            'ClientEphemeral': client_challenge,
            'ClientProof': client_proof,
            'SRPSession': spr_session,
        }).json()

        if self._login_process(auth):
            self.logger.info("login success", "green")
        else:
            self.logger.error("login failure")

        self._parse_info_after_login(auth)

    def get_messages(self, page_size: int = 150) -> list[Message]:
        """
        Get all messages, sorted by time.

        :param page_size: number of posts per page. maximum number 150.
        :type page_size: ``int``
        :returns: :py:obj:`list[Message]`
        """
        count_page = ceil(self.get_messages_count()[5]['Total'] / page_size)
        args_list = [(page_num, page_size) for page_num in range(count_page)]
        messages_lists = self._process_for_async(self.__async_get_messages, args_list)
        messages_dict = self._flattening_lists(messages_lists)
        messages = [self._convert_dict_to_message(message) for message in messages_dict]

        return messages

    def get_messages_by_page(self, page: int, page_size: int = 150) -> list[Message]:
        """Get messages by page, sorted by time."""
        args_list = [(page, page_size)]
        messages_lists = self._process_for_async(self.__async_get_messages, args_list)
        messages_dict = self._flattening_lists(messages_lists)
        messages = [self._convert_dict_to_message(message) for message in messages_dict]

        return messages

    def get_messages_count(self) -> list[dict]:
        """get total count of messages, count of unread messages."""
        response = self._get('mail', 'mail/v4/messages/count').json()['Counts']
        return response

    def read_conversation(self, conversation_id: str) -> list[Message]:
        """Read conversation by conversation ID."""
        response = self._get('mail', f'mail/v4/conversations/{conversation_id}')
        messages = response.json()['Messages']
        messages = [self._convert_dict_to_message(message) for message in messages]

        return messages

    def get_conversations(self, page_size: int = 150) -> list[Conversation]:
        """Get all conversations, sorted by time."""
        count_page = ceil(self.get_messages_count()[0]['Total'] / page_size)
        args_list = [(page_num, page_size) for page_num in range(count_page)]
        conversations_lists = self._process_for_async(self.__async_get_conversations, args_list)
        conversations_dict = self._flattening_lists(conversations_lists)
        conversations = [self._convert_dict_to_conversation(c) for c in conversations_dict]

        return conversations

    def get_conversations_by_page(self, page: int, page_size: int = 150) -> list[Conversation]:
        """Get conversations by page, sorted by time."""
        args_list = [(page, page_size)]
        conversations_lists = self._process_for_async(self.__async_get_conversations, args_list)
        conversations_dict = self._flattening_lists(conversations_lists)
        conversations = [self._convert_dict_to_conversation(c) for c in conversations_dict]

        return conversations

    def decrypt_conversation(self, conversation_id: dict) -> dict:
        """Decrypt conversation by ID."""
        conversation = self._get(
            'api',
            f'mail/v4/conversations/{conversation_id}'
        ).json()
        messages = filter(None, (msg.get('Body') for msg in conversation.get('Messages', [])))
        return {'id': conversation_id, 'data': [self.pgp.decrypt(data) for data in messages]}

    def get_conversations_count(self) -> list[dict]:
        """get total count of conversations, count of unread conversations."""
        response = self._get('mail', 'mail/v4/conversations/count').json()['counts']
        return response

    def read_message(self, _id: str, mark_as_read: bool = True) -> Message:
        """
        Read message by ID.

        :param _id: the id of the message you want to read.
        :type _id: ``str``

        :param mark_as_read: Mark message as read.
        :type mark_as_read: ``bool``
        :returns: :py:obj:`Message`
        """
        response = self._get('mail', f'mail/v4/messages/{_id}')
        message = response.json()['Message']
        message = self._convert_dict_to_message(message)

        message.body = self.pgp.decrypt(message.body)

        parser = Parser()
        msg = parser.parsestr(message.body)
        if msg.is_multipart():

            body_text = body_html = None
            for i in msg.walk():
                if i.get('Content-Transfer-Encoding') == 'quoted-printable':
                    body_text = unicodedata.normalize('NFKD', i.get_payload(decode=True).decode())
                elif i.get_content_type() == 'text/html':
                    body_html = i.get_payload(decode=True).decode()
                elif i.get_content_type() == 'image/png':
                    content = i.get_payload(decode=True)
                    kwargs = {
                        'name': i.get_filename(),
                        'type': i.get_content_type(),
                        'content': content,
                        'is_decrypted': True,
                        'size': len(content),
                    }
                    if i.get_content_disposition() == 'inline':
                        kwargs['is_inserted'] = True
                        kwargs['cid'] = i.get('Content-ID')[1:-1]

                    message.attachments.append(Attachment(**kwargs))

                elif i.get_content_disposition() == 'attachment':
                    content = i.get_payload(decode=True)
                    kwargs = {
                        'name': i.get_filename(),
                        'type': i.get_content_type(),
                        'content': content,
                        'is_decrypted': True,
                        'size': len(content),
                    }
                    message.attachments.append(Attachment(**kwargs))

            message.body = body_html if body_html else body_text

        if mark_as_read:
            self.mark_messages_as_read([message])

        return message

    def render(self, message: Message) -> None:
        """
        Downloads pictures, decrypts, encodes in BASE64 and inserts into HTML.

        The finished template can be immediately saved to an .html file.
        :param message: the message you want to render
        :type message: ``Message``
        :returns: :py:obj:`None`
        """
        images_for_download = [img for img in message.attachments if img.is_inserted and not img.is_decrypted]
        self.download_files(images_for_download)
        images = [img for img in message.attachments if img.is_inserted]

        for image in images:
            image_b64 = b64encode(image.content).decode()
            template_before = f'src="cid:{image.cid}"'
            template_after = f'src="data:image/png;base64, {image_b64}"'
            message.body = message.body.replace(template_before, template_after)

    def download_files(self, attachments: list[Attachment]) -> list[Attachment]:
        """
        Downloads and decrypts files from the list.

        :param attachments: list of files
        :type attachments: ``list``
        :returns: :py:obj:`list[attachment]`
        """
        args_list = [(attachment, ) for attachment in attachments]
        results = self._process_for_async(self.__async_download_file, args_list)
        threads = [Thread(target=self.__decrypt_file, args=result) for result in results]
        [t.start() for t in threads]
        [t.join() for t in threads]

        return attachments

    def download_file(self, attachment: Attachment) -> Attachment:
        """
        Downloads and decrypts the file

        :param attachment: file
        :type attachment: ``attachment``
        :returns: :py:obj:`attachment`
        """
        return self.download_files([attachment])[0]

    def send_message(self, to: str, subject: str, body: str) -> Message:
        """
        Sends the message.

        :param to: the address to which the message will be sent.
        :type to: ``str``
        :param subject: message subject.
        :type subject: ``str``
        :param body: message body, supports html.
        :type body: ``str``
        :returns: :py:obj:`Message`
        """
        draft = self._create_draft(to, subject, body)
        message = self._prepare_message(body)

        body_message, session_key = self.pgp.encrypt_with_session_key(message)
        body_key = b64encode(session_key)

        fields = {
            f"Packages[multipart/mixed][Addresses][{to}][Type]": (None, '32'),
            f"Packages[multipart/mixed][Addresses][{to}][Signature]": (None, '1'),
            "Packages[multipart/mixed][MIMEType]": (None, 'multipart/mixed'),
            "Packages[multipart/mixed][Body]": ('blob', body_message, 'application/octet-stream'),
            "Packages[multipart/mixed][Type]": (None, '32'),
            "Packages[multipart/mixed][BodyKey][Key]": (None, body_key),
            "Packages[multipart/mixed][BodyKey][Algorithm]": (None, 'aes256'),
            "DelaySeconds": (None, '10'),
        }

        params = {
            'Source': 'composer',
        }

        boundary = '------WebKitFormBoundary' + ''.join(
            random.sample(string.ascii_letters + string.digits, 16)
        )
        multipart = MultipartEncoder(fields=fields, boundary=boundary)

        headers = {
            "Content-Type": multipart.content_type
        }
        response = self._post(
            'mail',
            f'mail/v4/messages/{draft.id}',
            headers=headers,
            params=params,
            data=multipart
        ).json()['Sent']
        message = self._convert_dict_to_message(response)

        return message

    def _create_draft(self, to: str, subject: str, body: str) -> Message:
        """Create the draft. body: html"""

        pgp_body = self.pgp.encrypt(body)

        json_data = {
            'Message': {
                'ToList': [
                    {
                        'Name': to,
                        'Address': to,
                    },
                ],
                'CCList': [],
                'BCCList': [],
                'Subject': subject,
                'Attachments': [],
                'MIMEType': 'text/html',
                'RightToLeft': 0,
                'Sender': {
                    'Name': self.account_name,
                    'Address': self.account_email,
                },
                'AddressID': self.account_id,
                'Unread': 0,
                'Body': pgp_body,
            },
        }

        response = self._post(
            'mail',
            'mail/v4/messages',
            json=json_data
        ).json()['Message']

        draft = self._convert_dict_to_message(response)

        return draft

    def delete_message(self, message: Message) -> None:
        """Deletes the message."""
        self.delete_messages([message])

    def delete_messages(self, messages: list[Message]) -> None:
        """Delete messages."""
        ids = [i.id for i in messages]

        data = {
            "IDs": ids,
        }

        self._put('mail', 'mail/v4/messages/delete', json=data)

    def mark_messages_as_read(self, messages: list[Message]) -> None:
        """
        Mark as read messages.

        :param messages: list of messages.
        :type messages: :py:obj:`Message`
        """
        data = {
            'IDs': [i.id for i in messages],
        }
        self._put('mail', 'mail/v4/messages/read', json=data)

    def pgp_import(self, private_key: str, passphrase: str) -> None:
        """
        Import private pgp key and passphrase.

        :param private_key: your private pgp key that you exported from ProtonMail settings.
                            example: ``privatekey.YourACC@proton.me-12...99.asc``
        :type private_key: ``str``, ``path``, ``file``
        :param passphrase: the passphrase you created when exporting the private key.
        :type passphrase: ``str``
        """
        self.pgp.import_pgp(private_key, passphrase)

    def get_user_info(self) -> dict:
        """User information."""
        return self._get('account', 'core/v4/users').json()

    def get_all_sessions(self) -> dict:
        """Get a list of all sessions."""
        return self._get('account', 'auth/v4/sessions').json()

    def revoke_all_sessions(self) -> dict:
        """revoke all sessions except the current one."""
        return self._delete('account', 'auth/v4/sessions').json()

    def save_session(self, path: str) -> None:
        """
        Saving the current session to a file for later loading.

        WARNING: the file contains sensitive data, do not share it with anyone,
        otherwise someone will gain access to your mail.
        """
        sliced_aes256_keys = dict(list(self.pgp.aes256_keys.items())[:100])
        pgp = {
            'public_key': self.pgp.public_key,
            'private_key': self.pgp.private_key,
            'passphrase': self.pgp.passphrase,
            'aes256_keys': sliced_aes256_keys,
        }
        account = {
            'id': self.account_id,
            'email': self.account_email,
            'name': self.account_name,
        }
        headers = dict(self.session.headers)
        cookies = self.session.cookies.get_dict()
        options = {
            'pgp': pgp,
            'account': account,
            'headers': headers,
            'cookies': cookies,
        }
        with open(path, 'wb') as file:
            pickle.dump(options, file)

    def load_session(self, path: str) -> None:
        """Loading a previously saved session."""
        with open(path, 'rb') as file:
            options = pickle.load(file)

        pgp = options['pgp']
        account = options['account']
        headers = options['headers']
        cookies = options['cookies']

        self.pgp.public_key = pgp['public_key']
        self.pgp.private_key = pgp['private_key']
        self.pgp.passphrase = pgp['passphrase']
        self.pgp.aes256_keys = pgp['aes256_keys']

        self.account_id = account['id']
        self.account_email = account['email']
        self.account_name = account['name']

        self.session.headers = headers
        for name, value in cookies.items():
            self.session.cookies.set(name, value)

    @staticmethod
    def _flattening_lists(list_of_lists: list[list[any]]) -> list[any]:
        flattened_list = [
            item
            for items_list in list_of_lists
            for item in items_list
        ]
        return flattened_list

    @staticmethod
    def _convert_dict_to_message(response: dict) -> Message:
        """
        Converts dictionary to message object.

        :param response: The dictionary from which the message will be created.
        :type response: ``dict``
        :returns: :py:obj:`Message`
        """
        to = [UserMail(user['Name'], user['Address']) for user in response['ToList']]
        attachments_dict = response.get('Attachments', [])
        attachments = []
        for attachment in attachments_dict:
            is_inserted = attachment['Disposition'] == 'inline'
            cid = attachment['Headers'].get('content-id')
            if cid:
                cid = cid[1:-1]
            attachments.append(
                Attachment(
                    id=attachment['ID'],
                    name=attachment['Name'],
                    size=attachment['Size'],
                    type=attachment['MIMEType'],
                    is_inserted=is_inserted,
                    key_packets=attachment['KeyPackets'],
                    cid=cid,
                    extra=attachment
                )
            )

        message = Message(
            id=response['ID'],
            conversation_id=response['ConversationID'],
            subject=response['Subject'],
            unread=response['Unread'],
            sender=UserMail(response['Sender']['Name'], response['Sender']['Address']),
            to=to,
            time=response['Time'],
            size=response['Size'],
            body=response.get('Body', ''),
            type=response.get('MIMEType', ''),
            labels=response['LabelIDs'],
            attachments=attachments,
            extra=response,
        )
        return message

    @staticmethod
    def _convert_dict_to_conversation(response: dict) -> Conversation:
        """
        Converts dictionary to conversation object.

        :param response: The dictionary from which the conversation will be created.
        :type response: ``dict``
        :returns: :py:obj:`Conversation`
        """
        senders = [UserMail(user['Name'], user['Address']) for user in response['Senders']]
        recipients = [UserMail(user['Name'], user['Address']) for user in response['Recipients']]
        conversation = Conversation(
            id=response['ID'],
            subject=response['Subject'],
            senders=senders,
            recipients=recipients,
            num_messages=response['NumMessages'],
            num_unread=response['NumUnread'],
            time=response['Time'],
            size=response['Size'],
            labels=response['LabelIDs'],
            extra=response,
        )
        return conversation

    @staticmethod
    def _prepare_message(data: str) -> str:
        """Converting an unencrypted message into a multipart mime."""
        data_base64 = b64encode(data.encode())

        msg_mixed = MIMEMultipart('mixed')
        msg_alt = MIMEMultipart('alternative')
        msg_plain = MIMEText('', _subtype='plain')
        msg_related = MIMEMultipart('related')
        msg_base = MIMEText('', _subtype='html')

        msg_base.replace_header('Content-Transfer-Encoding', 'base64')
        msg_base.set_payload(data_base64, 'utf-8')

        msg_plain.replace_header('Content-Transfer-Encoding', 'quoted-printable')
        msg_plain.set_payload('hello', 'utf-8')

        msg_alt.attach(msg_plain)
        msg_related.attach(msg_base)
        msg_alt.attach(msg_related)

        msg_mixed.attach(msg_alt)
        message = msg_mixed.as_string().replace('MIME-Version: 1.0\n', '')

        return message

    @staticmethod
    def __update_attachment_content(attachment, content):
        attachment.content = content
        attachment.is_decrypted = True
        attachment.size = len(content)

    def _parse_info_before_login(self, info, password: str) -> tuple[str, str, str]:
        verified = self.pgp.message(info['Modulus'])
        modulus = b64decode(verified.message)
        server_challenge = b64decode(info['ServerEphemeral'])
        salt = b64decode(info['Salt'])
        spr_session = info['SRPSession']

        self.user = User(password, modulus)
        client_challenge = b64encode(self.user.get_challenge()).decode('utf8')
        client_proof = b64encode(self.user.process_challenge(salt, server_challenge)).decode('utf8')

        return client_challenge, client_proof, spr_session

    def _login_process(self, auth: dict) -> bool:
        if auth["Code"] not in (1000, 1001):
            if auth["Code"] == 9001:
                raise NotImplementedError("CAPTCHA not implemented")
            if auth["Code"] == 2028:
                raise ConnectionRefusedError("Too many recent logins")

        self.user.verify_session(b64decode(auth['ServerProof']))

        return self.user.authenticated()

    def _parse_info_after_login(self, auth: dict) -> None:
        self.pgp.session_key = self.user.get_session_key()

        self.session.headers.update({
            'authorization': f'{auth["TokenType"]} {auth["AccessToken"]}',
            'x-pm-uid': auth['UID'],
        })

        address = self.__addresses()['Addresses'][0]

        self.account_id = address['ID']
        self.account_email = address['Email']
        self.account_name = address['DisplayName']

        keys = address['Keys'][0]
        self.pgp.public_key = keys['PublicKey']

    async def __async_get_messages(self, client: ClientSession, page: int, page_size: int = 150) -> list:
        params = {
            "Page": page,
            "PageSize": page_size,
            "Limit": page_size,
            "LabelID": "5",
            "Sort": "Time",
            "Desc": "1",
        }
        response = await client.get(f"{urls_api['mail']}/mail/v4/messages", params=params)
        messages = await response.json()
        return messages['Messages']

    async def __async_get_conversations(self, client: ClientSession, page: int, page_size: int = 150) -> list:
        params = {
            "Page": page,
            "PageSize": page_size,
            "Limit": page_size,
            "LabelID": 0,
            "Sort": "Time",
            "Desc": "1",
            # 'Attachments': 1, # only get messages with attachments
        }
        response = await client.get(f"{urls_api['mail']}/mail/v4/conversations", params=params)
        conversations = await response.json()
        return conversations['Conversations']

    def _process_for_async(self, func: callable, args_list: list[tuple]) -> list[any]:
        results = asyncio.run(
            self.__async_process(func, args_list)
        )
        return results

    async def __async_process(self, func: callable, args_list: list[tuple[any]]) -> list[Coroutine]:
        connector = TCPConnector(limit=100)
        headers = dict(self.session.headers)
        cookies = self.session.cookies.get_dict()

        async with ClientSession(headers=headers, cookies=cookies, connector=connector) as client:
            funcs = (func(client, *args) for args in args_list)
            return await tqdm_asyncio.gather(*funcs, desc=func.__name__)

    async def __async_download_file(self, client: ClientSession, image: Attachment) -> tuple[Attachment, bytes]:
        _id = image.id
        response = await client.get(f"{urls_api['mail']}/mail/v4/attachments/{_id}")
        content = await response.read()
        return image, content

    def __decrypt_file(self, attachment: Attachment, content: bytes) -> None:
        key_packets = attachment.key_packets

        content = self.pgp.message(content).message.ct
        key = self.pgp.decrypt_session_key(key_packets)
        packet_bytes = self.pgp.aes256_decrypt(content, key)

        attachment_bin = self.pgp.message(packet_bytes).message

        self.__update_attachment_content(attachment, attachment_bin)

    def _get(self, base: str, endpoint: str, **kwargs) -> Response:
        return self.__request('get', base, endpoint, **kwargs)

    def _post(self, base: str, endpoint: str, **kwargs) -> Response:
        return self.__request('post', base, endpoint, **kwargs)

    def _put(self, base: str, endpoint: str, **kwargs) -> Response:
        return self.__request('put', base, endpoint, **kwargs)

    def _delete(self, base: str, endpoint: str, **kwargs) -> Response:
        return self.__request('delete', base, endpoint, **kwargs)

    def __request(self, method: str, base: str, endpoint: str, **kwargs) -> Response:
        methods = {
            'get': self.session.get,
            'post': self.session.post,
            'put': self.session.put,
            'delete': self.session.delete
        }
        response = methods[method](f'{urls_api[base]}/{endpoint}', **kwargs)
        return response

    def __addresses(self, params: dict = None) -> dict:
        params = params or {
            'Page': 0,
            'PageSize': 150,  # max page size
        }
        return self._get('api', 'core/v4/addresses', params=params).json()
