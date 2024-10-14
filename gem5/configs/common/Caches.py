from m5.defines import buildEnv
from m5.objects import *

# Base implementations of L1, L2, IO and TLB-walker caches. There are
# used in the regressions and also as base components in the
# system-configuration scripts. The values are meant to serve as a
# starting point, and specific parameters can be overridden in the
# specific instantiations.

class NewRandIdxTest(NewRandIdx):
    nbits = 6

class NewRandTagTest(NewRandTag):
    indexing_policy = NewRandIdxTest()
    nbits = 6
'''
class NewRandIdxTestL2(NewRandIdx):
    nbits = 0

class NewRandTagTestL2(NewRandTag):
    indexing_policy = NewRandIdxTestL2()
    nbits = 0
'''
class L1Cache(Cache):
    assoc = 2
    tag_latency = 1
    data_latency = 1
    response_latency = 0
    mshrs = 4
    tgts_per_mshr = 20

class L1_ICache(L1Cache):
    is_read_only = True
    tags = BaseSetAssoc()
    # Writeback clean lines as well
    writeback_clean = True
    replacement_policy = LRURP()
    #replacement_policy = RandomRP()

class L1_DCache(L1Cache):
    assoc = 8
    tag_latency = 1
    data_latency = 1
    response_latency = 0

    randspec = True
    cache_level = 1

    # GYGY: quickly setting replacement policy
    tags = BaseSetAssoc()
    replacement_policy = RandomRP()

    #replacement_policy = LRURP()

    #tags = NewRandTagTest()
    #replacement_policy = RandomRP()

    mshrs = 4
#    demand_mshr_reserve = 8

class L2Cache(Cache):
    assoc = 16
    data_latency = 6
    response_latency = 6
    tag_latency = 6
    mshrs = 20
    tgts_per_mshr = 12
    write_buffers = 8

    randspec = True
    cache_level = 2

    # GYGY: quickly setting replacement policy
    #tags = NewRandTagTestL2()
    #replacement_policy = RandomRP()
    #tag_latency = 18

    replacement_policy = LRURP()

class IOCache(Cache):
    assoc = 8
    tag_latency = 50
    data_latency = 50
    response_latency = 50
    mshrs = 20
    size = '1kB'
    tgts_per_mshr = 12

class PageTableWalkerCache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 10
    size = '1kB'
    tgts_per_mshr = 12

    # the x86 table walker actually writes to the table-walker cache
    if buildEnv['TARGET_ISA'] in ['x86', 'riscv']:
        is_read_only = False
    else:
        is_read_only = True
        # Writeback clean lines as well
        writeback_clean = True
