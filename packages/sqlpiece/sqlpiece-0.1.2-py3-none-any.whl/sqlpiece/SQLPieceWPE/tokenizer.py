# coding=utf-8
# Copyright 2018 The Open AI Team Authors and The HuggingFace Inc. team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tokenization class for MorphPieceWPE"""

from transformers import BertTokenizer, WordpieceTokenizer
from transformers.models.bert.tokenization_bert import load_vocab
import pickle
from transformers.utils import logging
from pathlib import Path

logger = logging.get_logger(__name__)
path = Path(__file__).parent

class MorphPieceWPE(BertTokenizer):
    r""" Construct a MorphPieceWPE tokenizer. Based on BertTokenizer, but uses a MorphPiece mechanism for the morphemes. For more information, please refer to the `MorphPiece paper <https://arxiv.org/abs/xxx.xxx>`.

    This tokenizer inherits from [`BertTokenizer`] which contains all the methods, except _tokenize() function, which implements the MorphPiece tokenization for WordPiece. Users should refer to this superclass for more information regarding those methods.

    Attention : Please do NOT use .from_pretrained() method as it will override the custom vocabularies. Instead instentiate the class without any arguments to load the default vocabularies.

    Args:
        All arguments are the same as BertTokenizer except for the following additional arguments:
        no_morph_vocab (`Path`):
            Path to a custom vocabulary file for the WordpieceTokenizer().
        lookup_table (`Path`):
            Path to the lookup table for the morpheme splits.
        
        The original 'vocab_file' argument now points to another custom vocabulary.
        'vocab_size' now refers to the cumulative size of the two custom vocabularies.

    Example:
    ```
    >>> from morphpiece import MorphPieceWPE
    >>> tokenizer = MorphPieceWPE()
    >>> tokenizer.tokenize("Hello world")
    ['hello', 'world']
    ```
    """
    def __init__(
        self,
        vocab_file=path/'with_morph_vocab.txt',
        no_morph_vocab=path/'no_morph_vocab.txt',
        lookup_table=path/'lookup_dict.pkl',
        do_lower_case=True,
        do_basic_tokenize=True,
        never_split=None,
        unk_token="[UNK]",
        sep_token="[SEP]",
        pad_token="[PAD]",
        cls_token="[CLS]",
        mask_token="[MASK]",
        tokenize_chinese_chars=True,
        strip_accents=None,
        **kwargs,
    ):
        super().__init__(
            vocab_file=vocab_file,
            do_lower_case=do_lower_case,
            do_basic_tokenize=do_basic_tokenize,
            never_split=never_split,
            unk_token=unk_token,
            sep_token=sep_token,
            pad_token=pad_token,
            cls_token=cls_token,
            mask_token=mask_token,
            tokenize_chinese_chars=tokenize_chinese_chars,
            strip_accents=strip_accents,
            **kwargs,
        )

        self.no_morph_vocab = load_vocab(no_morph_vocab)  
        self.morpheme_table = pickle.load(open(lookup_table,'rb'))  
        self.morphpiece_tokenizer = WordpieceTokenizer(vocab=self.no_morph_vocab, unk_token=self.unk_token)
        
        self.counter_morph = dict.fromkeys(self.morpheme_table,0)  
        self.counter_bpe = dict()  
        self.counter_token = dict()  
        self.counter_nonsplit = dict()  

    def _tokenize(self, text):
        split_tokens = []
        if self.do_basic_tokenize:
            for token in self.basic_tokenizer.tokenize(text, never_split=self.all_special_tokens):

                morph_splits = self.morpheme_table.get(token,None)  
                
                # If the token is part of the never_split set
                if token in self.basic_tokenizer.never_split:
                    split_tokens.append(token)
                elif morph_splits is not None:  
                    split_tokens.extend(morph_splits)  
                else:
                    split_tokens += self.morphpiece_tokenizer.tokenize(token)
        else:
            morph_splits = self.morpheme_table.get(token,None)  
            if morph_splits is not None:  
                split_tokens.extend(morph_splits)  
            else:  
                split_tokens = self.morphpiece_tokenizer.tokenize(text)
        return split_tokens

    @property
    def vocab_size(self):
        return len(self.vocab) + len(self.no_morph_vocab)