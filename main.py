import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import random
import json

# Load environment variables from .env file
load_dotenv()

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot
bot = discord.Bot(intents=intents)

# Slash command to greet the user
@bot.slash_command(
    description="Command the bot to say a random comedy quote.",
    guild_ids=[1346952384965902450]
)
async def say_something(interaction: discord.Interaction):
    # Open and read the quotes.json file
    with open('quotes.json', 'r') as file:
        quotes_data = json.load(file)
    
    # Get a random comedy quote
    tips_quotes = quotes_data.get("tips", [])
    if tips_quotes:
        quote = random.choice(tips_quotes)
    else:
        quote = "I couldn't find any comedy quotes, but here's a joke: Why don't programmers like nature? It has too many bugs!"

    await interaction.response.send_message(quote)

# Event modal to collect information
class EventModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Create an Event!")

        # Add questions as inputs
        self.add_item(discord.ui.InputText(label="Event Name", placeholder="The name of your event.", required=True))
        self.add_item(discord.ui.InputText(label="Link", placeholder="Drop any links to register for the event.", required=True))
        self.add_item(discord.ui.InputText(label="Location", placeholder="Where is it taking place?", required=True))
        self.add_item(discord.ui.InputText(label="Date & Time", placeholder="e.g., Monday, September 21st @ 12:00PM", required=True))
        self.add_item(discord.ui.InputText(label="Image URL (optional)", placeholder="image URL", required=False))

    # This method needs to be indented properly to be part of the class
    async def callback(self, interaction: discord.Interaction):
        try:
            event_name = str(self.children[0].value)
            form_link = str(self.children[1].value)
            location = str(self.children[2].value)
            date_time = str(self.children[3].value)
            image_url = str(self.children[4].value).strip() if self.children[4].value else None

            # Create embed with linked title
            embed = discord.Embed(
                title=f"**{event_name}**",
                url=form_link,
                color=discord.Color.blurple()
            )
            
            # Add fields with proper formatting
            embed.add_field(name="**Where:**", value=location, inline=False)
            embed.add_field(name="**When:**", value=date_time, inline=False)
            
            # Set the image if a URL was provided
            if image_url:
                try:
                    # Clean up the URL - remove spaces and ensure it's properly formatted
                    image_url = image_url.strip()
                    
                    # Add the image to the embed
                    embed.set_image(url=image_url)
                    
                except Exception as img_error:
                    # If there's an error with the image, still create the event but log the error
                    print(f"Image error: {str(img_error)}")
                    # You could add a field to the embed noting the image failed to load
                    embed.add_field(name="**Note:**", value="Image could not be loaded", inline=False)
            
            # Send the embed to the specific channel
            channel = interaction.guild.get_channel(1355611106382708736)
            if channel:
                await channel.send(embed=embed)
                await interaction.response.send_message("Event submitted successfully!", ephemeral=True)
            else:
                await interaction.response.send_message("The specified channel could not be found.", ephemeral=True)

        except Exception as e:
            # Print detailed error for debugging
            import traceback
            traceback.print_exc()
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)

# Button to open the event modal
class EventButton(discord.ui.View):
    @discord.ui.button(label="Create Event", style=discord.ButtonStyle.primary)
    async def create_event(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Open the modal to fill out event details
        await interaction.response.send_modal(EventModal())

# Slash command to display the event creation button
@bot.slash_command(
    description="Display the button to create an event.",
    guild_ids=[1346952384965902450]  # Replace with your server ID
)
async def event_button(interaction: discord.Interaction):
    # Display the button for creating an event
    view = EventButton()  # Instantiate the button view properly
    await interaction.response.send_message("Click the button to create an event!", view=view)

# Bot ready event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Run the bot with your token
try:
    token = os.getenv("TOKEN")
    if not token:
        raise Exception("Please add your token to the .env file.")
    bot.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
    else:
        raise e