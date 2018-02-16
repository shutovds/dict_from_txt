import re

class Word():

    def __init__(self, word):
        
        self.word = word
        self.frequency = 1
        self.transcription =''
        self.translation = ''

        
    def set_to_dict(self, dictionary):

        if self.word in dictionary:
            self.frequency=dictionary[self.word][0] + 1
            
        dictionary[self.word]=[self.frequency, [self.transcription, self.translation]]


    def rem_from_dict(self, dictionary):
        if self.word in dictionary:
            del dictionary[self.word]
            
#-----------------
            
#read data from txt
def read_from_txt(filename):
    
    file = open(filename, 'r')
    f=re.split(r'\W+'  ,file.read())
    file.close()
    return f


#read words from anki dictionarry  'Английский слова.txt'
def read_from_anki_txt(filename):
    file = open(filename)
    i=0
    words = []
    for line in file:
        word = line.split(None, 1)[0]
        words.append(word)
    file.close()
    return words

#-----------------  

def rem_from(stopwords, dictionary):
    for sword in stopwords:
        inst = Word(sword)
        inst.rem_from_dict(dictionary)
    return dictionary

#-----------------  

def write_to_txt(filename, word):
    file=open(filename, 'a')
    file.write(word+'\n')
    file.close()

#-----------------    

def frecWordsFromBook(filename):
    wdict ={}

    #read a book fele
    words = read_from_txt(filename)
    for word in words:
        inst = Word(word)
        inst.set_to_dict(wdict)
        
    new_words_number =len(wdict)
    #print('Количество слов в тексте ', filename, ' = ', new_words_number)

    stopwords = read_from_txt('stopwords.txt')
    wdict = rem_from(stopwords, wdict)

    stopwords = read_from_txt('for_Anki_words.txt')
    wdict = rem_from(stopwords, wdict)

    ankiwords = read_from_anki_txt('Английский слова.txt')
    wdict = rem_from(ankiwords, wdict)
        

    # words sorted by friequency
    #frecWords=sorted(wdict.items(), key=lambda item: item[1], reverse = True)

    return wdict #frecWords

#---------------------------------------------------



mainWords = frecWordsFromBook('book_textfile.txt')
sorted_words=sorted(mainWords.items(), key=lambda item: item[1], reverse = True)

part_book_words = frecWordsFromBook('book_textfile_reading_now.txt')
sorted_part_book_words = sorted(part_book_words.items(), key=lambda item: item[1], reverse = True)

weight_part_book_words = {}
unknown_words_number = 0
for word in sorted_part_book_words:
    w = word[0]
    if w in mainWords:
        weight_part_book_words[w]=[word[1][0] + mainWords[w][0], word[1][0], mainWords[w][0]]
        unknown_words_number += word[1][0]
        
sorted_weight_part_book_words = sorted(weight_part_book_words.items(), key=lambda item: item[1], reverse = True)
#print(sorted_weight_part_book_words)



all_words_intext=read_from_txt('book_textfile_reading_now.txt')
print('Всего слов в отрывке: ', len(all_words_intext))
print('Количество необработанных слов в отрывке: ', unknown_words_number)
percets = ((len(all_words_intext) - unknown_words_number)/len(all_words_intext))*100
print('Процент проработки/знания лексики отрывка: %3.4f %%' % (percets))
    

#interface ------------------------------------


new_words_number = len(sorted_words)
print('\nКоличество новых слов в лексической базе (во всех текстах) =  ', new_words_number)

new_part_book_words_number = len(sorted_part_book_words)
print('Количество новых слов в отрывке', new_part_book_words_number, '\n')

#-------

procede_words = input("""Если Вы хотите обработать слова из (всех текстов)  - введите   y,
                                                                                         - если не хотите - нажмите Enter:  """)
if procede_words == 'y':
    print(' Добавить слово в стоп слова - Enter, в словарь для изучения - d, пропустить слово -p ')
    for word in sorted_words:

        print(word[1][0], '  -  ', word[0], '  -  ', new_words_number)
        new_words_number -= 1
        action = input(' : ')
        print(action)
        
        if action == '':
            write_to_txt('stopwords.txt', word[0])
        elif action =='d':
            write_to_txt('for_Anki_words.txt', word[0])
        elif action =='p':
            pass

#-------

procede_words = input("""\nЕсли Вы хотите обработать слова       (из отрывка)    - введите   y,
                                                                                         - если не хотите - нажмите Enter:  """)
        
if procede_words == 'y':
    print(' Добавить слово в стоп слова - Enter, в словарь для изучения - d, пропустить слово -p ')
    for word in sorted_weight_part_book_words:
        
        print(word[1][0], '  -  ', word[0], '  -  осталось слов:', new_part_book_words_number, \
              ',  встречаемость общая: ', word[1][2], ', в данном отрывке: ', word[1][1])
        
        new_part_book_words_number -= 1
        action = input(' : ')
        print(action)
        
        if action == '':
            write_to_txt('stopwords.txt', word[0])
        elif action =='d':
            write_to_txt('for_Anki_words.txt', word[0])
        elif action =='p':
            pass






