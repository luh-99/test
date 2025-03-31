import os
from io import BytesIO
from PIL import Image
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ApplicationBuilder, ContextTypes
from telegram.ext import filters
import asyncio
import nest_asyncio

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

TOKEN = 'YOUR_BOT_TOKEN'  # Replace with your actual bot token

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Send me a .webp image and I will convert it to .png and .jpg formats!')

async def convert_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file = update.message.photo[-1].get_file()
    await file.download('temp.webp')

    # Convert .webp to .png
    with Image.open('temp.webp') as img:
        img.save('converted.png', 'PNG')

    # Convert .webp to .jpg
    with Image.open('temp.webp') as img:
        img.convert('RGB').save('converted.jpg', 'JPEG')

    # Send the converted images
    with open('converted.png', 'rb') as png_file:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=png_file)

    with open('converted.jpg', 'rb') as jpg_file:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=jpg_file)

    # Clean up temporary files
    os.remove('temp.webp')
    os.remove('converted.png')
    os.remove('converted.jpg')

async def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.PHOTO, convert_image))

    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
