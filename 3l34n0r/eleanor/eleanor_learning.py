import nltk

from pyMiniTele import telegram

nltk.data.path.append('~/Workspace/nltk_data')

INDEX = TOKEN = 0; TUPLE = TAG = 1

memory = dict()

def find_pos_index(tagged_tokens, pos):
    ''' Returns a list of indices of a pos in tagged_tokens '''

    pos_index_list = list()
    for tag in enumerate(tagged_tokens):
        if tag[TUPLE][TAG] in pos:
            pos_index_list += [tag[INDEX]]
    
    return pos_index_list

def main():
    tokens = nltk.word_tokenize(input('>>> '))
    tagged = nltk.pos_tag(tokens)
    
    index_VBZ = find_pos_index(tagged, ['VBZ', 'VBP'])[0]
    index_PRPS = find_pos_index(tagged, ['PRP$'])[0]

    if index_VBZ > index_PRPS:
        key = tagged[index_PRPS][TOKEN].lower()
        sub = tagged[index_PRPS + 1][TOKEN]
        obj = tagged[index_VBZ + 1][TOKEN]

        if key not in memory.keys():
            memory[key] = dict()
        memory[key][sub] = obj
    
    print(memory)

while 1:
    main()
