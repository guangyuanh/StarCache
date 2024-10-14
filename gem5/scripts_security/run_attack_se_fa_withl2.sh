ATTACK_ROOT=$1
ATTACK_NAME=$2
EXE_DIR=${ATTACK_ROOT}/${ATTACK_NAME}
EXE_NAME=$3
EXE_OPTIONS=$4
COMMENTS=${EXE_NAME}_fa

#path_to_gem5
GEM5_DIR=../

BUILD_DIR=${GEM5_DIR}

cd $EXE_DIR
echo "Current working diretory: "
pwd
$BUILD_DIR/build/X86/gem5.opt --outdir=$GEM5_DIR/result_side_channel/${ATTACK_NAME}/$COMMENTS \
        $GEM5_DIR/configs/example/se.py \
        --num-cpus=1 --cpu-type=DerivO3CPU \
        --mem-type=SimpleMemory --mem-size=4GB \
        --caches --l2cache --l1d_size=32kB --l1d_assoc=512 \
	--l1i_size=32kB --l1i_assoc=4 \
        --l2_size=2MB --l2_assoc=16 --cacheline_size=64 \
        --num-dirs=1 \
        --mark-spec \
	-c $EXE_NAME \
        --options=${COMMENTS}_"$EXE_OPTIONS"
