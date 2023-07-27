from aiogram.fsm.state import StatesGroup, State

class Network(StatesGroup):
    mainnet_tran = State()
    testnet_tran = State()