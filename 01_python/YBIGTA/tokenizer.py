from typing import Optional, Union, List
from YBIGTA.preprocessor import Preprocessor

class Tokenizer:
    def __init__(self, 
                 corpus: Optional[Union[List[str], str]] = None
    ) -> None:
        '''
        Args:
            corpus (List[str], str)
        Returns:
            None
        '''
        self.corpus = []
        self.word_freq = {}
        self.preprocessor = Preprocessor()
        if corpus is not None:
            self.add_corpus(corpus)

    def __call__(self,
                 text: Union[List[str], str],
                 padding: bool = False,
                 max_length: Optional[int] = None
    ) -> Union[List[List[int]], List[int]]:
        '''
        Tokenize the input text into a list of token IDs
        Args:
            text (List[str], str)
            padding (bool): whether or not to add padding token
            max_length (int): maximum length of list of tokens
        Return:
            List of token IDs from input text
        '''
        return self.tokenize(text, padding, max_length)

    def add_corpus(self, 
                   corpus: Optional[Union[List[str], str]] = None
    ) -> None:
        '''
        Add corpus to self.corpus and update word_freq
        Args:
            corpus (List[str], str)
        Returns:
            None
        '''
        if corpus is None:
            return 
        
        if isinstance(corpus, str):
            # Update self.corpus
            self.corpus.append(corpus)

            # Update self.word_freq
            words = self.text_to_words(corpus)
            for word in words:
                if word in self.word_freq:
                    self.word_freq[word] += 1
                else:
                    self.word_freq[word] = 1
        elif isinstance(corpus, list):
            # Update self.corpus
            self.corpus += corpus

            # Update self.word_freq
            for text in corpus:
                words = self.text_to_words(text)
                for word in words:
                    if word in self.word_freq:
                        self.word_freq[word] += 1
                    else:
                        self.word_freq[word] = 1
        else:
            raise TypeError('corpus is neither a string nor a list of strings')

    def tokenize(self,
                 text: Union[List[str], str],
                 padding: bool = False,
                 max_length: Optional[int] = None
    ) -> Union[List[List[int]], List[int]]:
        '''
        Tokenize the input text into a list of token IDs
        Args:
            text (List[str], str)
            padding (bool): whether or not to add padding token
            max_length (int): maximum length of list of tokens
        Return:
            List of token IDs from input text
        '''
        # Need to convert text to token and truncate if necessary
        text_tokens = []
        if isinstance(text, str):
            text_tokens.append(self.text_to_tokens(text, max_length))
        elif isinstance(text, list):
            for curtext in text:
                text_tokens.append(self.text_to_tokens(curtext, max_length))
        else:
            raise TypeError('text is neither a string nor a list of strings')
        
        # Need to convert from token to token ID
        text_tokenIDs = []
        for word_tokens in text_tokens:
            text_tokenIDs.append(self.tokens_to_tokenIDs(word_tokens))

        # Need to add padding token if necessary
        if padding:
            token_padding = self.tokens.index('*')
            max_length_word_tokens = 0
            for word_tokens in text_tokens:
                max_length_word_tokens = max(max_length_word_tokens, len(word_tokens))
            for i in range(len(text_tokenIDs)):
                for _ in range(max_length_word_tokens - len(text_tokenIDs[i])):
                    text_tokenIDs[i].append(token_padding)
        
        return text_tokenIDs

    def text_to_words(self, 
                      text: str
    ) -> List[str]:
        '''
        Split the text into words
        Args:
            text (str): preprocessed text
        Return:
            List of words splitted from text
        '''
        raise NotImplementedError

    def text_to_tokens(self, 
                       text: str, 
                       max_length: Optional[int] = None
    ) -> List[str]:
        '''
        Convert from text to list of tokens
        Args:
            text (str): unpreprocessed text
            max_length (int): maximum length of list of tokens
        Returns:
            List of tokens from text
        '''
        # Convert from text to words
        words = self.text_to_words(text)

        # Split words into tokens
        text_tokens = []
        for word in words:
            cur_token = ''
            for i in range(len(word)):
                if str(cur_token + word[i]) not in self.tokens:
                    text_tokens.append(cur_token)
                    cur_token = word[i]
                else:
                    cur_token += word[i]
            text_tokens.append(cur_token)

        # Truncate text_tokens if its length is greater than max_length
        if max_length is not None and len(text_tokens) > max_length:
            text_tokens = text_tokens[:max_length]

        return text_tokens
    
    def tokens_to_tokenIDs(self, 
                           word_tokens: List[str]
    ) -> List[int]:
        '''
        Convert from tokens to their corresponding token IDs
        Args:
            word_tokens (List[str]): a list of tokens
        Returns:
            List of their corresponding token IDs
        '''
        word_tokenIDs = []
        for i in range(len(word_tokens)):
            if word_tokens[i] not in self.tokens:
                word_tokenIDs.append(-1)
            else:
                word_tokenIDs.append(self.tokens.index(word_tokens[i]))
            
        return word_tokenIDs