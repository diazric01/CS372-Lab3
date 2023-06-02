import os
os.chdir('myfiles')

import socket
import asyncio

INTERFACE, SPORT = 'localhost', 8093
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


async def ftp_list(reader,writer):
    # Directory list code obtained from "https://docs.python.org/3/library/os.html#os.listdir"
    # How to move back one directory. "https://stackoverflow.com/questions/12280143/how-to-move-to-one-folder-back-in-python"
    list_string = os.listdir(path='.')

    new_string = ""

    for ele in list_string:
        new_string += (ele + " ")

    new_string += "\n"
    await send_message(new_string, writer)

    return

# Better understanding on os.remove() obtained from "https://www.geeksforgeeks.org/python-os-remove-method/"
async def ftp_remove(reader,writer, file):
    location = '.'
    path = os.path.join(location, file)

    try:
        os.remove(path)
        ret_msg = ("% s Removed!\n" % file)
        await send_message(ret_msg, writer)
    except OSError as error:
        await send_message("NAK File not succesfully deleted! (Check file exists and was typed correctly)\n", writer)

    return

# Sources used: "https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files"
async def ftp_get_file(reader, writer, file):

    try:
        f = open(file, 'r', encoding="utf-8")
        file_contents = f.read()
        f.close()
        await send_message(file_contents, writer)
    except OSError:
        error_msg = ("NAK Trouble getting file: %s (Check file exists and was typed correctly)\n" % file)
        await send_message(error_msg, writer)

    return

async def ftp_put_file(reader, writer, file):
    error_sent = False
    file_contents = await receive_long_message(reader)

    split_contents = file_contents.split(" ")

    if(split_contents[0] != "NAK"):
        try:
            with open(file, 'w') as f:
                f.write(file_contents)
            f.close()
        except:
            error_sent = True
            await send_message("NAK Error Creating File\n", writer)
    else:
        error_sent = True
        await send_message("NAK Error Downloading File\n", writer)

    if(error_sent == False):
        await send_message("ACK Succesfull\n",writer)

    
    
    return

async def ftp_server_cmds(reader, writer):
    # I realized too late that a switch case would've made for cleaner code.
    while (1):
        command = await receive_long_message(reader)
        split_command = command.split(" ")

        # await send_message("ACK\n", writer)

        if(split_command[0] == "close"):
            await send_message("ACK\n", writer)
            break

        elif(split_command[0] == "list"):
            await send_message("ACK\n", writer)
            await ftp_list(reader, writer)
            
        elif(split_command[0] == "remove"):
            await send_message("ACK\n", writer)
            await ftp_remove(reader, writer, split_command[1])

        elif(split_command[0] == "get"):
            await send_message("ACK\n", writer)
            await ftp_get_file(reader, writer, split_command[1])

        elif(split_command[0] == "put"):
            await send_message("ACK\n", writer)
            await ftp_put_file(reader,writer, split_command[1])


        else:
            await send_message("NAK Unknown command!\n", writer)

        split_command.clear()
   
    return


async def handle_client(reader, writer):

    # TODO: send the introduction message by implementing `send_message` above.
    intro_message = "Please enter the correct password within 3 tries to access the server.\n"
    deny_message = "Incorrect password. Try Again! \n"
    pass_message = "Correct! Welcome to my (diazric) server! I'm majoring in CS\n"

    await send_message(intro_message, writer)

    key = "cs372"
    tries = 0

    while(tries != 3):
        message = await receive_long_message(reader)

        if(message == key):
            await send_message(pass_message, writer)
            await ftp_server_cmds(reader, writer)
            break
        else:
            await send_message(deny_message , writer)
        
        tries +=1

    writer.close()
    await writer.wait_closed()
    print("Server: Closed Connection")


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
