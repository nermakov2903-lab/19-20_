import asyncio #асинхронный цикл для Telegram-бота
import random
from aiogram import Bot, Dispatcher, F #маршрутизатор событий, фильтры входных сообщений
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton #кнопки
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup #автоматы

from task3 import rotate_matrix_algo, generate_random_matrix
from task4 import big_number_operation
from task8 import count_common_with_reverse
from messages import MESSAGES

TOKEN = "8473375695:AAGpInHH6Ctsp79GkpUu_vm3bfJ41uLhj-Q"

# ==================================================
# FSM STATES
# ==================================================

class MainFSM(StatesGroup):
    menu = State()


class Task3FSM(StatesGroup):
    menu = State() #выбор действия
    input_matrix = State()
    input_direction = State()


class Task4FSM(StatesGroup):
    menu = State()
    input_arrays = State()
    input_op = State()


class Task8FSM(StatesGroup):
    menu = State()
    input_arrays = State()


# ==================================================
# KEYBOARDS
# ==================================================

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Задание 3")],
        [KeyboardButton(text="Задание 4")],
        [KeyboardButton(text="Задание 8")],
    ],
    resize_keyboard=True
)

task3_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ввести матрицу вручную")],
        [KeyboardButton(text="Сгенерировать случайную матрицу")],
        [KeyboardButton(text="Выполнить поворот")],
        [KeyboardButton(text="Показать результат")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True
)

task4_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ввести массивы вручную")],
        [KeyboardButton(text="Сгенерировать массивы случайно")],
        [KeyboardButton(text="Выполнить операцию")],
        [KeyboardButton(text="Показать результат")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True
)

task8_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ввести массивы вручную")],
        [KeyboardButton(text="Сгенерировать массивы случайно")],
        [KeyboardButton(text="Выполнить алгоритм")],
        [KeyboardButton(text="Показать результат")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True
)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ==================================================
# START / MAIN MENU
# ==================================================

#Пользователь отправляет /start
#Бот показывает главное меню
#Устанавливается состояние MainFSM.menu

@dp.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    await message.answer("Выберите задание:", reply_markup=main_kb)
    await state.set_state(MainFSM.menu)


@dp.message(MainFSM.menu, F.text == "Задание 3")
async def task3_start(message: Message, state: FSMContext):
    await message.answer(MESSAGES["task3"]["title"], reply_markup=task3_kb)
    await state.set_state(Task3FSM.menu)


@dp.message(MainFSM.menu, F.text == "Задание 4")
async def task4_start(message: Message, state: FSMContext):
    await message.answer(MESSAGES["task4"]["title"], reply_markup=task4_kb)
    await state.set_state(Task4FSM.menu)


@dp.message(MainFSM.menu, F.text == "Задание 8")
async def task8_start(message: Message, state: FSMContext):
    await message.answer(MESSAGES["task8"]["title"], reply_markup=task8_kb)
    await state.set_state(Task8FSM.menu)

# ==================================================
# TASK 3 (логика = task3.py)
# ==================================================

def format_matrix(matrix):
    return "\n".join(" ".join(map(str, row)) for row in matrix)

@dp.message(Task3FSM.menu, F.text == "Ввести матрицу вручную")
async def task3_input(message: Message, state: FSMContext): #асинхронная функция
    await message.answer("Введите матрицу построчно, строки через ;") #await = «подожди, пока операция завершится»
    await state.set_state(Task3FSM.input_matrix) #Установить текущее состояние автомата


@dp.message(Task3FSM.input_matrix)
async def task3_save_matrix(message: Message, state: FSMContext):
    try:
        rows = message.text.split(";")
        matrix = [list(map(int, r.split())) for r in rows]

        await state.update_data(matrix=matrix, result=None)

        text = "Исходная матрица:\n" + format_matrix(matrix)
        await message.answer(text, reply_markup=task3_kb)

        await state.set_state(Task3FSM.menu)
    except:
        await message.answer(MESSAGES["task3"]["input_error"])


@dp.message(Task3FSM.menu, F.text == "Сгенерировать случайную матрицу")
async def task3_generate(message: Message, state: FSMContext):
    matrix = generate_random_matrix(3, 3)
    await state.update_data(matrix=matrix, result=None) # Хранение данных между шагами.
    text = "Сгенерированная матрица:\n" + format_matrix(matrix)
    await message.answer(text, reply_markup=task3_kb)


@dp.message(Task3FSM.menu, F.text == "Выполнить поворот")
async def task3_rotate(message: Message, state: FSMContext):
    data = await state.get_data()
    if "matrix" not in data:
        await message.answer(MESSAGES["task3"]["no_matrix"])
        return
    await message.answer("Введите направление (clockwise / counterclockwise):")
    await state.set_state(Task3FSM.input_direction)


@dp.message(Task3FSM.input_direction)
async def task3_do_rotate(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        result = rotate_matrix_algo(data["matrix"], message.text)
        await state.update_data(result=result)
        await message.answer(MESSAGES["task3"]["rotation_done"], reply_markup=task3_kb)
        await state.set_state(Task3FSM.menu)
    except:
        await message.answer(MESSAGES["task3"]["input_error"])


@dp.message(Task3FSM.menu, F.text == "Показать результат")
async def task3_show(message: Message, state: FSMContext):
    data = await state.get_data()
    if "result" in data and data["result"] is not None:
        text = "Результат:\n" + "\n".join(map(str, data["result"]))
        await message.answer(text)
    else:
        await message.answer(MESSAGES["task3"]["no_result"])


@dp.message(Task3FSM.menu, F.text == "Назад")
async def task3_back(message: Message, state: FSMContext):
    await message.answer("Главное меню", reply_markup=main_kb)
    await state.set_state(MainFSM.menu)

# ==================================================
# TASK 4 (логика = task4.py)
# ==================================================

@dp.message(Task4FSM.menu, F.text == "Ввести массивы вручную")
async def task4_input(message: Message, state: FSMContext):
    await message.answer("Введите два массива через ;")
    await state.set_state(Task4FSM.input_arrays)


@dp.message(Task4FSM.input_arrays)
async def task4_save(message: Message, state: FSMContext):
    try:
        a, b = message.text.split(";")
        a = list(map(int, a.split()))
        b = list(map(int, b.split()))
        await state.update_data(a=a, b=b, result=None)
        await message.answer("Массивы сохранены", reply_markup=task4_kb)
        await state.set_state(Task4FSM.menu)
    except:
        await message.answer(MESSAGES["task4"]["input_error"])


@dp.message(Task4FSM.menu, F.text == "Сгенерировать массивы случайно")
async def task4_generate(message: Message, state: FSMContext):
    a = [random.randint(0, 9) for _ in range(5)]
    b = [random.randint(0, 9) for _ in range(5)]
    await state.update_data(a=a, b=b, result=None)
    await message.answer(f"A={a}\nB={b}", reply_markup=task4_kb)


@dp.message(Task4FSM.menu, F.text == "Выполнить операцию")
async def task4_op(message: Message, state: FSMContext):
    await message.answer("Введите операцию (add / sub):")
    await state.set_state(Task4FSM.input_op)


@dp.message(Task4FSM.input_op)
async def task4_do_op(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        result = big_number_operation(data["a"], data["b"], message.text)
        await state.update_data(result=result)
        await message.answer(MESSAGES["task4"]["operation_done"], reply_markup=task4_kb)
        await state.set_state(Task4FSM.menu)
    except:
        await message.answer(MESSAGES["task4"]["input_error"])


@dp.message(Task4FSM.menu, F.text == "Показать результат")
async def task4_show(message: Message, state: FSMContext):
    data = await state.get_data()
    if "result" in data:
        await message.answer(f"Результат: {data['result']}")
    else:
        await message.answer(MESSAGES["task4"]["no_result"])


@dp.message(Task4FSM.menu, F.text == "Назад")
async def task4_back(message: Message, state: FSMContext):
    await message.answer("Главное меню", reply_markup=main_kb)
    await state.set_state(MainFSM.menu)

# ==================================================
# TASK 8 (логика = task8.py)
# ==================================================

@dp.message(Task8FSM.menu, F.text == "Ввести массивы вручную")
async def task8_input(message: Message, state: FSMContext):
    await message.answer("Введите два массива через ;")
    await state.set_state(Task8FSM.input_arrays)


@dp.message(Task8FSM.input_arrays)
async def task8_save(message: Message, state: FSMContext):
    try:
        a, b = message.text.split(";")
        a = list(map(int, a.split()))
        b = list(map(int, b.split()))
        await state.update_data(a=a, b=b, result=None)
        await message.answer("Массивы сохранены", reply_markup=task8_kb)
        await state.set_state(Task8FSM.menu)
    except:
        await message.answer(MESSAGES["task8"]["input_error"])


@dp.message(Task8FSM.menu, F.text == "Сгенерировать массивы случайно")
async def task8_generate(message: Message, state: FSMContext):
    a = [random.randint(-99, 99) for _ in range(5)]
    b = [random.randint(-99, 99) for _ in range(5)]
    await state.update_data(a=a, b=b, result=None)
    await message.answer(f"A={a}\nB={b}", reply_markup=task8_kb)


@dp.message(Task8FSM.menu, F.text == "Выполнить алгоритм")
async def task8_run(message: Message, state: FSMContext):
    data = await state.get_data()
    if "a" not in data:
        await message.answer(MESSAGES["task8"]["no_data"])
        return
    result = count_common_with_reverse(data["a"], data["b"])
    await state.update_data(result=result)
    await message.answer(MESSAGES["task8"]["algorithm_done"])


@dp.message(Task8FSM.menu, F.text == "Показать результат")
async def task8_show(message: Message, state: FSMContext):
    data = await state.get_data()
    if "result" in data:
        await message.answer(f"Результат: {data['result']}")
    else:
        await message.answer(MESSAGES["task8"]["no_result"])


@dp.message(Task8FSM.menu, F.text == "Назад")
async def task8_back(message: Message, state: FSMContext):
    await message.answer("Главное меню", reply_markup=main_kb)
    await state.set_state(MainFSM.menu)

# ==================================================
# RUN
# ==================================================

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
