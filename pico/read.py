lines = ['Readme', 'How to write text files in Python']
test = 'im another testing string!!!!!!!!!!!!!!!!!'
with open('readme.txt', 'a') as f:
    f.write(test + '\n')