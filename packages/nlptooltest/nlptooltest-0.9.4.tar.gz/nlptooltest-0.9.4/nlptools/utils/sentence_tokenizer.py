import argparse

def remove_empty_values(sentences):
    return [value for value in sentences if value != '']


def sent_tokenize(text, dot=True, new_line=True, question_mark=True, exclamation_mark=True):
    """
    This method tokenizes a text into a set of sentences based on the selected separators, including the dot, new line, question mark, and exclamation mark.

    Args:
        text (:obj:`str`): Arabic text to be tokenized.
        dot (:obj:`str`): flag to split text based on Dot (default is True).
        new_line (:obj:`str`): flag to split text based on new_line (default is True).
        question_mark (:obj:`str`): flag to split text based on question_mark (default is True).
        exclamation_mark (:obj:`str`): flag to split text based on exclamation_mark (default is True).

    Returns:
        :obj:`list`: list of sentences.

    **Example:**

    .. highlight:: python
    .. code-block:: python

        from nlptools.utils import sentence_tokenizer
        sentences = sentence_tokenizer.sent_tokenize("مختبر سينا لحوسبة اللغة والذكاء الإصطناعي. في جامعة بيرزيت.", dot=True, new_line=True, question_mark=True, exclamation_mark=True)
        print(sentences)

        #output
        ['مختبر سينا لحوسبة اللغة والذكاء الإصطناعي.', 'في جامعة بيرزيت.']
    """
    separators = []
    split_text = [text]
    if dot==True:
        separators.append('. ')
    if new_line==True:
        separators.append('\n')
    if question_mark==True:
        separators.append('?')
        separators.append('؟')
    if exclamation_mark==True:
        separators.append('!')
    
    for sep in separators:
        new_split_text = []
        for part in split_text:
            tokens = part.split(sep)
            tokens_with_separator = [token + sep for token in tokens[:-1]]
            tokens_with_separator.append(tokens[-1].strip())
            new_split_text.extend(tokens_with_separator)
        split_text = new_split_text
    
    split_text = remove_empty_values(split_text)    
    return split_text

def main():
    tokenizer = argparse.ArgumentParser(description='Arabic text tokenization tool')
    
    # Adding arguments
    tokenizer.add_argument('--text', type=str, required=True, help='Arabic text to be stripped')
    tokenizer.add_argument('--dot', type=str, default=True, help='Whether to split based on dot')
    tokenizer.add_argument('--new_line', type=str, default=True, help='Whether to split based on new line')
    tokenizer.add_argument('--question_mark', type=str, default=True, help='Whether to split based on question_mark')
    tokenizer.add_argument('--exclamation_mark', type=str, default=True, help='Whether to split based on exclamation_mark')

    args = tokenizer.parse_args()

    tokenized_text = sent_tokenize(args.text, dot=args.dot, new_line=args.new_line, question_mark=args.question_mark, exclamation_mark=args.exclamation_mark)
    
    print(tokenized_text)

if __name__ == '__main__':
    main()