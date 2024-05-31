def word_replace(filename, old_word, new_word):
    file = open(filename, 'r', encoding='utf-8')
    filedata = file.read()
    data = filedata.replace(old_word, new_word)
    file = open(filename, 'w', encoding='utf-8')
    file.write(data)
