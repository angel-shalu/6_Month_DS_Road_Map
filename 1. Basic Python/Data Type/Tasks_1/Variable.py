# Variables in Python

first_name = 'SHALINI'
last_name = 'KUMARI'
country = 'Madhya Pradesh'
city = 'Bhopal'
age = 7888749
is_married = False
skills = ['HTML', 'CSS', 'SQL', 'Java', 'Python']
person_info = {
    'firstname':'Shalu', 
    'lastname':'Shalini', 
    'country':'India',
    'city':'Bhopal'
    }

# Printing the values stored in the variables

print('First name:', first_name)
print('First name length:', len(first_name))
print('Last name: ', last_name)
print('Last name length: ', len(last_name))
print('Country: ', country)
print('City: ', city)
print('Age: ', age)
print('Married: ', is_married)
print('Skills: ', skills)
print('Person information: ', person_info)


# Declaring multiple variables in one line

first_name, last_name, country, age, is_married = 'Shalu', 'Shalini', 'Bhopal', 250, False

print(first_name, last_name, country, age, is_married)
print('First name:', first_name)
print('Last name: ', last_name)
print('Country: ', country)
print('Age: ', age)
print('Married: ', is_married)