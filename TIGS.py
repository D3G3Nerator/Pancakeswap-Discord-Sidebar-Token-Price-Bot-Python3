import discord, json
from discord.ext.commands import Bot
from web3 import Web3
import asyncio




###################################################################
#######                       SETTINGS                      #######
###################################################################
DISCORD_TOKEN = '<YOUR DISCORD TOKEN>'


BEP20_QUOTETOKEN_ADDRESS = '0xe9e7cea3dedca5984780bafc599bd69add087d56' #<= BUSD 
BEP20_QUOTETOKEN_DECIMALS = 18 #BUSD => 18


BEP20_TOKEN_SYMBOL = "TIGS"
BEP20_TOKEN = '0x34FaA80FEC0233e045eD4737cc152a71e490e2E3' #<= TIGS
BEP20_TOKEN_DECIMALS = 18


TRADINGTIGERSROUTER = '0xdEdf20172b6dC39817026c125f52d4fad8E0f29b' #This contract do all the work for you, find the best Pool and convert too your QuoteToken. <= (PancakeSwap)

FINAL_PRICE_ROUND_TO_DECIMALS = 3
###################################################################

bot = Bot(command_prefix="$") # Not used, but prefix is need.
ABI = [{
        "inputs": [
            {
                "internalType": "address",
                "name": "TokenA",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "TokenB",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "getOutputfromTokentoToken",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "address[]",
                "name": "",
                "type": "address[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }]


def get_TokenPrice():
    w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))
    swapper = w3.eth.contract(address=Web3.toChecksumAddress(TRADINGTIGERSROUTER), abi=ABI)
    OneQuoteToken = 1 * (10**BEP20_TOKEN_DECIMALS)
    
    TOKEN_Price = swapper.functions.getOutputfromTokentoToken(
        Web3.toChecksumAddress(BEP20_TOKEN), #<= Input Token from whom we want to know the price!
        Web3.toChecksumAddress(BEP20_QUOTETOKEN_ADDRESS), #<= Output Token we use BUSD, so we know USD price!
        OneQuoteToken
        ).call()[0]
        
    TokenTokenPrice = round(TOKEN_Price / (10**BEP20_QUOTETOKEN_DECIMALS), FINAL_PRICE_ROUND_TO_DECIMALS)
    return TokenTokenPrice
    

async def status_update():
    while True:
        price = str(BEP20_TOKEN_SYMBOL) + " | " + str(get_TokenPrice()) + " $"
        print(price)
        await bot.user.edit(username=price)
        await asyncio.sleep(1800)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    bot.loop.create_task(status_update())
		
bot.run(DISCORD_TOKEN)