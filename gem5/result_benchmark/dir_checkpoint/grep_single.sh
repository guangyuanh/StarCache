NAME=$1
GREPDIR="greps/"
CHECKPOINT="restore_10000M"
SIMCYCLE="500M"

mkdir -p $GREPDIR
mkdir -p $GREPDIR/perf
mkdir -p $GREPDIR/starcache

grep -i cpu.numcycles 2006_*/${CHECKPOINT}_${NAME}_$SIMCYCLE/stats.txt > $GREPDIR/perf/perf_${SIMCYCLE}_${NAME}.grep
grep -i system.cpu.lsq0.starldSqinvSent 2006_*/${CHECKPOINT}_${NAME}_$SIMCYCLE/stats.txt > $GREPDIR/starcache/starldsqinvsent_${SIMCYCLE}_${NAME}.grep

grep -i system.cpu.lsq0.starldSqinvNotNeeded   2006_*/${CHECKPOINT}_${NAME}_$SIMCYCLE/stats.txt > $GREPDIR/starcache/starldsqinvnotneeded_${SIMCYCLE}_${NAME}.grep
grep -i system.cpu.lsq0.starldSqinvNonSpec 2006_*/${CHECKPOINT}_${NAME}_$SIMCYCLE/stats.txt > $GREPDIR/starcache/starldsqinvnonspec_${SIMCYCLE}_${NAME}.grep
grep -i "system.cpu.lsq0.starldCommitted " 2006_*/${CHECKPOINT}_${NAME}_$SIMCYCLE/stats.txt > $GREPDIR/starcache/starldcommitted_${SIMCYCLE}_${NAME}.grep
grep -i system.cpu.lsq0.starldCommittedSpec 2006_*/${CHECKPOINT}_${NAME}_$SIMCYCLE/stats.txt > $GREPDIR/starcache/starldcommittedspec_${SIMCYCLE}_${NAME}.grep
grep -i system.cpu.lsq0.starldCommittedNonSpec 2006_*/${CHECKPOINT}_${NAME}_$SIMCYCLE/stats.txt > $GREPDIR/starcache/starldcommittednonspec_${SIMCYCLE}_${NAME}.grep
grep -i system.cpu.dcache.numTagMissSpec 2006_*/${CHECKPOINT}_${NAME}_$SIMCYCLE/stats.txt > $GREPDIR/starcache/tagmissspec_${SIMCYCLE}_${NAME}.grep

grep -i system.cpu.dcache.numSqinv 2006_*/${CHECKPOINT}_${NAME}_$SIMCYCLE/stats.txt > $GREPDIR/starcache/numsqinv_${SIMCYCLE}_${NAME}.grep

grep -i system.cpu.icache.demandMissRate::cpu.inst 2006_*/${CHECKPOINT}_${NAME}_$SIMCYCLE/stats.txt > $GREPDIR/starcache/l1i_demand_missrate_${SIMCYCLE}_${NAME}.grep
grep -i system.cpu.dcache.demandMissRate::cpu.data 2006_*/${CHECKPOINT}_${NAME}_$SIMCYCLE/stats.txt > $GREPDIR/starcache/l1d_demand_missrate_${SIMCYCLE}_${NAME}.grep
