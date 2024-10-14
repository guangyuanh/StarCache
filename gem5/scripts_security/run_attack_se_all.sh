# path to gem5
GEM5_DIR=../

SCRIPT_NAME=sa
#SCRIPT_NAME=fa
COMMENTS=${SCRIPT_NAME}

cd ${GEM5_DIR}/scripts_security
sh run_attack_se_${SCRIPT_NAME}_withl2.sh ${GEM5_DIR} spectre_v1 secret30_exe ""
sh run_attack_se_${SCRIPT_NAME}_withl2.sh ${GEM5_DIR} spectre_v1 pp_secret30_exe ""
cd ${GEM5_DIR}/spectre_v1
python plot-time-single.py secret30_exe_${COMMENTS}__time.csv
python pp-plot-time.py pppp_secret30_exe_${COMMENTS}__time.csv 64 8

cd ${GEM5_DIR}/scripts_security
sh run_attack_se_${SCRIPT_NAME}_withl2.sh ${GEM5_DIR}/side_channel_src prime_probe exe_prime_probe "timing 256"
cd ${GEM5_DIR}/side_channel_src/prime_probe
python plot_heatmap.py exe_prime_probe_${COMMENTS}_timing

cd ${GEM5_DIR}/scripts_security
sh run_attack_se_${SCRIPT_NAME}_withl2.sh ${GEM5_DIR}/side_channel_src flush_reload exe_fr_d_domain "timing 256"
cd ${GEM5_DIR}/side_channel_src/flush_reload
python plot_heatmap.py exe_fr_d_domain_${COMMENTS}_timing
