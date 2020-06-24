import config
import discord
from discord.ext import commands
from discord.utils import get
from collections import defaultdict


client = discord.Client()
client = commands.Bot('!')

client.remove_command("help")
helpercommands =['!help', '!creator','!trades','!portfolio']
cm = ['!buy','!sell','!bought','!sold']
cmb = ['!BUY','!bought']
cmS = ['!sell','!sold']
emoji = '\N{THUMBS UP SIGN}'
soldStockListCount=dict()
boughtStockListCount=dict()
soldStockUserList=dict()
UserStockPortfolio=dict()

#lookup = defaultdict(lambda: [0,0,0])

def check_availability(element, collection: iter):
    return element in collection

@client.event
async def on_message(masg):
    #check to see if the message starts with ! and that its not written by the bot or the current user.
    if masg.content.startswith('!'):
        if masg.author == client.user: return
        if masg.author.bot: return
        if masg.author.bot == client.user: return
        masg.content = masg.content.lower()
        bt = masg.content.split(" ")
        if check_availability(bt[0], cm) is True and len(bt) > 2:
            await masg.add_reaction(emoji)
            await client.process_commands(masg)
        elif check_availability(bt[0], helpercommands) is True:
            await masg.add_reaction(emoji)
            await client.process_commands(masg)

@client.command(name="help", description="help2")
async def help(msg):
    trades_channel = client.get_channel(config.trades_channel_id)
    await trades_channel.send(f'Commands Are: ')
    await  trades_channel.send(f'!bought [ticker] [price] - Used to send bought messages to #trades Example: !bought MMEX .02: ')
    await  trades_channel.send(f'!buy [ticker] [price] - Used to send bought messages to #trades Example: !buy MMEX .02: ')
    await  trades_channel.send(f'!sold [ticker] [price] - Used to send sell messages to #trades Example: !sold MMEX .02: ')
    await  trades_channel.send(f'!sell [ticker] [price] - Used to send sell messages to #trades Example: !sell MMEX .02: ')
    await  trades_channel.send(f'!trades - See a list of Buy and Sell Stock Counts!')
    await  trades_channel.send(f'!portfolio - See your current stock holdings with purchase price!')
    await  trades_channel.send(f'!help - Get a list of commands')
    await  trades_channel.send(f'!creator - WHOIS the creator')

@client.command()
async def trades(msg):
    if msg.message.content.startswith('!trades'):
        trades_channel = client.get_channel(config.trades_channel_id)
        s = sorted(soldStockListCount.items(), key=lambda x:x[1], reverse=True)
        b = sorted(boughtStockListCount.items(), key=lambda x:x[1], reverse=True)
        for k,v in s:
            await  trades_channel.send(f'Sold: {k}, {v}')
        
        for k,v in b:
            await  trades_channel.send(f'Bought: {k}, {v}')

@client.command()
async def portfolio(msg):
    if msg.message.content.startswith('!portfolio'):
        trades_channel = client.get_channel(config.trades_channel_id)
        if msg.author.id in UserStockPortfolio:
            if len(UserStockPortfolio[msg.author.id])>0:
                await  trades_channel.send(f'{msg.author} Portfolio:')
                for k in UserStockPortfolio[msg.author.id]:
                    v = UserStockPortfolio[msg.author.id].get(k, None)
                    await  trades_channel.send(f'{k}:${v}')
            else:
                UserStockPortfolio.pop(msg.author.id, None)
                await  trades_channel.send(f'Your portfolio is currently empty')
        else:
            await  trades_channel.send(f'No Portfolio')

@client.command()
async def creator(msg):
    if msg.message.content.startswith('!creator'):
        trades_channel = client.get_channel(config.trades_channel_id)
        await  trades_channel.send(f'This BOT was written by epuches@gmail.com.  For licensing or request please contact me.  Thanks!')
    

@client.command(name="buy", description="buy2")
async def buy(msg):
   if msg.message.content.startswith('!buy'):
    await pickupthatshit(msg)

@client.command()
async def bought(msg):
   if msg.message.content.startswith('!bought'):
    await pickupthatshit(msg)

async def pickupthatshit(msg):
    trades_channel = client.get_channel(config.trades_channel_id)
    msgParts = msg.message.content.split(" ")
    stringcount = len(msgParts)
    if stringcount>=3:
        try:
            if msgParts[1].isalpha() and isinstance(str(msgParts[1]).upper(), str) :
                try:
                    if isinstance(float(msgParts[2]), float):
                        await boughtStockListFunction(msg)
                        print(f'BUY:{str(msgParts[1]).upper()}:${float(msgParts[2])}')
                        await trades_channel.send(f'{msg.author.mention} just scooped up {str(msgParts[1]).upper()} '
                                f'at ${float(msgParts[2]):.2f}')
                except ValueError:
                    await trades_channel.send(f'format must be !buy TICKER PRICE example !buy AAPL 1.50 - EC671')
        except ValueError:
                await trades_channel.send(f'format must be !buy TICKER PRICE example !buy AAPL 1.50 - EC670')
    else:
        await trades_channel.send(f'format must be !buy TICKER PRICE example !buy AAPL 1.50  - 672')

async def helpmeobione(msg):
    trades_channel = client.get_channel(config.trades_channel_id)
    await trades_channel.send(f'Commands are {cm}.')

@client.command()
async def sell(msg):
    if msg.message.content.startswith('!sell'):
        await dropthatshit(msg)

@client.command()
async def sold(msg):
    if msg.message.content.startswith('!sold'):
        await dropthatshit(msg)

async def dropthatshit(msg):
        trades_channel = client.get_channel(config.trades_channel_id)
        msgParts = msg.message.content.split(" ")
        stringcount = len(msgParts)
        if stringcount>=3:
            try:
                if isinstance(str(msgParts[1]).upper(), str): 
                    try:
                        if isinstance(float(msgParts[2]), float):
                            foundMsg = False
                            async for authorMessages in trades_channel.history(limit=500):
                                if authorMessages.author.id != config.bot_id:
                                    continue
                                if len(authorMessages.mentions) == 0:
                                    continue
                                if authorMessages.content.startswith('~~~'):
                                    continue
                                if authorMessages is None:
                                    await sellmsgtext(msg)
                                    await soldStockListFunction(msg)
                                    return
                                else:
                                    if authorMessages.mentions[0].id == msg.author.id:
                                        if authorMessages.content.split(" ")[4] == msgParts[1].upper():                                       
                                            boughttickerprice = float(authorMessages.content.split(" ")[6].replace('$',''))
                                            soldTickerPrice = float(msgParts[2])
                                            pricechange = ((soldTickerPrice-boughttickerprice)/boughttickerprice)*100
                                            if float(pricechange)>0:
                                                print(f'SOLD:GAIN:{str(msgParts[1]).upper()}:${float(msgParts[2])}')
                                                await trades_channel.send(f'{msg.author.mention} just dumped {str(msgParts[1]).upper()}'
                                                                f' at ${float(msgParts[2]):.2f} for a gain of {pricechange:.2f}%')
                                            else:
                                                print(f'SOLD:LOSS:{str(msgParts[1]).upper()}:${float(msgParts[2]):.2f}')
                                                await trades_channel.send(f'{msg.author.mention} just dumped {str(msgParts[1]).upper()}'
                                                                f' at ${float(msgParts[2]):.2f} for a loss of {pricechange:.2f}%')
                                            c = '~~~' + authorMessages.content
                                            await soldStockListFunction(msg)
                                            await authorMessages.edit(content=c)
                                            foundMsg = True
                                            return
                        if foundMsg == False:
                            await sellmsgtext(msg)
                            await soldStockListFunction(msg)
                            return
                    except ValueError:
                        await trades_channel.send(f'format must be !sell TICKER PRICE example !sell AAPL 1.50 - EC681')
            except ValueError:
                await trades_channel.send(f'format must be !sell TICKER PRICE example !sell AAPL 1.50 - EC680')
        else:
            await trades_channel.send(f'format must be !sell TICKER PRICE example !sell AAPL 1.50  - 682')

async def sellmsgtext(msg):
    trades_channel = client.get_channel(config.trades_channel_id)
    msgParts = msg.message.content.split(" ")
    print(f'SOLD:NOBUY:{str(msgParts[1]).upper()}:${float(msgParts[2])}')
    await trades_channel.send(f'{msg.author.mention} just dumped {str(msgParts[1]).upper()}'
                                                        f' at ${float(msgParts[2])}')

async def soldStockListFunction(msg):
    msgParts = msg.message.content.split(" ")
    ticker = msgParts[1].upper()
    author = msg.author
    authorid = author.id
    #await trades_channel.send(f'author: {author}, authorid: {authorid}, ticker:{ticker}, price:{price}')
    if ticker in soldStockListCount:
        soldStockListCount[ticker]=soldStockListCount[ticker]+1
    else:  
        soldStockListCount[ticker]=1
    if authorid in UserStockPortfolio:
        dictt = UserStockPortfolio[authorid]
        car = dictt.get(ticker, None)
        if car is not None:
            dictt.pop(ticker, None)

async def boughtStockListFunction(msg):
    msgParts = msg.message.content.split(" ")
    ticker = msgParts[1].upper()
    price = msgParts[2]
    author = msg.author
    authorid = author.id
    #await trades_channel.send(f'author: {author}, authorid: {authorid}, ticker:{ticker}, price:{price}')
    if ticker in boughtStockListCount:
        boughtStockListCount[ticker]=boughtStockListCount[ticker]+1
    else:  
        boughtStockListCount[ticker]=1
    if authorid in UserStockPortfolio:
        car = UserStockPortfolio[authorid].get(ticker, None)
        if car is None:
            UserStockPortfolio[authorid].update({ticker:price})
    else:
        UserStockPortfolio[authorid] = {ticker:price}

@client.event
async def on_ready():
    """
    Prints a message if the bot is ready to work
    :return:
    """
    print('Never fear the DollarBot is here')

client.run(config.access_token)    # Bot token

