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


async def ftp_list(reader,writer):
    # Directory list code obtained from "https://docs.python.org/3/library/os.html#os.listdir"
    list_string = os.listdir(path='../../server/myfiles')

    # Print format obtained from "https://stackoverflow.com/questions/13893399/python-print-array-with-new-line"
    print(*list_string, sep='\n')

    # Extra print used for text alignment in terminal
    print(" ")
    return

# Better understanding on os.remove() obtained from "https://www.geeksforgeeks.org/python-os-remove-method/"
async def ftp_remove(reader,writer):
    file_to_del = input("Enter the file name with extension to delete: \n")
    location = '../../server/myfiles'
    path = os.path.join(location, file_to_del)

    try:
        os.remove(path)
        print("% s removed!\n" % file_to_del)
    except OSError as error:
        print(error)
        print("File not succesfully deleted!")

    return




async def ftp_client_cmds(reader, writer):
    command = ""
    
    while(command != "close"):
        command = input("ftp> ")
        await send_long_message(writer, command)

        confirmation = await recv_intro_message(reader)
        # print(confirmation[:len(confirmation)-1])

        if(command == "list"):
            await ftp_list(reader, writer)

        if(command == "remove"):
            await ftp_remove(reader, writer)


    return


async def connect():
    reader, writer = await asyncio.open_connection(IP, DPORT)

    # TODO: receive the introduction message by implementing `recv_intro_message` above.
    intro = await recv_intro_message(reader)
    print(intro)

    password = input("Enter the password: ")

    # Send message
    await send_long_message(writer, password)

    response = await recv_intro_message(reader)
    
    print(response)

    tries = 0

    while(tries != 3):

        if(response != "Correct! Welcome to my (diazric) server! I'm majoring in CS\n"):
            tries +=1
            if(tries < 3):
                password = input("Enter the password: ")
                await send_long_message(writer, password)
                response = await recv_intro_message(reader)
                if((tries != 2) or (response == "Correct! Welcome to my (diazric) server! I'm majoring in CS\n")):
                    print(response)
        else:
            #grant access to user, continue implementation here
            break

    if ((tries != 3)):
        await ftp_client_cmds(reader, writer)
        return 0
    else:
        print("Too many failed attempts! Bye!")

    return 0

async def main():
    tasks = []
    #for i in range(100):
        #tasks.append(connect(str(i).rjust(8, '0')))

    tasks.append(connect())

    await asyncio.gather(*tasks)
    print("Connection Closed")

# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())