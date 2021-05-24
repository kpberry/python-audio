import numpy as np
from tqdm import tqdm

from springs import SpringChain


def spring_chain_reverb(samples: np.array, chain: SpringChain):
    reverb = np.zeros(samples.shape)
    for i, s in tqdm(enumerate(samples)):
        chain.apply_force_left(s)
        chain.act()
        reverb[i] = chain.get_force_at_right()
    return reverb


def kernel_reverb(samples: np.array, kernel: np.array):
    result = np.zeros(samples.shape)
    for i, s in tqdm(list(enumerate(samples))):
        end = min(i + len(kernel), len(samples))
        result[i:end] += s * kernel[:end - i]
    return result
