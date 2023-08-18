# %%
import subprocess
import json
import triton
from tqdm import tqdm
import itertools

from lmetric.llamacpp.utils import convert_to_json, split_str, tuning_args, get_arg_parser, preprocess_args


args = get_arg_parser().parse_args()
vargs, model_path, prompt, max_tokens, n_repeats, cmd, params = preprocess_args(args)

# Run
measures = []
for _ in params:
    measures.append({
        'prompt_eval_max': 0,
        'prompt_eval_min': 1e8,
        'prompt_eval_avg': 0,
        'eval_max': 0,
        'eval_min': 1e8,
        'eval_avg': 0,
    })

for _ in tqdm(range(n_repeats)):
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    decoded_str = result.stderr.decode('utf-8')
    results = decoded_str.split(split_str)[1:]

    for idx, res in enumerate(results):
        timing = [line for line in
                res.split('\n') if line.startswith('llama_print_timings')]
        timing = convert_to_json(timing)
        # print(json.dumps(convert_to_json(timing), indent=4))
        prompt_eval_time = timing['prompt_eval_time_pt']
        eval_time = timing['eval_time_pt']

        if prompt_eval_time > measures[idx]['prompt_eval_max']:
            measures[idx]['prompt_eval_max'] = prompt_eval_time
        if prompt_eval_time < measures[idx]['prompt_eval_min']:
            measures[idx]['prompt_eval_min'] = prompt_eval_time
        measures[idx]['prompt_eval_avg'] += prompt_eval_time / n_repeats
        if eval_time > measures[idx]['eval_max']:
            measures[idx]['eval_max'] = eval_time
        if eval_time < measures[idx]['eval_min']:
            measures[idx]['eval_min'] = eval_time
        measures[idx]['eval_avg'] += eval_time / n_repeats

# Search
min_avg_eval = 1e8
min_avg_eval_param = None
min_avg_peval = 1e8
min_avg_peval_param = None
for idx, measure in enumerate(measures):
    if measure['prompt_eval_avg'] < min_avg_peval:
        min_avg_peval = measure['prompt_eval_avg']
        min_avg_peval_param = params[idx]
    if measure['eval_avg'] < min_avg_eval:
        min_avg_eval = measure['eval_avg']
        min_avg_eval_param = params[idx]

print('===================')
print(f'min eval avg: {min_avg_eval}, min eval param: {min_avg_eval_param}')
print(f'min prompt eval avg: {min_avg_peval}, min prompt eval param: {min_avg_peval_param}')
print('===================')


# Plot
is_plotting = False
plotting_args = ''
dim_cnt = 0
for targs in tuning_args:
    val = vargs[targs['name']]
    if isinstance(val, list) and len(val) > 1:
        dim_cnt += 1
        plotting_args = targs['name']
if dim_cnt != 1:
    is_plotting = False
else:
    is_plotting = True

def get_param_idx_with_val(params, name, val):
    for idx, p in enumerate(params):
        if p[name] == val:
            return idx
    return -1

if is_plotting:
    # Plot
    @triton.testing.perf_report(
        triton.testing.Benchmark(
            x_names=['val'],  # Argument names to use as an x-axis for the plot.
            x_vals=vargs[plotting_args],  # Different possible values for `x_name`.
            x_log=False,  # x axis is logarithmic.
            line_arg='provider',  # Argument name whose value corresponds to a different line in the plot.
            line_vals=[''],  # Possible values for `line_arg`.
            line_names=[''],  # Label name for the lines.
            #styles=['-'],  # Line styles.
            ylabel='Prompt Eval Time',  # Label name for the y-axis.
            plot_name='Prompt Eval Time',  # Name for the plot. Used also as a file name for saving the plot.
            args={},  # Values for function arguments not in `x_names` and `y_name`.
        )
    )
    def benchmark1(val, provider):
        # input initialization
        idx = get_param_idx_with_val(params, plotting_args, val)
        assert idx != -1
        return measures[idx]['prompt_eval_avg'], \
                measures[idx]['prompt_eval_max'], \
                measures[idx]['prompt_eval_min']

    @triton.testing.perf_report(
        triton.testing.Benchmark(
            x_names=['val'],  # Argument names to use as an x-axis for the plot.
            x_vals=vargs[plotting_args],  # Different possible values for `x_name`.
            x_log=False,  # x axis is logarithmic.
            line_arg='provider',  # Argument name whose value corresponds to a different line in the plot.
            line_vals=[''],  # Possible values for `line_arg`.
            line_names=[''],  # Label name for the lines.
            #styles=['-'],  # Line styles.
            ylabel='Eval Time',  # Label name for the y-axis.
            plot_name='Eval Time',  # Name for the plot. Used also as a file name for saving the plot.
            args={},  # Values for function arguments not in `x_names` and `y_name`.
        )
    )
    def benchmark2(val, provider):
        # input initialization
        idx = get_param_idx_with_val(params, plotting_args, val)
        assert idx != -1
        return measures[idx]['eval_avg'], \
                measures[idx]['eval_max'], \
                measures[idx]['eval_min']

    benchmark1.run(print_data=True, show_plots=True)
    benchmark2.run(print_data=True, show_plots=True)
# %%