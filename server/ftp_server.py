import os
os.chdir('myfiles')

import socket
import asyncio

INTERFACE, SPORT = 'localhost', 8080
CHUNK = 100



# TODO: Implement me for Part 1!
async def send_message(message, writer):

    writer.write(message.encode())
    await writer.drain()


# TODO: Implement me for Part 2!
async def receive_long_message(reader: asyncio.StreamReader):
    # First we receive the length of the message: this should be 8 total hexadecimal digits!
    # Note: `socket.MSG_WAITALL` is just to make sure the data is received in this case.
    data_length_hex = await reader.readexactly(8)

    # Then we convert it from hex to integer format that we can work with
    data_length = int(data_length_hex, 16)

    full_data = await reader.readexactly(data_length)
    return full_data.decode()


async def handle_client(reader, writer):

    # TODO: send the introduction message by implementing `send_message` above.
    intro_message = "Please enter the correct password to access the server\n"
    deny_message = "Incorrect password. Try Again! \n"
    pass_message = "Correct! Welcome to my (diazric) server! I'm majoring in CS\n"

    await send_message(intro_message, writer)

    # TODO: Implement function above
    message = await receive_long_message(reader)

    key = "cs372"

    if(message == key):
        await send_message(pass_message, writer)
        writer.close()
        await writer.wait_closed()
    else:
        await send_message(deny_message , writer)

    message = await receive_long_message(reader)

    if(message == key):
        await send_message(pass_message, writer)
        writer.close()
        await writer.wait_closed()
    else:
        await send_message(deny_message, writer)

    message = await receive_long_message(reader)

    if(message == key):
        await send_message(pass_message, writer)
        writer.close()
        await writer.wait_closed()
    else:
        await send_message(deny_message, writer)


    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(
            handle_client,
            INTERFACE, SPORT
    )

    async with server:
        await server.serve_forever()

# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())