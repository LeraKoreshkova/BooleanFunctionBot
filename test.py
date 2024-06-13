import random
import math
from typing import List


def is_argument(str):
    if str.isdigit() and str != '0':
        return True
    return False


def is_bin(str):
    try:
        if int(str, 2) or int(str, 2) == 0:
            return True
    except ValueError as e:
        return False


def is_ostat(str):
    if str == "0" or str == "1":
        return True
    return False


def is_power_of_two_length(length):
    power = 0
    while 2**power <= length:
        if 2**power == length:
            return True
        power += 1
    return None


def power_of_two_length(length):
    power = 0
    while 2**power <= length:
        if 2**power == length:
            return power
        power += 1


# def as_vec_bool(vec):
#     v = list()
#     for i in range(len(vec)):
#         if vec[i] == "1":
#             v.append(i)
#     return v
#
# a = as_vec_bool("11001011")
# print(5//2)

def is_T0(vec):
    return vec[0] == "0"


def is_T1(vec):
    return vec[-1] == "1"


def is_S(vec):
    for i in range(len(vec)//2):
        if vec[i] == vec[len(vec) - 1 - i]:
            return False

    return True


def is_M(vec):
    is_monot = True
    n = len(vec)
    for i in range(n):
        for j in range(i + 1, n):
            is_mon = True
            for k in range(n):
                if ((i >> k) & 1) > ((j >> k) & 1):
                    is_mon = False
                    break
            if is_mon:
                if vec[i] > vec[j]:
                    is_monot = False
    return is_monot
# print(3 & 2 == 0)

# print("1".lower() in ["1", "2", "3"])

def is_L(vec):
    arr_linear = []
    n = len(vec)

    for i in range(n):
        arr_linear.append([])
        for j in range(n - i):
            if i == 0:
                arr_linear[i].append(int(vec[j]))
            else:
                arr_linear[i].append(int(arr_linear[i - 1][j] != arr_linear[i - 1][j + 1]))

    for i in range(n):
        if arr_linear[i][0] == 1 and not ((i & (i - 1)) == 0):
            return False
    return True
# print(is_L("1110"))

def is_full(arr: list):
    n = len(arr)
    arr_classes = []

    for i in arr:
        if (not is_T0(i)):
            arr_classes.append(0)
            break
    else:
        arr_classes.append(1)

    for i in arr:
        if (not is_T1(i)):
            arr_classes.append(0)
            break
    else:
        arr_classes.append(1)

    for i in arr:
        if (not is_S(i)):
            arr_classes.append(0)
            break
    else:
        arr_classes.append(1)

    for i in arr:
        if (not is_M(i)):
            arr_classes.append(0)
            break
    else:
        arr_classes.append(1)

    for i in arr:
        if (not is_L(i)):
            arr_classes.append(0)
            break
    else:
        arr_classes.append(1)

    return arr_classes


def task11(arr):
    ans = []
    if arr[0] == 1:
        ans.append("T0")

    if arr[1] == 1:
        ans.append("T1")

    if arr[2] == 1:
        ans.append("S")

    if arr[3] == 1:
        ans.append("M")

    if arr[4] == 1:
        ans.append("L")

    return ans


def task1(n):
    n = int(n)
    m = 1 << n
    f = list()
    s = ""
    for i in range(m):
        f.append(int((random.random() * 100) % 2))
        s += str(f[i])
    return s


def task2(f, o, k):
    k = int(math.log(len(f), 2) + 1 - k)
    s = ""
    for i in range(len(f)):
        if (i % (1 << k) // (1 << (k - 1))) == o:
            s += f[i]
    return s


def task3(argument, zero, one):
    vector = ""

    k = int(math.log(len(zero) * 2, 2) + 1 - argument)

    count = 0

    for i in range(len(zero) * 2):
        if (i % (1 << k) // (1 << (k - 1))) == 0:
            vector += zero[i - count]
            zero = zero.replace(zero[i - count], "", 1)
            count += 1

        else:
            vector += one[i - count]
            one = one.replace(one[i - count], "", 1)
            count += 1

    return vector


def random_for_four_task():
    return int(random.random() * 1000) % 16

function_list_for_four = (
    '0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111',
    '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111'
)

function_dict_for_four = {
        "конъюнкция": "0001",
        "дизъюнкция": "0111",
        "сложение по mod 2": "0110",
        "штрих Шеффера": "1110",
        "стрелка Пирса": "1000",
        "импликация": "1101",
        "эквивалентность": "1001",
        "коимпликация": "0010",
        "обратная импликация": "1011",
        "обратная коимпликация": "0100",
        "константа 0": "0000",
        "функция равна второму аргументу": "0101",
        "функция равна первому аргументу": "0011",
        "отрицание второго аргумента": "1010",
        "отрицание первого аргумента": "1100",
        "константа 1": "1111"
    }


def task5(vec, argument):
    if task2(vec, 0, argument) == task2(vec, 1, argument):
        return "Фиктивная"
    return "Существенная"


def get_SDNF(input_vector):
    n = power_of_two_length(len(input_vector))
    sdnf = []
    if not input_vector or '1' not in input_vector:
        return False  # Формула для случая, когда вектор функции состоит только из 0

    for i, char in enumerate(input_vector):
        if char == '1':
            term = ''.join(
                ['¬' + 'x' + str(j + 1) if i & (1 << (n - 1 - j)) == 0 else 'x' + str(j + 1) for j in range(n)])
            sdnf.append(term)
    sdnf_str = " ∨ ".join(sdnf)
    return sdnf_str


def tabl_istin_sdnf(input_vector: str):
    ans = "Таблица истинности: \n\n"
    n = power_of_two_length(len(input_vector))

    for i in range(2 ** n):
        binary_rep = format(i, f"0{n}b")
        char = input_vector[i]
        term = ''.join(['¬' + 'x' + str(j + 1) if binary_rep[j] == '0' else 'x' + str(j + 1) for j in range(n)])
        ans += (f"{char} = {binary_rep} ({term}) \n")

    return ans


def get_SKNF(input_vector):
    n = power_of_two_length(len(input_vector))
    sknf = []
    if not input_vector or '0' not in input_vector:
        return False  # Формула для случая, когда вектор функции состоит только из 1
    for i, char in enumerate(input_vector):
        if char == '0':
            term = ''.join(['x' + str(j + 1) if i & (1 << (n - 1 - j)) == 0 else '¬x' + str(j + 1) for j in range(n)])
            sknf.append(term)
    sknf_str = " ∧ ".join(sknf)
    return sknf_str


def tabl_istin_sknf(input_vector: str):
    ans = "Таблица истинности: \n\n"
    n = power_of_two_length(len(input_vector))

    for i in range(2 ** n):
        binary_rep = format(i, f"0{n}b")
        char = input_vector[i]
        term = '∨'.join(['¬x' + str(j + 1) if binary_rep[j] == '1' else 'x' + str(j + 1) for j in range(n)])
        ans += (f"{char} = {binary_rep} ({term}) \n")

    return ans


# Задача 12 Метод Куайна — Мак-Класки


def comparing(str1, str2):
    bool_list = []
    q = 0
    ans = ""
    for i in range(len(str1)):
        bool_list.append(str1[i] == str2[i])
        if not str1[i] == str2[i]:
            q = i
    if bool_list.count(False) == 1:
        ans = str1[0:q] + "*" + str1[q + 1:]

    return ans


def change_to(truth_table):
    table = []

    for i in range(len(truth_table)):
        table.append(truth_table[i])

    table_delete = []
    for i in range(len(truth_table)):
        for j in range(i, len(truth_table)):
            result = comparing(truth_table[i], truth_table[j])
            if result != "":
                if truth_table[i] not in table_delete:
                    table_delete.append(truth_table[i])
                if truth_table[j] not in table_delete:
                    table_delete.append(truth_table[j])
                table.append(result)

    for i in range(len(table_delete)):
        if table_delete[i] in table:
            table.remove(table_delete[i])


    return table


def prime_table_truth(truth_table):
    table1 = truth_table
    table2 = change_to(truth_table)


    if table1 == table2:
        return table1

    else:
        table1, table2 = table2, []
        return prime_table_truth(table1)


def get_mdnf(tab):
    ans = ""
    a = set(tab)
    table = []

    for i in range(len(a)):
        table.append(a.pop())

    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] == "0":
                ans += f"¬x{j + 1}"
            elif table[i][j] == "1":
                ans += f"x{j + 1}"
        ans += " ∨ "
    ans = ans[:-3]

    if ans == "":
        ans = 1

    return ans


# vector = "10000000"
def task12(vec):
    if not vec or '1' not in vec:
        return False  # Формула для случая, когда вектор функции состоит только из 0

    count_args = power_of_two_length(len(vec))
    truth_table = []

    for i in range(len(vec)):
        if vec[i] == "1":
            index = bin(i)[2:].zfill(count_args)
            truth_table.append(index)

    return get_mdnf(prime_table_truth(truth_table))

# print(task12("11001101"))


def task6(user_str, right_str):
    user = user_str.split('∨')

    for i in range(len(user)):
        user[i] = user[i].replace(' ', '')

    right = right_str.split('∨')

    for i in range(len(right)):
        right[i] = right[i].replace(' ', '')

    return set(user) == set(right)

# print(task6("¬x2 ∨ x1x3", "¬x2 ∨ x1x3 ∨ x1x2"))