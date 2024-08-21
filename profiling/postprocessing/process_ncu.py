import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--results_dir', type=str, required=True,
                        help='path to directory containing the profiling files')
args = parser.parse_args()

# remove non-csv content.
with open(f'{args.results_dir}/output_ncu.csv','r') as fin:
    fin_lines = fin.readlines()
for i in range(len(fin_lines)):
    if '\"ID\",\"Process ID\",\"Process Name\",\"Host Name\",\"thread Domain:Push/Po' in fin_lines[i]:
        with open(f'{args.results_dir}/output_ncu.clean.csv','w') as fout:
            fout.writelines(fin_lines[i:])
        break

df = pd.read_csv(f'{args.results_dir}/output_ncu.clean.csv', index_col=0)
kernels = []
metrics_to_get = ['Duration', 'Block Size', 'Grid Size', 'Compute (SM) Throughput', 'DRAM Throughput', 'Registers Per Thread', 'Static Shared Memory Per Block']

unique_kernel_names = set()

for index, row in df.iterrows():
    kernel = row['Kernel Name']
    metric_name = row['Metric Name']

    if metric_name == 'DRAM Frequency':
        kernels.append([kernel])
        unique_kernel_names.add(kernel)
    elif metric_name in metrics_to_get:
        kernels[-1].append(row['Metric Value'])

for x in unique_kernel_names:
    print(x)
    print("------------------------------------")

# Correctness: thread&register calculation index
for kernel in kernels:
    num_threads = int(kernel[-3]) * int(kernel[-4])
    num_registers = num_threads * int(kernel[-2])
    kernel += [num_threads, num_registers]


print(len(kernels))
#print(kernels[0])
labels = ['Kernel_Name', 'DRAM_Throughput(%)', 'Duration(ns)', 'Compute(SM)(%)',  'Block', 'Grid', 'Registers_Per_Thread', 'Static_shmem_per_block', 'Number_of_threads', 'Number_of_registers']



df_new = pd.DataFrame(kernels, columns=labels)
print(df_new)
df_new.to_csv(f'{args.results_dir}/output_ncu_processed.csv')
