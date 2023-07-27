from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from tran.send_testnet_tran import send_testnet_tran
from tran.send_mainnet_tran import send_mainnet_tran
from aiogram.fsm.context import FSMContext
from src.states import Network
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage


import src.keyboards
import src.text
import re
import time

storage=MemoryStorage()
router = Router()

def is_valid_address(text):
    pattern = r'^0x[0-9a-fA-F]{40}$'
    return bool(re.match(pattern, text))


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(src.text.start_message.format(name=msg.from_user.full_name), reply_markup=src.keyboards.menu)


@router.callback_query(F.data == "get_testnet_tokens")
async def testnet_button(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Network.testnet_tran)
    await clbck.message.edit_text(src.text.ask_user_address_message) 


@router.message(Network.testnet_tran)
async def get_testnet_hash(msg: Message, state: FSMContext):
    user_address = msg.text
    data = await state.get_data()

    current_time = time.time()
    cooldown_time = 24 * 60 * 60

    if data == {}:
        await state.update_data(user_cooldown_testnet=0)
        await state.update_data(user_cooldown_mainnet=0)
        data = await state.get_data()



    if data['user_cooldown_testnet'] == 0 or current_time - data['user_cooldown_testnet'] >= cooldown_time:
        if is_valid_address(user_address):
            tran_link = send_testnet_tran(user_address)
            await msg.answer(src.text.success_tran_message.format(network='testnet'))
            await msg.answer(tran_link)
            await msg.answer(src.text.use_again)
            state.set_state(state=None)

            await state.update_data(user_cooldown_testnet=time.time())
        else:            
            await msg.answer(src.text.incorrect_address_message)      
    else:
        await msg.answer(src.text.cooldown_message.format(network='testnet'))
        await msg.answer(src.text.use_again)
        state.set_state(state=None)




@router.callback_query(F.data == "get_mainnet_tokens")
async def mainnet_button(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Network.mainnet_tran)
    await clbck.message.edit_text(src.text.ask_user_address_message)


@router.message(Network.mainnet_tran)
async def get_mainnet_hash(msg: Message, state: FSMContext):
    user_address = msg.text
    data = await state.get_data()

    current_time = time.time()
    cooldown_time = 24 * 60 * 60

    if data == {}:
        await state.update_data(user_cooldown_testnet=0)
        await state.update_data(user_cooldown_mainnet=0)
    
    if data['user_cooldown_mainnet'] == 0 or current_time - data['user_cooldown_mainnet'] >= cooldown_time:
        if is_valid_address(user_address):
            tran_link = send_mainnet_tran(user_address)
            await msg.answer(src.text.success_tran_message.format(network='mainnet'))
            await msg.answer(tran_link)
            await msg.answer(src.text.use_again)
            state.set_state(state=None)

            await state.update_data(user_cooldown_mainnet=time.time())

        else:
            await msg.answer(src.text.incorrect_address_message)  
    else:
        await msg.answer(src.text.cooldown_message.format(network='mainnet'))
        await msg.answer(src.text.use_again)
        state.set_state(state=None)