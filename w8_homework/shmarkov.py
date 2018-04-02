# shmarkov.py, simple and concise markov chain text generation

# Copyright (C) 2018 Allison Parrish
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the “Software”), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function
import random

def add_to_model(model, n, seq):
    seq = list(seq[:]) + [None]
    for i in range(len(seq)-n):
        gram = tuple(seq[i:i+n])
        next_item = seq[i+n]            
        if gram not in model:
            model[gram] = []
        model[gram].append(next_item)

def markov_model(n, seq):
    model = {}
    add_to_model(model, n, seq)
    return model

def gen_from_model(n, model, start=None, max_gen=100):
    if start is None:
        start = random.choice(list(model.keys()))
    output = list(start)
    for i in range(max_gen):
        start = tuple(output[-n:])
        next_item = random.choice(model[start])
        if next_item is None:
            break
        else:
            output.append(next_item)
    return output

def markov_model_from_sequences(n, sequences):
    model = {}
    for item in sequences:
        add_to_model(model, n, item)
    return model

def markov_generate_from_sequences(n, sequences, count, max_gen=100):
    starts = [item[:n] for item in sequences if len(item) >= n]
    model = markov_model_from_sequences(n, sequences)
    return [gen_from_model(n, model, random.choice(starts), max_gen)
           for i in range(count)]

def markov_generate_from_lines_in_file(n, filehandle, count, level='char', max_gen=100):
    if level == 'char':
        glue = ''
        sequences = [item.strip() for item in filehandle.readlines()]
    elif level == 'word':
        glue = ' '
        sequences = [item.strip().split() for item in filehandle.readlines()]
    generated = markov_generate_from_sequences(n, sequences, count, max_gen)
    return [glue.join(item) for item in generated]

if __name__ == '__main__':
    import sys
    try:
        n = int(sys.argv[1])
    except (ValueError, IndexError):
        n = 3
    for item in markov_generate_from_lines_in_file(n, sys.stdin, 20):
        print(item)
