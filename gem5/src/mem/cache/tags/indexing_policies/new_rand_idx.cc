/*
 * Copyright (c) 2018 Inria
 * Copyright (c) 2012-2014,2017 ARM Limited
 * All rights reserved.
 *
 * The license below extends only to copyright in the software and shall
 * not be construed as granting a license to any other intellectual
 * property including but not limited to intellectual property relating
 * to a hardware implementation of the functionality of the software
 * licensed hereunder.  You may use the software subject to the license
 * terms below provided that you ensure that this notice is replicated
 * unmodified and in its entirety in all distributions of the software,
 * modified or unmodified, in source code or in binary form.
 *
 * Copyright (c) 2003-2005,2014 The Regents of The University of Michigan
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met: redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer;
 * redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution;
 * neither the name of the copyright holders nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/**
 * @file
 * Definitions of a set associative indexing policy.
 */

#include "mem/cache/tags/indexing_policies/new_rand_idx.hh"

#include "base/intmath.hh"
#include "base/logging.hh"
#include "mem/cache/replacement_policies/replaceable_entry.hh"

NewRandIdx::NewRandIdx(const Params &p)
    : BaseIndexingPolicy(p),
      nbits(p.nbits)
{
    tagShift = floorLog2(p.size);
    indexMask = (1 << (floorLog2(p.size / p.entry_size)+nbits))-1;
    std::cout<<"NewRandIdx: indexMask: "<<indexMask<<
        ", setShift: "<<setShift<<", tagShift: "<<tagShift<<"\n";
    // GYGY debug
    // printf("GYGY debug NewRandIdx::NewRandIdx this: %p, &assoc: %p\n", this, &(this->assoc));
    printf("Creating NewRandIdx SZ:%lu, ASSOC: %lu, LINE_SZ: %lu!\n",
        p.size, p.assoc, p.entry_size);
    fatal_if(numSets != 1, "# of sets should be 1");
}

uint32_t
NewRandIdx::extractSet(const Addr addr) const
{
    //return (addr >> setShift) & setMask;
    panic_if(1, "This function NewRandIdx::extractSet "
        "should not be called!");
    return -1;
}

Addr
NewRandIdx::extractTag(const Addr addr) const
{
    return (addr >> (tagShift+nbits));
}

Addr
NewRandIdx::extractIndex(const Addr addr) const
{
    Addr extracted_index = (addr >> setShift) & indexMask;
    DPRINTF(Cache, "Addr:%x, setShift: %u, addr>>setShift:%x"
        "indexMask: %x, indx: %x\n",
        addr, setShift, addr >> setShift, indexMask, extracted_index);
    return extracted_index;
}

Addr
NewRandIdx::regenerateAddr(const Addr tag, const Addr index_bits) const
{
    DPRINTF(Cache, "TempDbg tag:%x, tagShift: %u, index:%x\n",
        tag, tagShift+nbits, index_bits);
    return (tag << (tagShift+nbits)) | (index_bits << setShift);
}

Addr
NewRandIdx::regenerateAddr(const Addr tag, const ReplaceableEntry* entry) const
{
    panic_if(1, "This function NewRandIdx::regenerateAddr "
        "should not be called!");
    return -1;
}

std::vector<ReplaceableEntry*>
NewRandIdx::getPossibleEntries(const Addr addr) const
{
    return sets[0];
}
