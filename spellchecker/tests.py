#-*- coding: utf-8 -*-
import re
# from itertools import product
from pprint import pprint
from pymystem3 import Mystem
import subprocess
import time
import enchant


def ed_1(word, score, table):
    '''
    итерация ed += 1
    '''
    # table = {'к': {'к': 1, 'г': 3},
    #          'b': {'4': 4, '2': 2}}
    # table = {'г': {'г': 0, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'б': {'г': 1, 'б': 0, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'щ': {'г': 1, 'б': 1, 'щ': 0, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'п': {'г': 1, 'б': 1, 'щ': 1, 'п': 0, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'т': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 0, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'ч': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 0, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'я': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 0, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'ы': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 0, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'ц': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 0, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'х': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 0, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'ъ': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 0, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'д': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 0, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'ф': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 0, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'к': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 0, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'и': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 0, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'ё': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 0, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'с': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 0, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'з': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 0, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'э': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 0, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'р': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 0, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'ж': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 0, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'ь': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 0, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'а': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 0, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'й': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 0, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'в': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 0, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'о': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 0, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'ш': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 0, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'м': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 0, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'н': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 0, 'е': 1, 'л': 1, 'у': 1, 'ю': 1}, 'е': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 0, 'л': 1, 'у': 1, 'ю': 1}, 'л': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 0, 'у': 1, 'ю': 1}, 'у': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 0, 'ю': 1}, 'ю': {'г': 1, 'б': 1, 'щ': 1, 'п': 1, 'т': 1, 'ч': 1, 'я': 1, 'ы': 1, 'ц': 1, 'х': 1, 'ъ': 1, 'д': 1, 'ф': 1, 'к': 1, 'и': 1, 'ё': 1, 'с': 1, 'з': 1, 'э': 1, 'р': 1, 'ж': 1, 'ь': 1, 'а': 1, 'й': 1, 'в': 1, 'о': 1, 'ш': 1, 'м': 1, 'н': 1, 'е': 1, 'л': 1, 'у': 1, 'ю': 0}}
    cands = {}
    # print('word', word)
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    # transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    # inserts?
    # print('transposes:', transposes)
    for begin, end in splits:
        if end:
            # какой-то фильтр
            if end[0] in table:
                for replacer in table[end[0]]:
                    offer = str(begin + replacer + end[1:])
                    cost = table[end[0]][replacer]
                    # print('candidate', offer)
                    cands[offer] = score + cost
                    # print('=', cands[offer])
                    # print('cands', cands)

    return cands
# print(ed_1("кот", 0))

    # for to_char, from_char in repl:
    #     options = [(c,) if c != from_char else (from_char, to_char) for c in word]
        # print(list((''.join(o) for o in product(*options))))


def evaluate_hunspell():
    d = {}
    with open("typo-orpho-ed_one_word.csv") as table:
        t = table.readlines()[1:]
        for l in t:
            l = re.sub('\n','',l)
            w, r, ed = l.split(',')
            d[w] = [r, ed]
            # print(w, r, ed)

    f = open("hunspell_one_word_aG.txt").readlines()
    for l in f:
        l = re.sub('\n','',l)
        # print(l.split(' '))
        if l.startswith('*'):
            print('ok')
        elif l.startswith(' +'):
            m = l.split(' ')[2]
            print('out', m, '@', '0', '@')
        elif l.startswith('#'):
            print(l.split(' '))
            if l.split(' ')[2] == '0':
                m = l.split(' ')[1]
                print('out', m, d[m][0], '0', d[m][1])
            else:
                left, right = l.split(':')
                m = left.split(' ')[1]
                num = left.split(' ')[2]
                sug = right.split(',')
                suggested = [w.strip() for w in sug]
                if d[m][0] in suggested:
                    print('in', m, d[m][0], num, d[m][1])
                else:
                    print('out', m, d[m][0], num, d[m][1])

# evaluate_hunspell()


def ed_iterating(word, table):
    '''
    takes a word
    ED = 2
    returns all the modifications
    {cand: score}
    '''
    candidates = {}
    first = ed_1(word, 0, table)
    print('first:', first, '\n============')
    for k in first:         # собрать уникальные кандидаты с весами в candidates
            if k not in candidates:
                candidates[k] = first[k]
            else:
                candidates[k] = min(candidates[k], first[k])
    for w in first:         # пополнить candidates кандидатами из новой итерации, снова все уникальные
        w_cands = ed_1(w, first[w], table)
        for k in w_cands:
            if k not in candidates:
                candidates[k] = w_cands[k]
            else:
                candidates[k] = min(candidates[k], w_cands[k])
    # print('кандидаты после новой итерации:')
    # for x in candidates:
    #     print(x, candidates[x])
    print('конец итерации, %d кандидатов' % len(candidates))

    return candidates


def hunspell(string):
    '''
    *
    # встертелись 0
    & этым 3 0: тым, этом, этим
    + друзь [без аффикса]
    '''
    # print(string)
    # start_time = time.time()
    echo = subprocess.Popen(['echo', string.encode('utf8')], stdout=subprocess.PIPE)
    result = subprocess.Popen(['hunspell', '-aG', '-d', 'ru_RU'], stdin=echo.stdout, stdout=subprocess.PIPE)
    cyr = result.communicate()[0].decode('utf-8')
    # print("---hunspell: %s seconds ---" % (time.time() - start_time))
    # print(cyr[15])
    if cyr[15] == '*':
        # mistake = False
        print('hunspell says OK')
        return False, [string]
    elif cyr[15] == '&':
        suggested = cyr.split(':')[1].split(',')
        suggested = [w.strip() for w in suggested]
        # print('hunspell suggests:', suggested)
        return True, suggested
    else:
        print('hunspell gives nothing')
        # look
        return True, []


def aspell(string):
    '''
    если ok:    False, []
    если ошибка: True, aspell_sug

    '''
    enchant.set_param("enchant.aspell.dictionary.path", "emeshch-spell-checker-a264623eaa3c/aspell6-ru-0.99f7-1")
    d = enchant.Dict("ru_RU")
    if d.check(string):      # aspell says OK
        # print('aspell says OK')
        return False, []
    else:
        # print('aspell says mistake and suggests:')
        aspell_sug = d.suggest(string)
        return True, aspell_sug

# print(aspell('птыца'))


def lookup_mystem(string):
    '''
    кашей{каша=S,жен,неод=твор,ед}
    '''
    # with open('myinput.in', 'w') as myinput:
    #     myinput.write(string)
    # inp = open('myinput.in')
    # start_time = time.time()
    # echo = subprocess.Popen(['echo', string.encode('utf8')], stdout=subprocess.PIPE)
    # result = subprocess.Popen(['./mystem', '-gnid', '-e', 'utf-8'], stdin=echo.stdout, stdout=subprocess.PIPE)
    result = subprocess.Popen(['./mystem', '-gnid', '-e', 'utf-8'], stdin=inp, stdout=subprocess.PIPE)

    cyr = result.communicate()[0].decode('utf-8')
    # print("---mystem+file %s seconds ---" % (time.time() - start_time))
    print(cyr)
    if '?' in cyr:
        mistake = True
    else:
        mistake = False
    print('mystem says', mistake)
    return mistake

# for i in ["эти", "эта", "этой", "мной", "други", "этои", "мнои", "времини"]:
#     print(i)
#     h = hunspell(i)
#     m = lookup_mystem(i)
# print(lookup_mystem('катастрофа'))


def make_table(alpha):
    d = {}
    abc = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    for x in abc:
        inner = {}
        for y in abc:
            if y == x:
                inner[y] = alpha
            else:
                inner[y] = (1-alpha)/(len(abc)-1)
        d[x] = inner
    # print(d)
    return d


def standard(word):
    table = make_table(0.9)
    mistake, ans = aspell(word)
    print(mistake, ans)
    if mistake:
        mods = ed_iterating(word, table)
        for mod in mods:
            mist, c = aspell(mod)
            if not mist:
                ans.append({mod: mods[mod]})
    pprint(ans)

# standard('этои')


# c = iterating('a+b')
def lookup_pymystem(string):
    is_mistake = False
    susp_index = 0
    lex = []            # потом эта лемма пойдёт в частотный словарь
    start_time = time.time()
    mystem = Mystem()
    mystemmed = mystem.analyze(string)
    '''
    [{'analysis': [{'gr': 'S,муж,неод=род,ед',
                'lex': 'котостроф',
                'qual': 'bastard'}],
      'text': 'котострофа'},
     {'text': '\n'}]
    '''
    # pprint(mystemmed[0])
    if 'qual' in mystemmed[0]['analysis'][0]:
        print('\tpymystem: mistake')
        return True
    else:
        print('\tpymystem: ok')
        return False
    # for entry in mystemmed[0]:
    #     if 'analysis' in entry:
    #         print(entry)
    #         for ana in entry['analysis']:
    #             # print(ana)
    #             if 'qual' in ana:
    #                 if ana['qual'] == 'bastard':
    # print("---pymystem: %s seconds ---" % (time.time() - start_time))
    #                     return True
            #             susp_index += 1
                    # else:
                        # lex.append(ana['lex'])                                                                                                 'text': 'заквакали'}, {'text': '.'}, {'text': '\n'}]
    # if susp_index > 0:
    #     is_mistake = True
    # return is_mistake, lex
# for i in ["кашей", "каша", "каши", "дружбость", "злостью"]:
# lookup_pymystem('катастрофа')

# for i in ["эти", "эта", "этой", "мной", "други", "этои", "мнои", "времини"]:
#     print(i)
#     h = hunspell(i)
#     m = lookup_mystem(i)
#     lookup_pymystem(i)


def context(table):
    '''
    буквенное окружение ошибки для Светы
    '''
    lines = open(table).readlines()
    with open('context_mistakes.csv', 'w') as f_out:
        f_out.write('left3' + '\t' + 'left2' + '\t' + 'ошибка' + '\t' + 'исправление'  + 'слово с ошибкой' + '\t' + 'исправленное слово' + '\n')
        # lines = data.readlines()
        for line in lines[1:]:
            # print(line, len(line))
            mistake, correct, ed = line.split(';')
            print(mistake, len(mistake), correct, len(correct))
            if len(mistake) == len(correct):        # замена буквы на букву
                for q, c in zip(mistake,correct):
                    if q != c:
                        left2 = mistake[max(int(mistake.index(q))-2, 0): mistake.index(q)]
                        left3 = mistake[max(int(mistake.index(q))-3, 0): mistake.index(q)]
                        print(left3 + '\t' + left2 + '\t' + q + c + mistake + '\t' + correct + '\n')
                        f_out.write(left3 + '\t' + left2 + '\t' + q + c + mistake + '\t' + correct + '\n')
            elif len(mistake) < len(correct):       # вставка буквы

                for c_index in range(len(correct)):
                    # print(c_index, correct[c_index], mistake[c_index])
                    if correct[c_index] != mistake[c_index]:
                        print(c_index, correct[c_index], mistake[c_index])
                        left2 = mistake[max(c_index-2, 0): c_index]
                        left3 = mistake[max(c_index-3, 0): c_index]
                        # @ обозначает пустую строку!
                        f_out.write(left3 + '\t' + left2 + '\t' + '@' + '\t' + correct[c_index]  + mistake + '\t' + correct + '\n')
                        break

            elif len(mistake) > len(correct):       # удаление буквы
                for m_index in range(len(mistake)):
                    if correct[m_index] != mistake[m_index]:
                        left2 = mistake[max(m_index-2, 0): m_index]
                        left3 = mistake[max(m_index-3, 0): m_index]
                        # @ обозначает пустую строку!
                        f_out.write(left3 + '\t' + left2 + '\t' + correct[c_index] + '@' + '\t' + mistake + '\t' + correct + '\n')
                        break
# context('typo-orpho-ed.txt')

# out_list = lookup()


def sort_freq():
    '''
    сортирует частотный список словоформ
    '''
    big_ru = {}
    ru = []
    with open('./Freq2011/wform.csv') as f:
        big = f.readlines()
        for line in big[2:]:
            # print(line, len(line.split('\t')))
            id, form, ipm, capital = line.strip().split('\t')
            # big_ru[form] = ipm
            ru.append([form, ipm])
            ru.sort(key=lambda x: float(x[1]))
            # if int(ipm) < 5:
            #     print('RARE', lemma, d)
    with open('./Freq2011/wform_sorted.csv', 'w') as out:
        for s in ru:
            out.write(' '.join(s) + '\n')
    return big_ru


def from_freq(string):
    '''
    take a word
    return [ipm, r, d]
    '''
    big_ru = {}
    start = time.time()
    with open('./Freq2011/freqrnc2011.csv') as rus:
        ru = rus.readlines()[1:]
        for line in ru:
            lemma, pos, ipm, r, d, doc = line.split('\t')
            # lp = lemma + ',' + pos
            big_ru[lemma + ',' + pos] = [ipm, r, d]
    print("dictionary: %s seconds" % (time.time() - start))
    start_time = time.time()
    mystem = Mystem()
    mystemmed = mystem.analyze(string)
    print("pymystem: %s seconds" % (time.time() - start_time))
    lemma_mystem = mystemmed[0]['analysis'][0]['lex']
    pos_mystem = mystemmed[0]['analysis'][0]['gr'].split('=')[0].split(',')[0].lower()
    try:
        return big_ru[lemma_mystem + ',' + pos_mystem]
    except:
        return ['', '', '']
# print(from_freq('мяуча'))


def csv2transform(scv):
    russian = u"абвгдеёжзийклмнопрстуфхцчшщъыьэюя- "
    english = u"abcdefghijklmnopqrstuvwxyz"
    table_dict = {}

    for l in english:
        table_dict[l] = []
    with open(scv, 'r', encoding='utf-8') as f_in:
        lines = f_in.read().split('\n')
        for line in lines:
            from_c, to_c = line.split(';')
            # в виде словаря
            table_dict[from_c] += to_c.split(' ')

    # pprint(table_dict)
    # print('='*20)
    # внимание! сначала кирилица, затем латиница
    table_set = []
    for k in table_dict:
        for v in table_dict[k]:
            table_set.append((v, k))
    # pprint(table_set)
    return table_set


# lat_table = csv2transform('латиница.csv')


def get_transpositions():
    '''
    контекст перестановки для Светы

    mistake;correct;ed

    Турдность - трудность / турд / урд / труд
    '''
    # mistake = 'турднотcь'
    # correct = 'трудность'
    # ed = 1

    with open("transpositions.csv", 'w') as f_out:
        for line in open("tableresult2.csv", encoding='cp1251').readlines()[1:]:
            mistake, correct, ed = line.split(';')

            skip = False
            if len(mistake) == len(correct):
                # print(mistake, correct)
                for i in range(len(mistake)):
                    if skip:
                        skip = False
                        continue
                    else:
                        if mistake[i] != correct[i]:
                            if len(mistake) < i+3:
                                    mistake += ' '*3
                            if len(correct) < i+3:
                                correct += ' '*3
                            if mistake[i] == correct[i+1]:
                                print('!', mistake[i-1:i+3], mistake[i:i+3], correct[i-1:i+3])
                                f_out.write(mistake + '\t' + correct + '\t' + mistake[i-1:i+3] + '\t' + mistake[i:i+3] + '\t' + correct[i-1:i+3] + '\n')
                                skip = True

# get_transpositions()


