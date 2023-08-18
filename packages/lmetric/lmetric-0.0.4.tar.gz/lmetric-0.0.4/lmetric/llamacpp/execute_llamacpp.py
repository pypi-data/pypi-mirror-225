# %%
from llama_cpp import Llama

import sys
from typing import Optional, Union

from lmetric.llamacpp.utils import split_str, get_arg_parser, preprocess_args

args = get_arg_parser().parse_args()
vargs, model_path, prompt, max_tokens, n_repeats, cmd, params = preprocess_args(args)

for param in params:
    llm = Llama(
        model_path=model_path,
        **param
        )

    llm(prompt, max_tokens=max_tokens, stop=["Q:", "\n"], echo=False)

    del llm


# %%