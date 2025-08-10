# Single line comment

letter = 'P'                # A string could be a single character or a bunch of texts
print(letter)               # P
print(len(letter))          # 1

greeting = 'Hello, World!'  # String could be  a single or double quote,"Hello, World!"
print(greeting)             # Hello, World!
print(len(greeting))        # 13

sentence = "I hope you are enjoying 30 days of python challenge"
print(sentence)



# Multiline String

multiline_string = '''I am a teacher and enjoy teaching.  
I didn't find anything as rewarding as empowering people.
That is why I created 30 days of python.'''
print(multiline_string)

# Another way of doing the same thing
multiline_string = """I am a teacher and enjoy teaching.
I didn't find anything as rewarding as empowering people.
That is why I created 30 days of python."""
print(multiline_string)


## String Concatenation
first_name = "Angel"
last_name = "Shalu"
space = " "
full_name = first_name + space + last_name
print(full_name)    # Angel Shalu

## Checking length of a string using len() builtin function
print(len(first_name))   #5
print(len(last_name))    #5
print(len(first_name)) ==  print(len(last_name))   # True
print(len(full_name))    #11


## Unpacking Character
language = "Python"
a,b,c,d,e,f = language    ## unpacking sequence characters into variables
print(a)   # P
print(b)   # y
print(c)   # t
print(d)   # h
print(e)   # o
print(f)   # n


# Accessing characters in strings by index
language = "Python"
first_letter = language[0]
print(first_letter)   # P

second_letter = language[1]
print(second_letter)   # y

last_index = len(language) - 1
last_letter = language[last_index]
print(last_letter)    # n

## If we want to start from right end we can use negative indexing. -1 is the last index
language = 'Python'
last_letter = language[-1]
print(last_letter) # n
second_last = language[-2]
print(second_last) # o



## Slicing

language = 'Python'
first_three = language[0:3] # starts at zero index and up to 3 but not include 3
last_three = language[3:6]
print(last_three) # hon

# Another way
last_three = language[-3:]
print(last_three)   # hon
last_three = language[3:]
print(last_three)   # hon

## Skipping character while splitting Python strings
language = 'Python'
pto = language[0:6:2] # 
print(pto) # pto


# Escape sequence
print('I hope every one enjoying the python challenge.\nDo you ?') # line break
print('Days\tTopics\tExercises')
print('Day 1\t3\t5')
print('Day 2\t3\t5')
print('Day 3\t3\t5')
print('Day 4\t3\t5')
print('This is a back slash  symbol (\\)') # To write a back slash
print('In every programming language it starts with \"Hello, World!\"')



## String Methods

# capitalize(): Converts the first character the string to Capital Letter
challenge = "thirty day of python"
print(challenge.capitalize())

# count(): returns occurrences of substring in string, count(substring, start=.., end=..)
challege = "thirty day of python"
print(challenge.count("y"))   # 3
print(challenge.count("y",7, 14))   # 1
print(challenge.count("th"))

# endswith(): Checks if a string ends with a specified ending
challenge = 'thirty days of python'
print(challenge.endswith('on'))   # True
print(challenge.endswith('tion')) # False

# expandtabs(): Replaces tab character with spaces, default tab size is 8. It takes tab size argument
challenge = 'thirty\tdays\tof\tpython'
print(challenge.expandtabs())   # 'thirty  days    of      python'
print(challenge.expandtabs(10)) # 'thirty    days      of        python'

