from aiogram import Bot, Dispatcher, executor, types
from keyboards import create_len, cancelkb, create_parents_keyboard
from config import TOKEN_API
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from writeword import write
from database import *
import os

storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)
payload = 0
dict_data = {}
class Create_len(StatesGroup):
    fio = State()
    study = State()
    birthday = State()
    country = State()
    millati = State()
    partiyaviylik = State()
    malumoti = State()
    tamomlagan = State()
    mutaxassisligi = State()
    language = State()
    mukofot = State()
    saylov = State()
    mehnat_faoliyati = State()
    photo = State()
    count_parents = State()

class Create_parents(StatesGroup):
    count_par = State()
    qarindoshligi = State()
    fio = State()
    birthday = State()
    work = State()
    location = State()
async def on_startup(_):
    print('bot started')
    await db_start()


def clear_history(user_id):
    os.remove(f"{user_id}.jpg")
    os.remove(f"{user_id}.docx")


COMMAND_START = f"""
<b>Salom bot Anketa yaratishga yordam beradi </b>

Endi sizga vaqt sarflab <b>kompyuter yonida o'tirishingiz kerak emas</b>👨‍💻

Anketaa yaratishni boshlash uchun<b> /create </b>komandasini yoki 
pasdagi 'create' knopkasini bosing
"""

COMMAND_CANCEL = f"""
<b>Anketani to'ldirish tugatildi🛑</b>

Boshqa yangi anketa yaratishni boshlash uchun /create komandasini yoki
pasdagi 'create' tugmasini bosing
"""
@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message):
    await message.answer(text=COMMAND_START,
                         reply_markup=create_len(),
                         parse_mode='HTML')
    await add_acet(message.from_user.id, 0)

@dp.message_handler(commands=['create'])
async def cmd_create(message: types.Message):
    image_path = os.path.join(os.getcwd(), 'pnganketa.jpg')
    with open(image_path, 'rb') as photo:
        await bot.send_photo(chat_id=message.chat.id,
                             photo=photo,
                             caption='Anketa dokumentiga misol shu tarzda bo\'ladi')
        await message.answer(text='Kim uchun anketa yaratilyapti <b>Ism Familiya Otasining ismi</b>ni kiriting',
                             reply_markup=cancelkb(),
                             parse_mode='html')
    await Create_len.fio.set()

@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    await update_user(message.from_user.id, 'count_parent', 0)
    if state is None:
        return
    await state.finish()
    await message.reply(text=COMMAND_CANCEL,
                        parse_mode='HTML',
                        reply_markup=create_len())


@dp.message_handler(commands=['end_parent'], state='*')
async def cmd_end_parent(message: types.Message, state: FSMContext):
    a = await check_user(message.from_user.id)
    print(a)
    print(dict_data)
    await write(message.from_user.id, dict_data, a)
    await update_user(message.from_user.id, 'count_parent', 0)
    await message.reply(text='Qarindosh qo\'shish tugatildi\n<b>MARHAMAT FAYL</b>',
                        parse_mode='html')

    if state is None:
        return
    await state.finish()
    file_name = f"{message.from_user.id}" + '.docx'

    try:
        with open(file_name, 'rb') as file:
            await bot.send_document(chat_id=message.from_user.id, document=file)
    except FileNotFoundError:
        print(f"File {file_name} not found.")
    clear_history(message.from_user.id)
    await message.answer(text=COMMAND_START,
                         reply_markup=create_len(),
                         parse_mode='HTML')
    print(dict_data)
@dp.message_handler(commands=['cancel_parent'], state='*')
async def cmd_end_parent(message: types.Message, state: FSMContext):
    await update_user(message.from_user.id, 'count_parent', 0)
    await message.reply(text='Qarindosh qo\'shish tugatildi\n<b>Hujjat to\'liq bo\'lmaganligi tufayli yaratilmadi</b>',
                        parse_mode='html')
    if state is None:
        return
    await state.finish()

@dp.message_handler(lambda message: not message.photo, state=Create_len.fio)
async def cmd_fio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fio'] = message.text
        dict_data[message.from_user.id] = {}
        dict_data[message.from_user.id]['fio'] = data['fio']
    await message.reply(f'{message.text} uchun ovyektivka to\'ldirishni boshladik\n\nQayerda o\'qiysiz',
                        reply_markup=cancelkb())
    await update_user(message.from_user.id, 'fio', message.text)
    await Create_len.next()
    print(dict_data[message.from_user.id]['fio'])

@dp.message_handler(state=Create_len.study)
async def cmd_study(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['study'] = message.text
        dict_data[message.from_user.id] = {}
        dict_data[message.from_user.id]['study'] = data['study']
    await message.reply(text='Tug\'ilgan kuni, yili, oyi',
                        reply_markup=cancelkb())
    await update_user(message.from_user.id, 'study', message.text)
    await Create_len.next()

@dp.message_handler(state=Create_len.birthday)
async def cmd_birtday(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['birthday'] = message.text
        dict_data[message.from_user.id] = {}
        dict_data[message.from_user.id]['birthday'] = data['birthday']
    await message.reply(text='Qayerda tug\'ilgan',
                        reply_markup=cancelkb())
    await update_user(message.from_user.id, 'birthday', message.text)
    await Create_len.next()

@dp.message_handler(state=Create_len.country)
async def cmd_millat(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['country'] = message.text
        dict_data[message.from_user.id] = {}
        dict_data[message.from_user.id]['country'] = data['country']
    await message.reply(text='Millati',
                        reply_markup=cancelkb())
    await update_user(message.from_user.id, 'country', message.text)
    await Create_len.next()

@dp.message_handler(state=Create_len.millati)
async def cmd_millat(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    #     data['millati'] = message.text
    #     dict_data[message.from_user.id] = {}
    #     dict_data[message.from_user.id]['millati'] = data['millati']

    await update_user(message.from_user.id, 'millati', message.text)
    await message.reply(text='Partiyaviyligi \n Bor bo\'lsa turi bo\'lmasa yo\'q deb javob bering',
                        reply_markup=cancelkb())
    await Create_len.next()

@dp.message_handler(state=Create_len.partiyaviylik)
async def cmd_partiya(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    #     data['partiyaviylik'] = message.text
    #     dict_data[message.from_user.id] = {}
    #     dict_data[message.from_user.id]['partiyaviylik'] = data['partiyaviylik']
    await message.reply(text='Ma\'lumoti',
                        reply_markup=cancelkb())

    await update_user(message.from_user.id, 'partiyaviylik', message.text)
    await Create_len.next()

@dp.message_handler(state=Create_len.malumoti)
async def cmd_malumot(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    #     data['malumoti'] = message.text
    #     dict_data[message.from_user.id] = {}
    #     dict_data[message.from_user.id]['malumoti'] = data['malumoti']
    await message.reply(text='Qayerni tugatib bu yerga keldi?',
                        reply_markup=cancelkb())

    await update_user(message.from_user.id, 'malumoti', message.text)
    await Create_len.next()

@dp.message_handler(state=Create_len.tamomlagan)
async def cmd_mutaxassis(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    #     data['tamomlagan'] = message.text
    #     dict_data[message.from_user.id] = {}
    #     dict_data[message.from_user.id]['tamomlagan'] = data['tamomlagan']
    await message.reply(text='Ma\'lumoti bo\'yicha mutaxassisligi qanaqa?',
                        reply_markup=cancelkb())
    await update_user(message.from_user.id, 'tamomlagan', message.text)
    await Create_len.next()

@dp.message_handler(state=Create_len.mutaxassisligi)
async def cmd_mutaxassis(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    #     data['mutaxassislik'] = message.text
    #     dict_data[message.from_user.id] = {}
    #     dict_data[message.from_user.id]['mutaxassislik'] = data['mutaxassislik']
    await message.reply(text='Qaysi tillarni biladi',
                        reply_markup=cancelkb())
    await update_user(message.from_user.id, 'mutaxassislik', message.text)
    await Create_len.next()

@dp.message_handler(state=Create_len.language)
async def cmd_language(message: types.Message, state=FSMContext):
    # async with state.proxy() as data:
    #     data['language'] = message.text
    #     dict_data[message.from_user.id] = {}
    #     dict_data[message.from_user.id]['language'] = data['language']
    await message.reply(text='Qanaqa mukofotlar olgan',
                        reply_markup=cancelkb())
    await update_user(message.from_user.id, 'language', message.text)
    await Create_len.next()

@dp.message_handler(state=Create_len.mukofot)
async def cmd_mikofot(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    #     data['mukofot'] = message.text
    #     dict_data[message.from_user.id] = {}
    #     dict_data[message.from_user.id]['mukofot'] = data['mukofot']
    await message.reply(text="Xalq  deputatlari, respublika, viloyat, shahar va tuman Kengashi deputatimi yoki boshqa\nsaylanadigan organlarning a’zosimi (to‘liq ko‘rsatilishi lozim)",
                        reply_markup=cancelkb())
    await update_user(message.from_user.id, 'mukofot', message.text)
    await Create_len.next()

@dp.message_handler(state=Create_len.saylov)
async def cmd_saylov(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    #     data['saylov'] = message.text
    #     dict_data[message.from_user.id] = {}
    #     dict_data[message.from_user.id]['saylov'] = data['saylov']
    await message.reply(text='Mehnat faoliyati haqida ma\'lumot bering',
                        reply_markup=cancelkb())
    await update_user(message.from_user.id, 'saylov', message.text)
    await Create_len.next()

@dp.message_handler(state=Create_len.mehnat_faoliyati)
async def cmd_work(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    #     data['mehnat_faoliyati'] = message.text
    #     dict_data[message.from_user.id] = {}
    #     dict_data[message.from_user.id]['mehnat_faoliyati'] = data['mehnat_faoliyati']
    await message.reply(text='Rasm uzating')
    await update_user(message.from_user.id, 'mehnat_faoliyati', message.text)
    await Create_len.next()


@dp.message_handler(lambda message: not message.photo, state=Create_len.photo)
async def chek_photo(message: types.Message):
    await message.reply('bu rasm  emas rasm uzating')


@dp.message_handler(state=Create_len.photo, content_types='photo')
async def cmd_work(message: types.Message, state: FSMContext):
    await message.photo[-1].download(f"{message.from_user.id}.jpg")

    await message.reply(text='Ota onasi qarindoshlari haqida ma\'lumotlar',
                        reply_markup=create_parents_keyboard())
    await Create_len.next()
    await message.reply(
        text='Oila a\'zolari kimlardan iborat Misol uchun otasi, onasi, akasi, opasi')
    await update_user(message.from_user.id, 'qarindoshlari', message.text)
    await Create_parents.count_par.set()
async def load_photo(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

    # await message.reply(text='Yaqin qarindoshlari \nMisol uchun(otasi, onasi, akasi, opasi,singlisi, farzandlari, xotini/eri)')
    await update_user(message.from_user.id, 'qarindoshlari', message.text)
# @dp.message_handler(state = Create_len.count_parents)
# async def count_parents(message: types.Message, state: FSMContext):
#     #shu yerda turini oladi.
    await Create_len.next()
    # await Create_parents.count_par.set()

@dp.message_handler(commands=['create_person'], state='*')
async def cmd_perents(message: types.Message, state=FSMContext):
    a = await check_user(message.from_user.id)+1
    await update_user(message.from_user.id, 'count_parent', int(a))
    # await create_parentbase(message.from_user.id)
    # async with state.proxy() as data:
    #     data[f'qarindoshlik_turi{a}'] = message.text
    #     dict_data[message.from_user.id] = {}
    #     dict_data[message.from_user.id][f'qarindoshlik_turi{a}'] = data[f'qarindoshlik_turi{a}']
    #     print(message.text)
    await message.answer(text='Qarindoshining turi (otasi, onasi, akasi, opasi, ...) ning ismi')
    await Create_parents.fio.set()
    print(a)

@dp.message_handler(state=Create_parents.count_par)
async def cmd_perents(message: types.Message, state=FSMContext):
    await update_user(message.from_user.id, 'qarindoshlari', message.text)
    nds = message.text
    parent_list = nds.split(',')
    print(len(parent_list))
    await create_parentbase(message.from_user.id)
    a = await check_user(message.from_user.id)
    for i in range(1,len(parent_list)+1):
        await insert_parentbase(message.from_user.id, parent_list[i-1])
    # await update_parent(message.from_user.id,'qarindoshligi', message.text)
    await message.answer(text=f"{parent_list[0]} haqida ma'lumotlarni yig'ish uchun /create_person tugmasini bosing")
    await Create_parents.next()

@dp.message_handler(state=Create_parents.qarindoshligi)
async def cmd_perents(message: types.Message, state=FSMContext):
    a = await check_user(message.from_user.id)
    nds = await select_user(message.from_user.id, 'qarindoshlari')
    parent_list = nds.split(',')
    # nds = await select_user(message.from_user.id, 'qarindoshlari')
    # parent_list = nds.split(',')
    await update_parent(message.from_user.id, 'qarindoshligi', parent_list[a-1],message.text)
    await message.answer(text='Familiya ism otasining ismi ')
    await Create_parents.next()

@dp.message_handler(state=Create_parents.fio)
async def cmdfio(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    #     data[f'pfio{a}'] = message.text
    #     dict_data[message.from_user.id] = {}
    #     dict_data[message.from_user.id][f'pfio{a}'] = data[f'pfio{a}']
    # nds = await select_user(message.from_user.id, 'qarindoshlari')
    # parent_list = nds.split(',')
    a = await check_user(message.from_user.id)
    nds = await select_user(message.from_user.id, 'qarindoshlari')
    parent_list = nds.split(',')
    await update_parent(message.from_user.id, 'fio', parent_list[a-1], message.text)
    await message.answer(text='Tug\'ilgan kuni va joyi ')
    await Create_parents.next()

@dp.message_handler(state=Create_parents.birthday)
async def cmdfio(message: types.Message, state: FSMContext):
    a = await check_user(message.from_user.id)
    # async with state.proxy() as data:
    #     data[f'pbirthday{a}'] = message.text
    #     dict_data[message.from_user.id] = {}
    #     dict_data[message.from_user.id][f'pbirthday{a}'] = data[f'pbirthday{a}']
    # nds = await select_user(message.from_user.id, 'qarindoshlari')
    # parent_list = nds.split(',')

    nds = await select_user(message.from_user.id, 'qarindoshlari')
    parent_list = nds.split(',')
    await update_parent(message.from_user.id, 'birthday',parent_list[a-1], message.text)
    await message.answer(text='Ishlash joyi va lavozimi')
    await Create_parents.next()

@dp.message_handler(state=Create_parents.work)
async def cmdfio(message: types.Message, state: FSMContext):
    a = await check_user(message.from_user.id)
    # async with state.proxy() as data:
    #     data[f'pwork{a}'] = message.text
    #     dict_data[message.from_user.id] = {}
    #     dict_data[message.from_user.id][f'pwork{a}'] = data[f'pwork{a}']
    # nds = await select_user(message.from_user.id, 'qarindoshlari')
    # parent_list = nds.split(',')
    nds = await select_user(message.from_user.id, 'qarindoshlari')
    parent_list = nds.split(',')
    await update_parent(message.from_user.id, 'work',parent_list[a-1], message.text)
    await message.answer(text='Turar joyi ')
    await Create_parents.next()

@dp.message_handler(state=Create_parents.location)
async def cmdfio(message: types.Message, state: FSMContext):
    a = await check_user(message.from_user.id)
    # async with state.proxy() as data:
    #     data[f'plocation{a}'] = message.text
    #     dict_data[message.from_user.id] = {}
    #     dict_data[message.from_user.id][f'plocation{a}'] = data[f'plocation{a}']
    # nds = await select_user(message.from_user.id, 'qarindoshlari')
    # parent_list = nds.split(',')

    nds = await select_user(message.from_user.id, 'qarindoshlari')
    parent_list = nds.split(',')
    await update_parent(message.from_user.id, 'location',parent_list[a-1], message.text)

    await message.answer(text=f"Qarindosh sifatida qo'shildi\nYana qarindosh qo'shish uchun <b>/create_person</b> tugmasini bosing",
                         reply_markup=create_parents_keyboard(),
                         parse_mode='html')

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)