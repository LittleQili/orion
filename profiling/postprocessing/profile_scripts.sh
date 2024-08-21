result_folder=/dyj/relwork/orion/profiling/benchmarks/vision_models/resnet101_train

python3 process_ncu.py --results_dir ${result_folder}
python3 get_num_blocks.py --results_dir ${result_folder}
python3 roofline_analysis.py --results_dir ${result_folder}
python3 process_nsys.py --results_dir ${result_folder} --metric SM
python3 process_nsys.py --results_dir ${result_folder} --metric Comp
python3 process_nsys.py --results_dir ${result_folder} --metric Mem
