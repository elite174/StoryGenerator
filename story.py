import random

d = {}
asd = '123'

a = [1, 2, 3]


def correct_line(line):
    line = line.strip()
    line = line.replace(',', ' ,')
    line = line.replace('.', ' .')
    line = line.replace('!', ' !')
    line = line.replace('?', ' ?')
    line = line.replace('"', '')
    line = line.replace(':', ' :')
    line = line.replace(';', ' ;')
    # print(line)
    return line


def get_word(word):
    word = word.lower()
    if word in d:
        data = d[word]
        data.sort(key=lambda item: item[1], reverse=True)
        counters = [item[1] for item in data]
        sum = 0
        for i in counters:
            sum += i
        pr = random.random()
        p = 0
        for i in range(len(counters)):
            p += counters[i] / sum
            if pr <= p:
                return data[i][0]
    else:
        return '-1'


def add_word(word, next_word):
    word = word.lower()
    if word in d:
        number = -1
        for i in range(len(d[word])):
            item = d[word][i]
            if item[0] == next_word:
                number = i
                break
        if number != -1:
            count = d[word][number][1]
            count += 1
            d[word].remove(d[word][number])
            d[word].append((next_word, count))
        else:
            d[word].append((next_word, 1))
    else:
        d[word] = [(next_word, 1)]


signs = [',', '.', '!', '?', ':', ';']
start_words = set()


def analyze(line, last):
    global d, start_words
    data = line.split(' ')
    new_data = []
    if last != '' and last != ' ':
        new_data = [last]
    for i in data:
        if i != '' and i != ' ':
            new_data.append(i.strip())
    for i in range(len(new_data) - 1):
        if not ((new_data[i] in signs) and (new_data[i + 1] in signs)):
            if (not (new_data[i][0]).islower()) and not (new_data[i][0] in signs):
                start_words.add(new_data[i])
            add_word(new_data[i], new_data[i + 1])
    return new_data[len(new_data) - 1].strip()


def generate_text(count_of_words):
    rand = random.randint(0, len(start_words) - 1)
    word = list(start_words)[rand]
    file = open('out.txt', 'w', encoding='utf-8')
    file.write(word + ' ')
    word = word.lower()
    count = 0
    while count < count_of_words:
        word = get_word(word)
        if word == '-1':
            break
        if word in signs:
            file.write(word)
            if word == '.' or word == '?' or word == '!':
                count += 1
        else:
            file.write(' ' + word)
        word = word.lower()
        if not (word in d):
            file.close()
            break

    file.close()


def create_dict(filename):
    file = open(filename, 'r', encoding='utf-8')
    last = ''
    for line in file:
        last = analyze(correct_line(line), last)
    file.close()


create_dict('kafka.txt')

generate_text(10)
