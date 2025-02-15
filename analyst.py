import discord
import aiohttp
from openai import OpenAI

# Set your API keys
DISCORD_BOT_TOKEN = "INSERT DISCORD TOKEN HERE"
OPENAI_API_KEY = "INSERT OPEN AI KEY HERE"

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Discord bot
bot = discord.Client(intents=intents)

async def analyze_image(image_url):
    """Sends the image to OpenAI GPT-4o-mini for analysis."""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",  # GPT-4o supports image analysis
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this crypto or stock chart"},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ],
                }
            ],
            max_tokens=500  # Adjust response length
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error processing image: {str(e)}"

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    """Handles incoming messages, detects images, and forwards them for analysis."""
    if message.author == bot.user:
        return  # Ignore the bot's own messages

    # Check if an image is attached
    if message.attachments:
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith("image/"):
                image_url = attachment.url
                await message.channel.send(f"📌 **Analyzing Chart with GPT-4o-mini**")

                # Analyze the image
                analysis = await analyze_image(image_url)

                # Send OpenAI's response back to Discord
                await message.channel.send(f"📊 **Analysis:** {analysis}")

# Run the bot
bot.run(DISCORD_BOT_TOKEN)
