from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton

def create_len():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='/create'))

def cancelkb():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='/cancel'))

def create_parents_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text='/create_person'))
    keyboard.insert(KeyboardButton(text='/end_parent'))
    keyboard.insert(KeyboardButton(text='/cancel_parent'))
    return keyboard