from discord.ext import commands
from pathlib import Path
import sqlite3

bot = commands.Bot(command_prefix='>')

existed = Path("./example.db").exists()
CON = sqlite3.connect("example.db")
CUR = CON.cursor()

if not existed:
    CUR.execute(
        '''CREATE TABLE prs
        (name text, type text, reps int, weight int)'''
    )
    
    CUR.execute("INSERT INTO prs VALUES ('JimBOT', 'squat', 100, 1000)")

    CON.commit()

def make_mention(_id) -> str:
    return f"<@{_id}>"

def pretty_pr(pr_list) -> str:
    message = ""

    for pr in pr_list:
        name, type, reps, weight = pr
        name = make_mention(name)
        message +=f"{name}'s {reps} rep(s) of {type} is {weight}\n"

    return message



with open("./token.txt") as file:
    TOKEN = file.read().rstrip()

#
@bot.command()
async def ping(ctx):
    await ctx.send("pong")


#get all prs
@bot.command()
async def getall(ctx):
    """Gets all prs"""
    prs = CUR.execute("SELECT * FROM prs")
    await ctx.send(list(prs))


#get a specific pr
@bot.command()
async def get(ctx):
    name = ctx.author.id
    """Get a single pr '>get [name]'"""
    prs = list(CUR.execute("SELECT * FROM prs WHERE name = ?", (name, )))
    if len(prs) == 0:
        await ctx.send(ctx.author.mention + " Name not found!")
    else:
        await ctx.send(pretty_pr(prs))


#add a pr
@bot.command()
async def add(ctx, type, reps, weight):
    """Add pr to bot database '>add [type] [reps] [weight]'"""
    name = ctx.author.id
    CUR.execute("INSERT INTO prs VALUES (?,?,?,?)", (name, type, reps, weight))
    CON.commit()
    await ctx.send("Added!")

bot.run(TOKEN)