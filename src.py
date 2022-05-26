# coding:UTF-8
from discord.ext import commands, tasks
import discord
import random
import json

#main config
file = "./config.json"
config = json.loads(open(file).read())

bossgame = json.loads(open(config['boss']['file']).read())

bot = commands.Bot(command_prefix=config['main']['prefix'])
bot.remove_command('help')

prefix = config['main']['prefix']
footer = config["embed"]["embed_footer"]

#Events
@bot.event
async def on_ready():
    change_staus.start()
    servers = 0
    print('♦═════════════════════SERVERS LIST═════════════════════♦')
    for guild in bot.guilds:
        print("> " + str(guild) + "  |  ID: " + str(guild.id))
        servers += 1
    print(f"\nServers: {servers}")
    print('♦════════════════════════INFO══════════════════════════♦')
    print('               • The bot is Online! •')
    print('               • Made by UNIVERSUM •')
    print('♦══════════════════════════════════════════════════════♦')

@tasks.loop(seconds=10)
async def change_staus():
    status = ['Made by mitko8009#7498', f'Use {str(config["main"]["prefix"])}help', 'Discord Server: https://discord.gg/DtY4herZJn']
    await bot.change_presence(activity=discord.Game(random.choice(status)))


@bot.command()
async def attack(ctx):
    if str(ctx.author) == str(bossgame['boss']):
        embed = discord.Embed(title="You cannot attack yourself", color=discord.Color.dark_purple())
        await ctx.send(embed=embed)
    else:
        health = float(bossgame['health'])
        
        if health > 80:
            attack_dm = (random.randrange(20, 81))*(float(bossgame['attackboost']))
            health -= attack_dm
            embed = discord.Embed(title=f"{ctx.author} attack the boss", description=f"*-{str(attack_dm)} boss hp*", color=discord.Color.dark_purple())
            await ctx.send(embed=embed)
            bossgame['health'] = str(health)

        elif 40 < health <= 80:
            attack_dm = (random.randrange(20, 41))*(float(bossgame['attackboost']))
            health -= attack_dm
            embed = discord.Embed(title=f"{ctx.author} attack the boss", description=f"*-{str(attack_dm)} boss hp*", color=discord.Color.dark_purple())
            await ctx.send(embed=embed)
            bossgame['health'] = str(health)

        elif 20 < health <= 40:
            attack_dm = (random.randrange(10, 21))*(float(bossgame['attackboost']))
            health -= attack_dm
            embed = discord.Embed(title=f"{ctx.author} attack the boss", description=f"*-{str(attack_dm)} boss hp*", color=discord.Color.dark_purple())
            await ctx.send(embed=embed)
            bossgame['health'] = str(health)

        elif health <= 20:
            embed = discord.Embed(title=f"{ctx.author} killed the boss\n{ctx.author} is a new boss", description=f"*-{str(health)} boss hp*", color=discord.Color.dark_purple())
            embed.set_footer(text=footer)
            await ctx.send(embed=embed)
            print(f"{ctx.author} is a new boss")
            attack_dm = health
            health = 0
            bossgame['health_limit'] = str(int(bossgame['health_limit'])*int(bossgame['health_level']))
            bossgame['health'] = bossgame['health_limit']
            bossgame['boss'] =  str(ctx.author)

    with open(config['boss']['file'], "w") as jsonfile:
        json.dump(bossgame, jsonfile, indent='\t')
    await ctx.message.delete()

@bot.command()
async def heal(ctx):
    if str(ctx.author) == str(bossgame['boss']):
        if float(bossgame['health']) <= float(bossgame['health_limit'])-20:
            heal = random.randrange(1, 21)*(int(bossgame['healboost']))
            embed = discord.Embed(title=f"{ctx.author} heal yourself", description=f"*+{str(heal)} boss hp*", color=discord.Color.dark_purple())
            print(f"{ctx.author} heal yourself | +{str(heal)} boss hp")
            await ctx.send(embed=embed)
            config.set('boss', 'health', str(float(bossgame['health'])+heal))
        elif float(bossgame['health_limit'])-21 < float(bossgame['health'])-1:
            heal = float(bossgame['health_limit'])
            embed = discord.Embed(title=f"{ctx.author} heal yourself", description=f"*The boss on {str(heal)} hp*", color=discord.Color.dark_purple())
            print(f"{ctx.author} heal yourself | The boss on {str(heal)} hp")
            await ctx.send(embed=embed)
            config.set('boss', 'health', str(float(bossgame['health_limit'])))
    else:
        embed = discord.Embed(title=f"{ctx.author} cannot heal the boss", color=discord.Color.dark_purple())
        await ctx.send(embed=embed)

    with open(file, "w") as jsonfile:
        json.dump(config, jsonfile, indent='\t')
    await ctx.message.delete()

@bot.command(aliases = ['hp'])
async def health(ctx):
    embed = discord.Embed(title=f"The boss health is {bossgame['health']}\nThe boss is {bossgame['boss']}", color=discord.Color.dark_purple())
    embed.set_footer(text=footer)
    await ctx.send(embed=embed)
    await ctx.message.delete()

@bot.command(aliases = ["bossinfo"])
async def boss_info(ctx):
    embed = discord.Embed(title="Boss info"
    ,description =f"User: {bossgame['boss']}\nHealth: {str(bossgame['health'])}\n"
    ,color=discord.Color.dark_purple())
    embed.add_field(name="Boosts", value=f"Attack Boost: {str(bossgame['attackboost'])}\nHeal Boost: {str(bossgame['healboost'])}")
    await ctx.send(embed=embed)

@bot.command(aliases = ['trb'])
async def transfer_boss(ctx, *, arg):
    if str(ctx.author) == str(bossgame['boss']):
        config.set('boss', 'boss', str(arg))
        embed = discord.Embed(title=f"The boss is now {str(arg)}", color=discord.Color.dark_purple())
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"{ctx.author} cannot transfer the boss", color=discord.Color.dark_purple())
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    with open(file, "w") as jsonfile:
        json.dump(config, jsonfile, indent='\t')
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def set_hp(ctx, *, arg):
    embed = discord.Embed(title=f"The boss hp set to {str(arg)}", color=discord.Color.dark_purple())
    embed.set_footer(text=footer)
    await ctx.send(embed=embed)
    config.set('boss', 'health', str(arg))
    
    with open(file, "w") as jsonfile:
        json.dump(config, jsonfile, indent='\t')
    await ctx.message.delete()
        
@bot.command()
@commands.has_permissions(administrator=True)
async def set_limit(ctx, *, arg):
    config.set('boss', 'health_limit', str(arg))
    embed = discord.Embed(title=f"The boss hp limit set to {str(arg)}", color=discord.Color.dark_purple())
    embed.set_footer(text=footer)
    await ctx.send(embed=embed)
    
    with open(file, "w") as jsonfile:
        json.dump(config, jsonfile, indent='\t')
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def set_boss(ctx, *, arg):
    config.set('boss', 'boss', str(arg))
    embed = discord.Embed(title=f"The boss is now {str(arg)}", color=discord.Color.dark_purple())
    embed.set_footer(text=footer)
    await ctx.send(embed=embed)
    
    with open(file, "w") as jsonfile:
        json.dump(config, jsonfile, indent='\t')
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def set_num(ctx, *, arg):
    config.set('boss', 'health_level', str(arg))
    embed = discord.Embed(title=f"The boss num is now {str(arg)}", color=discord.Color.dark_purple())
    embed.set_footer(text=footer)
    embed.set_footer(text=footer)
    await ctx.send(embed=embed)
    
    with open(file, "w") as jsonfile:
        json.dump(config, jsonfile, indent='\t')
    await ctx.message.delete()

@bot.command(aliases = ['set_ab'])
@commands.has_permissions(administrator=True)
async def set_attackboost(ctx, *, arg):
    config.set('boss', 'attackboost', str(arg))
    with open(file, "w") as jsonfile:
        json.dump(config, jsonfile, indent='\t')

    embed = discord.Embed(title=f"Attack boost is now {str(arg)}", color=discord.Color.dark_purple())
    embed.set_footer(text=footer)
    await ctx.send(embed=embed)
    await ctx.message.delete()

@bot.command(aliases = ['set_hb'])
@commands.has_permissions(administrator=True)
async def set_healboost(ctx, *, arg):
    config.set('boss', 'healboost', str(arg))
    with open(file, "w") as jsonfile:
        json.dump(config, jsonfile, indent='\t')

    embed = discord.Embed(title=f"Heal boost is now {str(arg)}", color=discord.Color.dark_purple())
    embed.set_footer(text=footer)
    await ctx.send(embed=embed)
    await ctx.message.delete()

bot.run(config['main']['token'])
