import random
import sys
import threading
import multiprocessing
import time


#################      Konfiguration     #################

log_mode = "Y"  # "X" für Konsole, "Y" für Log

n = int(23)  # Zahl, die getestet werden soll

why_not = "j"  # "j" um 2^2^n zu berechnen

# Ab 23 wird why_not nicht mehr in der Konsole dargestellt, test läuft aber
# 20 < 1sec | 21 < 5sec | 22 ~ 20sec | 23 > 80sec 
fermat_bei_why_not = "yesplease"  # "yesplease" fermat bei why_not


# HINWEIS: OHNE FERMAT TESTEN (DAUERT EWIG)
# Bei zu großen Zahlen (mit why_not aktiv) wird die Zahl zu groß.
# Gerne eine 0 mehr einfügen, dadurch wird die größe 
# zumindest ein wenig umgangen

#Standard 8300
sys.set_int_max_str_digits(15000000)

#################      ab hier nichts ändern     #################

if log_mode == "Y":
    with open('log.txt', 'w') as f:
        f.write('')

def calculate_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Die Berechnung hat {total_time:.4f} Sekunden gedauert.")
        return result
    return wrapper


def is_prime(num):
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False

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
            output_str = f"{result}\nist wahrscheinlich prim"
        else:
            output_str = f"{result}\nist zusammengesetzt"
    else:
        output_str = str(result)

    if log_mode == "X":
        print(output_str)
    elif log_mode == "Y":
        with open("log.txt", "a") as f:
            f.write(f"{output_str}\n")


def why_not_thread(start, end, thread_results):
    for i in range(start, end):
        result = pow(2, pow(2, i))
        if is_prime(result):
            thread_results.append(result)
            break


@calculate_time
def run_threads():
    global thread_results
    thread_results = []
    threads = []
    num_threads = multiprocessing.cpu_count()
    chunk_size = (6 - n) // num_threads
    if chunk_size == 0:
        chunk_size = 1
    for i in range(n + 1, 6, chunk_size):
        t = threading.Thread(
            target=why_not_thread, args=(i, i + chunk_size, thread_results)
        )
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