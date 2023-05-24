import os
os.chdir('myfiles')

import socket
from time import sleep
from threading import Thread
import asyncio

IP, DPORT = 'localhost', 8080

# Helper function that converts integer into 8 hexadecimal digits
# Assumption: integer fits in 8 hexadecimal digits
def to_hex(number):
    # Verify our assumption: error is printed and program exists if assumption is violated
    assert number <= 0xffffffff, "Number too large"
    return "{:08x}".format(number)

async def recv_intro_message(reader: asyncio.StreamReader):
    full_data = await reader.readline()
    return full_data.decode()
    

async def send_long_message(writer: asyncio.StreamWriter, data):
    # TODO: Send the length of the message: this should be 8 total hexadecimal digits
    #       This means that ffffffff hex -> 4294967295 dec
    #       is the maximum message length that we can send with this method!
    #       hint: you may use the helper function `to_hex`. Don't forget to encode before sending!

    # Add a delay to simulate network latency
    await asyncio.sleep(1)

    writer.write(to_hex(len(data)).encode())
    writer.write(data.encode())

    await writer.drain()


async def connect(i):
    reader, writer = await asyncio.open_connection(IP, DPORT)

    """
    Part 1: Introduction
    """
    # TODO: receive the introduction message by implementing `recv_intro_message` above.
    intro = await recv_intro_message(reader)
    print(intro)

    long_msg = "This is a very long message" * 100 + f" AND I AM CLIENT {i}"

    """
    Part 2: Long Message Exchange Protocol
    """

    # Send message
    await send_long_message(writer, long_msg)


    print("Done sending", i)


    return 0

async def main():
    tasks = []
    #for i in range(100):
        #tasks.append(connect(str(i).rjust(8, '0')))

    tasks.append(connect(str(i).rjust(8, '0')))

    await asyncio.gather(*tasks)
    print("done")

# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())
