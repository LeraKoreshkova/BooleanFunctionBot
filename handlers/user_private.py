import random

from aiogram import F, Router, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards import reply
import test


user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Здравствуй! Выбери задачу, которую хотел бы решить!", reply_markup=reply.start_kb)

@user_private_router.message(StateFilter('*'), or_f(Command('stop', 'close'), F.text.lower() == "stop", F.text.lower() == "close", F.text.lower() == "стоп", F.text.lower() ==  "отмена"))
async def stop_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Решение задачи прервано! Можете выбрать другую задачу!", reply_markup=reply.start_kb)




# Задача 1



class FirstTask(StatesGroup):
    n = State()


@user_private_router.message(StateFilter(None), or_f(Command('first_task'), F.text.lower() == "задача 1"))
async def task_first_cmd(message: types.Message, state: FSMContext):
    await message.answer("Введите число n, количество аргументов функции: ", reply_markup=ReplyKeyboardRemove())
    await state.set_state(FirstTask.n)


@user_private_router.message(FirstTask.n, F.text)
async def task_first_answer(message: types.Message, state: FSMContext):
    await state.update_data(n = message.text)
    data = await state.get_data()
    if test.is_argument(data['n']):
        if data['n'] != "1":
            await message.answer("Булева функция от " + message.text + " переменных: " + test.task1(int(data['n'])), reply_markup=reply.start_kb)
        else:
            await message.answer("Булева функция от " + message.text + " переменной: " + test.task1(int(data['n'])), reply_markup=reply.start_kb)
        await state.clear()
    else:
        await message.answer("Введите число больше нуля: ")



# Задача 2



class SecondTask(StatesGroup):
    vector = State()
    ostat = State()
    argument = State()


@user_private_router.message(StateFilter(None), or_f(Command('second_task'), F.text.lower() == "задача 2"))
async def task_second_cmd(message: types.Message, state: FSMContext):
    await message.answer("Введите вектор функции: ", reply_markup=ReplyKeyboardRemove())
    await state.set_state(SecondTask.vector)


@user_private_router.message(SecondTask.vector, F.text)
async def task_second_get_vector(message: types.Message, state: FSMContext):
    await state.update_data(vector = message.text)
    data = await state.get_data()
    if test.is_bin(data['vector']):
        if test.is_power_of_two_length(len(data['vector'])):
            await message.answer("Введите 0 или 1: ")
            await state.set_state(SecondTask.ostat)
        else:
            await message.answer(f"{data['vector']} не является вектором. \n\n"
                                 f"Введите корректные данные: ")
    else:
        await message.answer(f"{data['vector']} не является вектором. \n\n"
                             f"Введите корректные данные: ")


@user_private_router.message(SecondTask.ostat, F.text)
async def task_second_get_ostat(message: types.Message, state: FSMContext):
    await state.update_data(ostat = message.text)
    data = await state.get_data()
    if test.is_ostat(data['ostat']):
        await message.answer("Введите аргумент функции: ")
        await state.set_state(SecondTask.argument)
    else:
        await message.answer("Введите корректные данные(0 или 1): ")


@user_private_router.message(SecondTask.argument, F.text)
async def task_second(message: types.Message, state: FSMContext):
    await state.update_data(argument = message.text)
    data = await state.get_data()
    if test.is_argument(data['argument']):
        if int(data['argument']) <= test.power_of_two_length(len(data['vector'])):
            await message.answer(f"{data['ostat']} остаточная по {data['argument']} аргументу: {test.task2(data['vector'], int(data['ostat']), int(data['argument']))}", reply_markup=reply.start_kb)
            await state.clear()
        else:
            await message.answer(f"{data['argument']} больше количества допустимых аргументов вектора. \n\n"
                                 f"Введите корректные данные: ")
    else:
        await message.answer(f"{data['argument']} не число. \n\n"
                             f" Введите корректные данные: ")



# Задача 3



class ThirdTask(StatesGroup):
    argument = State()
    zero = State()
    one = State()
    length = None


@user_private_router.message(StateFilter(None), or_f(Command('third_task'), F.text.lower() == "задача 3"))
async def task_third_cmd(message: types.Message, state: FSMContext):
    await message.answer("Введите нулевую остаточную: ", reply_markup=ReplyKeyboardRemove())
    await state.set_state(ThirdTask.zero)


@user_private_router.message(ThirdTask.zero, F.text)
async def task_third_get_zero(message: types.Message, state:FSMContext):
    await state.update_data(zero = message.text)
    data = await state.get_data()
    if test.is_power_of_two_length(len(data['zero'])):
        if test.is_bin(data['zero']):
            await message.answer("Введите единичную остаточную: ")
            await state.set_state(ThirdTask.one)
        else:
            await message.answer(f"{data['zero']} не является остаточной функции. \n\n"
                                 f"Введите корректные данные: ")
    else:
        await message.answer(f"{data['zero']} не является остаточной функции. \n\n"
                                 f"Введите корректные данные: ")


@user_private_router.message(ThirdTask.one, F.text)
async def task_third_get_one(message: types.Message, state:FSMContext):
    await state.update_data(one = message.text)
    data = await state.get_data()
    if test.is_power_of_two_length(len(data['one'])):
        if test.is_bin(data['one']):
            if len(data['one']) == len(data['zero']):
                await message.answer("Введите номер аргумента: ")
                await state.set_state(ThirdTask.argument)
            else:
                await message.answer(f"Длины нулевой и единичной остаточных функций не совпадают. \n\n"
                                     f"Введите корректные данные: ")
        else:
            await message.answer(f"{data['one']} не является остаточной функции. \n\n"
                                 f"Введите корректные данные: ")
    else:
        await message.answer(f"{data['one']} не является остаточной функции. \n\n"
                                 f"Введите корректные данные: ")


@user_private_router.message(ThirdTask.argument, F.text)
async def task_third_get_argument(message: types.Message, state:FSMContext):
    await state.update_data(argument = message.text)
    data = await state.get_data()
    ThirdTask.length = test.power_of_two_length(len(data['zero'])) + 1
    # print(ThirdTask.length)
    if test.is_argument(data['argument']):
        if int(data['argument']) <= int(ThirdTask.length):
            await message.answer(f"Ваш вектор функции: {test.task3(int(data['argument']), data['zero'], data['one'])}", reply_markup=reply.start_kb)
            await state.clear()
        else:
            await message.answer(f"{data['argument']} больше количества допустимых аргументов вектора. \n\n"
                                 f"Введите корректные данные: ")
    else:
        await message.answer(f"{data['argument']} не число. \n\n"
                             f" Введите корректные данные: ")



# Задача 4



class FourthTask(StatesGroup):
    vec = None
    ans = State()


@user_private_router.message(StateFilter(None), or_f(Command('fourth_task'), F.text.lower() == "задача 4"))
async def task_fourth_cmd(message: types.Message, state: FSMContext):
    n = test.random_for_four_task()
    FourthTask.vec = test.function_list_for_four[n]
    await message.answer(f"Угадай имя функции для вектора: {FourthTask.vec}", reply_markup=reply.four_kb)
    await state.set_state(FourthTask.ans)


@user_private_router.message(FourthTask.ans, F.text)
async def task_fourth_get_ans(message: types.Message, state: FSMContext):
    await state.update_data(ans = message.text)
    data = await state.get_data()
    if FourthTask.vec == test.function_dict_for_four[f"{data['ans']}"]:
        await message.answer("Урррра!🥳 Вы угадали!", reply_markup=reply.start_kb)
        await state.clear()
    else:
        await message.answer("Увы 😢 \n"
                             "Попробуйте ещё раз!")



# Задача 5



class FifthTask(StatesGroup):
    vec = None
    n = None
    arg1 = State()
    arg2 = State()
    arg3 = State()


@user_private_router.message(StateFilter(None), or_f(Command('fifth_task'), F.text.lower() == "задача 5"))
async def task_fifth_cmd(message: types.Message, state: FSMContext):
    FifthTask.n = random.randint(1, 3)
    FifthTask.vec = test.task1(FifthTask.n)
    await message.answer(f"Вектор: {FifthTask.vec} \n\n"
                         f"Является ли x1 существенной переменной?", reply_markup=reply.five_kb)
    await state.set_state(FifthTask.arg1)


@user_private_router.message(FifthTask.arg1, F.text)
async def task_five_get_arg1(message: types.Message, state: FSMContext):
    await state.update_data(arg1 = message.text)
    data = await state.get_data()
    if FifthTask.n == 1:
        for i in range(1, FifthTask.n + 1):
            if data[f'arg{i}'] != test.task5(FifthTask.vec, i):
                await message.answer(f"Где-то вы дупустили ошибку, попробуйте ещё раз! \n\n"
                                     f"Вектор: {FifthTask.vec} \n"
                                     f"Является ли x1 существенной переменной?")
                await state.set_state(FifthTask.arg1)
                break
        else:
            await message.answer("Поздравляем, вы угадали! 🥳🎉", reply_markup=reply.start_kb)
            await state.clear()
    else:
        await message.answer(f"Вектор: {FifthTask.vec} \n\n"
                             f"Является ли x2 существенной переменной?", reply_markup=reply.five_kb)
        await state.set_state(FifthTask.arg2)


@user_private_router.message(FifthTask.arg2, F.text)
async def task_five_get_arg2(message: types.Message, state: FSMContext):
    await state.update_data(arg2 = message.text)
    data = await state.get_data()
    if FifthTask.n == 2:
        for i in range(1, FifthTask.n + 1):
            if data[f'arg{i}'] != test.task5(FifthTask.vec, i):
                await message.answer(f"Где-то вы дупустили ошибку, попробуйте ещё раз! \n\n"
                                     f"Вектор: {FifthTask.vec} \n"
                                     f"Является ли x1 существенной переменной?")
                await state.set_state(FifthTask.arg1)
                break
        else:
            await message.answer("Поздравляем, вы угадали! 🥳🎉", reply_markup=reply.start_kb)
            await state.clear()
    else:
        await message.answer(f"Вектор: {FifthTask.vec} \n\n"
                             f"Является ли x3 существенной переменной?", reply_markup=reply.five_kb)
        await state.set_state(FifthTask.arg3)


@user_private_router.message(FifthTask.arg3, F.text)
async def task_five_get_arg3(message: types.Message, state: FSMContext):
    await state.update_data(arg3 = message.text)
    data = await state.get_data()
    if FifthTask.n == 3:
        for i in range(1, FifthTask.n + 1):
            if data[f'arg{i}'] != test.task5(FifthTask.vec, i):
                await message.answer(f"Где-то вы дупустили ошибку, попробуйте ещё раз! \n\n"
                                     f"Вектор: {FifthTask.vec} \n"
                                     f"Является ли x1 существенной переменной?")
                await state.set_state(FifthTask.arg1)
                break
        else:
            await message.answer("Поздравляем, вы угадали! 🥳🎉", reply_markup=reply.start_kb)
            await state.clear()



# Задача 6



class SixthTask(StatesGroup):
    n = None
    vec = None
    dnf = State()


@user_private_router.message(StateFilter(None), or_f(Command('sixth_task'), F.text.lower() == "задача 6"))
async def task_sixth_cmd(message: types.Message, state: FSMContext):
    SixthTask.n = random.randint(1, 3)
    SixthTask.vec = test.task1(SixthTask.n)

    if test.task12(SixthTask.vec) == False:
        SixthTask.vec = test.task1(SixthTask.n)

    await message.answer(f"Введите ДНФ для вектора {SixthTask.vec}:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(SixthTask.dnf)


@user_private_router.message(SixthTask.dnf, F.text)
async def task_sixth_get_dnf(message: types.Message, state: FSMContext):
    await state.update_data(dnf = message.text)
    data = await state.get_data()

    if test.task6(data['dnf'], test.task12(SixthTask.vec)):
        await message.answer("Поздравляем, вы правильно ввели днф!🥳", reply_markup=reply.start_kb)
        await state.clear()
    else:
        await message.answer("Увы, неправильно, в следующий раз обязательно получится!😢", reply_markup=reply.start_kb)
        await state.clear()



# Задача 7



@user_private_router.message(StateFilter(None), or_f(Command('seventh_task'), F.text.lower() == "задача 7"))
async def task_seventh_cmd(message: types.Message, state: FSMContext):
    await message.answer("Технические неполадки!")



# Задача 8



class EighthTask(StatesGroup):
    vector = State()


@user_private_router.message(StateFilter(None), or_f(Command('eighth_task'), F.text.lower() == "задача 8"))
async def task_eighth_cmd(message: types.Message, state:FSMContext):
    await message.answer("Введите вектор функции: ", reply_markup=ReplyKeyboardRemove())
    await state.set_state(EighthTask.vector)


@user_private_router.message(EighthTask.vector, F.text)
async def task_eighth_get_vec(message: types.Message, state: FSMContext):
    await state.update_data(vector = message.text)
    data = await state.get_data()
    if test.is_bin(data['vector']):
        if test.is_power_of_two_length(len(data['vector'])):
            if test.get_SDNF(data['vector']) != False:
                await message.answer(f"СДНФ для вектора {data['vector']}: {test.get_SDNF(data['vector'])} \n\n"
                                     f"{test.tabl_istin_sdnf(data['vector'])}", reply_markup=reply.start_kb)
                await state.clear()
            else:
                await message.answer(f"СДНФ для вектора {data['vector']} не существует!", reply_markup=reply.start_kb)
        else:
            await message.answer(f"{data['vector']} не является вектором. \n\n"
                                 f"Введите корректные данные: ")
    else:
        await message.answer(f"{data['vector']} не является вектором. \n\n"
                             f"Введите корректные данные: ")



# Задание 9



class NinthTask(StatesGroup):
    vector = State()


@user_private_router.message(StateFilter(None), or_f(Command('ninth_task'), F.text.lower() == "задача 9"))
async def task_ninth_cmd(message: types.Message, state:FSMContext):
    await message.answer("Введите вектор функции: ", reply_markup=ReplyKeyboardRemove())
    await state.set_state(NinthTask.vector)


@user_private_router.message(NinthTask.vector, F.text)
async def task_ninth_get_vec(message: types.Message, state: FSMContext):
    await state.update_data(vector = message.text)
    data = await state.get_data()
    if test.is_bin(data['vector']):
        if test.is_power_of_two_length(len(data['vector'])):
            if test.get_SKNF(data['vector']) != False:
                await message.answer(f"СКНФ для вектора {data['vector']}: {test.get_SKNF(data['vector'])} \n\n"
                                     f"{test.tabl_istin_sknf(data['vector'])}", reply_markup=reply.start_kb)
                await state.clear()
            else:
                await message.answer(f"СКНФ для вектора {data['vector']} не существует!", reply_markup=reply.start_kb)
        else:
            await message.answer(f"{data['vector']} не является вектором. \n\n"
                                 f"Введите корректные данные: ")
    else:
        await message.answer(f"{data['vector']} не является вектором. \n\n"
                             f"Введите корректные данные: ")



# Задание 10



class TenthTask(StatesGroup):
    arr_classes = []
    n = None
    vec = None
    T0 = State()
    T1 = State()
    S = State()
    M = State()
    L = State()


@user_private_router.message(StateFilter(None), or_f(Command('tenth_task'), F.text.lower() == "задача 10"))
async def task_tenth_cmd(message: types.Message, state: FSMContext):
    TenthTask.n = random.randint(1, 3)
    TenthTask.vec = test.task1(TenthTask.n)
    await message.answer(f"Принадлежит ли вектор {TenthTask.vec} классу функций, сохраняющих нуль?",
                         reply_markup=reply.ten_kb)
    await state.set_state(TenthTask.T0)
    TenthTask.arr_classes.clear()


@user_private_router.message(TenthTask.T0, F.text)
async def task_tenth_get_t0(message: types.Message, state: FSMContext):
    await state.update_data(T0 = message.text)
    data = await state.get_data()
    TenthTask.arr_classes.clear()
    if (data['T0'] == "Принадлежит" and test.is_T0(TenthTask.vec)) or\
            (data['T0'] == "Не принадлежит" and not test.is_T0(TenthTask.vec)):
        TenthTask.arr_classes.append(1)
    else:
        TenthTask.arr_classes.append(0)


    await message.answer(f"Принадлежит ли вектор {TenthTask.vec} классу функций, сохраняющих единицу?",
                         reply_markup=reply.ten_kb)
    await state.set_state(TenthTask.T1)


@user_private_router.message(TenthTask.T1, F.text)
async def task_tenth_get_t1(message: types.Message, state: FSMContext):
    await state.update_data(T1 = message.text)
    data = await state.get_data()
    if (data['T1'] == "Принадлежит" and test.is_T1(TenthTask.vec)) or\
            (data['T1'] == "Не принадлежит" and not test.is_T1(TenthTask.vec)):
        TenthTask.arr_classes.append(1)
    else:
        TenthTask.arr_classes.append(0)


    await message.answer(f"Принадлежит ли вектор {TenthTask.vec} классу самодвойственных функций?",
                         reply_markup=reply.ten_kb)
    await state.set_state(TenthTask.S)


@user_private_router.message(TenthTask.S, F.text)
async def task_tenth_get_s(message: types.Message, state: FSMContext):
    await state.update_data(S = message.text)
    data = await state.get_data()
    if (data['S'] == "Принадлежит" and test.is_S(TenthTask.vec)) or\
            (data['S'] == "Не принадлежит" and not test.is_S(TenthTask.vec)):
        TenthTask.arr_classes.append(1)
    else:
        TenthTask.arr_classes.append(0)


    await message.answer(f"Принадлежит ли вектор {TenthTask.vec} классу монотонных функций?",
                         reply_markup=reply.ten_kb)
    await state.set_state(TenthTask.M)


@user_private_router.message(TenthTask.M, F.text)
async def task_tenth_get_m(message: types.Message, state: FSMContext):
    await state.update_data(M = message.text)
    data = await state.get_data()
    if (data['M'] == "Принадлежит" and test.is_M(TenthTask.vec)) or\
            (data['M'] == "Не принадлежит" and not test.is_M(TenthTask.vec)):
        TenthTask.arr_classes.append(1)
    else:
        TenthTask.arr_classes.append(0)


    await message.answer(f"Принадлежит ли вектор {TenthTask.vec} классу линейных функций?",
                         reply_markup=reply.ten_kb)
    await state.set_state(TenthTask.L)


@user_private_router.message(TenthTask.L, F.text)
async def task_tenth_get_l(message: types.Message, state: FSMContext):
    await state.update_data(L = message.text)
    data = await state.get_data()
    if (data['L'] == "Принадлежит" and test.is_L(TenthTask.vec)) or\
            (data['L'] == "Не принадлежит" and not test.is_L(TenthTask.vec)):
        TenthTask.arr_classes.append(1)
    else:
        TenthTask.arr_classes.append(0)

    print(TenthTask.arr_classes)
    if 0 in TenthTask.arr_classes:
        await message.answer(f"Где-то вы дупустили ошибку, попробуйте ещё раз! \n\n"
                             f"Принадлежит ли вектор {TenthTask.vec} классу функций, сохраняющих нуль?")
        await state.set_state(TenthTask.T0)
    else:
        await message.answer("Поздравляем, вы угадали! 🥳🎉", reply_markup=reply.start_kb)
        await state.clear()



# Задача 11



class EleventhTask(StatesGroup):
    n = None
    vec1 = None
    vec2 = None
    vec3 = None
    arr_vec = []
    full = State()
    ans = State()



@user_private_router.message(StateFilter(None), or_f(Command('eleventh_task'), F.text.lower() == "задача 11"))
async def task_eleventh_cmd(message: types.Message, state: FSMContext):
    EleventhTask.n = random.randint(1, 3)
    EleventhTask.vec1 = test.task1(EleventhTask.n)
    EleventhTask.vec2 = test.task1(EleventhTask.n)
    EleventhTask.vec3 = test.task1(EleventhTask.n)

    EleventhTask.arr_vec.clear()

    EleventhTask.arr_vec.append(EleventhTask.vec1)
    EleventhTask.arr_vec.append(EleventhTask.vec2)
    EleventhTask.arr_vec.append(EleventhTask.vec3)

    print(EleventhTask.arr_vec)

    await message.answer(f"Является ли набор функций полным? \n"
                         f"{EleventhTask.vec1}\n"
                         f"{EleventhTask.vec2}\n"
                         f"{EleventhTask.vec3}\n", reply_markup=reply.eleven_full_kb)
    await state.set_state(EleventhTask.full)


@user_private_router.message(EleventhTask.full, F.text)
async def task_eleventh_get_full(message: types.Message, state: FSMContext):
    await state.update_data(full = message.text)
    data = await state.get_data()

    print(test.is_full(EleventhTask.arr_vec))

    if (data['full'] == "Полный" and not 1 in test.is_full(EleventhTask.arr_vec)):
        await message.answer("Поздравляем, вы угадали! 🥳🎉", reply_markup=reply.start_kb)
        await state.clear()

    elif (data['full'] == "Неполный" and not 1 in test.is_full(EleventhTask.arr_vec)) or (data['full'] == "Полный" and 1 in test.is_full(EleventhTask.arr_vec)):
        await message.answer("Вы не угадали! 😢\n"
                             "Но не расстраивайтесь в следующий раз обязательно получится!!!", reply_markup=reply.start_kb)
        await state.clear()

    else:
        await message.answer("Укажите каким замкнутым классам(T0, T1, S, M, L) принадлежит данный набор функций, через пробел и без запятых: ", reply_markup=ReplyKeyboardRemove())
        await state.set_state(EleventhTask.ans)


@user_private_router.message(EleventhTask.ans, F.text)
async def task_eleventh_get_ans(message: types.Message, state: FSMContext):
    await state.update_data(ans = message.text)
    data = await state.get_data()

    print(set(data['ans'].split()))
    print(set(test.task11(test.is_full(EleventhTask.arr_vec))))

    if (set(data['ans'].split()) == set(test.task11(test.is_full(EleventhTask.arr_vec)))):
        await message.answer("Поздравляем, вы угадали! 🥳🎉", reply_markup=reply.start_kb)
        await state.clear()
    else:
        await message.answer("Вы не угадали! 😢\n"
                             "Попробуйте ещё раз: ",
                             reply_markup=ReplyKeyboardRemove())



# Задача 12



class TwelfthTask():
    n = None
    vec = None


@user_private_router.message(StateFilter(None), or_f(Command('twelfth_task'), F.text.lower() == "задача 12"))
async def task_twelfth_cmd(message: types.Message, state: FSMContext):
    TwelfthTask.n = random.randint(1, 3)
    TwelfthTask.vec = test.task1(TwelfthTask.n)
    a = test.task12(TwelfthTask.vec)
    if a == False:
        TwelfthTask.vec = test.task1(TwelfthTask.n)
    else:
        await message.answer(f"ДНФ для вектора {TwelfthTask.vec}: {a}", reply_markup=reply.start_kb)
    # print(test.task12(TwelfthTask.vec))
