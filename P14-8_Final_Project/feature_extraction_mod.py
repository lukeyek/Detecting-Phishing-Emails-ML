from nltk import ngrams
import phishing_keywords as pk_data
import numpy as np

def calc_caps_percent(col):
    # Count total alphabetical letters
    total_chars = col.str.count(r'[a-zA-Z]')
    # Count uppercase letters
    capital_chars = col.str.count(r'[A-Z]')
    # Calculate the percentage
    return np.where(total_chars > 0, (capital_chars / total_chars * 100).round(2), 0)

def calc_word_count(col):
    # Count total words excluding numbers
    return col.str.split().apply(lambda x: [word for word in x if not word.isdigit()]).str.len()

def count_matching_ngrams(col, n):
    if n == 1:
        ngram_dict_data = pk_data.unigrams.values()
    elif n == 2:
        ngram_dict_data = pk_data.bigrams.values()
    else:
        ngram_dict_data = pk_data.trigrams.values()
    counts = []
    for body in col:
        words = body.lower().split()
        generated_ngram = ngrams(words, n)
        count = 0
        for ngram in generated_ngram:
            ngram_string = ' '.join(ngram)
            if any(ngram_string in sus_ngram for sus_ngram in ngram_dict_data):
                count += 1
        counts.append(count)
    return counts

def calc_composite_score(unigram_count, bigram_count, trigram_count):
    unigram_weight = 0.1667
    bigram_weight = 0.3333
    trigram_weight = 0.5
    return (unigram_weight * unigram_count) + (bigram_weight * bigram_count) + (trigram_weight * trigram_count)