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
"""Tokenization class for MorphPieceBPE"""

import pickle
from typing import List, Optional, Union
import regex as re
from transformers import GPT2Tokenizer
from transformers.utils import logging
from pathlib import Path

from transformers.tokenization_utils_base import TruncationStrategy, PaddingStrategy, TensorType, BatchEncoding

logger = logging.get_logger(__name__)
path = Path(__file__).parent

class SQLPieceBPE(GPT2Tokenizer):
    r""" Construct a SQLPieceBPE tokenizer. Based on BPE, but uses a split vocabulary paradigm to tokenize SQL statements. For more information, please refer to the `MorphPiece paper <https://arxiv.org/abs/xxx.xxx>`.

    This tokenizer inherits from [`GPT2Tokenizer`] which contains all the methods, except _tokenize() function, which implements the MorphPiece tokenization for WordPiece. Users should refer to this superclass for more information regarding those methods.

    Attention : Please do NOT use .from_pretrained() method as it will override the custom vocabularies. Instead instentiate the class without any arguments to load the default vocabularies.

    Args:
        All arguments are the same as GPT2Tokenizer except for the following additional argument:
        morpheme_file (`Path`):
            Path to a pickled file which has both the morpheme vocabulary and lookup table.
        
        The original 'vocab_file' and 'merges_file' arguments now point to a custom vocabulary and merges which takes into account the morpheme vocabulary.

    Example:
    ```
    >>> from sqlpiece import SQLPieceBPE
    >>> tokenizer = SQLPieceBPE()
    >>> tokenizer.tokenize("SELECT name FROM students WHERE age > 10")
    ['SELECT', 'name', 'FROM', 'stud', 'ents', 'WHERE', 'age', '>', '10']
    ```

    """
    model_input_names: List[str] = ["input_ids", "token_type_ids", "attention_mask"]
    
    def __init__(
        self,
        vocab_file=None,
        merges_file=None,
        sql_vocab_file=None,
        ver=1.0,
        errors="replace",
        unk_token="<UNK>",
        bos_token="<BOS>",
        eos_token="<EOS>",
        pad_token="<PAD>",
        add_prefix_space=False,
        add_bos_token=False,
        **kwargs
    ):
        if sql_vocab_file is None:
            if ver==1.0:
                sql_vocab_file = path/'vocab/sql_vocab.pkl'
                vocab_file = path/'vocab/vocab.json'
                merges_file = path/'vocab/merges.txt'

        if kwargs.pop("model_max_length", kwargs.pop("max_len", None)) is None:
            logger.warning('model_max_length has not been set. Defaulting to 512.')
            kwargs["model_max_length"] = 512

        super().__init__(
        vocab_file,
        merges_file,
        errors,
        unk_token,
        bos_token,
        eos_token,
        pad_token,
        add_prefix_space,
        add_bos_token,
        **kwargs
        )
        
        self.sql_vocab = pickle.load(open(sql_vocab_file,'rb'))
        self.counter_sql = dict.fromkeys(self.sql_vocab,0)   
        self.counter_bpe = dict()   
        self.counter_token = dict()

        special_tokens_dict = {
                               "cls_token": "<CLS>",
                               "sep_token": "<SEP>",
                               "mask_token": "<MASK>",
                            #    "pad_token": "<PAD>",
                            #    "unk_token": "<UNK>",
                            #    "bos_token": "<BOS>",
                            #    "eos_token": "<EOS>",
                               }

        self.add_special_tokens(special_tokens_dict)   

    def get_byte_encoding(self,token):
        return "".join(
            self.byte_encoder[b] for b in token.encode("utf-8")
        )  # Maps all our bytes to unicode strings, avoiding control tokens of the BPE (spaces in our case)
        
    def _get_bpe(self,token):
        byte_encoded_token = self.get_byte_encoding(token)
        return [bpe_token for bpe_token in self.bpe(byte_encoded_token).split(" ")]
        
    def reset_counters(self):
        self.counter_sql = dict.fromkeys(self.sql_vocab,0)
        self.counter_bpe = dict()
        self.counter_token = dict()

    def increment_counter(self,counter,token):
        if token in counter:
            counter[token]+=1
        else:
            counter[token]=1
    
    def _tokenize(self, text):
        """Tokenize a string."""
        all_tokens = []
        self.sql_ids = []
        pretokens = text.split() # SQL statements are first split by space.
        
        for token in pretokens:
            self.increment_counter(self.counter_token,token)
            if token.upper() in self.sql_vocab:
                self.increment_counter(self.counter_sql,token.upper())
                all_tokens.append(token)
                self.sql_ids.append(0)
            else:
                bpe_pretokens = re.findall(self.pat, token) # and then split by bpe regex

                for token in bpe_pretokens:
                    self.increment_counter(self.counter_bpe,token)
                    bpe_tokens = self._get_bpe(token)
                    all_tokens.extend(bpe_tokens)
                    self.sql_ids.extend([1]*len(bpe_tokens))
        
        return all_tokens
    
    def _convert_bpe_tokens_to_string(self, tokens):
        """Converts a sequence of BPE tokens (string) in a single string."""
        text = "".join(tokens)
        text = bytearray([self.byte_decoder[c] for c in text]).decode("utf-8", errors=self.errors)
        return text

    def from_pretrained(self,x):
        raise NotImplementedError("Please do not use from_pretrained() method for SQLPieceBPE. Instead, instantiate the class without any arguments to load the default vocabularies.")
    
    # def create_token_type_ids_from_sequences(
    #     self, token_ids_0: List[int], token_ids_1: Optional[List[int]] = None
    # ) -> List[int]:

    #     if token_ids_1 is not None:
    #         return NotImplemented("This tokenizer determines token_type_ids for only 1 sequence.")
    #     return self.sql_ids

    def prepare_for_model(
        self,
        ids: List[int],
        pair_ids: Optional[List[int]] = None,
        add_special_tokens: bool = True,
        padding: Union[bool, str, PaddingStrategy] = False,
        truncation: Union[bool, str, TruncationStrategy] = None,
        max_length: Optional[int] = None,
        stride: int = 0,
        pad_to_multiple_of: Optional[int] = None,
        return_tensors: Optional[Union[str, TensorType]] = None,
        return_token_type_ids: Optional[bool] = None,
        return_attention_mask: Optional[bool] = None,
        return_overflowing_tokens: bool = False,
        return_special_tokens_mask: bool = False,
        return_offsets_mapping: bool = False,
        return_length: bool = False,
        verbose: bool = True,
        prepend_batch_axis: bool = False,
        **kwargs,
    ) -> BatchEncoding:
        """
        Prepares a sequence of input id, or a pair of sequences of inputs ids so that it can be used by the model. It
        adds special tokens, truncates sequences if overflowing while taking into account the special tokens and
        manages a moving window (with user defined stride) for overflowing tokens. Please Note, for *pair_ids*
        different than `None` and *truncation_strategy = longest_first* or `True`, it is not possible to return
        overflowing tokens. Such a combination of arguments will raise an error.

        Args:
            ids (`List[int]`):
                Tokenized input ids of the first sequence. Can be obtained from a string by chaining the `tokenize` and
                `convert_tokens_to_ids` methods.
            pair_ids (`List[int]`, *optional*):
                Tokenized input ids of the second sequence. Can be obtained from a string by chaining the `tokenize`
                and `convert_tokens_to_ids` methods.
        """

        # Backward compatibility for 'truncation_strategy', 'pad_to_max_length'

        assert pair_ids is None, "Presently SQLPiece does not support pair_ids"

        padding_strategy, truncation_strategy, max_length, kwargs = self._get_padding_truncation_strategies(
            padding=padding,
            truncation=truncation,
            max_length=max_length,
            pad_to_multiple_of=pad_to_multiple_of,
            verbose=verbose,
            **kwargs,
        )

        pair = bool(pair_ids is not None)
        len_ids = len(ids)
        len_pair_ids = len(pair_ids) if pair else 0

        if return_token_type_ids and not add_special_tokens:
            raise ValueError(
                "Asking to return token_type_ids while setting add_special_tokens to False "
                "results in an undefined behavior. Please set add_special_tokens to True or "
                "set return_token_type_ids to None."
            )

        if (
            return_overflowing_tokens
            and truncation_strategy == TruncationStrategy.LONGEST_FIRST
            and pair_ids is not None
        ):
            raise ValueError(
                "Not possible to return overflowing tokens for pair of sequences with the "
                "`longest_first`. Please select another truncation strategy than `longest_first`, "
                "for instance `only_second` or `only_first`."
            )

        # Load from model defaults
        if return_token_type_ids is None:
            return_token_type_ids = "token_type_ids" in self.model_input_names
        if return_attention_mask is None:
            return_attention_mask = "attention_mask" in self.model_input_names

        encoded_inputs = {}

        # Compute the total size of the returned encodings
        total_len = len_ids + len_pair_ids + (self.num_special_tokens_to_add(pair=pair) if add_special_tokens else 0)

        # Truncation: Handle max sequence length
        overflowing_tokens = []
        if truncation_strategy != TruncationStrategy.DO_NOT_TRUNCATE and max_length and total_len > max_length:
            ids, pair_ids, overflowing_tokens = self.truncate_sequences(
                ids,
                pair_ids=pair_ids,
                num_tokens_to_remove=total_len - max_length,
                truncation_strategy=truncation_strategy,
                stride=stride,
            )

            self.sql_ids, _, _ = self.truncate_sequences( # Haris
                self.sql_ids,
                pair_ids=None,
                num_tokens_to_remove=total_len - max_length,
                truncation_strategy=truncation_strategy,
                stride=stride,
            )

        if return_overflowing_tokens:
            encoded_inputs["overflowing_tokens"] = overflowing_tokens
            encoded_inputs["num_truncated_tokens"] = total_len - max_length

        # Add special tokens
        if add_special_tokens:
            sequence = self.build_inputs_with_special_tokens(ids, pair_ids)
            token_type_ids = self.sql_ids #self.create_token_type_ids_from_sequences(ids, pair_ids) # Haris
        else:
            sequence = ids + pair_ids if pair else ids
            token_type_ids = self.sql_ids #[0] * len(ids) + ([0] * len(pair_ids) if pair else []) # Haris

        # Build output dictionary
        encoded_inputs["input_ids"] = sequence
        if return_token_type_ids:
            encoded_inputs["token_type_ids"] = token_type_ids
        if return_special_tokens_mask:
            if add_special_tokens:
                encoded_inputs["special_tokens_mask"] = self.get_special_tokens_mask(ids, pair_ids)
            else:
                encoded_inputs["special_tokens_mask"] = [0] * len(sequence)

        # Check lengths
        self._eventual_warn_about_too_long_sequence(encoded_inputs["input_ids"], max_length, verbose)

        # Padding
        if padding_strategy != PaddingStrategy.DO_NOT_PAD or return_attention_mask:
            encoded_inputs = self.pad(
                encoded_inputs,
                max_length=max_length,
                padding=padding_strategy.value,
                pad_to_multiple_of=pad_to_multiple_of,
                return_attention_mask=return_attention_mask,
            )

        if return_length:
            encoded_inputs["length"] = len(encoded_inputs["input_ids"])

        batch_outputs = BatchEncoding(
            encoded_inputs, tensor_type=return_tensors, prepend_batch_axis=prepend_batch_axis
        )

        return batch_outputs