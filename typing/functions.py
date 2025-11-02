""" functios for analyzing text"""

def clean_console():
    """Clean console"""
    print(chr(27) + "[2J" + chr(27) + "[;H")

def read_file(file):
    """Read file"""
    with open(file, 'r', encoding='UTF-8') as filehandler:
        list_lines = filehandler.readlines()
        return list_lines

def write_file(file, text):
    """Write file"""
    with open(file, 'a', encoding='UTF-8') as filehandler:
        filehandler.write(text + "\n")

def sort_chars(item):
    """Sort function"""
    return (item[1], item[0])

def sort_scores(item):
    """Sort scores"""
    f_sorting = {"hard": 0, "medium": 1, "easy": 2}
    return (f_sorting.get(item[2], 0), -float(item[1]))

def save_scores(name, precision, grade):
    """Save scores"""
    write_file("score.txt", f"{name.strip()}: {precision}% {grade.strip()}")

def get_grade(filename):
    """ Get the grade level based on the filename. """
    try:
        if filename == "easy.txt":
            return "easy"
        if filename == "medium.txt":
            return "medium"
        if filename == "hard.txt":
            return "hard"
    except FileExistsError:
        print("file does not exist")
    return None

def count_words(text):
    """Analyze text and return number of words."""
    words = text.split()
    return len(words)

def count_chars_in_words(words):
    """Count all characters of each word"""
    total_chars = 0
    words = words.split()
    for word in words:
        total_chars += len(word)
    return total_chars

def show_score_file(file):
    """shows the sorted results in score.txt"""
    try:
        lines = read_file(file)
    except FileNotFoundError:
        return "there is no result to show, please start the test!"
    scores = []
    for line in lines:
        split_line = line.strip().rsplit(' ', 2)
        scores.append((split_line))
    for index in scores:
        index[1]=float(index[1].replace("%",""))
    sorted_scores=sorted(scores, key=sort_scores)
    result = []
    for name, precision, grade in sorted_scores:
        result.append(f"{name} {precision}% {grade}")
    return "\n".join(result)


def limit_inp_words(orginal, user_input):
    """ignores the extra words in the input"""
    org_words = orginal.split()
    input_words = user_input.split()
    limit_input_words = []

    for i in range(len(org_words)):
        if i < len(input_words):
            limit_input_words.append(input_words[i])

    return limit_input_words

def count_wrong_words(orginal, user_input):
    """Count the number of wrong words"""
    org_words = orginal.split()
    input_words = limit_inp_words(orginal, user_input)
    wrong_words = 0
    for word in org_words:
        if  word not in input_words:
            wrong_words += 1
    return wrong_words


def count_wrong_chars(orginal, user_input):
    """count the number of wrong chars"""
    org_words = orginal.split()
    input_words = user_input.split()
    wrong_chars = 0
    for i, org_word in enumerate(org_words):
        if i < len(input_words):
            inp_word = input_words[i]
            for j, char in enumerate(org_word):
                if j < len(inp_word):
                    if char != inp_word[j]:
                        wrong_chars += 1
                else:
                    wrong_chars += 1
        else:
            wrong_chars += len(org_word)

    return wrong_chars


def count_misspelled_chars(orginal, user_input):
    """Calculate misspelled chars"""
    misspelled_chars = {}
    org_words = orginal.split()
    input_words= user_input.split()
    word_length = 0
    if len(org_words) < len(input_words):
        word_length = len(org_words)
    else:
        word_length = len(input_words)

    for i in range(word_length):
        org_word = org_words[i]
        inp_word = input_words[i]

        for j, char in enumerate(org_word):
            if j < len(inp_word) and char != inp_word[j]:
                if char != ' ':
                    if char in misspelled_chars:
                        misspelled_chars[char] += 1
                    else:
                        misspelled_chars[char] = 1
            elif j >= len(inp_word):
                if char != ' ':
                    if char in misspelled_chars:
                        misspelled_chars[char] += 1
                    else:
                        misspelled_chars[char] = 1

    for i in range(word_length, len(org_words)):
        current_word = org_words[i]
        if current_word != ' ':
            for char in current_word:
                if char in misspelled_chars:
                    misspelled_chars[char] += 1
                else:
                    misspelled_chars[char] = 1

    sorted_chars= sorted(misspelled_chars.items(), key=sort_chars, reverse=True)
    result = {}
    for char, count in sorted_chars:
        result[char] = count
    return result

def calculate_precision(wrong, total):
    """calculate precision"""
    precision = round(((total- wrong) / total * 100), 2)
    return precision

def show_results(word_precision,char_precision,misspelled_chars):
    """ show results"""
    print("-" * 40)
    print(f"ordprecision: {word_precision}%\nTeckenprecision: {char_precision}%\nFelstavaden tecken:{misspelled_chars}")
    print("-" * 40)

def test_function(filename):
    """run the typing test"""
    lines = read_file(filename)
    total_org_word = count_words(" ".join(lines))
    total_org_char = count_chars_in_words(" ".join(lines))
    wrong_words=0
    wrong_chars=0
    total_misspelled = {}

    word_precision=calculate_precision(wrong_words, total_org_word)
    char_precision=calculate_precision(wrong_chars, total_org_char)
    show_results(word_precision,char_precision,"\n".join(total_misspelled))

    for line in lines:
        print("write the sentence below\n" + ("-" * 30))
        print(line.strip())
        user_inputs = input("").strip()
        clean_console()
        wrong_words_temp = count_wrong_words(line.strip(), user_inputs)
        wrong_words += wrong_words_temp
        word_precision =(calculate_precision(wrong_words,total_org_word ))

        wrong_chars_temp = count_wrong_chars(line.strip(), user_inputs)
        wrong_chars += wrong_chars_temp
        char_precision =(calculate_precision(wrong_chars,total_org_char ))

        misspelled_chars = count_misspelled_chars(line.strip(), user_inputs)
        for char, count in misspelled_chars.items():
            if char in total_misspelled:
                total_misspelled[char] += count
            else:
                total_misspelled[char] = count

        sorted_chars = {}
        sorted_chars= sorted(total_misspelled.items(), key=sort_chars, reverse=True)
        total_misspelled_chars ="\n".join(f"{char}: {count}" for char, count in sorted_chars)

        show_results(word_precision,char_precision,total_misspelled_chars)

    clean_console()
    print("you finished the test!\n")

    input("Press enter to see results")
    clean_console()
    show_results(word_precision,char_precision,total_misspelled_chars)

    username = input("Enter your name to add to highscore: ")
    clean_console()
    grade = get_grade(filename)
    save_scores(username, word_precision, grade)
    print("Your result is saved.")
