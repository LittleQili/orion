# /opt/nvidia/nsight-compute/2021.2.0/nv-nsight-cu-cli -o output_ncu --set detailed --nvtx --nvtx-include "start/" python3 script.py
# /opt/nvidia/nsight-compute/2021.2.0/nv-nsight-cu-cli  --csv --set detailed --nvtx --nvtx-include "start/" python3 script.py  > output_ncu.csv
# nsys profile -w true -t cuda,nvtx,osrt,cudnn,cublas -s none -o output_nsys --cudabacktrace=true --capture-range=cudaProfilerApi --stop-on-range-end=true  -f true -x true python3 script.py
# nsys stats --report gputrace --format csv,column --output .,- output_nsys.qdrep

nsys profile -w true -t cuda,nvtx,osrt,cudnn,cublas -s none -o output_nsys --cudabacktrace=true --capture-range=cudaProfilerApi --capture-range-end=stop-shutdown  -f true -x true python3 vision_models.py

nsys stats --report gputrace --format csv,column --output .,- output_nsys.nsys-rep

ncu -o output_ncu --set detailed --nvtx --nvtx-include "start/" python3 vision_models.py

ncu -i output_ncu.ncu-rep --csv --page raw > raw_ncu.csv

ncu --csv --set detailed --nvtx --nvtx-include "start/" --log-file output_ncu.csv python3 vision_models.py
