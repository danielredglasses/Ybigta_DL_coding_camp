import re
from typing import Optional, Union, List

class Preprocessor:
    def __init__(self) -> None:
        '''
        Args:
            None
        Returns:
            None
        '''

        self.complement_alphabet = r' [`\-=[];,./~!@#$%^&*()_+{\}|:"<>?]'
        self.combined_alphabet = f'{self.complement_alphabet}'

    def split_string(self,
                     input_string: Union[List[str], str]
    ) -> List[str]:
        '''
        Basic preprocessing for input string without rule
        Args:
            input_string (List[str], str)
        Returns:
            preprocessed_input_string (str)
        '''
        # Convert str to List[str] if necessary
        if isinstance(input_string, list):
            pass
        elif isinstance(input_string, str):
            input_string = [input_string]
        else:
            raise TypeError('input_string is neither a string nor a list of strings')

        # Remove capital letters
        for i in range(len(input_string)):
            input_string[i] = input_string[i].lower()

        # Rll possible cases for split
        for i in range(len(input_string)):
            input_string[i] = input_string[i].split()
            input_string[i] = " ".join(input_string[i])
            input_string[i] = re.split(r'[' + re.escape(self.complement_alphabet) + ']', input_string[i])

        # Remove empty strings
        temp_string = []
        for i in range(len(input_string)):
            temp_string.append([])
            for s in input_string[i]:
                if s != '':
                    temp_string[i].append(s)

        preprocessed_string = temp_string
        return preprocessed_string
        
    def split_string_with_rule(self, 
                     input_string: Union[List[str], str]
    ) -> List[str]:
        '''
        Basic preprocessing for input string with rule
        and return list of strings
        Args:
            input_string: input string, recommended to be string,
                        but edge case handling codes included.
        Returns:
            preprocess_list: list of strings after preprocessing
        '''
        input_string = self.split_string(input_string)

        # Remove special characters
        preprocess_list = []

        for i in range(len(input_string)):
            preprocess_list.append([])
            for word in input_string[i]:
                if "'" in word:
                    first, second = self.single_quote_handle(word)
                    preprocess_list[i].append(first)

                    if second is not None:
                        preprocess_list[i].append(second)
                else:
                    preprocess_list[i].append(word)

            # Add blank space between each words and add <\w> at the end of each words.
            preprocess_list[i] = " ".join(list(preprocess_list[i]))
            preprocess_list[i] += ' <\w>'

        return preprocess_list

    @staticmethod
    def single_quote_handle(single_string) -> tuple[str, str]:
        ''' Handling with single quotation mark ( ' )
        divide cases, and divide the words by each cases
        Args:
            single_string: string that contains single quotation mark ( ' )
        Returns:
            first: first part of the word
            second: second part of the word (possible to be None)
        '''
        first = single_string
        second = None

        # Remove normal [ ' ] from the word (quotes)
        while "'" in single_string:
            if single_string.startswith("'"):
                single_string = single_string[1:]
            elif (single_string.endswith("'") \
                and not single_string.endswith("s'")):
                single_string = single_string[:-1]
            else:
                break
        
        # Handle with edge cases (contractions / possessive)
        if "'" in single_string:
            if single_string.endswith("n't") \
                or single_string.endswith("'ve") \
                or single_string.endswith("'ll") \
                or single_string.endswith("'re"):
                first = single_string[:-3]
                second = single_string[-3:]
            
            elif single_string.endswith("'d") \
                or single_string.endswith("'m") \
                or single_string.endswith("'s") \
                or single_string.endswith("s'"):
                first = single_string[:-2]
                second = single_string[-2:]
            else:
                print(f'special case that does not fit in ordinary cases: \
                        {single_string}')
        else:
            first = single_string
            second = None
        return first, second
            
    # @staticmethod
    # def letter_splitter(word):
    #     ''' split the word by each letter
    #     '''
    #     return [char for char in word]