# Discord AI Chatbot
#### Your Discord AI Companion!
Originally made by [MishalHossin](https://github.com/mishalhossin/Discord-AI-Chatbot/) and all credit for this excellent code goes to them.

## Features and commands 🌟

<summary><strong>Features</strong></summary>

 - [x] Hybrid Command System: Get the best of both slash and normal commands.
 - [x] Free LLM Model: Use this powerful language model without spending anything.
 - [x] Mention Recognition: The bot will always respond when mentioned or called by name.
 - [x] Message Handling: The bot knows when you're replying to someone else, avoiding confusion.
 - [x] Channel-Specific Responses: Use the /toggleactive command to disable the bot in specific channels.
 - [x] Secure Credential Management: Protect your credentials with environment variables.
 - [x] Web Access: Internet-enabled LLM to allow for current awareness.

<summary><strong>Commands</strong></summary>

- [x] `/help`: Get all commands

Too lazy to list all of em here


## Additional configurations ⚙️

<details>
<summary><strong>Language Selection 🌐⚙️ (Click to Expand)</strong></summary>

To select a Language, set the value of `"LANGUAGE"` of `config.yml` with the valid Language Codes listed below:

- `tr` - Türkçe 🇹🇷  
- `en` - English 🇺🇸
- `ar` - Arabic 🇦🇪
- `fr` - Français 🇫🇷
- `es` - Español 🇪🇸
- `de` - Deutsch 🇩🇪  
- `vn` - Vietnamese 🇻🇳
- `cn` - Chinese 🇨🇳
- `ru` - Russian 🇷🇺
- `ua` - Ukrainian 🇺🇦
- `pt` - Português 🇧🇷
- `pl` - Polish 🇵🇱
  
</details>
  
<summary><strong> Creating a Personality</strong></summary>

To create a custom personality, follow these steps:
1. Create a `.txt` file like `yourfile.txt` inside the `instructions` folder.
2. Add the way you want the bot to act in `yourfile.txt`
3. Open the `config.yml` file and locate [line 17](https://github.com/ArchAngel2190/TrumpBot/blob/fb3857c2db30bfe246f365ab06c96b426f7bdc0c/config.yml#L17).
4. Set the value of INSTRUCTIONS at [line 17](https://github.com/ArchAngel2190/TrumpBot/blob/fb3857c2db30bfe246f365ab06c96b426f7bdc0c/config.yml#L17) as `"yourfile"` to specify the custom persona.

⚠️ You don't explicitly need to use the name `yourfile` for persona name and set it in `config.yml`, name it whatever you want.

# Installation
Follow this guide in its entirety. Or don't, I'm not your real dad.

## Prerequisites:
This bot runs on **Python <3.13.** If you try to run this bot on Python 3.13, *it will fail and you will be confused.* This bot MUST use Python 3.12 or older. Use venv or pipx to install older python versions and make sure that to run the bot you use **python3.12 main.py** and not **python main.py.**

## Installation guide:

### Step 1. Git clone repository
```
git clone https://github.com/ArchAngel2190/TrumpBot/
```
### Step 2. Changing directory to cloned directory
```
cd TrumpBot
```
### Step 3. Install requirements
```
python3.10 -m pip install -r requirements.txt
```
### Step 4. Getting discord bot token and enabling intents from [HERE](https://discord.com/developers/applications)

<details>
<summary><strong>Read more...  ⚠️  (Click to expand)</strong></summary>

##### Select the correct application from your Discord Developer dashboard

##### Enable intents
The intents the bot needs are Presence, Server Members, and Message Content. These should be enabled by default.

##### Copy your bot's secret token (only shown once, so make sure you copy it then or you will have to regenerate it)
</details>

### Step 5. [Create a Groq account](https://console.groq.com/login)
### Step 6. [Get Groq api key](https://console.groq.com/keys)
### Step 7. Open `.env` and put in the Discord bot token and your Groq key. 
Keep in mind that if you are on Linux, `.env` will be hidden by default and must be opened by navigating to `/.env` or checking "Show hidden files" in your file manger.  

When properly filled out, `.env` will look like this:
```
DISCORD_TOKEN=DISCORD_TOKEN_HERE
API_KEY=GROQ_TOKEN_HERE
```
### Step 7. 🚀 Run the bot with
```
python3.12 main.py
```
Ensure you use whatever Python version you have installed. If you are using venv, you may not need the `python3.12` command and `python` may work.

#### You may need to run as admin if you are on Windows (but you shouldn't be - why do that to yourself?)
### Step 8. 🔗 Invite the bot 
You can Invite your bot using the link in console, or by creating an invite link in Discord Developer's console and giving it the permissions "Bot" and subsequently "Send messages"
![image](https://user-images.githubusercontent.com/91066601/236673317-64a1789c-f6b1-48d7-ba1b-dbb18e7d802a.png)

#### There are 2 ways to talk to the AI
- Invite your bot and DM (Direct Message) it | ⚠️ Make sure you have DM enabled
- If you want it in the server channel, use **/toggleactive** 
- For more awesome commands, use **/help**

### Using docker to run 🐳 (useful for hosting)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
- Have a working bot token
- Follow up to step 4
#### Install docker-compose on a Linux machine:
For Debian-based distributions (such as Ubuntu):
```
apt update -y; sudo apt upgrade -y; sudo apt autoremove -y; sudo apt install docker-compose -y
```
<details>
<summary><strong>Other Linux distro (Click to expand)</strong></summary>
  
For Red Hat-based distributions (such as CentOS and Fedora):
```
sudo yum update -y && sudo yum install -y docker-compose
```
For Arch-based distributions (such as Arch Linux):
```
sudo pacman -Syu --noconfirm && sudo pacman -S --noconfirm docker-compose
```
For SUSE-based distributions (such as openSUSE):
```
sudo zypper update -y && sudo zypper install -y docker-compose
```
</details>

#### Start the bot in Docker container:
```
sudo docker-compose up --build
```
## This entire bot was built by [MishalHossin](https://github.com/mishalhossin/Discord-AI-Chatbot/) and I take no credit for its creation.
Certain parts of their code were modified to create this bot in its present form. 
### Main differences:
- Mishal's bot uses Mistral AI, this one uses Llama
- Serious error handling fixes and adjustments that are borne not out of Mishal's code, but out of the fact that his bot was created in older versions of python
- trump.txt is my own creation

### Original contributors to Mishal Hossin's bot: 

<a href="https://github.com/mishalhossin/Discord-AI-Chatbot/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=mishalhossin/Discord-AI-Chatbot" />
</a>
