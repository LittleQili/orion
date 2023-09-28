import os
import time

num_runs = 1
trace_files = [
    ("ResNet50", "ResNet50", "rnet_rnet", 160000),
    ("ResNet50", "MobileNetV2", "rnet_mnet", 150000),
    ("MobileNetV2", "ResNet50", "mnet_rnet", 160000),
    ("MobileNetV2", "MobileNetV2", "mnet_mnet", 150000),
    ("ResNet101", "ResNet50", "rnet101_rnet", 160000),
    ("ResNet101", "MobileNetV2", "rnet101_mnet", 150000),
    ("BERT", "ResNet50", "bert_rnet", 160000),
    ("BERT", "MobileNetV2", "bert_mnet", 150000),
    ("Transformer", "ResNet50", "trans_rnet", 160000),
    ("Transformer", "MobileNetV2", "trans_mnet", 150000),
]

for (be, hp, f, max_be_duration) in trace_files:
    for run in range(num_runs):
        print(be, hp, run, flush=True)
        # run
        file_path = f"config_files/{f}.json"
        os.system(f"LD_PRELOAD='/home/image-varuna/orion/src/cuda_capture/libinttemp.so' python ../../benchmarking/launch_jobs.py --algo orion --config_file {file_path} --orion_max_be_duration {max_be_duration}")

        # copy results
        os.system(f"cp client_1.json results/orion/{be}_{hp}_{run}_hp.json")
        os.system(f"cp client_0.json results/orion/{be}_{hp}_{run}_be.json")

        os.system("rm client_1.json")
        os.system("rm client_0.json")