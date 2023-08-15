// Copyright (c) 2023, Tri Dao.

// Splitting the different head dimensions to different files to speed up compilation.

#include "flash_bwd_launch_template.h"

template<>
void run_mha_bwd_<cutlass::half_t, 256>(Flash_bwd_params &params, cudaStream_t stream, const bool configure) {
    run_mha_bwd_hdim256<cutlass::half_t>(params, stream, configure);
}