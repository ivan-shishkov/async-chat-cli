import asyncio
import socket
import datetime

from aiofile import AIOFile
import configargparse


def add_datetime_info(text):
    now = datetime.datetime.now()
    return f'[{now.strftime("%d.%m.%Y %H:%M")}] {text}'


async def write_to_file(file_object, text, enable_adding_datetime_info=True):
    text = add_datetime_info(text) if enable_adding_datetime_info else text

    await file_object.write(text)
    await file_object.fsync()


async def run_chat_reading_cycle(
        host, port, output_file_object,
        connection_attempts_count_without_timeout=2,
        timeout_between_connection_attempts=3):
    current_connection_attempt = 0

    while True:
        try:
            current_connection_attempt += 1

            reader, _ = await asyncio.open_connection(host=host, port=port)

            current_connection_attempt = 0

            await write_to_file(
                file_object=output_file_object,
                text='Connection established\n',
            )
            while True:
                message = await reader.readline()
                await write_to_file(
                    file_object=output_file_object,
                    text=f'{message.decode()}',
                )
        except (socket.gaierror, ConnectionRefusedError, ConnectionResetError):
            if current_connection_attempt < connection_attempts_count_without_timeout:
                await write_to_file(
                    file_object=output_file_object,
                    text='No connection. Retrying.\n',
                )
            else:
                await write_to_file(
                    file_object=output_file_object,
                    text=f'No connection. '
                         f'Retrying in {timeout_between_connection_attempts} sec.\n',
                )
                await asyncio.sleep(timeout_between_connection_attempts)


async def run_chat_reader(host, port, output_filepath):
    async with AIOFile(output_filepath, 'a') as file_object:
        await run_chat_reading_cycle(
            host=host,
            port=port,
            output_file_object=file_object,
        )


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
        help='Port for connect to chat for reading messages. Default: 5000',
        env_var='CHAT_READ_PORT',
        type=int,
        default=5000,
    )
    parser.add_argument(
        '--output',
        help='Filepath for save chat messages. Default: chat.txt',
        env_var='OUTPUT_FILEPATH',
        type=str,
        default='chat.txt',
    )
    return parser.parse_args()


def main():
    command_line_arguments = get_command_line_arguments()

    asyncio.run(
        run_chat_reader(
            host=command_line_arguments.host,
            port=command_line_arguments.port,
            output_filepath=command_line_arguments.output,
        ),
    )


if __name__ == '__main__':
    main()
