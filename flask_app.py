from flask import Flask, request, render_template, jsonify, Response
from nighthawks import NightHawks, Generator, Handler, UIDBypass
import requests
import discord
from discord.ext import commands
import json
from nighthawks import UIDBypass, Handler
from threading import Thread

# Init Classes...
nighthwaks = NightHawks()
license_generator = Generator()
accountManager = Handler(level_0 = 3, level_1 = 7, level_2 = 30)
bypass = UIDBypass()

# Auth Methods...
def createLicense(note, level, duration):
    key = license_generator.generateLicenseKey(
        note=note,
        subscripiton_level=level,
        duration=duration
    )

    return key

def daysLeft(username, password):
    days_left = accountManager.DaysLeft(username=username, password=password)
    return days_left
    
def register(key, user, password, hwind):
    response = accountManager.RegisterAccount(
        license_key=key, 
        username=user, 
        password=password,
        hwind=hwind
    )
    return response

def login(username, password, hwind):
    response = accountManager.LoginAccount(username=username, password=password, hwind=hwind)
    return response

# Panel Patching Methods...
def patch_pattern(pattern):
    response = nighthwaks.patchPattern(aob_pattern=pattern)
    return response

def patch_head_offset(offset):
    response = nighthwaks.patchHeadOffset(head_offset=offset)
    return response

def patch_left_ear_offset(offset):
    response = nighthwaks.patchLeftEarOffset(left_ear_offset=offset)
    return response

def patch_right_ear_offset(offset):
    response = nighthwaks.patchRightEarOffset(right_ear_offset=offset)
    return response

def patch_left_shoulder_offset(offset):
    response = nighthwaks.patchLeftShoulderOffset(left_shoulder_offset=offset)
    return response

def patch_right_shoulder_offset(offset):
    response = nighthwaks.patchRightShoulderOffet(right_shoulder_offset=offset)
    return response


def load_panel_data():
    return nighthwaks.LoadPanelData()


def patch_status(status):
    return nighthwaks.patchStatus(status=status)

# uid bypass ...
def whitelist_uid(uid: str, username: str, password: str):
    return bypass.whitelistUid(uid=uid, username=username, password=password)




# app init
app = Flask(__name__, template_folder=".")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/uidwhitelist")
def whitelistpage():
    return render_template("uidwhitelist.html")


@app.route("/createlicensekey")
def CreateLicenseKey():
    note = request.args.get("note")
    level = request.args.get("level")
    duration = request.args.get("duration")
    license_key = createLicense(note=note, level=int(level), duration=int(duration))

    return license_key


@app.route("/register")
def Register():
    key = request.args.get("key")
    user = request.args.get("user")
    password = request.args.get("password")
    hwind = request.args.get("hwind")

    return register(key=key, user=user, password=password, hwind=hwind)

@app.route("/login")
def Login():
    username = request.args.get("user")
    password = request.args.get("password")
    hwind = request.args.get("hwind")
    response = login(username=username, password=password, hwind=hwind)

    return response


@app.route("/accountduration")
def Duration():
    username = request.args.get("user")
    password = request.args.get("password")
    response = daysLeft(username=username, password=password)
    return response

@app.route("/patchpattern")
def PatchPattern():
    pattern = request.args.get("pattern")
    response = patch_pattern(pattern=pattern)
    return response

@app.route("/patchheadoffset")
def PatchHeadOffset():
    offset = request.args.get("offset")
    response = patch_head_offset(offset=offset)
    return response

@app.route("/patchleftearoffset")
def PatchLeftEarOffset():
    offset = request.args.get("offset")
    response = patch_left_ear_offset(offset=offset)
    return response

@app.route("/patchrightearoffset")
def PatchRightEarOffset():
    offset = request.args.get("offset")
    response = patch_right_ear_offset(offset=offset)
    return response

@app.route("/patchleftshoulderoffset")
def PatchLeftShoulderOffset():
    offset = request.args.get("offset")
    response = patch_left_shoulder_offset(offset=offset)
    return response

@app.route("/patchrightshoulderoffset")
def PatchRightShoulderOffset():
    offset = request.args.get("offset")
    response = patch_right_shoulder_offset(offset=offset)
    return response


@app.route("/patchpanelstatus")
def PatchPanelStatus():
    status = request.args.get("status")
    response = patch_status(status=status)
    return response

@app.route("/loadpaneldata")
def LoadPanelData():
    response = load_panel_data()
    return jsonify(response)


# uid bypass
@app.route('/whitelist')
def uid_whitelist():
    uid = request.args.get("uid")
    username = request.args.get("username")
    password = request.args.get("password")

    try:
        response = whitelist_uid(uid, username, password)
        return jsonify({'response': response}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
    


# discord bot 
def get_token() -> str:
    with open("bot.json", 'r') as token_file:
        data = json.load(token_file)

    return str(data['token']) 

discord_token = get_token()



discord_token = get_token()


# intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

# create bot
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return 
    
    await bot.process_commands(message)



@bot.command()
async def bypass(ctx, *, command):
    bypass = UIDBypass()
    handler = Handler()

    await ctx.send(f'{ctx.author.mention} - Please wait...')
    
    uid, username, password = command.split(" ")

    # first attempt login
    login_response = handler.LoginAccount(username, password, is_bot_request=True)
    
    if login_response == "Login Success":
        bypass_response = bypass.whitelistUid(uid, username, password)
        await ctx.send(f'{ctx.author.mention} - \nUID: {uid}\nUsername: {username}\nPassword: {password}\nStatus: {login_response}\nWhitelist Status: {bypass_response}')
    else:
        await ctx.send(f'{ctx.author.mention} - \nUID: {uid}\nUsername: {username}\nPassword: {password}\nStatus: {login_response}')


@bypass.error
async def bypass_error(ctx, error):
    await ctx.send(f'{ctx.author.mention} - {error}')


def run_discord_bot():
    bot.run(discord_token)

if __name__ == "__main__":
    Thread(target = run_discord_bot).start()
    app.run(debug=False, host="0.0.0.0", port=5002)

