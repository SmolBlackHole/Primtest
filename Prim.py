import random
import sys
import threading

log_mode = "X" # "X" für Konsole, "Y" für Log

n = int(42069) # Zahl, die getestet werden soll

# Wenn why_not "j" braucht alles ab 20 ewig
why_not = "n" # "j" um 2^2^n zu berechnen 

# (why_not muss für Fermattest von why_not aktiv sein) 
# 20 ~ 1sec
# 21 < 5sec
# 23 > 90sec (Berechnet, zeigt aber nichts mehr an mit Konsolenlog)
fermat_bei_why_not = "nahbro" # "yesplease" fermat bei why_not


#################      ab hier nichts ändern     ################# 

# weiter unten sind die Threads einstellbar

# Eine 0 mehr schadet nicht (bringt aber nichts)
# (Berechnung braucht ewig je größer n mit why_not "j")
sys.set_int_max_str_digits(15000000)

def is_prime(num):
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False

    # Fermattest mit 10 zufälligen basen
    for i in range(num - 1):
        base = random.randint(2, num - 1)
        result = pow(base, num - 1, num)
        if result != 1:
            return False
    return True

def calculate_why_not():
    result = pow(2, pow(2, n))
    if fermat_bei_why_not == "yesplease":
        if is_prime(result):
            print(f"{result} ist wahrscheinlich prim")
        else:
            print(f"{result} ist zusammengesetzt")
    else:
        if log_mode == "X":
            print(result)
        elif log_mode == "Y":
            with open("log.txt", "a") as f:
                f.write(f"{result}\n")

def why_not_thread(start, end):
    for i in range(start, end):
        result = pow(2, pow(2, i))
        if is_prime(result):
            thread_results.append(result)
            break

def run_threads():
    global thread_results
    thread_results = []
    threads = []

    # Standard 4
    chunk_size = (6 - n) // 4
    if chunk_size == 0:
        chunk_size = 1
    for i in range(n+1, 6, chunk_size):
        t = threading.Thread(target=why_not_thread, args=(i, i+chunk_size))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    if thread_results:
        result = thread_results[0]
        if fermat_bei_why_not == "yesplease":
            if is_prime(result):
                print(f"{result} ist wahrscheinlich prim")
            else:
                print(f"{result} ist zusammengesetzt")
        else:
            if log_mode == "X":
                print(result)
            elif log_mode == "Y":
                with open("log.txt", "a") as f:
                    f.write(f"{result}\n")
    else:
        calculate_why_not()

if why_not == "j":
    if n < 6:
        calculate_why_not()
    else:
        run_threads()
else:
    if is_prime(n):
        print(f"{n} ist wahrscheinlich prim")
    else:
        print(f"{n} ist zusammengesetzt")