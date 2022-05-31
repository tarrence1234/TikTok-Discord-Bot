import discord
from discord.ext import commands
import datetime
from datetime import datetime
import os
from urllib import request
import pyshorteners
import time
import requests
import random
import time

bot = commands.Bot(command_prefix='.', description="Official Whaxor's Server Bot")


@bot.event
async def on_ready():
    global times
    print(f'[* |{datetime.now().strftime("%H:%M:%S")}] Status > Online | Startup > {round(time.time() - times, 1)}s')
    await bot.change_presence(activity=discord.Game(name="discord.gg/whaxor"))


@bot.command()
async def satus(ctx):
    await ctx.send(f'Online! Latency: {round(bot.latency, 3)} ms')

@bot.command()
async def stats(ctx, *, videolink):
    if ctx.channel.id != 970156017507790878:
        await ctx.send(f'Wrong Channel ! Download in <#970156017507790878>')
        return

    try:
        if "vm.tiktok.com" in videolink or "vt.tiktok.com" in videolink:
            videolink = requests.head(videolink, stream=True, allow_redirects=True, timeout=5).url.split("/")[5].split("?", 1)[0]
        else:
            videolink = videolink.split("/")[5].split("?", 1)[0]
        e = requests.get(f"https://api.tiktokv.com/aweme/v1/multi/aweme/detail/?aweme_ids=%5B{id}%5D").json()["aweme_details"][0]
        r = e['statistics']

        embed = discord.Embed(title=f"TikTok Video Stat's", timestamp=datetime.utcnow(), color=discord.Color.blue())
        embed.add_field(name="id", value=r["aweme_id"])
        embed.add_field(name="Views", value=r["play_count"])
        embed.add_field(name="Hearts", value=r["digg_count"])
        embed.add_field(name="Shares", value=r["share_count"])
        embed.add_field(name="Comments", value=r['comment_count'])

        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/963776218665213952/a23bbceba4a369452a7576454c135637.webp?size=512")

        await ctx.send(embed=embed)
    except:
        await ctx.send("Link Invalid / An error occurred")



@bot.command()
async def user(ctx, *, message):
    if ctx.channel.id != 969893450210246706:
        await ctx.send(f'Wrong Channel ! Get info in <#969893450210246706>')
        return

    name = message
    link = f"https://m.tiktok.com/node/share/user/@{str(name)}"
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }

    try:
        r = requests.get(link, headers=headers).json()

        inf = r["userInfo"]["user"]
        avatar = inf["avatarLarger"]
        id = inf["id"]  #
        nick = inf["nickname"]  #
        user = inf["uniqueId"]
        verif = inf["verified"]  #
        prv = inf['privateAccount']
        stats = r["userInfo"]['stats']
        subs = stats['followerCount']
        subs1 = stats['followingCount']
        like = stats['heart']  #
        vids = stats['videoCount']  #
    except:
        await ctx.send(f"Username not available")
        return

    colour = random.randint(0x000000, 0xFFFFFF)
    web_data = {
        "embeds": [
            {
                "title": f"{nick}'s stats",
                "description": f'*Id* : **{id}**  |  *Username* : **{user}**\n'
                               f'*Followers* : **{subs}**  |  *Following* : **{subs1}**\n'
                               f'*Likes* : **{like}**  |  *Videos* : **{vids}**\n'
                               f'*Private* : **{prv}**  |  *Verified* : **{verif}**\n\n'
                               f'*Click* ***[here](https://www.tiktok.com/@{user})*** *to view on TikTok*',

                "color": colour,
                "image": {
                    "url": "https://cdn.discordapp.com/attachments/879486849108807720/888523658975412295/rainbow2.gif"
                },
                "thumbnail": {
                    "url": avatar
                },
                "footer": {
                },
            }
        ]
    }
    requests.post("WEBHOOK_HERE", json=web_data)


@bot.command()
async def startcheck(ctx):
    if ctx.channel.id != 969886041660076072:
        await ctx.send(f'Access unauthorized')
        return

    while True:
        chrs = 'abcdefghijklmnopqrstuvwxyz0123456789._'
        user = ''.join(random.choices(chrs, k=4))

        if not user[-1].isdigit():

            if not user.isdecimal():

                if not user[-1] == ".":

                    # await ctx.send(('Username:  >>> ',''.join(random.choices(chrs, k=4)),'<<<'))
                    head = {
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
                    }


                    #fast taken check
                    if requests.get(f"https://www.tiktok.com/@{user}", headers=head).status_code == 200:
                        embed = discord.Embed(title=f"Checked Username", timestamp=datetime.utcnow(), color=discord.Color.blue())
                        embed.add_field(name="Username", value=user)
                        embed.add_field(name="Status: ", value="[Taken]")

                        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/963776218665213952/a23bbceba4a369452a7576454c135637.webp?size=512")

                        await ctx.send(embed=embed)

                        time.sleep(round(random.random(), 1))

                        continue


                    #if not banned, status code check
                    r = requests.get(f"https://www.tiktok.com/node/share/user/@{user}", headers=head)

                    if 204 == r.status_code:
                        await ctx.send(f'Ratelimited ! Waiting 3 min')
                        time.sleep(150)



                    if 404 == r.status_code:
                        await ctx.send(f'Api Down ! Waiting 10 min')
                        time.sleep(600)


                    #if status is not 200, quit
                    if r.status_code != 200:
                        await ctx.send(f'An error occured, User {user} may be Available')
                        time.sleep(round(random.random(), 1))


                    if r.status_code == 200:
                        try:
                            if r.json()['statusCode'] == 10221:
                                embed = discord.Embed(title=f"Checked Username", timestamp=datetime.utcnow(), color=discord.Color.blue())
                                embed.add_field(name="Username", value=user)
                                embed.add_field(name="Status: ", value="[Banned]")

                                embed.set_thumbnail(url="https://cdn.discordapp.com/icons/963776218665213952/a23bbceba4a369452a7576454c135637.webp?size=512")

                                await ctx.send(embed=embed)

                                # await ctx.send(f'User :  {user} [Banned]')
                            if "seoProps" in r.json():
                                embed = discord.Embed(title=f"Checked Username", timestamp=datetime.utcnow(), color=discord.Color.blue())
                                embed.add_field(name="Username", value=user)
                                embed.add_field(name="Status: ", value="[Taken]")
                                embed.set_thumbnail(url="https://cdn.discordapp.com/icons/963776218665213952/a23bbceba4a369452a7576454c135637.webp?size=512")
                                await ctx.send(embed=embed)

                            if r.json()['statusCode'] == 10202:
                                embed = discord.Embed(title=f"Checked Username <@&969735246029402112>", timestamp=datetime.utcnow(), color=discord.Color.blue())
                                embed.add_field(name="Username", value=user)
                                embed.add_field(name="Status: ", value="[Available!]")
                                embed.set_thumbnail(url="https://cdn.discordapp.com/icons/963776218665213952/a23bbceba4a369452a7576454c135637.webp?size=512")
                                await ctx.send(embed=embed)

                            if r.json()['statusCode'] == 10223:
                                embed = discord.Embed(title=f"Checked Username", timestamp=datetime.utcnow(), color=discord.Color.blue())
                                embed.add_field(name="Username", value=user)
                                embed.add_field(name="Status: ", value="[Blacklisted!]")
                                embed.set_thumbnail(url="https://cdn.discordapp.com/icons/963776218665213952/a23bbceba4a369452a7576454c135637.webp?size=512")
                                await ctx.send(embed=embed)

                            if r.json()['statusCode'] == 10222:
                                embed = discord.Embed(title=f"Checked Username", timestamp=datetime.utcnow(), color=discord.Color.blue())
                                embed.add_field(name="Username", value=user)
                                embed.add_field(name="Status: ", value="[Taken]")
                                embed.set_thumbnail(url="https://cdn.discordapp.com/icons/963776218665213952/a23bbceba4a369452a7576454c135637.webp?size=512")
                                await ctx.send(embed=embed)

                        except:
                            try:
                                usern = user
                                embed = discord.Embed(title=f"Checked Username", timestamp=datetime.utcnow(), color=discord.Color.blue())
                                embed.add_field(name="Username", value=user)
                                embed.add_field(name="Status: ", value="[Taken]")
                                embed.set_thumbnail(url="https://cdn.discordapp.com/icons/963776218665213952/a23bbceba4a369452a7576454c135637.webp?size=512")
                                await ctx.send(embed=embed)
                            except:
                                pass

        time.sleep(round(random.random(), 1))


@bot.command()
async def tikdown(ctx, *, link):
    if ctx.channel.id != 969925920238489600:
        await ctx.send(f'Wrong Channel ! Download in <#969925920238489600>')
        return

    try:
        if "vm.tiktok.com" in link or "vt.tiktok.com" in link:
            link_id = requests.head(link, stream=True, allow_redirects=True, timeout=5).url.split("/")[5].split("?", 1)[0]
            link1 = link_id
        else:
            link_id = link.split("/")[5].split("?", 1)[0]
            link1 = link_id

        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        }

        link2 = requests.get(f'https://api.tiktokv.com/aweme/v1/multi/aweme/detail/?aweme_ids=%5B{link1}%5D', headers=headers).json()["aweme_details"][0]["video"]["play_addr"]["url_list"][0]

        link3 = pyshorteners.Shortener().tinyurl.short(link2)
        await ctx.send(f'Video: [No Watermark] [ {link3} ]')

    except:
        await ctx.send(f'Link not Supported !')


@bot.command()
async def getbitches(ctx, *, usern):
    await ctx.send(f'<@{usern}> should go get some bitches')

@bot.command()
async def bitches(ctx, *, usern):
    await ctx.send(f'<@{usern}> has {randint(0,1)} bitches')

@bot.command()
async def donatebitches(ctx, *, usern):
    await ctx.send(f'<@{usern}> Damn Waxor donated you one of is 1k bitches')


@bot.command()
async def check(ctx, *, user):

    if ctx.channel.id != 969925129670897684:
        await ctx.send(f'Wrong Channel ! Check in <#969925129670897684>')
        return

    await ctx.send(f'Checking {user}')

    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }

    r = requests.get(f"https://www.tiktok.com/node/share/user/@{user}", headers=head)

    if r.status_code != 200:
        await ctx.send(f'An error occured, User {user} may be Available')

    if r.status_code == 200:
        try:
            if r.json()['statusCode'] == 10221:
                embed = discord.Embed(title=f"Checked Username", timestamp=datetime.utcnow(), color=discord.Color.blue())
                embed.add_field(name="Username", value=user)
                embed.add_field(name="Status: ", value="[Banned]")

                embed.set_thumbnail(url="https://cdn.discordapp.com/icons/963776218665213952/a23bbceba4a369452a7576454c135637.webp?size=512")

                await ctx.send(embed=embed)


                #await ctx.send(f'User :  {user} [Banned]')
            if "seoProps" in r.json():
                embed = discord.Embed(title=f"Checked Username", timestamp=datetime.utcnow(), color=discord.Color.blue())
                embed.add_field(name="Username", value=user)
                embed.add_field(name="Status: ", value="[Taken]")
                embed.set_thumbnail(url="https://cdn.discordapp.com/icons/963776218665213952/a23bbceba4a369452a7576454c135637.webp?size=512")
                await ctx.send(embed=embed)

            if r.json()['statusCode'] == 10202:

                embed = discord.Embed(title=f"Checked Username <@&969735246029402112>", timestamp=datetime.utcnow(), color=discord.Color.blue())
                embed.add_field(name="Username", value=user)
                embed.add_field(name="Status: ", value="[Available!]")
                embed.set_thumbnail(url="https://cdn.discordapp.com/icons/963776218665213952/a23bbceba4a369452a7576454c135637.webp?size=512")
                await ctx.send(embed=embed)


            if r.json()['statusCode'] == 10223:
                embed = discord.Embed(title=f"Checked Username", timestamp=datetime.utcnow(), color=discord.Color.blue())
                embed.add_field(name="Username", value=user)
                embed.add_field(name="Status: ", value="[Blacklisted!]")
                embed.set_thumbnail(url="https://cdn.discordapp.com/icons/963776218665213952/a23bbceba4a369452a7576454c135637.webp?size=512")
                await ctx.send(embed=embed)



            if r.json()['statusCode'] == 10222:
                embed = discord.Embed(title=f"Checked Username", timestamp=datetime.utcnow(), color=discord.Color.blue())
                embed.add_field(name="Username", value=user)
                embed.add_field(name="Status: ", value="[Taken]")
                embed.set_thumbnail(url="https://cdn.discordapp.com/icons/963776218665213952/a23bbceba4a369452a7576454c135637.webp?size=512")
                await ctx.send(embed=embed)

        except:
            try:
                usern = user
                embed = discord.Embed(title=f"Checked Username", timestamp=datetime.utcnow(), color=discord.Color.blue())
                embed.add_field(name="Username", value=user)
                embed.add_field(name="Status: ", value="[Taken]")
                embed.set_thumbnail(url="https://cdn.discordapp.com/icons/963776218665213952/a23bbceba4a369452a7576454c135637.webp?size=512")
                await ctx.send(embed=embed)
            except:
                pass


@bot.command()
@commands.has_role('owner')
async def hehe(ctx):
    await ctx.send(f'You are authorized')


@bot.command()
async def ping(ctx):
    await ctx.send(f'Online! Latency: {round(bot.latency, 3)} ms')


@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Waxor's Server", timestamp=datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"2022-04-13 12:22")
    embed.add_field(name="Author", value=f"The Waxor's")
    embed.add_field(name="Server Region", value=f"Europe")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    # embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/963776218665213952/a23bbceba4a369452a7576454c135637.webp?size=512")

    await ctx.send(embed=embed)


@bot.command()
async def docu(ctx):
    embed = discord.Embed(title=f"WaxBot", description="Waxor's Official Bot", timestamp=datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Creation Date:", value=f"4/20/2022")
    embed.add_field(name="Bot Creator", value=f"Waxor#9999")
    embed.add_field(name="Command prefix", value=f"$")
    # embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/963776218665213952/a23bbceba4a369452a7576454c135637.webp?size=512")

    await ctx.send(embed=embed)


@bot.command(aliases=['purge', 'delete'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=None):
    if amount == None:
        await ctx.channel.purge(limit=1000000)
    else:
        try:
            int(amount)
        except:
            await ctx.send('zizi')
        else:
            await ctx.channel.purge(limit=amount)


if __name__ == '__main__':
    times = time.time()

    bot.run("BOT_TOKEN")
