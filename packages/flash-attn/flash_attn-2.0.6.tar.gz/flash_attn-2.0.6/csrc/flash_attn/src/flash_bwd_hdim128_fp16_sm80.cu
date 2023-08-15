// Copyright (c) 2023, Tri Dao.

// Splitting the different head dimensions to different files to speed up compilation.

#include "flash_bwd_launch_template.h"

// template<>
// void run_mha_bwd_<cutlass::half_t, 128>(Flash_bwd_params &params, cudaStream_t stream, const bool configure) {
//     using elem_type = cutlass::half_t;
//     if (params.h == params.h_k) {
//     // run_flash_bwd<Flash_bwd_kernel_traits<128, 32, 128, 8, 2, 2, 2, false, false, elem_type>>(params, stream, configure);
//     // This is faster, in the case of sequence-parallel bwd (where we need fewer registers).
//     // Out of these three, the 2nd one is slightly faster (2% faster than the first). Idk why.
//     // run_flash_bwd<Flash_bwd_kernel_traits<128, 64, 128, 8, 2, 2, 2, false, false, elem_type>>(params, stream, configure);
//         run_flash_bwd<Flash_bwd_kernel_traits<128, 64, 128, 8, 2, 4, 2, false, false, elem_type>>(params, stream, configure);
//     // run_flash_bwd<Flash_bwd_kernel_traits<128, 64, 128, 8, 2, 4, 4, false, false, elem_type>>(params, stream, configure);
//     // run_flash_bwd<Flash_bwd_kernel_traits<128, 128, 64, 8, 4, 4, 4, false, false, elem_type>>(params, stream, configure);
//     } else {
//         run_flash_bwd_seqq_parallel<Flash_bwd_kernel_traits<128, 128, 64, 8, 4, 4, 4, false, false, elem_type>>(params, stream, configure);
//     }
// }

template<>
void run_mha_bwd_<cutlass::half_t, 128>(Flash_bwd_params &params, cudaStream_t stream, const bool configure) {
    run_mha_bwd_hdim128<cutlass::half_t>(params, stream, configure);
}