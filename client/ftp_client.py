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

async def recv_message(reader: asyncio.StreamReader):
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


async def connect():
    reader, writer = await asyncio.open_connection(IP, DPORT)

    intro = await recv_message(reader)
    print(intro)

    password = input("Enter the password: ")

    # Send message
    await send_long_message(writer, password)

    response = await recv_message(reader)
    tries = 0

    await check_authorization(response, reader, writer,tries)

    return 0

async def check_authorization(response, reader, writer, tries):
    if (response == "Incorrect Password!"):
        if (tries == 3):
            print("NAK: Too many failed attempts.")
            return 0
        else:
            print("NAK: ",response)
            tries +=1
            #send new password attempt
            # password = input("Enter the password: ")

            # await send_message(writer, password)
            # response = await recv_message(reader)
            # check_authorization(response, reader, writer, tries)
    else:
        print(response)
    
    return 0


async def main():
    tasks = []
    # for i in range(100):
    #     tasks.append(connect())

    tasks.append(connect())

    await asyncio.gather(*tasks)
    print("Connection Closed")

# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())
