from typing import Union

import numpy as np
import pkg_resources
import torch
from opensr_degradation.kernels import BellBlur, GaussianBlur, SigmoidBlur
from opensr_degradation.parameters import parameters
from opensr_degradation.utils import hq_histogram_matching
from sklearn.linear_model import LinearRegression


def create_noisy(img, noisy_matrix):
    # Ranges of the SNR matrix
    reflectance_ranges = np.arange(0, 0.5, 0.005)
    noisy_ranges = np.arange(-0.0101, 0.0101, 0.0002)

    # Categorize the reflectance
    r_cat = np.digitize(img, reflectance_ranges)

    # Create noisy model
    vfunc = np.vectorize(lambda x: np.random.choice(noisy_ranges, p=noisy_matrix[x,]))
    return vfunc(r_cat)


class BlurModel(torch.nn.Module):
    def __init__(
        self, kernel_type: str = "gaussian", device: Union[str, torch.device] = "cpu"
    ):
        super(BlurModel, self).__init__()
        if kernel_type == "gaussian":
            pa = parameters["gaussian"]
            self.interpolation = pa["interpolation"]
            with torch.no_grad():
                self.blur_kernel_red = GaussianBlur(
                    kernel_size=17, params=pa["red"]["parameters"], device=device
                )
                self.blur_kernel_green = GaussianBlur(
                    kernel_size=17, params=pa["green"]["parameters"], device=device
                )
                self.blur_kernel_blue = GaussianBlur(
                    kernel_size=17, params=pa["blue"]["parameters"], device=device
                )
                self.blur_kernel_nir = GaussianBlur(
                    kernel_size=17, params=pa["nir"]["parameters"], device=device
                )
                self.blur_kernel = torch.stack(
                    [
                        self.blur_kernel_red.kernel,
                        self.blur_kernel_green.kernel,
                        self.blur_kernel_blue.kernel,
                        self.blur_kernel_nir.kernel,
                    ]
                )[:, None].to(device)
        elif kernel_type == "bell":
            with torch.no_grad():
                pa = parameters["bellshaped"]
                self.interpolation = pa["interpolation"]
                self.blur_kernel_nir = BellBlur(
                    kernel_size=17, params=pa["nir"]["parameters"], device=device
                )
                self.blur_kernel_red = BellBlur(
                    kernel_size=17, params=pa["red"]["parameters"], device=device
                )
                self.blur_kernel_green = BellBlur(
                    kernel_size=17, params=pa["green"]["parameters"], device=device
                )
                self.blur_kernel_blue = BellBlur(
                    kernel_size=17, params=pa["blue"]["parameters"], device=device
                )
                self.blur_kernel = torch.stack(
                    [
                        self.blur_kernel_red.kernel,
                        self.blur_kernel_green.kernel,
                        self.blur_kernel_blue.kernel,
                        self.blur_kernel_nir.kernel,
                    ]
                )[:, None].to(device)
        elif kernel_type == "sigmoid":
            with torch.no_grad():
                pa = parameters["sigmoid"]
                self.interpolation = pa["interpolation"]
                self.blur_kernel_nir = SigmoidBlur(
                    kernel_size=17, params=pa["nir"]["parameters"], device=device
                )
                self.blur_kernel_red = SigmoidBlur(
                    kernel_size=17, params=pa["red"]["parameters"], device=device
                )
                self.blur_kernel_green = SigmoidBlur(
                    kernel_size=17, params=pa["green"]["parameters"], device=device
                )
                self.blur_kernel_blue = SigmoidBlur(
                    kernel_size=17, params=pa["blue"]["parameters"], device=device
                )
                self.blur_kernel = torch.stack(
                    [
                        self.blur_kernel_red.kernel,
                        self.blur_kernel_green.kernel,
                        self.blur_kernel_blue.kernel,
                        self.blur_kernel_nir.kernel,
                    ]
                )[:, None].to(device)
        elif kernel_type == "none":
            pass
        else:
            raise NotImplementedError(f"Kernel type {kernel_type} is not implemented.")
        self.kernel_type = kernel_type

    def forward(self, x):
        if self.kernel_type == "none":
            lr_hat = torch.nn.functional.interpolate(
                input=x[None], scale_factor=0.250, mode="bicubic", antialias=True
            ).squeeze()
        else:
            lr_hat = torch.nn.functional.interpolate(
                input=x[None], scale_factor=2, mode="nearest", antialias=False
            )
            lr_hat = torch.nn.functional.conv2d(
                lr_hat, self.blur_kernel, groups=4, padding="same"
            )
            lr_hat = torch.nn.functional.interpolate(
                input=lr_hat,
                scale_factor=0.125,
                mode=self.interpolation,
                antialias=False,
            ).squeeze()

        return lr_hat


class ReflectanceModel(torch.nn.Module):
    def __init__(
        self,
        device: Union[str, torch.device] = "cpu",
        correction: str = "histogram_matching",
    ):
        super(ReflectanceModel, self).__init__()

        file = pkg_resources.resource_filename(
            "opensr_degradation", "models/model_reflectance.pt"
        )

        # load torchscript model from file
        self.reflectance = torch.jit.load(file, map_location=device)
        self.correction = correction

    def forward(self, x):
        # Make the tensor divisible by 32
        h, w = x.shape[-2:]
        h_new = h + (32 - h % 32) % 32
        w_new = w + (32 - w % 32) % 32
        x = torch.nn.functional.pad(x, (0, w_new - w, 0, h_new - h), mode="reflect")

        # forward pass
        x_hat = self.reflectance(x[None])

        # remove padding
        x_hat = x_hat[..., :h, :w].squeeze()
        x = x[..., :h, :w].squeeze()

        if self.correction == "histogram_matching":
            return hq_histogram_matching(x, x_hat, channel_axis=None)

        elif self.correction == "simple":
            # fit a linear regression for each band
            x_hat_i = x_hat.flatten().detach().numpy().mean()
            x_i = x.flatten().detach().numpy().mean()

            # parameters of the linear regression
            ratio = x_hat_i / x_i
            x_new_i = x * ratio

            return x_new_i

        elif self.correction == "local_simple":
            x_hat_1 = torch.nn.functional.interpolate(
                x_hat[None], scale_factor=0.0625, mode="bicubic", antialias=True
            ).squeeze()
            x_1 = torch.nn.functional.interpolate(
                x[None], scale_factor=0.0625, mode="bicubic", antialias=True
            ).squeeze()
            ratio = x_hat_1.mean(axis=0) / x_1.mean(axis=0)
            ratio_1 = torch.nn.functional.interpolate(
                ratio[None, None], size=x.shape[1:3], mode="bicubic", antialias=True
            ).squeeze()
            x_new = x * ratio_1[None]
            return x_new

        elif self.correction == "linear":
            # Linear Model Fit
            x_hat_i = x_hat.flatten().detach().numpy()
            x_i = x.flatten().detach().numpy()
            reg = LinearRegression().fit(x_i[:, None], x_hat_i[:, None])

            # parameters of the linear regression
            a = reg.coef_[0][0]
            b = reg.intercept_[0]
            x_new_i = x * a + b

            return x_new_i


class NoiseModel(torch.nn.Module):
    def __init__(
        self, kernel_type: str = "gaussian", device: Union[str, torch.device] = "cpu"
    ):
        super(NoiseModel, self).__init__()

        file = pkg_resources.resource_filename(
            "opensr_degradation", "models/model_noise.pt"
        )

        # load torchscript model from file
        self.noise_matrix = torch.load(file, map_location=device)

    def forward(self, x):
        return create_noisy(x, self.noise_matrix)


def blur_model(kernel_type: str = "gaussian", device: Union[str, torch.device] = "cpu"):
    return BlurModel(kernel_type=kernel_type, device=device)


def reflectance_model(
    device: Union[str, torch.device] = "cpu", correction: str = "linear"
):
    return ReflectanceModel(device=device, correction=correction)


def noise_model(device: Union[str, torch.device] = "cpu"):
    return NoiseModel(device=device)
