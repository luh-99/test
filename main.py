import os
from io import BytesIO
from PIL import Image
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ApplicationBuilder, ContextTypes
from telegram.ext import filters
import asyncio

TOKEN = '7467798825:AAFf4L4WFZby8P_Rz5Fj9HxJtSb5gsfluxE'  # Replace with your actual bot token

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
    try:
        asyncio.run(main())  # Use this if you're sure you're in a fresh environment
    except RuntimeError as e:
        if 'event loop is already running' in str(e):
            # Handle the case if the event loop is already running
            loop = asyncio.get_event_loop()
            loop.create_task(main())
        else:
            raise
