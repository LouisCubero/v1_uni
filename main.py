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

        # Get the appropriate school logo based on user roles
    def get_school_logo(self, member):
        # Dictionary mapping role IDs to school logo URLs
        school_logos = {
            # Replace these IDs with your actual role IDs
            1355788273058058371: "https://cdn.discordapp.com/attachments/1355611106382708736/1356740823118774482/columbialogo.png?ex=67edaadb&is=67ec595b&hm=6067f1cd9564605c2f4b2418090f243bd3298b62bbb622d07b0eb96ee4d9b440&",  # Columbia
            1355791552768774174: "https://cdn.discordapp.com/attachments/1355611106382708736/1356742046857039943/nyulogo.png?ex=67edabff&is=67ec5a7f&hm=bd66e1bc1b3394f7183e2ed9e59ee91d3db554830714bf0a3ccd384eae1e43ae&",  # NYU
            1355789472494780477: "https://cdn.discordapp.com/attachments/1355611106382708736/1356743401965359145/mhclogo.png?ex=67edad42&is=67ec5bc2&hm=d4abc711fc9014ed5261329b2944565ec2ecdcf238c2af76741aa5df3a405c35&",  # Macaulay Honors
            1355790991835271168: "https://cdn.discordapp.com/attachments/1355611106382708736/1356743487155994776/baruchcollegelogo.png?ex=67edad56&is=67ec5bd6&hm=e84dbc46690ee8de63e5364b0898cc2eae7940879c48d3fb48fadfe727a409d8&",  # Baruch
            1355790760443641886: "https://cdn.discordapp.com/attachments/1355611106382708736/1356744779324461239/hunterlogo.png?ex=67edae8a&is=67ec5d0a&hm=36cc89d356bc12c6b952ee7677daf704f272c3850769f633c415b7f6ff4057d1&",  # Hunter
            1349057678667939870: "https://cdn.discordapp.com/attachments/1355611106382708736/1356693672283996406/qclogov1.png?ex=67ed7ef1&is=67ec2d71&hm=409ee1bed3b5479134aa580cc5eeea88571ae57de0bc8fd8e219c1147c19c5b4&",  # Queens College
            1355857070989246555: "https://cdn.discordapp.com/attachments/1355611106382708736/1356746273637531718/paceuniversitylogo.png?ex=67edafee&is=67ec5e6e&hm=0f468f6786cf99a3e04fdd7786a2e3a0a3a5eab85ecfea35c862e9203bef0336&",  # Pace University
            1355794438877745243: "https://cdn.discordapp.com/attachments/1355611106382708736/1356746851793109032/brooklyncollegelogo.png?ex=67edb078&is=67ec5ef8&hm=e229ea1e5c35df0d6d3f42b08a82599e35fc27df709bbec312cbc0e573cadf1a&",  # Brooklyn College
            1355793900648005723: "https://cdn.discordapp.com/attachments/1355611106382708736/1356747464216154293/lehmancollegelogo.png?ex=67edb10a&is=67ec5f8a&hm=7ad427bb9db2c84b78bb33179069715d66fd5cde0e6f5b971bc86791916b37c8&",  # Lehman College
            1355792094907596841: "https://cdn.discordapp.com/attachments/1355611106382708736/1356748002240237618/ccnylogo.png?ex=67edb18a&is=67ec600a&hm=1e375f4a2f4bd652dd73e0f947e8f2f5cb128e2a58501c87cfab3a6a6237b1a8&",  # CCNY
            1355795331710980096: "https://cdn.discordapp.com/attachments/1355611106382708736/1356748930435645543/melogo.png?ex=67edb268&is=67ec60e8&hm=554a234a05dc8e4c43a94cd8fc948b27a7c18117ab5cd42fc10795d05c352ccb&",  # Medgar Evers
            1355792949358886942: "https://cdn.discordapp.com/attachments/1355611106382708736/1356749592099684524/johnjaylogo.png?ex=67edb305&is=67ec6185&hm=fa8388b21095d99ab7e0e36df73f654c44ab7509e8f562b2e85d977e7664da59&",  # John Jay
            1355793530072731791: "https://cdn.discordapp.com/attachments/1355611106382708736/1356750312337309927/CSIlogo.png?ex=67edb3b1&is=67ec6231&hm=980d610024929711e4134f2428872ca8fc051e4adf535dbdb9a4920c9bd50367&",  # CSI
            1355796615348097064: "https://cdn.discordapp.com/attachments/1355611106382708736/1356751191228284969/yorkcollegelogo.png?ex=67edb483&is=67ec6303&hm=7e1dae52346ba893255b8b529e2e2a70e76659f7f06767220253ebb984f69e70&",  # York College
            1355796615348097064: "https://cdn.discordapp.com/attachments/1355611106382708736/1356751716518723795/citytechlogo.png?ex=67edb500&is=67ec6380&hm=389ce0ab3ab5d59d7270a3229b926d66f023788e083c58184f6089729c2ab13d&",  # City Tech
        }
        
        # Default logo in case no matching role is found
        default_logo = "https://example.com/default_logo.png"
        
        # Check if the member has any of the specified roles
        for role in member.roles:
            if role.id in school_logos:
                return school_logos[role.id]
        
        # Return default logo if no matching role found
        return default_logo

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
            
            if image_url:
                try:
                    # Clean up the URL - remove spaces and ensure it's properly formatted
                    image_url = image_url.strip()
                    
                    # Add the image to the embed
                    embed.set_image(url=image_url)
                except Exception as img_error:
                    print(f"Image error: {str(img_error)}")
                    # Use school logo if image URL fails
                    school_logo = self.get_school_logo(interaction.user)
                    embed.set_thumbnail(url=school_logo)
            else:
                # If no image URL is provided, use the appropriate school logo
                school_logo = self.get_school_logo(interaction.user)
                embed.set_thumbnail(url=school_logo)
            
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

# Button to open the event modal with permission check
class EventButton(discord.ui.View):
    @discord.ui.button(label="Create Event", style=discord.ButtonStyle.primary)
    async def create_event(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Check if the user has the required role
        required_role_id = 1347727872084807700
        
        # Check if user has the required role
        if not any(role.id == required_role_id for role in interaction.user.roles):
            # For normal users without permission, respond with an ephemeral message 
            # (only visible to them) or simply do nothing by deferring the response
            await interaction.response.defer()
            return
            
        # If user has permission, open the modal to fill out event details
        await interaction.response.send_modal(EventModal())

# Slash command to display the event creation button - restricted to specific role
@bot.slash_command(
    description="Display the button to create an event.",
    guild_ids=[1346952384965902450]
)
# Only students with Club Leader role have access to make event button + actually use it.
async def event_button(interaction: discord.Interaction):
    # Check if the user has the required role
    required_role_id = 1347727872084807700
    
    # Check if user has the required role
    if not any(role.id == required_role_id for role in interaction.user.roles):
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return
    
    # If user has permission, display the button for creating an event
    view = EventButton()
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