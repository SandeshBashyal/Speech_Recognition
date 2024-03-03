import string

def remove_punctuation(input_string):
    # Make a translation table
    translator = str.maketrans('', '', string.punctuation)

    # Use the translate method to remove punctuation
    no_punct = input_string.translate(translator)

    return no_punct

# Example usage
original_string = "i love you."
string_without_punctuation = remove_punctuation(original_string)

print("Original string:", original_string)
print("String without punctuation:", string_without_punctuation)

phrase_to_character = {'open the door': 'A'}

# Accessing the mapping
input_phrase = 'open the door'

mapped_character = phrase_to_character.get(input_phrase, 'Not mapped')

print(f"The character for the phrase '{input_phrase}' is: {mapped_character}")

# Example usage
mapped_phrase_to_character ={
        'open the door' : 'A',
        'close the door' : 'B',
        'turn on the bulb' : 'C',
        'turn off the bulb' : 'D',
    }

def map_character(input_phrase, mapped_phrase = mapped_phrase_to_character):
    mapped_character = mapped_phrase.get(input_phrase, 'Not mapped')
    return mapped_character

input_phrase = 'open the door'
result = map_character(input_phrase)
print(f'{result}')
print(f"The character for the phrase '{input_phrase}' is: {result}")

