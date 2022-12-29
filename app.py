import asyncio

from time import time
from hashlib import md5
from translate import Translate

from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


TOKEN = "TOKEN"

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

rooms = {}


class User:
    def __init__(self, id):
        self.id = id

    async def send(self, text):
        await bot.send_message(self.id, text)

    async def recieve(self):
        print('Waiting for message...')
        return await bot.wait_for('message', check=lambda m: m.from_user.id == self.id)
    

class ChatRoom:
    def __init__(self, id):
        self.id = id
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def remove_user(self, user):
        self.users.remove(user)

    async def send(self, text):
        for user in self.users:
            await user.send(text)

    async def recieve(self):
        for user in self.users:
            await user.recieve()


class ConnectRoom(StatesGroup):
    code_room = State()
    password_room = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    start_text = 'Hello! I am a translator bot. I can translate your text into English and Ukrainian. Type /help if you need help.'
    await message.answer(start_text)


@dp.message_handler(commands=['create'])
async def create(message: types.Message):
    try:
        for code, room in rooms.items():
            for user in room.users:
                if user.id == message.from_user.id:
                    await message.answer('You are already in the room.')
                    return
    except RuntimeError:
        pass

    rooms[message.from_user.id] = ChatRoom(message.from_user.id)
    rooms[message.from_user.id].add_user(User(message.from_user.id))
    password = md5(str(time()).encode()).hexdigest()
    rooms[message.from_user.id].password = password
    await message.answer(f'Your room code is <code>{message.from_user.id}</code>. Your password is <code>{password}</code>. Send it to your friend to connect to the room.')
    await message.answer('Room is created!')
    await message.answer('Waiting for connection...')


@dp.message_handler(commands=['leave'])
async def leave(message: types.Message):
    try:
        for code, room in rooms.items():
            for user in room.users:
                if user.id == message.from_user.id:
                    await message.answer('You left the room.')
                    room.remove_user(user)
                else:
                    await user.send(f'User left the room.')
    except RuntimeError:
        pass


@dp.message_handler(commands=['connect'], state=None)
async def connect(message: types.Message):
    await ConnectRoom.code_room.set()
    await message.answer('Enter the code of the room')


@dp.message_handler(state=ConnectRoom.code_room)
async def load_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['code'] = message.text
    await ConnectRoom.next()
    await message.answer('Enter the password of the room')


@dp.message_handler(state=ConnectRoom.password_room)
async def load_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
    await state.finish()
    code = int(data['code'])
    if rooms[code].password == data['password']:
        rooms[code].add_user(User(message.from_user.id))
        await message.answer('You are in the chat')
    else:
        await message.answer('Wrong password')
    
    for user in rooms[code].users:
        if user.id != message.from_user.id:
            await user.send(f'User connected to the room.')


@dp.message_handler(commands=['help'])
async def help(message: types.Message):      
    help_text = "Welcome to the chat bot. Here are the commands you can use:\n"
    help_text += "/create - create to the chat\n"
    help_text += "/leave - leave to the chat\n"
    help_text += "/connect - connect to the chat\n"
    help_text += "/help_translate - help use command translate\n"
    help_text += "/translate - translate the message\n (en - English or ua - Ukraine)\n"
    help_text += "/help - show this message\n"
    await message.answer(help_text)


@dp.message_handler(commands=['help_translate'])
async def help_translate(message: types.Message):
    help_text = "Welcome to the chat bot. Here are the commands you can use:\n"
    help_text += "/translate - translate the message\n (en - English or ua - Ukraine)\n"
    help_text += "Example /translate (Text for translate)"
    await message.answer(help_text)


@dp.message_handler(commands=['translate'])
async def translate(message: types.Message):
    text = message.text.split('/translate ')[1]
    translate = Translate()
    translate.translate(text)
    await message.answer(translate)


@dp.message_handler()
async def update(message: types.Message):
    for _, room in rooms.items():
        for user in room.users:
            if user.id != message.from_user.id:
                text = f'<code>{message.text}</code>'
                await User(user.id).send(text)


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        tasks = [executor.start_polling(dp, skip_updates=True)]
        loop.run_until_complete(asyncio.wait(tasks))
    except TypeError:
        pass
    
# create fucntion buble sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# create function selection sort
def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

