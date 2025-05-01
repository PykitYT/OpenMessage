import sys
import os
import shutil

# Переменные для режима
debug = False
get_output = False
safe_mode = False
update_mode = False

# Функция для дебага
def deb(text):
    if debug:
        print(f"[debug] {text}")

# Функция для вывода только результата команды (если --get)
def output(text):
    if get_output:
        print(text)

# Обработка аргументов
try:
    if sys.argv[1] == "--debug":
        debug = True
    elif sys.argv[1] == "--get":
        get_output = True
    elif sys.argv[1] == "--reset":
        # Удаление системы и папки plugins
        if os.path.exists("plugins"):
            shutil.rmtree("plugins")  # Удаляет всю папку plugins и её содержимое
            output("System reset: 'plugins' folder deleted.")
        else:
            output("'plugins' folder does not exist.")
        exit()  # Завершаем выполнение программы после сброса
    elif sys.argv[1] == "--safe":
        safe_mode = True
    elif sys.argv[1] == "--update":
        update_mode = True
except IndexError:
    pass

# Плагины и их обработка
command = {}
start_plugins = {}

def process(file):
    try:
        text = open("plugins/" + file).read()
        strt = text.splitlines()[0]
        if strt == "#msg":
            command[file] = text
            deb(f"Loaded msg plugin: {file}")
        elif strt == "#start":
            start_plugins[file] = text
            deb(f"Loaded start plugin: {file}")
        else:
            print("Error loading plugin:", strt)
    except Exception as e:
        print(f"Plugin load failed: {file}, {type(e)} {e}")

def run(msg):
    for a, b in command.items():
        deb(f"Running plugin: {a} with command: {msg}")
        try:
            exec(b, globals(), {'c': msg})
        except Exception as e:
            deb(f"Error in plugin {a}: {type(e)} {e}")

def run_start_plugins():
    for a, b in start_plugins.items():
        deb(f"Running start plugin: {a}")
        try:
            exec(b, globals())
        except Exception as e:
            deb(f"Error in start plugin {a}: {type(e)} {e}")

def plg():
    for i in os.listdir("plugins/"):
        deb(f"Processing plugin: {i}")
        process(i)

# Основная программа
print("OpenCommand")
# Печатаем параметры загрузки через print
print("Loading system parameters:")
print(" - Debug mode: " + str(debug))
print(" - Get mode: " + str(get_output))
print(" - Safe mode: " + str(safe_mode))
print(" - Update mode: " + str(update_mode))

# Проверка и загрузка плагинов
try:
    plg()
    can = True
    output("Plugins loaded successfully.")
except:
    output("Use --update to install system.")
    can = False

run_start_plugins()

try:
    if sys.argv[1] == "--safe":
        command, start_plugins = {}, {}
        output("Safe mode activated: Resetting commands and plugins.")
    elif sys.argv[1] == "--update":
        con = True
        output("Welcome to installer")
        output("Press enter to continue")
        input()
        output("Warning! File main.exe can't be in Documents, create new folder!")
        output("Press ctrl+c to continue or enter to install")
        try:
            input()
        except:
            con = False
        if con:
            try:
                os.makedirs("./plugins")
                with open("./plugins/tutor.py", 'w') as file:
                    file.write("""#msg

#Tutorial
# #msg means run on message
# #start means on start
if c == "tutor":
    print("Tutorial")
    print("#msg means run on message")
    print("#start means run on start")
""")
            except Exception as e:
                output("Failed to load! " + str(type(e)) + " " + str(e))
        output("Finished!")
    elif sys.argv[1] == "--reset":
        # Этот код уже выполнится при использовании --reset, так что можно пропустить
        pass

except IndexError:
    pass

if not can:
    exit()

# Главный цикл
while True:
    try:
        c = input(">.>.>")
        
        if c == "":
            continue  # Просто ждем ввода команд

        if c == "safe-test":
            output("Safe-Test 1.0")
            text = ""
            for i in range(51):
                output("Processing " + str(i))
                text += str(i)
                output("Text " + text)
            output("Done\n" + text)
            output("Safe-Test End")

        run(c)

    except KeyboardInterrupt:
        break  # Выход из программы при нажатии Ctrl+C
