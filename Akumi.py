import discord
import asyncio
import mysql.connector

mydb = mysql.connector.connect(
  host="***********",
  user="**********",
  passwd="*******",
  database="*****"
)

print(mydb)


client = discord.Client()

mycursor = mydb.cursor(buffered=True)




@client.event
async def on_ready():
    print("Akumi is ready!")
    await client.change_presence(activity=discord.Activity(name="Playing a game"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return


    if message.content.lower() == "a>":
        await message.channel.send("Use **a>help** command to recieve a message of all the commands!")


    if message.content.lower() == "a>help":
        msg = "**___List of commands___**:\n\n ---------- \n\n **a>Play** or **a>P**: Rolls a new character\n\n **a>Mylist** or **a>ML**: Lists all the Devil Fruits you have. Use option(s) p, l, z, mz, az, s for Paramecia, Logia, Zoan, Mythical Zoan, Ancient Zoan, and SMILE types respectively\n\n **a>MyPoints** or **a>MP**: Shows you how many points you have earned so far\n\n **a>ServRank** or **a>sr**: Lists the server leaderboard for the current game. Use options p, df to sort based on points or number of devil fruits respectively\n"
        await message.author.send(msg)

    if message.content.startswith('a>greet'):
            channel = message.channel
            await channel.send('Say hello!')

            def check(m):
                return m.content == 'hello' and m.channel == channel

            try:

                msg = await client.wait_for('message', timeout=10, check=check)
            except asyncio.TimeoutError:
                await message.channel.send('Time up')
            else:
                await channel.send('Hello {.author}!'.format(msg))

    if message.content.startswith('a>r'):
        channel = message.channel
        await channel.send('Send me that ^ reaction, mate')

        def check(m):
            return m.author == message.author and m.content == '^'

        try:
            m = await client.wait_for('message', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await channel.send('v')
        else:
            await channel.send('^')


    if message.content.startswith('a>p'):
        mycursor.execute("SELECT * FROM devil_fruits WHERE imgurl IS NOT NULL")
        myresult = mycursor.fetchone()
        url = myresult[7]
        msg = "You have **15 seconds** to reply with **p**, **l**, **z**, **mz**, **az** for **paramecia**, **logia**, **zoan**, **mythical zoan**, **ancient zoan** respectively. Reply with **c** to **cancel**"
        await message.channel.send(url)
        await message.channel.send(msg)

        def check(m):
            return (m.content.lower() == 'p' or m.content.lower() == 'l' or m.content.lower() == 'z' or m.content.lower() == 'az' or m.content.lower() == 'mz') and m.author == message.author

        try:
            m = await client.wait_for('message', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await message.channel.send('Time up')

        else:
            if m.content.lower() == str(myresult[5]).lower():
                await message.channel.send('**Correct!** You now have **30 seconds** to name the devil fruit')
            else:
                await message.channel.send('**Wrong!**')
                return


        def check(m):
            return m.content.lower() != None and m.author == message.author

        try:
            m = await client.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await message.channel.send('Time up!')
        else:
            if m.content.lower() == str(myresult[3]).lower() or m.content.lower() == str(myresult[4]).lower():
                await message.channel.send('**Correct!** You now have the **Soru Soru no Mi**')
            else:
                await message.channel.send('**Wrong!**')
                return



        #type = None
        #if message.content.lower == "p":
        #    type = "paramecia"
        #elif message.content.lower == "l":
        #    type = "logia"
        #elif message.content.lower == "z":
        #    type = "zoan"
        #elif message.content.lower == "mz":
        #    type = "mythical zoan"
        #elif message.content.lower == "az":
        #    type = "ancient zoan"
        #elif message.content.lower == "c":
        #    type = "cancel"
        #if type == str(myresult[5]):
        #    msg = user.mention + " you have 30 seconds to name the devil fruit"
        #    await message.channel.send(msg)
        #    await client.wait_for(timeout=30, author=message.author)
        #    input = message.content.lower
        #    if input == myresult[3].lower or myresult[4].lower:
        #        msg = "Correct! You now have the " + myresult[3]
        #        await message.channel.send(msg)
        #    elif input == None:
        #        msg = "Time's up!"
        #        await message.channel.send(msg)
        #    else:
        #        msg = "Wrong!"
        #        await message.channel.send(msg)


client.run('NTU5OTgxNzU1MjU2NDA2MDI2.D3tr8g.TO4dhUGH-QB4c6YoZO55jTCgYcA')
