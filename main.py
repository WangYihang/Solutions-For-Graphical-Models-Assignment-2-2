#!/usr/bin/env python

import random
import string
import sys
import enchant

from colorama import init
from colorama import Fore
from termcolor import colored

init(autoreset=True)

def printer(data):
    sys.stdout.write(data)

def random_string(length=4, charset=string.ascii_lowercase):
    return "".join([random.choice(charset) for _ in range(length)])

def valid_word(letters):
    return enchant.Dict("en_US").check(letters)

def assignment_2_a(filenamefilename):
    results = []
    for i in range(100):
        letters = random_string()
        results.append(letters)
    return results

def analysis_letter_probalities(filename):
    frequencies = dict()
    with open(filename) as f:
        for line in f:
            for ch in line.lower():
                if ch not in frequencies.keys():
                    frequencies[ch] = 1
                else:
                    frequencies[ch] += 1
    probabilities = dict()
    total_letters = 0
    for i in string.ascii_lowercase:
        if i in frequencies.keys():
            total_letters += frequencies[i]

    for i in string.ascii_lowercase:
        if i in frequencies.keys():
            probabilities[i] = frequencies[i] / total_letters

    return probabilities


def random_string_with_probabilities(probabilities, length=4):
    result = ""
    for i in range(length):
        result += random.choices(list(probabilities.keys()), list(probabilities.values()))[0]
    return result

def assignment_2_b(filename):
    result = []
    probabilities = analysis_letter_probalities(filename)
    for i in range(100):
        letters = random_string_with_probabilities(probabilities, length=4)
        result.append(letters)
    return result

def print_matrix(data, columns=10):
    frequency = 0
    counter = 0
    for i in data:
        if counter % columns == 0 and counter != 0:
            printer("\n")
        if valid_word(i):
            frequency += 1
            printer(colored(i, 'green'))
        else:
            printer(i)
        printer("\t")
        counter += 1
    printer("\n")
    printer("Probability: %f" % (frequency / 100.0))
    printer("\n")
    printer("\n")


def analysis_letter_transition_probalities(words):
    transition_frequencies = dict()
    for word in words:
        if len(word) > 1:
            for index in range(len(word) - 1):
                pre_letter = word[index]
                post_letter = word[index + 1]
            
                if pre_letter not in transition_frequencies.keys():
                    transition_frequencies[pre_letter] = dict()

                if post_letter not in transition_frequencies[pre_letter]:
                    transition_frequencies[pre_letter][post_letter] = 1
                else:
                    transition_frequencies[pre_letter][post_letter] += 1

    transition_probabilities = dict()
    for i in transition_frequencies:
        total = 0
        for _ in transition_frequencies[i].values():
            total += _
        if i not in transition_probabilities.keys() and len(transition_frequencies[i]) != 0:
            transition_probabilities[i] = dict()
        for j in transition_frequencies[i]:
            transition_probabilities[i][j] = transition_frequencies[i][j] / total

    return transition_probabilities      

def lexical_analyzer(filename):
    words = []
    with open(filename) as f:
        data = f.read().lower()
    index = 0
    word = ""
    while True:
        if index == len(data):
            break
        if data[index] in string.ascii_lowercase:
            word += data[index]
        else:
            if word != "":
                words.append(word)
            word = ""
        index += 1
    return words


def random_string_with_transition_probabilities(initial_probobilities, transition_probabilities, length=4):
    result = ""
    pre_char = random.choices(list(initial_probobilities.keys()), list(initial_probobilities.values()))[0]
    result += pre_char
    for i in range(length - 1):
        current_char = random.choices(list(transition_probabilities[pre_char].keys()), list(transition_probabilities[pre_char].values()))[0]
        result += current_char
        pre_char = current_char
    return result
        

def assignment_2_c(filename):
    results = []
    words = lexical_analyzer(filename)
    probabilities = analysis_letter_probalities(filename)
    transition_probabilities = analysis_letter_transition_probalities(words)
    # for i in transition_probabilities:
    #     print("%s => %s" % (i, transition_probabilities[i]))
    for i in range(100):
        word = random_string_with_transition_probabilities(probabilities, transition_probabilities)
        results.append(word)
    return results

def analysis_letter_2_steps_transition_probalities(words):
    transition_frequencies = dict()
    for word in words:
        if len(word) > 2:
            for index in range(len(word) - 2):
                pre_two_letter = word[index:index+2]
                post_letter = word[index + 2]
            
                if pre_two_letter not in transition_frequencies.keys():
                    transition_frequencies[pre_two_letter] = dict()

                if post_letter not in transition_frequencies[pre_two_letter]:
                    transition_frequencies[pre_two_letter][post_letter] = 1
                else:
                    transition_frequencies[pre_two_letter][post_letter] += 1

    transition_probabilities = dict()
    for i in transition_frequencies:
        total = 0
        for _ in transition_frequencies[i].values():
            total += _
        if i not in transition_probabilities.keys() and len(transition_frequencies[i]) != 0:
            transition_probabilities[i] = dict()
        for j in transition_frequencies[i]:
            transition_probabilities[i][j] = transition_frequencies[i][j] / total

    return transition_probabilities      
    
    
def analysis_letter_2_steps_probalities(words):
    transition_frequencies = dict()
    total = 0
    for word in words:
        if len(word) > 2:
            for index in range(len(word) - 2):
                total += 1
                two_letter = word[index:index+2]
                if two_letter not in transition_frequencies.keys():
                    transition_frequencies[two_letter] = 1
                else:
                    transition_frequencies[two_letter] += 1

    probabilities = dict()
    for i in transition_frequencies:
        probabilities[i] = transition_frequencies[i] / total

    return probabilities

def random_string_with_2_steps_transition_probabilities(initial_probobilities, transition_probabilities, length=4):
    try:
        result = ""
        pre_two_char = random.choices(list(initial_probobilities.keys()), list(initial_probobilities.values()))[0]
        result += pre_two_char
        for i in range(length - 2):
            current_char = random.choices(list(transition_probabilities[pre_two_char].keys()), list(transition_probabilities[pre_two_char].values()))[0]
            result += current_char
            pre_two_char = result[i + 1] + current_char
        return result
    except Exception as e:
        return random_string_with_2_steps_transition_probabilities(initial_probobilities, transition_probabilities, length=4)

def assignment_2_d(filename):
    results = []
    words = lexical_analyzer(filename)
    transition_probabilities = analysis_letter_2_steps_transition_probalities(words)
    # print(transition_probabilities)
    probabilities = analysis_letter_2_steps_probalities(words)
    # print(probabilities)
    for i in range(100):
        word = random_string_with_2_steps_transition_probabilities(probabilities, transition_probabilities)
        results.append(word)
    return results


def main():
    filename = "spamiam.txt"
    print("Assignment 2 a")
    print_matrix(assignment_2_a(filename))
    print("Assignment 2 b")
    print_matrix(assignment_2_b(filename))
    print("Assignment 2 c")
    print_matrix(assignment_2_c(filename))
    print("Assignment 2 d")
    print_matrix(assignment_2_d(filename))

    filename = "saki_story.txt"
    print("Assignment 2 e b")
    print_matrix(assignment_2_b(filename))
    print("Assignment 2 e c")
    print_matrix(assignment_2_c(filename))
    print("Assignment 2 e d")
    print_matrix(assignment_2_d(filename))
    

if __name__ == "__main__":
    main()
