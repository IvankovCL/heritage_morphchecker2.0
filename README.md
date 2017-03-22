# Morphchecker     
Система обнаружения и коррекции морфологических ошибок 
для корпуса эритажного русского языка Russian Learner Corpora

### Инструкция
Собственно коррекция морфологических ошибок:
```
>>> m = Morphchecker()
>>> m.mcheck('баллотировается')
ИСПРАВЛЕНИЯ: [(3, 'баллотируется')]
```

Коррекция орфографических ошибок:
```
>>> m = Morphchecker()
>>> m.spellcheck('баллотировается')
СПЕЛЛЧЕК: ['баллотирования', 'баллотироваться', 'баллотировавшийся', 'баллотирование']
```

Локализация ошибки:
```
>>> m = Morphchecker()
>>> mchecked = m.mcheck('баллотировается')
>>> m.analyse(mchecked)
Если "баллотируется" - правильное исправление, то морфема 'ова' употреблена вместо морфемы "у"
```

### Используемые ресурсы
- Модуль morphchecker.py, реализующий общий алгоритм обнаружения и исправления ошибок
- Модуль prjscript.py, реализующий алгоритм деления слов на морфемы
- Модуль проверки орфографии, созданный для русского эритажного корпуса: https://bitbucket.org/emeshch/heritage_spell_checker
- Словарь морфем А.И. Кузнецовой, содержащий информацию о входящих в слово (в форме именительного падежа) морфемах и их алломорфах (resources/umorphodict2.csv)
- Словарь Hunspell, содержащий правила изменения леммы слова во все возможные для него формы (resources/ru_RU.dic; resources/ru_RU.aff)

### Необходимые модули
Для работы системы необходимо установить:
- nltk
- pymystem3
- pymorphy2
- pylev

Кроме того для работы модуля орфографии понадобятся:
- enchant
- numpy

### Основной алгоритм
1. Чтение файлов словарей. 
2. Получение списка исправлений от спеллчекера или информации о том, что в слове нет ошибок.
3. Деление ошибочного слова на морфемы. Извлечение корня и окончания. Определение граммем окончания по словарю.
4. Лемматизизация выдачи спеллчекера.
5. Сравнение части речи каждой леммы со списком граммем окончания. 
6. Сравнение корня леммы со списком алломорфов корня ошибочного слова. 
7. Определение по словарю набора правил, доступного для леммы с учётом граммем окончания.
8. Постановка леммы в формы, соответствующие граммемам окончания.
9. Вычисление расстояния Левенштейна между полученными исправлениями и ошибочным словом. Остаются исправления с минимальным расстоянием
10. Поморфемное сравнение оставшихся исправлений с ошибочным словом и локализация места ошибки.
