import os 
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Load the token from the .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

BOT_CATEGORY = "Bots"
BOT_CHANNEL = "commands"

# Define channels to create under the category
text_channels = ["discussions", "tasks", "git-commits","bug-reports","resource-sharing", "project-resources"]
voice_channels = ["meeting"]

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True  # Enables reading message content

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def setup(ctx, role_name: str):
    # Check if the command is being used in the "commands" channel within the "Bots" category
    if ctx.channel.name != BOT_CHANNEL or ctx.channel.category.name != BOT_CATEGORY:
        await ctx.send("This command can only be used in the #commands channel under the Bots category.")
        return

    # Check if the user has administrative privileges
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("You do not have the necessary permissions to use this command.")
        return
    
    guild = ctx.guild
    
    # Create a new role
    role = await guild.create_role(name=role_name)

    # Create a new category
    category = await guild.create_category(role_name)

    

    # Create text channels under the category
    for channel_name in text_channels:
        await guild.create_text_channel(name=channel_name, category=category)

    # Create voice channels under the category
    for channel_name in voice_channels:
        await guild.create_voice_channel(name=channel_name, category=category)

    # Restrict category visibility to the new role
    overwrite = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        role: discord.PermissionOverwrite(read_messages=True)
    }
    await category.edit(overwrites=overwrite)

    # Apply the same restrictions to each channel in the category
    for channel in category.channels:
        await channel.edit(overwrites=overwrite)

    await ctx.send(f"Setup complete! Category and channels created, and restricted to {role.name}.")

# Run the bot using a secure method to store the token
bot.run(DISCORD_TOKEN)
