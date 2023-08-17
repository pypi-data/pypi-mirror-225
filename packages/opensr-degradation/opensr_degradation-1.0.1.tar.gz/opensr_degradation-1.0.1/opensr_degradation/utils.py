from typing import Optional, Union

import numpy as np
import torch
from skimage.exposure import match_histograms


def hq_histogram_matching(
    image1: torch.Tensor, image2: torch.Tensor, channel_axis: Optional[int] = 0
) -> torch.Tensor:
    """ Lazy implementation of histogram matching 

    Args:
        image1 (torch.Tensor): The low-resolution image (C, H, W).
        image2 (torch.Tensor): The super-resolved image (C, H, W).
        channel_axis (Optional[int], optional): The channel axis. Defaults to 0.
        
    Returns:
        torch.Tensor: The super-resolved image with the histogram of the target image.
    """

    # Go to numpy
    np_image1 = image1.detach().cpu().numpy()
    np_image2 = image2.detach().cpu().numpy()

    # Apply histogram matching
    np_image1_hat = match_histograms(np_image1, np_image2, channel_axis=channel_axis)

    # Go back to torch
    image1_hat = torch.from_numpy(np_image1_hat).to(image1.device)

    return image1_hat


def create_noisy_1(
    img: Union[np.ndarray, torch.Tensor], noisy_matrix: np.ndarray
) -> torch.Tensor:
    """ Create noisy image from a noisy matrix

    Args:
        img (Union[np.ndarray, torch.Tensor]): The image to be noised. It must
            be a numpy array or a torch tensor with shape (C, H, W).
        noisy_matrix (np.ndarray): The noisy matrix. It must be a numpy array.

    Returns:
        torch.Tensor: The noisy image.
    """

    # if image is torch tensor, convert to numpy
    if isinstance(img, torch.Tensor):
        img = img.detach().cpu().numpy()
        noisy_matrix = noisy_matrix.detach().cpu().numpy()

    # Ranges of the SNR matrix
    reflectance_ranges = np.arange(0, 0.5, 0.005)
    noisy_ranges = np.arange(-0.0101, 0.0101, 0.0002)

    # Categorize the reflectance
    r_cat = np.digitize(img, reflectance_ranges)

    # Create noisy model
    vfunc = np.vectorize(lambda x: np.random.choice(noisy_ranges, p=noisy_matrix[x,]))
    return torch.from_numpy(vfunc(r_cat)).squeeze().float()


def create_noisy_2(img: torch.Tensor) -> torch.Tensor:
    """ Create noisy image from a noisy matrix

    Args:
        img (torch.Tensor): The image to be noised. It must
            be a torch tensor with shape (C, H, W).
    Returns:
        torch.Tensor: The noisy image.
    """
    rnoisy = torch.normal(0, 0.025, size=img.shape).to(img.device)
    ratio_noisy = torch.sqrt(torch.mean(img ** 2, dim=(1, 2), keepdim=True)) * rnoisy
    return ratio_noisy
