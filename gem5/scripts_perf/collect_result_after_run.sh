# path_to_gem5
GEM5_DIR=../

# name of evaluated system
# consistant with run_checkpoint.sh
COMMENTS_RESTORE="salru"

cd ${GEM5_DIR}/result_benchmark/dir_checkpoint/
sh grep_single.sh $COMMENTS_RESTORE
cd ..
python plot-perf-sfillinv-tagmiss.py
python plot-specld-nonspecld.py

print "Figure and data are saved to gem5/result_benchmark"
