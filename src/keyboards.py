from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = [
    [InlineKeyboardButton(text="Testnet", callback_data="get_testnet_tokens"),
    InlineKeyboardButton(text="Mainnet", callback_data="get_mainnet_tokens")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)