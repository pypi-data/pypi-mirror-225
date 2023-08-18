import re
import multiprocessing
import itertools

split_str = 'llama.cpp: loading model from'

import argparse


tuning_args = [
    {'name': 'n_batch', 'type': int, 'default': [512], 'help': 'batch size'},
    {'name': 'n_gpu_layers', 'type': int, 'default': [0], 'help': 'number of gpu layers'},
    {'name': 'n_threads', 'type': int, 'default': [max(multiprocessing.cpu_count() // 2, 1)], 'help': 'number of threads'},
    {'name': 'last_n_tokens_size', 'type': int, 'default': [64], 'help': 'max number of tokens to keep in last_n_tokens deque'},
    {'name': 'use_mmap', 'type': bool, 'default': [True], 'help': 'use mmap'},
    {'name': 'use_mlock', 'type': bool, 'default': [False], 'help': 'use mlock'},
    {'name': 'low_vram', 'type': bool, 'default': [False], 'help': 'use low vram'},
]

def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', required=True, type=str, help='model path')
    parser.add_argument('--prompt', '-p', type=str, default="Q: Name the planets in the solar system? A: ", help='input text')
    parser.add_argument('--max_tokens', type=int, default=32, help='max num of tokens of input text')

    for targs in tuning_args:
        parser.add_argument(f"--{targs['name']}", type=targs['type'], nargs='+', default=targs['default'], help=targs['help'])

    parser.add_argument('--n_repeats', type=int, default=1, help='number of repeatitions for benchmarking')
    return parser

def preprocess_args(args):
    vargs = vars(args)

    # Cmd
    cmd = [
            'python', '-m', 'lmetric.llamacpp.execute_llamacpp',
            '--model_path', args.model_path,
            '-p', args.prompt,
            '--max_tokens', str(args.max_tokens)
    ]

    for targs in tuning_args:
        if vargs[targs['name']] is not None:
            cmd += [f"--{targs['name']}"]
            cmd += [str(x) for x in vargs[targs['name']]]


    # Param
    model_path = args.model_path
    prompt = args.prompt
    max_tokens = args.max_tokens
    n_repeats = args.n_repeats

    vargs.pop('prompt')
    vargs.pop('model_path')
    vargs.pop('max_tokens')
    vargs.pop('n_repeats')
    param_combinations = list(itertools.product(*vargs.values()))
    params = []
    for combination in param_combinations:
        params_dict = {key: value for key, value in zip(vargs.keys(), combination)}
        params.append(params_dict)
    
    return vargs, model_path, prompt, max_tokens, n_repeats, cmd, params

def convert_to_json(array):
    result = {}

    load_time = re.search(r'load time =\s*([\d.]+)', array[0])
    if load_time:
        result['load_time'] = float(load_time.group(1))

    sample_time = re.search(r'sample time =\s*([\d.]+)', array[1])
    sample_runs = re.search(r'(\d+)\s+runs', array[1])
    if sample_time and sample_runs:
        result['sample_time'] = float(sample_time.group(1))
        result['sample_time_pt'] = result['sample_time'] / int(sample_runs.group(1))

    prompt_eval_time = re.search(r'prompt eval time =\s*([\d.]+)', array[2])
    prompt_eval_tokens = re.search(r'(\d+)\s+tokens', array[2])
    if prompt_eval_time and prompt_eval_tokens:
        result['prompt_eval_time'] = float(prompt_eval_time.group(1))
        result['prompt_eval_time_pt'] = result['prompt_eval_time'] / int(prompt_eval_tokens.group(1))

    eval_time = re.search(r'eval time =\s*([\d.]+)', array[3])
    eval_runs = re.search(r'(\d+)\s+runs', array[3])
    if eval_time and eval_runs:
        result['eval_time'] = float(eval_time.group(1))
        result['eval_time_pt'] = result['eval_time'] / int(eval_runs.group(1))

    total_time = re.search(r'total time =\s*([\d.]+)', array[4])
    if total_time:
        result['total_time'] = float(total_time.group(1))

    return result
