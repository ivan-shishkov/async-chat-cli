import asyncio
import logging
import json
import sys

import configargparse


async def register(host, port, nickname):
    reader, writer = await asyncio.open_connection(host=host, port=port)

    greeting_message = await reader.readline()
    logging.debug(f'Received: {greeting_message.decode().strip()}')

    writer.write('\n'.encode())
    logging.debug('Sent: empty line')

    enter_nickname_message = await reader.readline()
    logging.debug(f'Received: {enter_nickname_message.decode().strip()}')

    writer.write(f'{get_sanitized_text(nickname)}\n'.encode())
    logging.debug(f'Sent: {nickname}')

    user_credentials_message = await reader.readline()
    logging.debug(f'Received: {user_credentials_message.decode().strip()}')

    writer.close()

    return json.loads(user_credentials_message.decode())


async def authorise(host, port, auth_token):
    reader, writer = await asyncio.open_connection(host=host, port=port)

    greeting_message = await reader.readline()
    logging.debug(f'Received: {greeting_message.decode().strip()}')

    writer.write(f'{auth_token}\n'.encode())
    logging.debug(f'Sent: {auth_token}')

    user_credentials_message = await reader.readline()
    logging.debug(f'Received: {user_credentials_message.decode().strip()}')

    if json.loads(user_credentials_message.decode()) is None:
        writer.close()
        return None

    return reader, writer


async def submit_message(reader, writer, message):
    info_message = await reader.readline()
    logging.debug(f'Received: {info_message.decode().strip()}')

    writer.write(f'{get_sanitized_text(message)}\n\n'.encode())
    logging.debug(f'Sent: {message}')


def get_sanitized_text(text):
    return text.replace('\n', '')


async def run_chat_writer(host, port, nickname, auth_token, message):
    if nickname and not auth_token:
        logging.info('Auth token not given. Executing user registration...')

        user_credentials = await register(
            host=host,
            port=port,
            nickname=nickname,
        )
        auth_token = user_credentials['account_hash']

        logging.info(f'Registered successfully. Your auth token: {auth_token}')

    logging.info('Executing user authorisation...')

    stream_handlers = await authorise(
        host=host,
        port=port,
        auth_token=auth_token,
    )

    if stream_handlers is None:
        logging.info('Unknown token. Check it or re-register.')
        return

    logging.info('Successfully authorised')

    reader, writer = stream_handlers

    logging.info('Sending message...')

    await submit_message(
        reader=reader,
        writer=writer,
        message=message,
    )
    logging.info('Message sent successfully')

    writer.close()


def get_command_line_arguments():
    parser = configargparse.ArgumentParser()

    parser.add_argument(
        '--host',
        help='Host for connect to chat. Required',
        env_var='CHAT_HOST',
        type=str,
        required=True,
    )
    parser.add_argument(
        '--port',
        help='Port for connect to chat for writing messages. Default: 5050',
        env_var='CHAT_WRITE_PORT',
        type=int,
        default=5050,
    )
    parser.add_argument(
        '--nickname',
        help='User nickname for registering in chat.',
        env_var='CHAT_NICKNAME',
        type=str,
        default='',
    )
    parser.add_argument(
        '--token',
        help='User token for authorisation in chat.',
        env_var='CHAT_AUTH_TOKEN',
        type=str,
        default='',
    )
    parser.add_argument(
        '--message',
        help='User message for sending to chat. Required',
        env_var='CHAT_MESSAGE',
        type=str,
        required=True,
    )
    return parser.parse_args()


def main():
    command_line_arguments = get_command_line_arguments()

    if not command_line_arguments.nickname and not command_line_arguments.token:
        logging.critical(
            'User credentials are not given '
            '(should be set either nickname or auth token)',
        )
        sys.exit(1)

    logging.basicConfig(level=logging.INFO)

    asyncio.run(
        run_chat_writer(
            host=command_line_arguments.host,
            port=command_line_arguments.port,
            nickname=command_line_arguments.nickname,
            auth_token=command_line_arguments.token,
            message=command_line_arguments.message,
        ),
    )


if __name__ == '__main__':
    main()
