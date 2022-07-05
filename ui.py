import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication

import re
import webbrowser
import speech_recognition
from sound import Sound
import os
import pyttsx3
import datetime
from translate import Translator
from num2words import num2words

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

tts = pyttsx3.init()  # запуск инициализации озвучки
RU_VOICE_ID = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
# усатновка голоса из (windows)
tts.setProperty('voice', RU_VOICE_ID)  # выбор озвучки


class Window(QMainWindow):  # создание класса для приложения(удобнее, можно использовать вне класса)
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle('Голосовой асистент Дмитрий')  # создание окна с надписью
        self.setGeometry(800, 200, 400, 100)  # установка размеров окна
        self.setFixedSize(400, 100)  # фиксированный размер окна

        self.setWindowIcon(QtGui.QIcon('1.png'))  # установка иконки из библиотеки

        self.main_text = QtWidgets.QLabel(self)  # добавление изменяющегося текста
        self.main_text.setText('Привет я голосовой асистент Дмитрий')  # установка текста
        self.main_text.move(10, 25)  # перемещение текста внутри окна
        self.main_text.adjustSize()  # выравнивание текста по длине самого текста

        self.new_text = QtWidgets.QLabel(self)  # добавление изменяющегося текста
        self.new_text.setText('')
        self.new_text.move(150, 55)
        self.new_text.adjustSize()

        self.sub_text = QtWidgets.QLabel(self)  # добавление текста для суммы
        self.sub_text.setText(' ')
        self.sub_text.move(50, 25)
        self.sub_text.adjustSize()

        self.run_button = QtWidgets.QPushButton(self)  # добавление кнопки для вызова преобразователя голоса
        self.run_button.setText('Сказать команду:')
        self.run_button.move(10, 50)
        self.run_button.adjustSize()
        self.run_button.clicked.connect(self.voice_asistant)  # связь между кнопкой и запуском асистента
        tts.say("Привет я голосовой асистент Дмитрий")
        tts.runAndWait()

    def voice_asistant(self):  # запуск самого асистента
        sr = speech_recognition.Recognizer()  # инициализация текстового преобразователя
        sr.pause_threshold = 0.5  # пауза между словами = 0.5 секунды
        oper = ""  # переменная для поиска слов(словосочетаний)
        translator = Translator(to_lang="Russian")
        try:

            with speech_recognition.Microphone() as mic:  # запуск преобразователя(микрофона)
                sr.adjust_for_ambient_noise(source=mic, duration=0.5)  # подавление шумов
                audio = sr.listen(source=mic)  # ввод голоса напрмую из микрофона
                oper = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
                # присваивание значения переменной для поиска слов
                self.new_text.setText(sr.recognize_google(audio_data=audio, language='ru-RU').lower())
                print(sr.recognize_google(audio_data=audio, language='ru-RU').lower())
                # напечатать то что сказали
                self.new_text.adjustSize()
                self.sub_text.setText(' ')  # отчиска текста для избежания наложения

            if (oper.find("привет") >= 0) or (oper.find("здравствуй") >= 0):  # добавление приветсвия
                tts.say("Привет")  # что будет говорить ассистент(Привет)
                tts.runAndWait()
                self.main_text.setText('Привет)')
                self.main_text.adjustSize()

            elif (oper.find("пока") >= 0) or (oper.find("до свидания") >= 0):  # добавление функции - Пока(
                tts.say("Пока")
                tts.runAndWait()
                self.main_text.setText('Пока(')
                self.main_text.adjustSize()
                self.close()  # закрытие приложения

            elif (oper.find("открой диспетчер задач") >= 0) or \
                    (oper.find("открыть диспетчер задач") >= 0):  # открытие диспетчера задач(если слово найдено)
                tts.say("Открывается диспетчер задач")
                tts.runAndWait()
                self.main_text.setText('Открывается диспетчер задач')
                self.main_text.adjustSize()
                os.system('Taskmgr')  # командная строка = taskmgr

            elif (oper.find("открой настройки") >= 0) or (oper.find("открыть настройки") >= 0):  # открытие настроек
                tts.say("Открываются настройки системы")
                tts.runAndWait()
                self.main_text.setText('Открываются настройки системы')
                self.main_text.adjustSize()
                os.system('Control')  # командная строка = control

            elif (oper.find("Открыть файл hosts в блокноте") >= 0) or (oper.find("Открой файл hosts в блокноте") >= 0):
                tts.say("Открываю файл hosts в блокноте")
                tts.runAndWait()
                self.main_text.setText('Открываю файл hosts в блокноте')
                self.main_text.adjustSize()
                os.system('notepad C:\Windows\System32\drivers\etc\hosts')

            elif (oper.find("поиск в интернете") >= 0) or (oper.find("найди в интернете") >= 0) or \
                    (oper.find("найти в интернете") >= 0):  # поисковый запрос в гугле
                all_word = ""  # введение новой переменной для теста
                split = oper.split(" ")  # разделение текста на слова по пробелам
                poisk = split[3:]  # (не учитывать первые три слова)
                for word in poisk:
                    all_word += word + " "  # сборка всего поискового запроса

                url = 'https://www.google.com/search?q=' + all_word  # url поискового запроса
                tts.say("Ищу в интернете ваш запрос" + all_word)
                tts.runAndWait()
                self.main_text.setText('Ищу в интернете ваш запрос:' + all_word)
                self.main_text.adjustSize()
                webbrowser.open_new(url)  # открыть браузер с писковым запросом(url)

            elif oper.find("что такое") >= 0:  # поисковый запрос в гугле
                all_word = ""  # введение новой переменной для теста
                split = oper.split(" ")  # разделение текста на слова по пробелам
                poisk = split[2:]  # (не учитывать первые три слова)
                for word in poisk:
                    all_word += word + " "  # сборка всего поискового запроса

                url = 'https://ru.wikipedia.org/wiki/' + all_word  # url поискового запроса
                tts.say("Ищу в интернете ваш запрос" + all_word)
                tts.runAndWait()
                self.main_text.setText('Ищу в интернете ваш запрос:' + all_word)
                self.main_text.adjustSize()
                webbrowser.open_new(url)  # открыть браузер с писковым запросом(url)

            elif (oper.find("открой youtube") >= 0) or (oper.find("открыть youtube") >= 0):
                tts.say("Открываю YouTube")
                tts.runAndWait()
                self.main_text.setText('Открываю YouTube')
                self.main_text.adjustSize()
                webbrowser.open_new('https://www.youtube.com/')  # открыть youtube в новой вкладке

            elif (oper.find("открой vk") >= 0) or (oper.find("открыть вконтакте") >= 0) or \
                    (oper.find("открой вконтакте") >= 0) or (oper.find("открыть vk") >= 0) or (
                    oper.find("открыть вк") >= 0) or (
                    oper.find("открой вк") >= 0):
                tts.say("Открываю VK(ВКонтакте)")
                tts.runAndWait()
                self.main_text.setText('Открываю VK(ВКонтакте)')
                self.main_text.adjustSize()
                webbrowser.open_new('https://vk.com/')  # открыть vk в новой вкладке

            elif (oper.find("открыть новую вкладку в браузере") >= 0) or (
                    oper.find("открой новую вкладку в браузере") >= 0):
                # октрытие новой вкладки в браузере
                tts.say("Открытие новой вкладки в браузере")
                tts.runAndWait()
                self.main_text.setText('Открытие новой вкладки в браузере')
                self.main_text.adjustSize()
                webbrowser.open_new('https:')  # открыть браузер с новой вкладкой

            elif (oper.find("сколько будет") >= 0) or (oper.find("посчитай сколько будет") >= 0):  # поиск слов
                if (oper.find("+") >= 0) or (oper.find("плюс") >= 0):
                    nums = re.findall('[0-9]+', oper)  # поиск и отлов цифр(regex)
                    rez = int(nums[0]) + int(nums[1])  # сложение цифр(в формате int)
                    tts.say("Ответ:" + str(rez))
                    tts.runAndWait()
                    self.main_text.setText('Ответ:')
                    self.main_text.adjustSize()
                    self.sub_text.setText(str(rez))
                    self.sub_text.adjustSize()
                    # вывод результата

                elif (oper.find("-") >= 0) or (oper.find("минус") >= 0):
                    nums = re.findall('[0-9]+', oper)  # поиск и отлов цифр(regex)
                    rez = int(nums[0]) - int(nums[1])  # вычитание цифр(в формате int)
                    tts.say("Ответ:" + str(rez))
                    tts.runAndWait()
                    self.main_text.setText('Ответ:')
                    self.main_text.adjustSize()
                    self.sub_text.setText(str(rez))
                    self.sub_text.adjustSize()
                    # вывод результата

                elif (oper.find("х") >= 0) or (oper.find("*") >= 0) or (oper.find("умножить") >= 0):
                    nums = re.findall('[0-9]+', oper)  # поиск и отлов цифр(regex)
                    rez = int(nums[0]) * int(nums[1])  # умножение цифр(в формате int)
                    self.main_text.setText('Ответ:')
                    self.main_text.adjustSize()
                    self.sub_text.setText(str(rez))
                    self.sub_text.adjustSize()
                    # вывод результата

                elif (oper.find("/") >= 0) or (oper.find("разделить") >= 0) or (oper.find("дробью") >= 0):
                    nums = re.findall('[0-9]+', oper)  # поиск и отлов цифр(regex)
                    if float(nums[1]) == 0.0:  # добавление исключений = / 0
                        tts.say("На ноль делить нельзя")
                        tts.runAndWait()
                        self.main_text.setText('На ноль делить нельзя')
                        self.main_text.adjustSize()
                    else:
                        rez = float(nums[0]) / float(nums[1])  # деление цифр(в формате float)
                        tts.say("Ответ:" + str(int(rez)))
                        tts.runAndWait()
                        self.main_text.setText('Ответ:')
                        self.main_text.adjustSize()
                        self.sub_text.setText(str(rez))
                        self.sub_text.adjustSize()
                        # вывод результата

            elif (oper.find("поставь громкость на") >= 0) or (oper.find("поставить громкость на") >= 0):
                vol = re.findall('[0-9]+', oper)  # поиск и отлов цифр(regex)
                vol1 = int(vol[0])  # передача целого значения для регулировки
                tts.say("Громкость уcтановлена на:" + str(vol[0]))
                tts.runAndWait()
                self.main_text.setText("Громкость уcтановлена на" + str(vol[0]))
                self.main_text.adjustSize()
                Sound.volume_set(vol1)  # регулировка громкости(sound.py, keyboard.py)

            elif (oper.find("выключить звук") >= 0) or (oper.find("выключи звук") >= 0):
                tts.say("Громкость уcтановлена на:0")
                tts.runAndWait()
                self.main_text.setText("Громкость уcтановлена на: 0")
                self.main_text.adjustSize()
                Sound.volume_set(0)  # регулировка громкости(sound.py, keyboard.py)

            elif (oper.find("включить звук") >= 0) or (oper.find("включи звук") >= 0):
                tts.say("Громкость уcтановлена на: 100")
                tts.runAndWait()
                self.main_text.setText("Громкость уcтановлена на: 100")
                self.main_text.adjustSize()
                Sound.volume_set(100)  # регулировка громкости(sound.py, keyboard.py)

            elif (oper.find("какой сейчас год") >= 0) or (oper.find("какой год сейчас") >= 0):
                dt = datetime.datetime.now()
                dt_string = dt.strftime("%Y")
                year = num2words(dt_string, lang='ru', to='ordinal')
                tts.say("Сейчас:" + year + "год")
                tts.runAndWait()
                self.main_text.setText("Сейчас:" + year + " год")
                self.main_text.adjustSize()

            elif (oper.find("сколько сейчас время") >= 0) or (oper.find("сколько сейчас времени") >= 0) or \
                    (oper.find("который час") >= 0) or (oper.find("текущее время") >= 0):
                dt = datetime.datetime.now()
                dt_string = dt.strftime("%H:%M")
                tts.say("Сейчас:" + dt_string)
                tts.runAndWait()
                self.main_text.setText("Сейчас:" + dt_string)
                self.main_text.adjustSize()

            elif (oper.find("какой сейчас месяц") >= 0) or (oper.find("какой сегодня месяц") >= 0):
                dt = datetime.datetime.now()
                dt_string = dt.strftime("%B")
                translation = translator.translate(dt_string)
                tts.say("Сейчас:" + translation)
                tts.runAndWait()
                self.main_text.setText("Сейчас:" + translation)
                self.main_text.adjustSize()

            elif (oper.find("какой сейчас день недели") >= 0) or (oper.find("какой сегодня день недели") >= 0):
                dt = datetime.datetime.now()
                dt_string = dt.strftime("%A")
                translation = translator.translate(dt_string)
                tts.say("Сейчас:" + translation)
                tts.runAndWait()
                self.main_text.setText("Сейчас:" + translation)
                self.main_text.adjustSize()

            elif (oper.find("какое сегодня число") >= 0) or (oper.find("какая сегодня дата") >= 0):

                def get_date(date):
                    day_list = ['первое', 'второе', 'третье', 'четвёртое',
                                'пятое', 'шестое', 'седьмое', 'восьмое',
                                'девятое', 'десятое', 'одиннадцатое', 'двенадцатое',
                                'тринадцатое', 'четырнадцатое', 'пятнадцатое', 'шестнадцатое',
                                'семнадцатое', 'восемнадцатое', 'девятнадцатое', 'двадцатое',
                                'двадцать первое', 'двадцать второе', 'двадцать третье',
                                'двадацать четвёртое', 'двадцать пятое', 'двадцать шестое',
                                'двадцать седьмое', 'двадцать восьмое', 'двадцать девятое',
                                'тридцатое', 'тридцать первое']
                    month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                                  'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
                    date_list = date.split('/')
                    return (day_list[int(date_list[0]) - 1] + ' ' +
                            month_list[int(date_list[1]) - 1])

                dt = datetime.datetime.now()
                dt_year = dt.strftime("%Y")
                year_str = num2words(dt_year, lang='ru', to='ordinal')
                tts.say("Сегодня:" + get_date(dt.strftime("%d/%m")) + year_str + ' год')
                tts.runAndWait()
                self.main_text.setText("Сегодня:" + dt.strftime("%d/%m/%Y") + ' год' + ' ' +
                                       '(' + get_date(dt.strftime("%d/%m")) + ' ' + year_str + ' год' + ')')
                self.main_text.adjustSize()

            elif (oper.find("увеличить громкость на") >= 0) or (oper.find("уменьшить громкость на") >= 0) or \
                    (oper.find("увеличь громкость на") >= 0) or (oper.find("уменьши громкость на") >= 0):
                d = {a: 0 for a in range(101)}
                d[0] = -65.25
                d[1] = -56.992191314697266
                d[2] = -51.671180725097656
                d[3] = -47.73759078979492
                d[4] = -44.61552047729492
                d[5] = -42.026729583740234
                d[6] = -39.81534194946289
                d[7] = -37.88519287109375
                d[8] = -36.17274856567383
                d[9] = -34.63383865356445
                d[10] = -33.23651123046875
                d[11] = -31.956890106201172
                d[12] = -30.77667808532715
                d[13] = -29.681535720825195
                d[14] = -28.66002082824707
                d[15] = -27.70285415649414
                d[16] = -26.80240821838379
                d[17] = -25.95233154296875
                d[18] = -25.147287368774414
                d[19] = -24.38274574279785
                d[20] = -23.654823303222656
                d[21] = -22.960174560546875
                d[22] = -22.295886993408203
                d[23] = -21.6594181060791
                d[24] = -21.048532485961914
                d[25] = -20.461252212524414
                d[26] = -19.895822525024414
                d[27] = -19.350669860839844
                d[28] = -18.824398040771484
                d[29] = -18.315736770629883
                d[30] = -17.82354736328125
                d[31] = -17.3467960357666
                d[32] = -16.884546279907227
                d[33] = -16.435937881469727
                d[34] = -16.000192642211914
                d[35] = -15.576590538024902
                d[36] = -15.164472579956055
                d[37] = -14.763236045837402
                d[38] = -14.372318267822266
                d[39] = -13.991202354431152
                d[40] = -13.61940860748291
                d[41] = -13.256492614746094
                d[42] = -12.902039527893066
                d[43] = -12.555663108825684
                d[44] = -12.217005729675293
                d[45] = -11.88572883605957
                d[46] = -11.561516761779785
                d[47] = -11.2440767288208
                d[48] = -10.933131217956543
                d[49] = -10.62841796875
                d[50] = -10.329694747924805
                d[51] = -10.036728858947754
                d[52] = -9.749302864074707
                d[53] = -9.46721076965332
                d[54] = -9.190258026123047
                d[55] = -8.918261528015137
                d[56] = -8.651047706604004
                d[57] = -8.388449668884277
                d[58] = -8.130311965942383
                d[59] = -7.876484394073486
                d[60] = -7.626824855804443
                d[61] = -7.381200790405273
                d[62] = -7.1394829750061035
                d[63] = -6.901548862457275
                d[64] = -6.6672821044921875
                d[65] = -6.436570644378662
                d[66] = -6.209307670593262
                d[67] = -5.98539400100708
                d[68] = -5.764730453491211
                d[69] = -5.547224998474121
                d[70] = -5.33278751373291
                d[71] = -5.121333599090576
                d[72] = -4.912779808044434
                d[73] = -4.707049369812012
                d[74] = -4.5040669441223145
                d[75] = -4.3037590980529785
                d[76] = -4.1060566902160645
                d[77] = -3.9108924865722656
                d[78] = -3.718202590942383
                d[79] = -3.527923583984375
                d[80] = -3.339998245239258
                d[81] = -3.1543679237365723
                d[82] = -2.970977306365967
                d[83] = -2.7897727489471436
                d[84] = -2.610703229904175
                d[85] = -2.4337174892425537
                d[86] = -2.2587697505950928
                d[87] = -2.08581280708313
                d[88] = -1.9148017168045044
                d[89] = -1.7456932067871094
                d[90] = -1.5784454345703125
                d[91] = -1.4130167961120605
                d[92] = -1.2493702173233032
                d[93] = -1.0874667167663574
                d[94] = -0.9272695183753967
                d[95] = -0.768743097782135
                d[96] = -0.6118528842926025
                d[97] = -0.4565645754337311
                d[98] = -0.30284759402275085
                d[99] = -0.15066957473754883
                d[100] = 0.0

                if (oper.find('увеличить') >= 0) or (oper.find('увеличь') >= 0):
                    def volume_control_plus(n):
                        global vol
                        if volume.GetMasterVolumeLevel() == d[100]:
                            vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[99]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[1])]):
                                vol = d[99 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[98]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[2])]):
                                vol = d[98 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[97]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[3])]):
                                vol = d[97 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[96]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[4])]):
                                vol = d[96 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[95]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[5])]):
                                vol = d[95 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[94]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[6])]):
                                vol = d[94 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[93]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[7])]):
                                vol = d[93 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[92]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[8])]):
                                vol = d[92 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[91]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[9])]):
                                vol = d[91 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[90]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[10])]):
                                vol = d[90 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[89]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[11])]):
                                vol = d[89 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[88]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[12])]):
                                vol = d[88 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[87]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[13])]):
                                vol = d[87 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[86]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[14])]):
                                vol = d[86 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[85]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[15])]):
                                vol = d[85 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[84]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[16])]):
                                vol = d[84 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[83]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[17])]):
                                vol = d[83 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[82]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[18])]):
                                vol = d[82 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[81]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[19])]):
                                vol = d[81 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[80]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[20])]):
                                vol = d[80 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[79]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[21])]):
                                vol = d[79 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[78]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[22])]):
                                vol = d[78 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[77]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[23])]):
                                vol = d[77 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[76]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[24])]):
                                vol = d[76 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[75]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[25])]):
                                vol = d[75 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[74]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[26])]):
                                vol = d[74 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[73]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[27])]):
                                vol = d[73 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[72]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[28])]):
                                vol = d[72 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[71]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[29])]):
                                vol = d[71 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[70]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[30])]):
                                vol = d[70 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[69]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[31])]):
                                vol = d[69 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[68]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[32])]):
                                vol = d[68 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[67]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[33])]):
                                vol = d[67 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[66]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[34])]):
                                vol = d[66 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[65]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[35])]):
                                vol = d[65 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[64]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[36])]):
                                vol = d[64 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[63]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[37])]):
                                vol = d[63 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[62]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[38])]):
                                vol = d[62 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[61]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[39])]):
                                vol = d[61 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[60]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[40])]):
                                vol = d[60 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[59]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[41])]):
                                vol = d[59 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[58]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[42])]):
                                vol = d[58 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[57]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[43])]):
                                vol = d[57 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[56]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[44])]):
                                vol = d[56 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[55]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[45])]):
                                vol = d[55 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[54]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[46])]):
                                vol = d[54 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[53]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[47])]):
                                vol = d[53 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[52]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[48])]):
                                vol = d[52 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[51]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[49])]):
                                vol = d[51 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[50]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[50])]):
                                vol = d[50 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[49]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[51])]):
                                vol = d[49 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[48]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[52])]):
                                vol = d[48 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[47]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[53])]):
                                vol = d[47 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[46]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[54])]):
                                vol = d[46 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[45]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[55])]):
                                vol = d[45 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[44]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[56])]):
                                vol = d[44 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[43]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[57])]):
                                vol = d[43 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[42]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[58])]):
                                vol = d[42 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[41]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[59])]):
                                vol = d[41 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[40]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[60])]):
                                vol = d[40 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[39]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[61])]):
                                vol = d[39 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[38]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[62])]):
                                vol = d[38 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[37]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[63])]):
                                vol = d[37 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[36]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[64])]):
                                vol = d[36 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[35]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[65])]):
                                vol = d[35 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[34]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[66])]):
                                vol = d[34 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[33]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[67])]):
                                vol = d[33 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[32]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[68])]):
                                vol = d[32 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[31]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[69])]):
                                vol = d[31 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[30]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[70])]):
                                vol = d[30 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[29]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[71])]):
                                vol = d[29 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[28]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[72])]):
                                vol = d[28 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[27]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[73])]):
                                vol = d[27 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[26]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[74])]):
                                vol = d[26 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[25]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[75])]):
                                vol = d[25 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[24]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[76])]):
                                vol = d[24 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[23]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[77])]):
                                vol = d[23 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[22]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[78])]):
                                vol = d[22 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[21]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[79])]):
                                vol = d[21 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[20]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[80])]):
                                vol = d[20 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[19]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[81])]):
                                vol = d[19 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[18]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[82])]):
                                vol = d[18 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[17]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[83])]):
                                vol = d[17 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[16]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[84])]):
                                vol = d[16 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[15]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[85])]):
                                vol = d[15 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[14]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[86])]):
                                vol = d[14 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[13]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[87])]):
                                vol = d[13 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[12]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[88])]):
                                vol = d[12 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[11]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[89])]):
                                vol = d[11 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[10]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[90])]):
                                vol = d[10 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[9]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[91])]):
                                vol = d[9 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[8]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[92])]):
                                vol = d[8 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[7]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[93])]):
                                vol = d[7 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[6]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[94])]):
                                vol = d[6 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[5]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[95])]):
                                vol = d[5 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[4]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[96])]):
                                vol = d[4 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[3]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[97])]):
                                vol = d[3 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[2]:
                            if n > int(list(d.keys())[list(d.values()).index(d[98])]):
                                vol = d[2 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[1]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[99])]):
                                vol = d[1 + n]
                            else:
                                vol = d[100]
                        elif volume.GetMasterVolumeLevel() == d[0]:
                            if n <= int(list(d.keys())[list(d.values()).index(d[100])]):
                                vol = d[0 + n]
                            else:
                                vol = d[100]

                        return vol

                    nums = re.findall('[0-9]+', oper)
                    num = int(nums[0])
                    volume.SetMasterVolumeLevel(volume_control_plus(num), None)

                    tts.say("Громкость увеличена на" + ' ' + str(num))
                    tts.runAndWait()
                    self.main_text.setText("Громкость увеличена на" + ' ' + str(num))
                    self.main_text.adjustSize()

                else:
                    def volume_control_min(n):
                        global vol
                        if volume.GetMasterVolumeLevel() == d[100]:
                            if n > int(list(d.keys())[list(d.values()).index(d[100])]):
                                vol = d[0]
                            else:
                                vol = d[100 - n]
                        elif volume.GetMasterVolumeLevel() == d[99]:
                            if n > int(list(d.keys())[list(d.values()).index(d[99])]):
                                vol = d[0]
                            else:
                                vol = d[99 - n]
                        elif volume.GetMasterVolumeLevel() == d[98]:
                            if n > int(list(d.keys())[list(d.values()).index(d[98])]):
                                vol = d[0]
                            else:
                                vol = d[98 - n]
                        elif volume.GetMasterVolumeLevel() == d[97]:
                            if n > int(list(d.keys())[list(d.values()).index(d[97])]):
                                vol = d[0]
                            else:
                                vol = d[97 - n]
                        elif volume.GetMasterVolumeLevel() == d[96]:
                            if n > int(list(d.keys())[list(d.values()).index(d[96])]):
                                vol = d[0]
                            else:
                                vol = d[96 - n]
                        elif volume.GetMasterVolumeLevel() == d[95]:
                            if n > int(list(d.keys())[list(d.values()).index(d[95])]):
                                vol = d[0]
                            else:
                                vol = d[95 - n]
                        elif volume.GetMasterVolumeLevel() == d[94]:
                            if n > int(list(d.keys())[list(d.values()).index(d[94])]):
                                vol = d[0]
                            else:
                                vol = d[94 - n]
                        elif volume.GetMasterVolumeLevel() == d[93]:
                            if n > int(list(d.keys())[list(d.values()).index(d[93])]):
                                vol = d[0]
                            else:
                                vol = d[93 - n]
                        elif volume.GetMasterVolumeLevel() == d[92]:
                            if n > int(list(d.keys())[list(d.values()).index(d[92])]):
                                vol = d[0]
                            else:
                                vol = d[92 - n]
                        elif volume.GetMasterVolumeLevel() == d[91]:
                            if n > int(list(d.keys())[list(d.values()).index(d[91])]):
                                vol = d[0]
                            else:
                                vol = d[91 - n]
                        elif volume.GetMasterVolumeLevel() == d[90]:
                            if n > int(list(d.keys())[list(d.values()).index(d[90])]):
                                vol = d[0]
                            else:
                                vol = d[90 - n]
                        elif volume.GetMasterVolumeLevel() == d[89]:
                            if n > int(list(d.keys())[list(d.values()).index(d[89])]):
                                vol = d[0]
                            else:
                                vol = d[89 - n]
                        elif volume.GetMasterVolumeLevel() == d[88]:
                            if n > int(list(d.keys())[list(d.values()).index(d[88])]):
                                vol = d[0]
                            else:
                                vol = d[88 - n]
                        elif volume.GetMasterVolumeLevel() == d[87]:
                            if n > int(list(d.keys())[list(d.values()).index(d[87])]):
                                vol = d[0]
                            else:
                                vol = d[87 - n]
                        elif volume.GetMasterVolumeLevel() == d[86]:
                            if n > int(list(d.keys())[list(d.values()).index(d[86])]):
                                vol = d[0]
                            else:
                                vol = d[86 - n]
                        elif volume.GetMasterVolumeLevel() == d[85]:
                            if n > int(list(d.keys())[list(d.values()).index(d[85])]):
                                vol = d[0]
                            else:
                                vol = d[85 - n]
                        elif volume.GetMasterVolumeLevel() == d[84]:
                            if n > int(list(d.keys())[list(d.values()).index(d[84])]):
                                vol = d[0]
                            else:
                                vol = d[84 - n]
                        elif volume.GetMasterVolumeLevel() == d[83]:
                            if n > int(list(d.keys())[list(d.values()).index(d[83])]):
                                vol = d[0]
                            else:
                                vol = d[83 - n]
                        elif volume.GetMasterVolumeLevel() == d[82]:
                            if n > int(list(d.keys())[list(d.values()).index(d[82])]):
                                vol = d[0]
                            else:
                                vol = d[82 - n]
                        elif volume.GetMasterVolumeLevel() == d[81]:
                            if n > int(list(d.keys())[list(d.values()).index(d[81])]):
                                vol = d[0]
                            else:
                                vol = d[81 - n]
                        elif volume.GetMasterVolumeLevel() == d[80]:
                            if n > int(list(d.keys())[list(d.values()).index(d[80])]):
                                vol = d[0]
                            else:
                                vol = d[80 - n]
                        elif volume.GetMasterVolumeLevel() == d[79]:
                            if n > int(list(d.keys())[list(d.values()).index(d[79])]):
                                vol = d[0]
                            else:
                                vol = d[79 - n]
                        elif volume.GetMasterVolumeLevel() == d[78]:
                            if n > int(list(d.keys())[list(d.values()).index(d[78])]):
                                vol = d[0]
                            else:
                                vol = d[78 - n]
                        elif volume.GetMasterVolumeLevel() == d[77]:
                            if n > int(list(d.keys())[list(d.values()).index(d[77])]):
                                vol = d[0]
                            else:
                                vol = d[77 - n]
                        elif volume.GetMasterVolumeLevel() == d[76]:
                            if n > int(list(d.keys())[list(d.values()).index(d[76])]):
                                vol = d[0]
                            else:
                                vol = d[76 - n]
                        elif volume.GetMasterVolumeLevel() == d[75]:
                            if n > int(list(d.keys())[list(d.values()).index(d[75])]):
                                vol = d[0]
                            else:
                                vol = d[75 - n]
                        elif volume.GetMasterVolumeLevel() == d[74]:
                            if n > int(list(d.keys())[list(d.values()).index(d[74])]):
                                vol = d[0]
                            else:
                                vol = d[74 - n]
                        elif volume.GetMasterVolumeLevel() == d[73]:
                            if n > int(list(d.keys())[list(d.values()).index(d[73])]):
                                vol = d[0]
                            else:
                                vol = d[73 - n]
                        elif volume.GetMasterVolumeLevel() == d[72]:
                            if n > int(list(d.keys())[list(d.values()).index(d[72])]):
                                vol = d[0]
                            else:
                                vol = d[72 - n]
                        elif volume.GetMasterVolumeLevel() == d[71]:
                            if n > int(list(d.keys())[list(d.values()).index(d[71])]):
                                vol = d[0]
                            else:
                                vol = d[71 - n]
                        elif volume.GetMasterVolumeLevel() == d[70]:
                            if n > int(list(d.keys())[list(d.values()).index(d[70])]):
                                vol = d[0]
                            else:
                                vol = d[70 - n]
                        elif volume.GetMasterVolumeLevel() == d[69]:
                            if n > int(list(d.keys())[list(d.values()).index(d[69])]):
                                vol = d[0]
                            else:
                                vol = d[69 - n]
                        elif volume.GetMasterVolumeLevel() == d[68]:
                            if n > int(list(d.keys())[list(d.values()).index(d[68])]):
                                vol = d[0]
                            else:
                                vol = d[68 - n]
                        elif volume.GetMasterVolumeLevel() == d[67]:
                            if n > int(list(d.keys())[list(d.values()).index(d[67])]):
                                vol = d[0]
                            else:
                                vol = d[67 - n]
                        elif volume.GetMasterVolumeLevel() == d[66]:
                            if n > int(list(d.keys())[list(d.values()).index(d[66])]):
                                vol = d[0]
                            else:
                                vol = d[66 - n]
                        elif volume.GetMasterVolumeLevel() == d[65]:
                            if n > int(list(d.keys())[list(d.values()).index(d[65])]):
                                vol = d[0]
                            else:
                                vol = d[65 - n]
                        elif volume.GetMasterVolumeLevel() == d[64]:
                            if n > int(list(d.keys())[list(d.values()).index(d[64])]):
                                vol = d[0]
                            else:
                                vol = d[64 - n]
                        elif volume.GetMasterVolumeLevel() == d[63]:
                            if n > int(list(d.keys())[list(d.values()).index(d[63])]):
                                vol = d[0]
                            else:
                                vol = d[63 - n]
                        elif volume.GetMasterVolumeLevel() == d[62]:
                            if n > int(list(d.keys())[list(d.values()).index(d[62])]):
                                vol = d[0]
                            else:
                                vol = d[62 - n]
                        elif volume.GetMasterVolumeLevel() == d[61]:
                            if n > int(list(d.keys())[list(d.values()).index(d[61])]):
                                vol = d[0]
                            else:
                                vol = d[61 - n]
                        elif volume.GetMasterVolumeLevel() == d[60]:
                            if n > int(list(d.keys())[list(d.values()).index(d[60])]):
                                vol = d[0]
                            else:
                                vol = d[60 - n]
                        elif volume.GetMasterVolumeLevel() == d[59]:
                            if n > int(list(d.keys())[list(d.values()).index(d[59])]):
                                vol = d[0]
                            else:
                                vol = d[59 - n]
                        elif volume.GetMasterVolumeLevel() == d[58]:
                            if n > int(list(d.keys())[list(d.values()).index(d[58])]):
                                vol = d[0]
                            else:
                                vol = d[58 - n]
                        elif volume.GetMasterVolumeLevel() == d[57]:
                            if n > int(list(d.keys())[list(d.values()).index(d[57])]):
                                vol = d[0]
                            else:
                                vol = d[57 - n]
                        elif volume.GetMasterVolumeLevel() == d[56]:
                            if n > int(list(d.keys())[list(d.values()).index(d[56])]):
                                vol = d[0]
                            else:
                                vol = d[56 - n]
                        elif volume.GetMasterVolumeLevel() == d[55]:
                            if n > int(list(d.keys())[list(d.values()).index(d[55])]):
                                vol = d[0]
                            else:
                                vol = d[55 - n]
                        elif volume.GetMasterVolumeLevel() == d[54]:
                            if n > int(list(d.keys())[list(d.values()).index(d[54])]):
                                vol = d[0]
                            else:
                                vol = d[54 - n]
                        elif volume.GetMasterVolumeLevel() == d[53]:
                            if n > int(list(d.keys())[list(d.values()).index(d[53])]):
                                vol = d[0]
                            else:
                                vol = d[53 - n]
                        elif volume.GetMasterVolumeLevel() == d[52]:
                            if n > int(list(d.keys())[list(d.values()).index(d[52])]):
                                vol = d[0]
                            else:
                                vol = d[52 - n]
                        elif volume.GetMasterVolumeLevel() == d[51]:
                            if n > int(list(d.keys())[list(d.values()).index(d[51])]):
                                vol = d[0]
                            else:
                                vol = d[51 - n]
                        elif volume.GetMasterVolumeLevel() == d[50]:
                            if n > int(list(d.keys())[list(d.values()).index(d[50])]):
                                vol = d[0]
                            else:
                                vol = d[50 - n]
                        elif volume.GetMasterVolumeLevel() == d[49]:
                            if n > int(list(d.keys())[list(d.values()).index(d[49])]):
                                vol = d[0]
                            else:
                                vol = d[49 - n]
                        elif volume.GetMasterVolumeLevel() == d[48]:
                            if n > int(list(d.keys())[list(d.values()).index(d[48])]):
                                vol = d[0]
                            else:
                                vol = d[48 - n]
                        elif volume.GetMasterVolumeLevel() == d[47]:
                            if n > int(list(d.keys())[list(d.values()).index(d[47])]):
                                vol = d[0]
                            else:
                                vol = d[47 - n]
                        elif volume.GetMasterVolumeLevel() == d[46]:
                            if n > int(list(d.keys())[list(d.values()).index(d[46])]):
                                vol = d[0]
                            else:
                                vol = d[46 - n]
                        elif volume.GetMasterVolumeLevel() == d[45]:
                            if n > int(list(d.keys())[list(d.values()).index(d[45])]):
                                vol = d[0]
                            else:
                                vol = d[45 - n]
                        elif volume.GetMasterVolumeLevel() == d[44]:
                            if n > int(list(d.keys())[list(d.values()).index(d[44])]):
                                vol = d[0]
                            else:
                                vol = d[44 - n]
                        elif volume.GetMasterVolumeLevel() == d[43]:
                            if n > int(list(d.keys())[list(d.values()).index(d[43])]):
                                vol = d[0]
                            else:
                                vol = d[43 - n]
                        elif volume.GetMasterVolumeLevel() == d[42]:
                            if n > int(list(d.keys())[list(d.values()).index(d[42])]):
                                vol = d[0]
                            else:
                                vol = d[42 - n]
                        elif volume.GetMasterVolumeLevel() == d[41]:
                            if n > int(list(d.keys())[list(d.values()).index(d[41])]):
                                vol = d[0]
                            else:
                                vol = d[41 - n]
                        elif volume.GetMasterVolumeLevel() == d[40]:
                            if n > int(list(d.keys())[list(d.values()).index(d[40])]):
                                vol = d[0]
                            else:
                                vol = d[40 - n]
                        elif volume.GetMasterVolumeLevel() == d[39]:
                            if n > int(list(d.keys())[list(d.values()).index(d[39])]):
                                vol = d[0]
                            else:
                                vol = d[39 - n]
                        elif volume.GetMasterVolumeLevel() == d[38]:
                            if n > int(list(d.keys())[list(d.values()).index(d[38])]):
                                vol = d[0]
                            else:
                                vol = d[38 - n]
                        elif volume.GetMasterVolumeLevel() == d[37]:
                            if n > int(list(d.keys())[list(d.values()).index(d[37])]):
                                vol = d[0]
                            else:
                                vol = d[37 - n]
                        elif volume.GetMasterVolumeLevel() == d[36]:
                            if n > int(list(d.keys())[list(d.values()).index(d[36])]):
                                vol = d[0]
                            else:
                                vol = d[36 - n]
                        elif volume.GetMasterVolumeLevel() == d[35]:
                            if n > int(list(d.keys())[list(d.values()).index(d[35])]):
                                vol = d[0]
                            else:
                                vol = d[35 - n]
                        elif volume.GetMasterVolumeLevel() == d[34]:
                            if n > int(list(d.keys())[list(d.values()).index(d[34])]):
                                vol = d[0]
                            else:
                                vol = d[34 - n]
                        elif volume.GetMasterVolumeLevel() == d[33]:
                            if n > int(list(d.keys())[list(d.values()).index(d[33])]):
                                vol = d[0]
                            else:
                                vol = d[33 - n]
                        elif volume.GetMasterVolumeLevel() == d[32]:
                            if n > int(list(d.keys())[list(d.values()).index(d[32])]):
                                vol = d[0]
                            else:
                                vol = d[32 - n]
                        elif volume.GetMasterVolumeLevel() == d[31]:
                            if n > int(list(d.keys())[list(d.values()).index(d[31])]):
                                vol = d[0]
                            else:
                                vol = d[31 - n]
                        elif volume.GetMasterVolumeLevel() == d[30]:
                            if n > int(list(d.keys())[list(d.values()).index(d[30])]):
                                vol = d[0]
                            else:
                                vol = d[30 - n]
                        elif volume.GetMasterVolumeLevel() == d[29]:
                            if n > int(list(d.keys())[list(d.values()).index(d[29])]):
                                vol = d[0]
                            else:
                                vol = d[29 - n]
                        elif volume.GetMasterVolumeLevel() == d[28]:
                            if n > int(list(d.keys())[list(d.values()).index(d[28])]):
                                vol = d[0]
                            else:
                                vol = d[28 - n]
                        elif volume.GetMasterVolumeLevel() == d[27]:
                            if n > int(list(d.keys())[list(d.values()).index(d[27])]):
                                vol = d[0]
                            else:
                                vol = d[27 - n]
                        elif volume.GetMasterVolumeLevel() == d[26]:
                            if n > int(list(d.keys())[list(d.values()).index(d[26])]):
                                vol = d[0]
                            else:
                                vol = d[26 - n]
                        elif volume.GetMasterVolumeLevel() == d[25]:
                            if n > int(list(d.keys())[list(d.values()).index(d[25])]):
                                vol = d[0]
                            else:
                                vol = d[25 - n]
                        elif volume.GetMasterVolumeLevel() == d[24]:
                            if n > int(list(d.keys())[list(d.values()).index(d[24])]):
                                vol = d[0]
                            else:
                                vol = d[24 - n]
                        elif volume.GetMasterVolumeLevel() == d[23]:
                            if n > int(list(d.keys())[list(d.values()).index(d[23])]):
                                vol = d[0]
                            else:
                                vol = d[23 - n]
                        elif volume.GetMasterVolumeLevel() == d[22]:
                            if n > int(list(d.keys())[list(d.values()).index(d[22])]):
                                vol = d[0]
                            else:
                                vol = d[22 - n]
                        elif volume.GetMasterVolumeLevel() == d[21]:
                            if n > int(list(d.keys())[list(d.values()).index(d[21])]):
                                vol = d[0]
                            else:
                                vol = d[21 - n]
                        elif volume.GetMasterVolumeLevel() == d[20]:
                            if n > int(list(d.keys())[list(d.values()).index(d[20])]):
                                vol = d[0]
                            else:
                                vol = d[20 - n]
                        elif volume.GetMasterVolumeLevel() == d[19]:
                            if n > int(list(d.keys())[list(d.values()).index(d[19])]):
                                vol = d[0]
                            else:
                                vol = d[19 - n]
                        elif volume.GetMasterVolumeLevel() == d[18]:
                            if n > int(list(d.keys())[list(d.values()).index(d[18])]):
                                vol = d[0]
                            else:
                                vol = d[18 - n]
                        elif volume.GetMasterVolumeLevel() == d[17]:
                            if n > int(list(d.keys())[list(d.values()).index(d[17])]):
                                vol = d[0]
                            else:
                                vol = d[17 - n]
                        elif volume.GetMasterVolumeLevel() == d[16]:
                            if n > int(list(d.keys())[list(d.values()).index(d[16])]):
                                vol = d[0]
                            else:
                                vol = d[16 - n]
                        elif volume.GetMasterVolumeLevel() == d[15]:
                            if n > int(list(d.keys())[list(d.values()).index(d[15])]):
                                vol = d[0]
                            else:
                                vol = d[15 - n]
                        elif volume.GetMasterVolumeLevel() == d[14]:
                            if n > int(list(d.keys())[list(d.values()).index(d[14])]):
                                vol = d[0]
                            else:
                                vol = d[14 - n]
                        elif volume.GetMasterVolumeLevel() == d[13]:
                            if n > int(list(d.keys())[list(d.values()).index(d[13])]):
                                vol = d[0]
                            else:
                                vol = d[13 - n]
                        elif volume.GetMasterVolumeLevel() == d[12]:
                            if n > int(list(d.keys())[list(d.values()).index(d[12])]):
                                vol = d[0]
                            else:
                                vol = d[12 - n]
                        elif volume.GetMasterVolumeLevel() == d[11]:
                            if n > int(list(d.keys())[list(d.values()).index(d[11])]):
                                vol = d[0]
                            else:
                                vol = d[11 - n]
                        elif volume.GetMasterVolumeLevel() == d[10]:
                            if n > int(list(d.keys())[list(d.values()).index(d[10])]):
                                vol = d[0]
                            else:
                                vol = d[10 - n]
                        elif volume.GetMasterVolumeLevel() == d[9]:
                            if n > int(list(d.keys())[list(d.values()).index(d[9])]):
                                vol = d[0]
                            else:
                                vol = d[9 - n]
                        elif volume.GetMasterVolumeLevel() == d[8]:
                            if n > int(list(d.keys())[list(d.values()).index(d[8])]):
                                vol = d[0]
                            else:
                                vol = d[8 - n]
                        elif volume.GetMasterVolumeLevel() == d[7]:
                            if n > int(list(d.keys())[list(d.values()).index(d[7])]):
                                vol = d[0]
                            else:
                                vol = d[7 - n]
                        elif volume.GetMasterVolumeLevel() == d[6]:
                            if n > int(list(d.keys())[list(d.values()).index(d[6])]):
                                vol = d[0]
                            else:
                                vol = d[6 - n]
                        elif volume.GetMasterVolumeLevel() == d[5]:
                            if n > int(list(d.keys())[list(d.values()).index(d[5])]):
                                vol = d[0]
                            else:
                                vol = d[5 - n]
                        elif volume.GetMasterVolumeLevel() == d[4]:
                            if n > int(list(d.keys())[list(d.values()).index(d[4])]):
                                vol = d[0]
                            else:
                                vol = d[4 - n]
                        elif volume.GetMasterVolumeLevel() == d[3]:
                            if n > int(list(d.keys())[list(d.values()).index(d[3])]):
                                vol = d[0]
                            else:
                                vol = d[3 - n]
                        elif volume.GetMasterVolumeLevel() == d[2]:
                            if n > int(list(d.keys())[list(d.values()).index(d[2])]):
                                vol = d[0]
                            else:
                                vol = d[2 - n]
                        elif volume.GetMasterVolumeLevel() == d[1]:
                            if n > int(list(d.keys())[list(d.values()).index(d[1])]):
                                vol = d[0]
                            else:
                                vol = d[1 - n]
                        elif volume.GetMasterVolumeLevel() == d[0]:
                            vol = d[0]

                        return vol

                    nums = re.findall('[0-9]+', oper)
                    num = int(nums[0])
                    volume.SetMasterVolumeLevel(volume_control_min(num), None)

                    tts.say("Громкость уменьшена на" + ' ' + str(num))
                    tts.runAndWait()
                    self.main_text.setText("Громкость уменьшена на" + ' ' + str(num))
                    self.main_text.adjustSize()

            else:
                tts.say("Я вас не понял")
                tts.runAndWait()
                self.main_text.setText('Я вас не понял')  # если не понял написать - (Я вас не понял)
                self.main_text.adjustSize()

        except speech_recognition.UnknownValueError:
            tts.say("Я вас не понял")
            tts.runAndWait()
            self.main_text.setText('Я вас не понял')  # если не понял написать - (Я вас не понял)
            self.main_text.adjustSize()
            return 'Я вас не понял'


def application():  # создание приложения и получение системных настроек
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec_())  # закрытие приложения


if __name__ == "__main__":  # запуск приложения
    application()
