import torch
import math
from torch import nn
import fmot
import numpy as np
from .conv1d import TemporalConv1d
from typing import List, Tuple
from torch import Tensor
from fmot.functional import cos_arctan
from . import atomics
from . import Sequencer
from .composites import TuningEpsilon
from python_speech_features.base import get_filterbanks
from .super_structures import SuperStructure

def _get_norm(normalized):
    norm = None
    if normalized:
        norm = 'ortho'
    return norm

def get_rfft_matrix(size, normalized=False):
    weight = np.fft.rfft(np.eye(size), norm=_get_norm(normalized))
    w_real, w_imag = np.real(weight), np.imag(weight)
    return torch.tensor(w_real).float(), torch.tensor(w_imag).float()

def get_irfft_matrix(size, normalized=False):
    in_size = size//2 + 1
    w_real = np.fft.irfft(np.eye(in_size), n=size, norm=_get_norm(normalized))
    w_imag = np.fft.irfft(np.eye(in_size)*1j, n=size, norm=_get_norm(normalized))
    return torch.tensor(w_real).float(), torch.tensor(w_imag).float()

def get_mel_matrix(sr, n_dft, n_mels=128, fmin=0.0, fmax=None, **kwargs):
    mel_matrix = get_filterbanks(
        nfilt=n_mels, 
        nfft=n_dft, 
        samplerate=sr, 
        lowfreq=fmin,
        highfreq=fmax)
    return torch.tensor(mel_matrix, dtype=torch.float32)

def get_dct_matrix(n, n_out=None, dct_type=2, normalized=False):
    N = n
    if n_out is None:
        n_out = n
    K = n_out

    if K > N:
        raise ValueError(f"DCT cannot have more output features ({K}) than input features ({N})")
    matrix = None
    if dct_type == 1:
        ns = np.arange(1, N-1)
        ks = np.arange(K)
        matrix = np.zeros((N, K))
        matrix[0, :] = 1
        matrix[-1, :] = -1**ks
        matrix[1:-1, :] = 2*np.cos((np.pi*ks.reshape(1,-1)*ns.reshape(-1,1))/(N-1))
    elif dct_type == 2:
        ns = np.arange(N).reshape(-1,1)
        ks = np.arange(K).reshape(1,-1)
        matrix = 2*np.cos(np.pi*ks*(2*ns+1)/(2*N))
        if normalized:
            matrix[:,0] /= np.sqrt(4*N)
            matrix[:,1:] /= np.sqrt(2*N)
    elif dct_type == 3:
        ns = np.arange(1, N).reshape(-1,1)
        ks = np.arange(K).reshape(1,-1)
        matrix = np.zeros((N, K))
        matrix[0, :] = 1
        matrix[1:, :] = 2*np.cos(np.pi*(2*ks+1)*ns/(2*N))
        if normalized:
            matrix[0, :] /= np.sqrt(N)
            matrix[1:, :] /= np.sqrt(2*N)
    elif dct_type == 4:
        ns = np.arange(N).reshape(-1,1)
        ks = np.arange(K).reshape(1,-1)
        matrix = 2*np.cos(np.pi*(2*ks+1)*(2*ns+1)/(4*N))
        if normalized:
            matrix /= np.sqrt(2*N)
    else:
        raise ValueError(f'DCT type {dct_type} is not defined.')
    return torch.tensor(matrix).float()

class RFFT(nn.Module):
    r"""DEPRECATED!

    Real-to-complex 1D Discrete Fourier Transform.

    Returns the real and imaginary parts as two separate tensors.

    Args:
        size (int): length of input signal
        normalized (bool): whether to use a normalized DFT matrix. Default is False

    Shape:
            - Input: :math:`(*, N)` where :math:`*` can be any number of additional dimensions.
              :math:`N` must match the :attr:`size` argument.
            - Output:
                - Real Part: :math:`(*, \lfloor N/2 \rfloor + 1)`
                - Imaginary Part: :math:`(*, \lfloor N/2 \rfloor + 1)`

    .. seealso::

        - :class:`IRFFT`
    """
    def __init__(self, size, normalized=False):
        super().__init__()
        w_real, w_imag = get_rfft_matrix(size, normalized)
        self.w_real = nn.Parameter(w_real, requires_grad=False)
        self.w_imag = nn.Parameter(w_imag, requires_grad=False)

    def forward(self, x: Tensor) -> Tuple[Tensor, Tensor]:
        r"""
        Args:
            x (Tensor): Input, of shape :math:`(*, N)`

        Returns:
            - Real part, of shape :math:`(*, \lfloor N/2 \rfloor + 1)`
            - Imaginary part, of shape :math:`(*, \lfloor N/2 \rfloor + 1)`
        """
        real = torch.matmul(x, self.w_real)
        imag = torch.matmul(x, self.w_imag)
        return real, imag

class IRFFT(nn.Module):
    r"""DEPRECATED!
    Inverse of the real-to-complex 1D Discrete Fourier Transform.

    Inverse to :class:`RFFT`. Requires two input tensors for the real and imaginary
    part of the RFFT.

    Args:
        size (int): length of original real-valued input signal
        normalized (bool): whether to use a normalized DFT matrix. Default is False.

    Shape:
        - Re: :math:`(*, \lfloor N/2 \rfloor + 1)` where :math:`*` can be any number
          of additional dimensions. :math:`N` must match the :attr:`size` argument.
        - Im: :math:`(*, \lfloor N/2 \rfloor + 1)`
        - Output: :math:`(*, N)`

    .. seealso::

        - :class:`RFFT`
    """
    def __init__(self, size, normalized=False):
        super().__init__()
        w_real, w_imag = get_irfft_matrix(size, normalized)
        self.w_real = nn.Parameter(w_real, requires_grad=False)
        self.w_imag = nn.Parameter(w_imag, requires_grad=False)

    def forward(self, real: Tensor, imag: Tensor) -> Tensor:
        r"""
        Args:
            real (Tensor): Real part of the input, of shape :math:`(*, \lfloor N/2 \rfloor + 1)`
            imag (Tensor): Imaginary part of the input,
                of shape :math:`(*, \lfloor N/2 \rfloor + 1)`.

        Returns:
            - Output, of shape :math:`(*, N)`
        """
        return torch.matmul(real, self.w_real) + torch.matmul(imag, self.w_imag)

class DCT(nn.Module):
    r"""
    Discrete Cosine Transformation.

    Performs the DCT on an input by multiplying it with the DCT matrix.
    DCT Types :attr:`1`, :attr:`2`, :attr:`3`, and :attr:`4` are implemented. See
    `scipy.fftpack.dct <https://docs.scipy.org/doc/scipy/reference/generated/scipy.fftpack.dct.html>`_
    for reference about the different DCT types. Type :attr:`2` is default.

    Args:
        in_features (int): Length of input signal that is going through the DCT
        out_features (int): Number of desired output DCT features. Default is :attr:`in_features`.
            Must satisfy :math:`\text{out_features} \leq \text{in_features}`
        dct_type (int): Select between types :attr:`1`, :attr:`2`, :attr:`3`, and :attr:`4`.
            Default is :attr:`2`.
        normalized (bool): If True and :attr:`dct_type` is :attr:`2`, :attr:`3`, or :attr:`4`,
            the DCT matrix will be normalized. Has no effect for :attr:`dct_type=1`.
            Setting normalized to True is equivalent to :attr:`norm="orth"` in
            `scipy.fftpack.dct <https://docs.scipy.org/doc/scipy/reference/generated/scipy.fftpack.dct.html>`_

    Shape:
        - Input: :math:`(*, N)` where :math:`N` is :attr:`in_features`
        - Output: :math:`(*, K)` where :math:`K` is :attr:`out_features`, or :attr:`in_features` if
          :attr:`out_features` is not specified.
    """
    def __init__(self, in_features, out_features=None, dct_type=2, normalized=True):
        super().__init__()
        weight = get_dct_matrix(n=in_features, n_out=out_features, dct_type=dct_type,
            normalized=normalized)
        self.weight = nn.Parameter(weight, requires_grad=False)

    def forward(self, x):
        r"""
        Args:
            x (Tensor): Input, of shape :math:`(*, N)`
        Returns:
            - Output, of shape :math:`(*, K)` where :math:`K` is :attr:`out_features`,
                or :attr:`in_features` if :attr:`out_features` is not specified.
        """
        return torch.matmul(x, self.weight)

class MaxMin(nn.Module):
    def __init__(self):
        super().__init__()
        self.gt0 = atomics.Gt0()

    def forward(self, x, y):
        x_g = self.gt0(x - y)
        y_g = 1 - x_g
        max_els = x_g*x + y_g*y
        min_els = y_g*x + x_g*y
        return max_els, min_els

class LogEps(nn.Module):
    r"""
    Natural logarithm with a minimum floor. Minimum floor is automatically
    tuned when exposed to data. The minimum floor ensures numerical stability.

    Returns:

        .. math::

            \text{output} = \begin{cases}
                \log(x) & x > \epsilon \\
                \log(\epsilon) & x \leq \epsilon
            \end{cases}
    """
    def __init__(self):
        super().__init__()
        self.add_eps = TuningEpsilon()

    def forward(self, x):
        """
        """
        x = self.add_eps(x)
        return torch.log(x)

class Magnitude(nn.Module):
    r"""
    Computes magnitude from real and imaginary parts.

    Mathematically equivalent to

    .. math::

        \text{mag} = \sqrt{\text{Re}^2 + \text{Im}^2},

    but designed to compress the signal as minimally as possible when quantized:

    .. math::

        &a_{max} = \text{max}(|\text{Re}|, |\text{Im}|) \\
        &a_{min} = \text{min}(|\text{Re}|, |\text{Im}|) \\
        &\text{mag} = a_{max}\sqrt{1 + \frac{a_{min}}{a_{max}}^2}

    .. note::

        .. math::

            \sqrt{1 + x^2} = \cos{\arctan{x}}
    """
    def __init__(self):
        super().__init__()
        self.add_epsilon = TuningEpsilon()
        self.max_min = MaxMin()
        self.mul = atomics.VVMul()

    def forward(self, real, imag):
        """
        Args:
            real (Tensor): Real part of input
            imag (Tensor): Imaginary part of input

        Returns:
            - Magnitude
        """
        a, b = self.max_min(real.abs(), imag.abs())
        eta = b / self.add_epsilon(a)
        eta_p = cos_arctan(eta)
        return self.mul(a, eta_p)
    
class _EMA(Sequencer):
    """Sequencer implementation of EMA"""
    def __init__(self, features: int, alpha: float, dim: int):
        super().__init__([[features]], 0, seq_dim=dim)
        assert 0 < alpha < 1
        self.alpha = alpha
        self.om_alpha = 1 - alpha

    @torch.jit.export
    def step(self, x: Tensor, state: List[Tensor]) -> Tuple[Tensor, List[Tensor]]:
        y, = state
        y = self.alpha * y + self.om_alpha * x
        return y, [y]

class EMA(nn.Module):
    """Exponential Moving Average
    
    Arguments:
        features (int): number of input features
        alpha (float): smoothing coefficient, between 0 and 1. Time constant is ``-1/log(alpha)`` frames
        dim (int): dimension to apply exponential moving average to. Should be the temporal/sequential dimension
    """
    def __init__(self, features: int, alpha: float, dim: int):
        super().__init__()
        self.ema = _EMA(features, alpha, dim)

    def forward(self, x):
        x, __ = self.ema(x)
        return x
    
class _AREMA(Sequencer):
    """Sequencer implementation of Attack-Release Exponential Moving Average (AREMA).

    Args:
        features (int): Number of input features.
        dim (int): Dimension to apply exponential moving average to. Should be the temporal/sequential dimension.
        attack_time (float): The attack time in seconds (the time constant for attack mode).
        release_time (float): The release time in seconds (the time constant for release mode).
        delta_t (float): The hop length (time difference between the start of two consecutive frames).
    """
    def __init__(self, features: int, dim: int, attack_time: float, release_time: float, delta_t: float):
        super().__init__([[features]], 0, seq_dim=dim) # batch_dim=0, seq_dim=1
        self.attack_time = attack_time
        self.release_time = release_time

        self.delta_t = delta_t

        self.attack_coeff = 1.0 - math.exp(-1.0 * self.delta_t / (self.attack_time))
        self.release_coeff = 1.0 - math.exp(-1.0 * self.delta_t / (self.release_time))

        self.gt0 = fmot.nn.Gt0()

    @torch.jit.export
    def step(self, x: Tensor, state: List[Tensor]) -> Tuple[Tensor, List[Tensor]]:

        y_prev, = state

        diff = x - y_prev

        # Apply attack coefficient if the new observation is greater than the previous EMA
        # Apply release coefficient if the new observation is less than or equal to the previous EMA
        diff_mask = self.gt0(diff) 
        alpha = diff_mask * self.attack_coeff + (1 - diff_mask) * self.release_coeff

        y = alpha * x + (1 - alpha) * y_prev
        
        return y, [y]

class AREMA(nn.Module):
    """Attack-Release Exponential Moving Average (AREMA) module.

    Args:
        features (int): Number of input features.
        dim (int): Dimension to apply exponential moving average to. Should be the temporal/sequential dimension.
        attack_time (float): The attack time in seconds (the time constant for attack mode).
        release_time (float): The release time in seconds (the time constant for release mode).
        delta_t (float): The hop length
    """
    def __init__(self, features: int, dim: int, attack_time: float, release_time: float, delta_t: float):
        super().__init__()
        self.arema = _AREMA(features, dim, attack_time, release_time, delta_t)

    def forward(self, x):
        x, __ = self.arema(x)
        return x
    

class DynamicRangeCompressor(nn.Module):
    """
    Implements Dynamic Range Compression as a PyTorch module.
    This module applies dynamic range compression to an input tensor.

    Args:
        threshold (float): The decibel value at which the compression starts.
        knee_width (float): The width of the knee region in decibels.
        ratio (float): The compression ratio.
        min_knee_width (float): The minimum allowed knee width.
    """

    def __init__(self, threshold=-80, knee_width=10, ratio=3, min_knee_width=1):
        super(DynamicRangeCompressor, self).__init__()

        self.threshold = float(threshold)
        self.knee_width = float(knee_width)
        self.ratio = float(ratio)

        self.gt0 = fmot.nn.Gt0()

        """
        Pre-Compute scalar operations at compile time 
        """
        self.const_one = (1/self.ratio - 1)
        self.const_two = (self.threshold - self.knee_width/2)
        self.const_three = self.knee_width * 2


    def forward(self, xG):
        """
        Forward pass of the Dynamic Range Compression module.

        Args:
            xG (torch.Tensor): The input tensor in decibel scale.

        Returns:
            torch.Tensor: The gain tensor in decibel scale that should be applied to the input for dynamic range compression.
        
        Note:
            1) xG must be supplied in the logarithmic domain, which can be any base, such as log10 or loge.
            2) When converting the gain back to the linear domain, ensure that the appropriate base is used. 
               For example, if the log domain was based on log10, the conversion can be done as follows: gain_linear = 10 ** (gain_db / 10).
        """        
        # In the code below the explanations assume: 
        # W = self.knee_width, R = self.ratio, T = self.threshold
        
        # Create a mask where the condition (2 * (xG - T) > W) is True.
        # These points are in the compression region and will be scaled down by 1/compression_ratio.
        compression_region_mask = self.gt0(2 * (xG - self.threshold) - self.knee_width)

        # Update yG using the compression_region_mask
        # yG = (T + (xG - T) / R) * compression_region_mask + xG * (1 - compression_region_mask)
        yG = (self.threshold + (xG - self.threshold) / self.ratio) * compression_region_mask 
        yG = yG + xG * (1 - compression_region_mask)

        # Create a mask where the condition (2 * torch.abs(xG - T) <= W) is True.
        # These points are in the transition region, which will be smoothed out using the knee width.
        transition_region_mask = self.gt0(self.knee_width - 2 * torch.abs(xG - self.threshold))

        # Update yG using the transition_region_mask
        # yG = (xG + (1 / R - 1) * (xG - T + W / 2) ** 2 / (2 * W)) * transition_region_mask + yG * (1 - transition_region_mask)
        yG = (xG + (self.const_one) * (xG - self.const_two) ** 2 / (self.const_three)) * transition_region_mask + yG * (1 - transition_region_mask)

        G = yG - xG
        return G


class Limiter(nn.Module):
    """
    Limiter module, which limits the amplitude of a signal to a specified threshold.
    The transition region around the threshold is smoothed using the knee width parameter.

    Args:
        threshold (float): The threshold above which the signal will be limited.
        knee_width (float): The width of the transition region around the threshold. Default: 10
        min_knee_width (float): The minimum width allowed for the transition region. Default: 1
    """

    def __init__(self, threshold, knee_width=10, min_knee_width=1):
        super(Limiter, self).__init__()
        
        self.threshold = float(threshold) #nn.Parameter(torch.tensor(threshold), requires_grad=False)
        self.knee_width = float(knee_width) #nn.Parameter(torch.tensor(knee_width), requires_grad=False)
        self.gt0 = fmot.nn.Gt0()

        """
        Pre-Compute scalar operations at compile time 
        """
        self.const_one = (self.threshold - self.knee_width/2)
        self.const_two = self.knee_width * 2

    def forward(self, xG):
        """
        Forward pass of the Limiter module.

        Args:
            xG (torch.Tensor): The input tensor in decibel scale.

        Returns:
            torch.Tensor: The gain tensor in decibel scale that should be applied to the input for limiting.

        Note:
            1) xG must be supplied in the logarithmic domain, which can be any base, such as log10 or loge.
            2) When converting the gain back to the linear domain, ensure that the appropriate base is used. 
               For example, if the log domain was based on log10, the conversion can be done as follows: gain_linear = 10 ** (gain_db / 10).
        """
        # In the code below the explanations assume: 
        # W = self.knee_width, T = self.threshold
        
        # Create a mask where the condition (2 * (xG - T) > W) is True.
        # These points are in the compression region and will be limited to the threshold.
        limiter_region_mask = self.gt0(2 * (xG - self.threshold) - self.knee_width)
        # Update yG using the limiter_region_mask
        yG = self.threshold * limiter_region_mask + xG * (1 - limiter_region_mask)

        # Create a mask where the condition (2 * torch.abs(xG - T) <= W) is True.
        # These points are in the transition region, which will be smoothed out using the knee width.
        transition_region_mask = self.gt0(self.knee_width - 2 * torch.abs(xG - self.threshold))
        # Update yG using the transition_region_mask
        
        # yG = (xG - (xG - T + W / 2) ** 2 / (2 * W)) * transition_region_mask + yG * (1 - transition_region_mask)
        yG = (xG - (xG - self.const_one) ** 2 / (self.const_two)) * transition_region_mask + yG * (1 - transition_region_mask)

        # Compute resultant gain
        G = yG - xG
        return G


class WideDynamicRangeCompressor(nn.Module):

    def __init__(self, compress_thresh,
                       compress_ratio,
                       lim_thresh,
                       knee_width=10):
        super(WideDynamicRangeCompressor, self).__init__()

        self.compressor = DynamicRangeCompressor(threshold=compress_thresh, knee_width=knee_width, ratio=compress_ratio, min_knee_width=1)
        self.limiter = Limiter(threshold=lim_thresh, knee_width=knee_width, min_knee_width=1)
        """
        Initializes the WideDynamicRangeCompressor.

        Args:
            compress_thresh (float): Threshold in dB for the dynamic range compressor.
            compress_ratio (float): Compression ratio for the dynamic range compressor.
            lim_thresh (float): Threshold in dB for the limiter.
            knee_width (float, optional): Knee width in dB for both the compressor and limiter. Defaults to 10.
        """

    def forward(self, xG):
        """
        Forward pass of the Wide Dynamic Range Compression module.

        Args:
            xG (torch.Tensor): The input tensor in decibel scale.

        Returns:
            torch.Tensor: The gain tensor in decibel scale that should be applied to the input for WDRC.
        
        Note:
            1) xG must be supplied in the logarithmic domain, which can be any base, such as log10 or loge.
            2) When converting the gain back to the linear domain, ensure that the appropriate base is used. 
               For example, if the log domain was based on log10 (xG = 20 * log10(x_linear)), the conversion can be done as follows: gain_linear = 10 ** (gain_db / 20).
        """    
        # Apply DRC
        gain_db = self.compressor(xG)
        xG_compressed = gain_db + xG

        # Apply limiting
        gain_db = self.limiter(xG_compressed)
        xG_compressed = gain_db  +  xG_compressed

        # Find the Overall gain
        gain_overall_db = xG_compressed - xG
        return gain_overall_db


class WDRCModule(nn.Module):

    def __init__(self, sr,
                       n_fft,
                       n_mels,
                       attack_time,
                       release_time,
                       delta_t,
                       compress_thresh,
                       compress_ratio,
                       lim_thresh,
                       knee_width=10,
                       seq_len_dim=1,
                       ) -> None:
        """
        Initializes the WDRCModule.

        Args:
            sr (int): Sample rate of the input audio signal.
            n_fft (int): Number of FFT points in the STFT.
            n_mels (int): Number of Mel filters.
            attack_time (float): Attack time for the AREMA smoothing in seconds.
            release_time (float): Release time for the AREMA smoothing in seconds.
            delta_t (float): Time between consecutive frames of the input in seconds.
            compress_thresh (float): Threshold in dB for the dynamic range compressor.
            compress_ratio (float): Compression ratio for the dynamic range compressor.
            lim_thresh (float): Threshold in dB for the limiter.
            knee_width (float, optional): Knee width in dB for both the compressor and limiter. Defaults to 10.
            seq_len_dim (int, optional): The index of the sequence length dimension in the input tensor. Defaults to 1.
        """
        super().__init__()
        self.arema = AREMA(features=n_mels, dim=seq_len_dim, attack_time=attack_time, release_time=release_time, delta_t=delta_t)


        self.wdrc = WideDynamicRangeCompressor(compress_thresh=compress_thresh, compress_ratio=compress_ratio, lim_thresh=lim_thresh, knee_width=knee_width)
        self.mel_transform = MelFilterBank(sr=sr, n_fft=n_fft, n_mels=n_mels, fmin=0.0)
        self.inv_mel_transform = InverseMelFilterBank(sr=sr, n_fft=n_fft, n_mels=n_mels, fmin=0.0, mode='transpose_stft_norm')

        self.magnitude = Magnitude()

        self.ln10_div_20 = 0.115

    def forward(self, stft_real_imag):
        """
        Apply the WDRC gain to the input STFT, returning the enhanced STFT.

        Args:
            stft_real_imag (torch.Tensor): The real and imaginary parts of the input STFT stacked along the feat dimension.

        Returns:
            torch.Tensor: The enhanced STFT with real and imaginary parts concatenated along the feat dimension.
        """
        stft_real, stft_imag = torch.chunk(stft_real_imag, chunks=2, dim=-1)

        # Compute power spectrum from real and imaginary parts of the STFT
        power_spec = self.magnitude(real=stft_real, imag=stft_imag) 

        # Convert power spectrum to Mel filter bank
        mel_fbank = self.mel_transform(power_spec)

        """
        Compute the WDRC gain in Mel domain
        """

        # Get the AREMA
        mfbank_fsema = self.arema(mel_fbank)

        # Convert `mfbank_fsema` to Log Domain for DRC/Limiter
        log_mel_spectrogram = 20 * torch.log10(mfbank_fsema + 1e-6)


        # Find the overall gain in dB -> And convert to linear scale
        wdrc_mel_gains_db = self.wdrc(log_mel_spectrogram)
        wdrc_mel_gains = torch.exp(self.ln10_div_20 * wdrc_mel_gains_db)

        """
        Convert Gain from Mel to STFT domain
        """

        # Convert the WDRC gain from Mel domain to STFT domain
        wdrc_stft_gains = self.inv_mel_transform(wdrc_mel_gains)

        """
        Apply gain in STFT domain
        """

        # Apply WDRC gains to the real and imaginary parts of the STFT
        stft_real_enhanced = wdrc_stft_gains * stft_real
        stft_imag_enhanced = wdrc_stft_gains * stft_imag

        stft_enhanced_real_imag = torch.cat([stft_real_enhanced, stft_imag_enhanced], dim=-1)

        return stft_enhanced_real_imag

    


class MelFilterBank(nn.Module):
    r"""
    Project FFT bins into Mel-Frequency bins.

    Applies a linear transformation to project FFT bins into Mel-frequency bins.

    Args:
        sr (int): audio sampling rate (in Hz)
        n_fft (int): number of FFT frequencies
        n_mels (int): number of mel-frequencies to create
        fmin (float): lowest frequency (in Hz), default is 0
        fmax (float): maximum frequency (in Hz). If :attr:`None`, the Nyquist frequency
            :attr:`sr/2.0` is used. Default is :attr:`None`.
        **kwargs: keyword arguments to pass to
            `librosa.filters.mel <https://librosa.org/doc/latest/generated/librosa.filters.mel.html>`_
            when generating the mel transform matrix

    Shape:
        - Input: :math:`(*, C_{in})` where :math:`*` is any number of dimensions and
          :math:`C_{in} = \lfloor \text{n_dft}/2 + 1 \rfloor`
        - Output: :math:`(*, \text{n_mels})`
    """
    def __init__(self, sr, n_fft, n_mels=128, fmin=0.0, fmax=None, **kwargs):
        super().__init__()
        weight = get_mel_matrix(sr, n_fft, n_mels, fmin, fmax, **kwargs)
        self.weight = nn.Parameter(weight.t(), requires_grad=False)

    def forward(self, x):
        """"""
        return torch.matmul(x, self.weight)


class InverseMelFilterBank(nn.Module):
    """
    Implements the Inverse Mel Filter Bank, which converts the Mel scale spectrogram back into the linear frequency domain.

    Attributes:
        weight (nn.Parameter): The weight matrix, computed using the inverse of the Mel filter bank matrix.
    """

    def __init__(self, sr: int, n_fft: int, n_mels: int = 128, fmin: float = 0.0, mode: str = 'transpose', fmax: float = None, **kwargs):
        """
        Initializes the InverseMelFilterBank.

        Args:
            sr (int): Sample rate of the input audio signal.
            n_fft (int): Number of FFT points in the STFT.
            n_mels (int, optional): Number of Mel filters. Defaults to 128.
            fmin (float, optional): Minimum frequency of the Mel filter bank. Defaults to 0.0.
            mode (str, optional): The method to use for computing the inverse Mel filter bank matrix. 
                                  Options: 'transpose', 'pinv'. Defaults to 'transpose'.
            fmax (float, optional): Maximum frequency of the Mel filter bank. Defaults to None.
        """
        super().__init__()
        mel_matrix = get_mel_matrix(sr, n_fft, n_mels, fmin, fmax, **kwargs).T # (N_FFTS, N_MELS)

        if mode == 'transpose':
            inv_mel_matrix = mel_matrix.T # (N_MELS, N_FFT)
        elif mode == 'transpose_stft_norm':
            inv_mel_matrix = mel_matrix.T # (N_MELS, N_FFT)
            inv_mel_matrix = self.normalize_inverse_mel_matrix_columns(inv_mel_matrix=inv_mel_matrix) # (N_MELS, N_FFT)
        elif mode == 'pinv':
            inv_mel_matrix = torch.linalg.pinv(mel_matrix) # (N_MELS, N_FFT)

        self.weight = nn.Parameter(inv_mel_matrix, requires_grad=False) # (N_MELS, N_FFT)

    @staticmethod
    def normalize_inverse_mel_matrix_columns(inv_mel_matrix, eps=1e-7):
        """
        Normalize the columns of the inverse Mel matrix. This is done to ensure that a Mel-domain 
        matrix of all ones is transformed to a STFT-domain matrix of all ones. In essence, 
        it scales each column of the matrix so that the sum of its elements is equal to 1.
        
        This normalization step is important in the context of spectrogram inversion, 
        where the Mel matrix is used to map a STFT (Short-Time Fourier Transform) spectrogram 
        to a Mel spectrogram and vice versa. The normalization ensures the consistency of this mapping.

        Args:
            inv_mel_matrix (torch.Tensor): Shape: (N_MELS, N_FFTS). The original inverse Mel matrix. This is a 2-D tensor
            where each column represents a frequency band of the Mel scale.
            Shape: (N_MELS, N_FFTS)

        Returns:
            torch.Tensor: Shape: (N_MELS, N_FFTS). The normalized inverse Mel matrix. This matrix has the same dimensions 
            as the input but each column of the matrix has been scaled so that the sum of its 
            elements is equal to 1.
        """
        # figure out which columns have sum=0. for thos columns, add a small value (eps)
        column_sums = torch.sum(inv_mel_matrix, dim=0) #Shape:  (N_FFT,)
        zero_cols = torch.where(column_sums == 0)[0] 
        inv_mel_matrix[:, zero_cols] = eps

        # Compute the sum of each column in the inverse Mel matrix.
        column_sums = torch.sum(inv_mel_matrix, dim=0)

        # Find the indices of the columns that do not sum to 1.
        non_one_columns = torch.where(column_sums != 1)[0]

        # Normalize each column that does not sum to 1.
        for column in non_one_columns:
            inv_mel_matrix[:, column] =  inv_mel_matrix[:, column] / (torch.sum(inv_mel_matrix[:, column]) + eps)

        return inv_mel_matrix


    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Applies the inverse Mel filter bank transformation to the input tensor.

        Args:
            x (torch.Tensor): Input tensor of shape (batch_size, seq_length, n_mels).

        Returns:
            torch.Tensor: Output tensor of shape (batch_size, seq_length, n_fft//2 + 1).
        """
        return torch.matmul(x, self.weight)
    
    
class MelTranspose(nn.Linear):
    r"""
    Project Mel-Frequency bins back into FFT bins.

    Args:
        sr (int): audio sampling rate (in Hz)
        n_fft (int): number of FFT frequencies
        n_mels (int): number of mel-frequencies to create
        fmin (float): lowest frequency (in Hz), default is 0
        fmax (float): maximum frequency (in Hz). If :attr:`None`, the Nyquist frequency
            :attr:`sr/2.0` is used. Default is :attr:`None`.

    Shape:
        - Input: :math:`(*, C_{in})` where :math:`*` is any number of dimensions and
          :math:`C_{in} = \lfloor \text{n_dft}/2 + 1 \rfloor`
        - Output: :math:`(*, \text{n_mels})`
    """
    def __init__(self, sr, n_fft, n_mels, fmin=0.0, fmax=None):
        super().__init__(
            out_features=n_fft//2 + 1,
            in_features=n_mels,
            bias=False)
        mat = get_mel_matrix(sr, n_fft, n_mels, fmin, fmax).T
        self.weight = nn.Parameter(mat, requires_grad=False)


class _Atan2(nn.Module):
    """Element-wise arctangent of ``y / x`` with consideration of the quadrant. Returns a new tensor with the 
    signed angles in radians between vector ``(x, y)`` and vector ``(1, 0)``. Useful in computation of complex phase.

    .. note:: 

        Note that input ``x``, the second input, is used as the x-coordinate, while ``y``, the first input, is used as the
        y-coordinate.

    .. note::

        We follow the convention that ``atan2(0, 0) = 0``, which is consistent with PyTorch's behavior
    
    """

    def __init__(self):
        super().__init__()
        self.gt0 = fmot.nn.Gt0()
        self.pi_halves = math.pi / 2
        self.two_pi = 2 * math.pi
        self.pi = math.pi
        self.eps = fmot.nn.TuningEpsilon(eps=2**-15)

    def forward(self, y, x):
        xgt0 = self.gt0(x)
        ygt0 = self.gt0(y)
        xlte0 = 1 - xgt0

        # offset = { 0,   x > 0
        #          { pi,  x<=0, y > 0
        #          { -pi, x<=0, y <=0
        offset = xlte0 * (self.two_pi * ygt0 - self.pi)

        # compute using just positive values
        # using arctan(-x) = -arctan(x)
        sign = (2 * xgt0 - 1) * (2 * ygt0 - 1)

        # take advantage of arctan(a/b) = -arctan(b/a) + pi/2 for positive b, a
        # to flip the ratio to avoid small denominators

        y_abs = torch.abs(y)
        x_abs = torch.abs(x)

        xgty = self.gt0(x_abs - y_abs)
        ygtex = 1 - xgty
        flip_offset = self.pi_halves * ygtex
        flip_sign = 2 * xgty - 1
        num = y_abs * xgty + x_abs * ygtex
        den = x_abs + y_abs - num

        # res = sign * torch.atan(torch.abs(y) / torch.abs(x)) + offset
        res = sign * (flip_sign * torch.atan(num / self.eps(den)) + flip_offset) + offset

        return res

class _MagNormalizer(nn.Module):
    def __init__(self):
        super().__init__()
        self.mag = Magnitude()
        self.eps = TuningEpsilon(eps=2**-14)

    def forward(self, x, y):
        mag = self.mag(x, y)
        rmag = torch.reciprocal(self.eps(mag))
        x = x * rmag
        y = y * rmag
        return x, y

class Atan2(SuperStructure):
    """Element-wise arctangent of ``y / x`` with consideration of the quadrant. Returns a new tensor with the 
    signed angles in radians between vector ``(x, y)`` and vector ``(1, 0)``. Useful in computation of complex phase.

    Arguments:
        norm (bool, optional): Whether to normalize inputs ``x`` and ``y`` by sqrt(x^2 + y^2) before performing atan2.
            This does not change the result, but reduces quantization error for small magnitude inputs. Default True.

    .. note:: 

        Note that input ``x``, the second input, is used as the x-coordinate, while ``y``, the first input, is used as the
        y-coordinate.

    .. note::

        We follow the convention that ``atan2(0, 0) = 0``, which is consistent with PyTorch's behavior
    
    """
    def __init__(self, norm=True):
        super().__init__()
        self.norm = norm

        if norm:
            self.normalizer = _MagNormalizer()

        self.atan = _Atan2()

    @torch.jit.ignore()
    def forward(self, y, x):
        if self.norm:
            y, x = self.normalizer(y, x)
        return self.atan(y, x)
    
class MagPhase(nn.Module):
    """Computes elementwise magnitude and phase (in radians) of a complex tensor"""
    def __init__(self):
        super().__init__()
        self.mag = Magnitude()
        self.eps = TuningEpsilon(eps=2**-14)
        self.atan2 = Atan2(norm=False)

    def forward(self, re: Tensor, im: Tensor) -> Tuple[Tensor, Tensor]:
        mag = self.mag(re, im)
        rmag = torch.reciprocal(self.eps(mag))

        re = re * rmag
        im = im * rmag

        phase = self.atan2(im, re)
        return mag, phase

class Phase(nn.Module):
    """Computes the phase (in radians) of a complex number"""
    def __init__(self):
        super().__init__()
        self.atan2 = Atan2(norm=True)

    def forward(self, re, im):
        return self.atan2(im, re)
    
class PolarToRect(nn.Module):
    """Converts a polar representation of a complex number 
    to rectangular form (inverse to MagPhase)."""
    def forward(self, mag: Tensor, phase: Tensor) -> Tuple[Tensor, Tensor]:
        re = torch.cos(phase) * mag
        im = torch.sin(phase) * mag
        return re, im