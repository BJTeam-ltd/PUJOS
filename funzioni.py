
# Validazione input: controlla la lunghezza e restituisce la stringa validata
# Continua a chiedere l'input per 5 volte
def input_val(max_len = 43):
    c = 1
    validated = False   # Input non ancora validato

    while not validated:
        in_str = input()
        if len(in_str) < max_len:   # Controllo massima lunghezza
            validated = True
        elif c > 5:
            exit(5)
        else:
            print('Invalid input')
            c += 1

    return in_str
