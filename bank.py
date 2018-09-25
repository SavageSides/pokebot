import discord
import json
import datetime
import random
from discord.ext import commands

TOKEN = "NDkzNTU5NzY3NDkxNjc0MTEy.DosQqQ.46XwsvGSoQH5HGy6vfMJSycBgqY"

client = commands.Bot(command_prefix="p?")
client.remove_command('help')

@client.event
async def on_ready():
    print("Ready to make some money!")
    await client.change_presence(game=discord.Game(name="Pokémon!", type=3))
    




@client.event
async def on_command_error(error, ctx):
    channel = ctx.message.channel
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(color=0xfff700, timestamp=datetime.datetime.utcnow())
        embed.add_field(name='Wrong Bank Command!', value='Please type ``p?help `` for Eco commands!', inline=True)
        await client.send_message(channel, embed=embed)
    if isinstance(error, commands.NoPrivateMessage):
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name='Unknown Error', value='```We beilive that you do not let random people text you!\nPlease enable your PM messages so you can see this amazing\nMessage!```', inline=True)
        await client.say(embed=embed)

@client.event
async def on_member_join(member):
    server = member.server
    channel = discord.utils.get(server.channels, name="general")
    await client.send_message(channel, f"Welcome {member.mention} to **{server}**. Have a great time!")

@client.event
async def on_member_remove(member):
    server = member.server
    channel = discord.utils.get(server.channels, name="general")
    await client.send_message(channel, f"Goodbye {member.mention} the **{server}** will miss you :(")

@client.command(pass_context=True)
@commands.cooldown(1, 864000, commands.BucketType.user)
async def work(ctx):
    with open("coins.json", "r") as f:
       	coins = json.load(f)
    author = ctx.message.author
    coinsc = random.randint(100, 700)
    if not ctx.message.server.id in coins:
       	coins[ctx.message.server.id] = {}
    if not author.id in coins[ctx.message.server.id]:
        coins[ctx.message.server.id][author.id] = 0
    coins[ctx.message.server.id][author.id] += coinsc
    embed = discord.Embed(color=0xfff700, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Work!", value=f"You have worked all day! You deserve  ``{coinsc}`` :dollar: as a prize!", inline=False)
    embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/493518731717115926/493559477468004383/image0.jpg", text="Type p?help for more commands!")
    await client.say(embed=embed)
    with open("coins.json", "w") as f:
        json.dump(coins, f, indent=4)
@work.error
async def cooldown_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await client.say("**You can only use the command each day**")

@client.command(pass_context=True)
async def bal(ctx):
    with open("coins.json", "r") as f:
        coins = json.load(f)
    author = ctx.message.author
    if not author.id in coins[ctx.message.server.id]:
        coins[ctx.message.server.id][author.id] = 0
    coinss = coins[ctx.message.server.id][author.id]
    embed = discord.Embed(color=0xfff700, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Your Balance!", value=f"You have ``{coinss}``:dollar:  in your bank account!", inline=False)
    embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/493518731717115926/493559477468004383/image0.jpg", text="Type p?help for more commands!")
    await client.say(embed=embed)

@client.command(pass_context=True)
@commands.cooldown(5, 10, commands.BucketType.user)
async def gamble(ctx, amount: int):
    with open("coins.json", "r") as f:
        coins = json.load(f)
    choices = random.randint(0, 1)
    amountt = coins[ctx.message.server.id][ctx.message.author.id]
    if coins[ctx.message.server.id][ctx.message.author.id] <= 1:
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name="Wrong!", value=f"You dont have enough! Required: ``2``. Your balance: ``{amountt}``.", inline=False)
        await client.say(embed=embed)
        return
    if amount > coins[ctx.message.server.id][ctx.message.author.id]:
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name="Not Enough!", value="You don't have sufficiant coins.", inline=False)
        await client.say(embed=embed)
        return
    if amount <= 0:
        embed = discord.Embed(color=0xff00f0)
        embed.add_field(name="Not Enough", value="You cannot gamble anything less then ``0``!", inline=False)
        await client.say(embed=embed)
        return
    if choices == 0:
        coins[ctx.message.server.id][ctx.message.author.id] += amount * 2
        won = amount * 2
        embed = discord.Embed(color=0xfff700, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="You won!", value=f"You won! You won ``{won}``:dollar: .", inline=False)
        await client.say(embed=embed)
    else:
        coins[ctx.message.server.id][ctx.message.author.id] -= amount
        embed = discord.Embed(color=0xfff700, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="You lost", value=f"You lost! Taken ``{amount}``:dollar:  from your balance.", inline=False)
        await client.say(embed=embed)
    with open("coins.json", "w") as f:
        json.dump(coins, f, indent=4)
@gamble.error
async def cooldown_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await client.say("You can only use the command each 10 seconds")

@client.command(pass_context=True)
@commands.cooldown(1, 864000, commands.BucketType.user)
async def daily(ctx):
    with open("coins.json", "r") as f:
       	coins = json.load(f)
    author = ctx.message.author
    coinsc = random.randint(100, 700)
    if not ctx.message.server.id in coins:
       	coins[ctx.message.server.id] = {}
    if not author.id in coins[ctx.message.server.id]:
        coins[ctx.message.server.id][author.id] = 0
    coins[ctx.message.server.id][author.id] += coinsc
    embed = discord.Embed(color=0xfff700, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Daily!", value=f"+ :moneybag: ``{coinsc}``", inline=False)
    embed.set_footer(text="Enjoy your money!")
    await client.say(embed=embed)
    with open("coins.json", "w") as f:
        json.dump(coins, f, indent=4)
@daily.error
async def cooldown_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await client.say("**Akward. Use this command in the next 24 hours!**")


@client.command( pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(color=0xfff700, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="***__Prefix:__***", value="``p?``", inline=True)
    embed.add_field(name="***__Economy:__***", value="**p?work** This will give you some extra earnings \n **p?daily** Will give you your daily pay \n **p?gamble <amount>** This will either give you to time the number you said or take it away \n **p?bal** Will show you your balance \n **p?profile @user** Will show the users coins atm \n **p?pay @user <amount>** Will pay that user the coins if you can aford them \n **p?wallets** Will search for wallets to steal", inline=True)
    embed.add_field(name="***__Utility:__***", value="**p?poll <channel_name> <message>** Will send the a poll to the channel with reactions", inline=True)
    embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/493518731717115926/493559477468004383/image0.jpg", text="Type p?help <command>")
    await client.send_message(author, embed=embed)
    await client.say(f"{author}, Please check your Private Messages. That Private Message contains the help message!")

@client.command(pass_context=True)
async def profile(ctx, user: discord.Member):
    with open("coins.json", "r") as f:
        coins = json.load(f)
    if not user.id in coins[ctx.message.server.id]:
        coins[ctx.message.server.id][user.id] = 0
    coinss = coins[ctx.message.server.id][user.id]
    embed = discord.Embed(color=0xfff700, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="***__Name:__***", value=f"{user.name}", inline=False)
    embed.add_field(name="***__Money:__***", value=f"{coinss}", inline=True)
    embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/493518731717115926/493559477468004383/image0.jpg", text="Profile's!")
    await client.say(embed=embed)


@client.command(pass_context=True)
async def pay(ctx, member:discord.Member=None, *, amount: int):
    with open("coins.json", "r") as f:
        coins = json.load(f)
        author = ctx.message.author
    if amount > coins[ctx.message.server.id][ctx.message.author.id]:
        embed = discord.Embed(color=0xfff700, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Error:", value="**You don't have enough coins!**", inline=False)
        embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/493518731717115926/493559477468004383/image0.jpg", text="No Coins Boi!")
        await client.say(embed=embed)
        return
    if author == member:
        embed = discord.Embed(color=0xfff700, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Error:", value="**You can't give money your self! Silly!**", inline=False)
        embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/493518731717115926/493559477468004383/image0.jpg", text="Lol!")
        await client.say(embed=embed)
        return
    if not ctx.message.server.id in coins:
        coins[ctx.message.server.id] = {}
    if not member.id in coins[ctx.message.server.id]:
        coins[ctx.message.server.id][member.id] = 0
        coins[ctx.message.server.id][member.id] += amount
        embed = discord.Embed(color=0xfff700, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Error:", value=f"Added **{amount} to **{member.name}** ", inline=False)
        embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/493518731717115926/493559477468004383/image0.jpg", text="Added!")
        await client.say(embed=embed)
    else:
        coins[ctx.message.server.id][member.id] += amount
        coins[ctx.message.server.id][ctx.message.author.id] -= amount
        embed = discord.Embed(color=0xfff700, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Added:", value=f"Added **{amount}** to **{member.name}** ", inline=False)
        embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/493518731717115926/493559477468004383/image0.jpg", text="Added!")
        await client.say(embed=embed)
    with open("coins.json", "w") as f:
        json.dump(coins, f, indent=4)

@client.command(pass_context=True)
async def wallets(ctx):
    with open("coins.json", "r") as f:
        coins = json.load(f)
    choices = random.randint(0, 1)
    coinss = random.randint(100, 700)
    if choices == 0:
        coins[ctx.message.server.id][ctx.message.author.id] += coinss
        won = coinss
        embed = discord.Embed(color=0xfff700, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="You won!", value=f"You stole {won} and went risk free!", inline=False)
        await client.say(embed=embed)
    else:
        embed = discord.Embed(color=0xfff700, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="You lost", value=f"Theres no wallets found!", inline=False)
        await client.say(embed=embed)
    with open("coins.json", "w") as f:
        json.dump(coins, f, indent=4)

@client.command(pass_context=True)
async def poll(ctx, channel_name, *, text):
    if ctx.message.author.server_permissions.administrator:
        channel = discord.utils.get(ctx.message.server.channels, name=channel_name)
        author = ctx.message.author
        embed = discord.Embed(color=0xfff700, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Poll!")
        embed.add_field(name="Created by: {0}".format(author.mention), value=f"{text}", inline=False)
        embed.add_field(name="Reactions:", value="Click :white_check_mark: for yes \n Click :x: for no", inline=True)
        embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/493518731717115926/493559477468004383/image0.jpg", text="Poll!")
        msg = await client.send_message(channel, embed=embed)
        await client.add_reaction(msg, "\U00002705")
        await client.add_reaction(msg, "\U0000274c")
        await client.say(f"I have sent a poll to **{channel_name}**")
    else:
        embed = discord.Embed(color=0xfff700, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="***__Perms:__***", value="You are missing perms: ``Administrator``", inline=False)
        await client.say(embed=embed)
        
@client.command(pass_context=True)
async def setup(ctx):
    server = ctx.message.server
    if ctx.message.author.server_permissions.administrator:
       await client.create_role(server=server, name='Legendary')
       await client.say("I have finished the setup. Roles added: ``Legendary``")
        
@client.group(pass_context=True)
async def buy(ctx):
    with open("coins.json", "r") as f:
        coins = json.load(f)
    with open("coins.json", "w") as f:
        json.dump(coins, f, indent=4)

@buy.command(name="legendary", pass_context=True)
async def _legendary(ctx):
    with open("coins.json", "r") as f:
        coins = json.load(f)
    author = ctx.message.author
    if coins[ctx.message.server.id][ctx.message.author.id] <= 10000:
        await client.say("Sorry, you dont have enough money!")
        return
    coins[ctx.message.server.id][ctx.message.author.id] -= 10000
    LegendaryRole = discord.utils.get(ctx.message.server.roles, name="Legendary")
    await client.add_roles(author, LegendaryRole)
    embed = discord.Embed(color=0xfff700, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Purchaced Item:", value="You have purchaced the legendary role.", inline=False)
    embed.add_field(name="Information:", value="I have taken ``10000`` Dollars out of your balance.", inline=True)
    await client.say(embed=embed)
    with open("coins.json", "w") as f:
        json.dump(coins, f, indent=4)

        
    



client.run(TOKEN)
