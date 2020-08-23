import telebot
import os

BOT = telebot.TeleBot(os.environ['BOT_TOKEN'])

ALLOWED_CHATS = list(map(int, os.environ['ALLOWED_CHATS'].split(", ")))  # Looks like [111111111, 111111111]
SHY_ANSWER = '*неловкое молчание*'


@BOT.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(message.chat.id)
    BOT.reply_to(message, SHY_ANSWER)


@BOT.message_handler(content_types=['text'])
def echo_text(message):
    send_to_everyone_else(message.chat.id, BOT.send_message, message.text)


@BOT.message_handler(content_types=['animation'])
def echo_animation(message):
    send_to_everyone_else(message.chat.id, BOT.send_animation, message.animation.file_id)


@BOT.message_handler(content_types=['audio'])
def echo_audio(message):
    send_to_everyone_else(message.chat.id, BOT.send_audio, message.audio.file_id)


@BOT.message_handler(content_types=['contact'])
def echo_contact(message):
    send_to_everyone_else(message.chat.id, BOT.send_contact,
                          message.contact.phone_number, message.contact.first_name, message.contact.last_name)


@BOT.message_handler(content_types=['document'])
def echo_document(message):
    send_to_everyone_else(message.chat.id, BOT.send_document, message.document.file_id)


@BOT.message_handler(content_types=['photo'])
def echo_photo(message):
    send_to_everyone_else(message.chat.id, BOT.send_photo, message.photo[0].file_id, message.caption)


@BOT.message_handler(content_types=['sticker'])
def echo_sticker(message):
    send_to_everyone_else(message.chat.id, BOT.send_sticker, message.sticker.file_id)


@BOT.message_handler(content_types=['video'])
def echo_video(message):
    send_to_everyone_else(message.chat.id, BOT.send_video, message.video.file_id)


@BOT.message_handler(content_types=['video_note'])
def echo_video_note(message):
    send_to_everyone_else(message.chat.id, BOT.send_video_note, message.video_note.file_id)


@BOT.message_handler(content_types=['voice'])
def echo_voice(message):
    send_to_everyone_else(message.chat.id, BOT.send_voice, message.voice.file_id)


@BOT.message_handler(content_types=['location'])
def echo_location(message):
    send_to_everyone_else(message.chat.id, BOT.send_location, message.location.latitude, message.location.longitude)


@BOT.message_handler(content_types=['venue'])
def echo_venue(message):
    send_to_everyone_else(message.chat.id, BOT.send_venue,
                          message.venue.location.latitude, message.venue.location.longitude,
                          message.venue.title, message.venue.address)


def send_to_everyone_else(chat_id, send_function, *content):
    receive_chats = get_recipients(chat_id)
    if receive_chats is not None:
        for chat in receive_chats:
            send_function(chat, *content)
    else:
        send_shy_answer(chat_id)


def get_recipients(chat_id):
    if chat_id not in ALLOWED_CHATS:
        return None

    receive_chats = ALLOWED_CHATS.copy()
    receive_chats.remove(chat_id)
    return receive_chats


def send_shy_answer(chat_id):
    BOT.send_message(chat_id, SHY_ANSWER)


BOT.polling(none_stop=True)
