from typing import Tuple

import numpy as np


def calc_wsdr(hypothesis: np.ndarray,
              reference: np.ndarray,
              with_log: bool = False,
              with_negate: bool = False) -> Tuple[float, np.ndarray, np.ndarray]:
    """Calculate weighted SDR (signal distortion ratio) using all source inputs of size [samples, nsrc].
       Uses true reference energy ratios to weight each cross-correlation coefficient cc = <y,yˆ>/∥y∥∥yˆ∥
       in a sum over all sources.

       range is -1 --> 1 as correlation/estimation improves or with_log -3db --> 70db (1e7 max)
       if with_negate, range is 1 --> -1 as correlation improves and with_log range 3db --> -70db (1e-7 min)

       Returns:  wsdr      scalar weighted signal-distortion ratio
                 ccoef     nsrc vector of cross correlation coefficients
                 cweights  nsrc vector of reference energy ratio weights

    Reference:
        WSDR: 2019-ICLR-dcunet-phase-aware-speech-enh

    :param hypothesis: [samples, nsrc]
    :param reference: [samples, nsrc]
    :param with_log: enable scaling (return 10*log10)
    :param with_negate: enable negation (for use as a loss function)
    :return: (wsdr, ccoef, cweights)
    """
    nsrc = reference.shape[-1]
    assert hypothesis.shape[-1] == nsrc

    # Calculate cc = <y,yˆ>/∥y∥∥yˆ∥ always in range -1 --> 1, size [1,nsrc]
    ref_e = np.sum(reference ** 2, axis=0, keepdims=True)  # [1,nsrc]
    hy_e = np.sum(hypothesis ** 2, axis=0, keepdims=True)
    allref_e = np.sum(ref_e)
    cc = np.zeros(nsrc)  # calc correlation coefficient
    cw = np.zeros(nsrc)  # cc weights (energy ratio)
    for i in range(nsrc):
        denom = np.sqrt(ref_e[0, i]) * np.sqrt(hy_e[0, i]) + 1e-7
        cc[i] = np.sum(reference[:, i] * hypothesis[:, i], axis=0, keepdims=True) / denom
        cw[i] = ref_e[0, i] / (allref_e + 1e-7)

    # Note: tests show cw sums to 1.0 (+/- 7 digits), so just use cw for weighted sum
    if with_negate:  # for use as a loss function
        wsdr = float(np.sum(cw * -cc))  # cc always in range 1 --> -1
        if with_log:
            wsdr = max(wsdr, -1.0)
            wsdr = 10 * np.log10(wsdr + 1 + 1e-7)  # range 3 --> -inf (or 1e-7 limit of -70db)
    else:
        wsdr = float(np.sum(cw * cc))  # cc always in range -1 --> 1
        if with_log:
            wsdr = min(wsdr, 1.0)  # (np.sum(cw * cc) needs sat ==1.0 for log)
            wsdr = 10 * np.log10(-1 / (wsdr - 1 - 1e-7))  # range -3 --> inf (or 1e-7 limit of 70db)

    return float(wsdr), cc, cw

    # From calc_sa_sdr:
    # These should include a noise to be a complete mixture estimate, i.e.,
    #     noise_est = sum-over-all-srcs(s_est(0:nsamples, :) - sum-over-non-noisesrc(s_est(0:nsamples, n))
    # should be one of the sources in reference (s_true) and hypothesis (s_est).
    #
    # Calculates -10*log10(sumn(||sn||^2) / sumn(||sn - shn||^2)
    # Note: for SA method, sums are done independently on ref and error before division, vs. SDR and SI-SDR
    # where sum over n is taken after divide (before log).  This is more stable in noise-only cases and also
    # when some sources are poorly estimated.
    # TBD: add soft-max option with eps and tau params
    #
    # if with_scale:
    #     # calc 1 x nsrc scaling factors
    #     ref_energy = np.sum(reference ** 2, axis=0, keepdims=True)
    #     # if ref_energy is zero, just set scaling to 1.0
    #     with np.errstate(divide='ignore', invalid='ignore'):
    #         opt_scale = np.sum(reference * hypothesis, axis=0, keepdims=True) / ref_energy
    #         opt_scale[opt_scale == np.inf] = 1.0
    #         opt_scale = np.nan_to_num(opt_scale, nan=1.0)
    #     scaled_ref = opt_scale * reference
    # else:
    #     scaled_ref = reference
    #     opt_scale = np.ones((1, reference.shape[1]), dtype=float)
    #
    # # Calculate Lsdr = −<y,yˆ>/∥y∥∥yˆ∥ always in range [1 --> -1], size [batch,]
    # t_tru_sq = torch.sum(torch.square(t_tru), -1)
    # t_denom = torch.sqrt(t_tru_sq) * torch.sqrt(torch.sum(torch.square(t_est), -1)) + 1e-7
    # t_wsdr = -torch.divide(torch.sum(torch.multiply(t_tru, t_est), -1), t_denom)
    # n_tru_sq = torch.sum(torch.square(n_tru), -1)
    # n_denom = torch.sqrt(torch.sum(torch.square(n_tru), -1)) \
    #           * torch.sqrt(torch.sum(torch.square(n_est), -1)) + 1e-7
    # n_wsdr = -torch.divide(torch.sum(torch.multiply(n_tru, n_est), -1), n_denom)
    # if self.cl_noise_wght > 0:
    #     wsdr = self.cl_target_wght * t_wsdr + self.cl_noise_wght * n_wsdr
    # else:  # adaptive per relative strength of target vs noise:  α = ||y||2/(||y||2 +||z||2)
    #     tweight = torch.divide(t_tru_sq, t_tru_sq + n_tru_sq + 1e-7)  # energy ratio target vs. noise
    #     wsdr = tweight * t_wsdr + (1 - tweight) * n_wsdr
    # wsdr = torch.mean(wsdr)  # reduction to scalar
    #
    # # multisrc sa-sdr, inputs must be [samples, nsrc]
    # err = scaled_ref - hypothesis
    #
    # # -10*log10(sumk(||sk||^2) / sumk(||sk - shk||^2)
    # # sum over samples and sources
    # num = np.sum(reference ** 2)
    # den = np.sum(err ** 2)
    # if num == 0 and den == 0:
    #     ratio = np.inf
    # else:
    #     ratio = num / (den + np.finfo(np.float32).eps)
    #
    # sa_sdr = 10 * np.log10(ratio)
    #
    # if with_negate:
    #     # for use as a loss function
    #     sa_sdr = -sa_sdr
    #
    # return sa_sdr, opt_scale
