from typing import Optional, Tuple, Union

import pkg_resources
import torch
from sklearn.linear_model import LinearRegression

from .kernels import BellBlur, GaussianBlur, SigmoidBlur
from .parameters import parameters
from .utils import create_noisy_1, create_noisy_2, hq_histogram_matching


class BlurModel(torch.nn.Module):
    """
    A PyTorch module that performs image blurring.

    Args:
        kernel_type (Optional[str]): The type of kernel to use for blurring. 
            Can be one of "gaussian", "bell", "sigmoid", or "none". Defaults to "gaussian".
        device (Union[str, torch.device], optional): The device to use for computation.
    """

    def __init__(
        self,
        kernel_type: Optional[str] = "gaussian",
        device: Union[str, torch.device, None] = "cpu",
    ) -> None:
        """
        Initializes a new instance of the BlurModel class.

        Creates a blur kernel using the specified kernel type and sets the device attribute.

        Args:
            kernel_type (Optinal[str]): The type of kernel to use for blurring.            
            device (Union[str, torch.device]): The device to use for processing.
        """
        super(BlurModel, self).__init__()

        # Create blur kernel using gaussian blur
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

        # Create blur kernel using bell-shaped blur
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

        # Create blur kernel using sigmoid blur
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

        # No blur kernel
        elif kernel_type == "none":
            pass
        else:
            raise NotImplementedError(f"Kernel type {kernel_type} is not implemented.")
        self.kernel_type = kernel_type

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Applies blurring to an input image.

        Args:
            x (torch.Tensor): The input image tensor.

        Returns:
            torch.Tensor: The blurred image tensor.
        """
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
    """
    A class representing a reflectance model for image restoration.

    Args:
        device (Union[str, torch.device]): The device to use for processing.
        correction (Optional[str]): The correction reflectance method to use. Can be "histogram_matching", 
            "simple", "local_simple", or "linear".

    Attributes:
        reflectance (torch.jit.ScriptModule): The reflectance model used for image restoration.
        correction (str): The correction method used for image restoration.
    
    Methods:
        forward(x: torch.Tensor, y: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
            Applies the reflectance model to the input tensors x and y and returns the corrected tensors.
    """

    def __init__(
        self,
        device: Union[str, torch.device, None] = "cpu",
        correction: Optional[str] = "histogram_matching",
    ) -> None:
        """
        Initializes a new instance of the ReflectanceModel class.

        Loads the reflectance model from a file and sets the device and correction attributes.

        Args:
            device (Union[str, torch.device]): The device to use for processing.
            correction (str): The correction method to use.
        """
        super(ReflectanceModel, self).__init__()

        file = pkg_resources.resource_filename(
            "opensr_degradation", "models/model_reflectance.pt"
        )

        # load torchscript model from file
        self.reflectance = torch.jit.load(file, map_location=device)
        self.correction = correction

    def forward(
        self, x: torch.Tensor, y: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Applies the reflectance model to the input tensors x and y and returns the restored tensors.

        Args:
            x (torch.Tensor): The input tensor to restore.
            y (torch.Tensor): The target tensor to restore.

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: The restored tensors.
        """
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
            return (
                hq_histogram_matching(x, x_hat, channel_axis=None),
                hq_histogram_matching(y, x_hat, channel_axis=None),
            )

        elif self.correction == "simple":
            # fit a linear regression for each band
            x_hat_i = x_hat.flatten().cpu().numpy().mean()
            x_i = x.flatten().cpu().numpy().mean()

            # parameters of the linear regression
            ratio = x_hat_i / x_i
            x_new_i = x * ratio
            y_new_i = y * ratio

            return x_new_i, y_new_i

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
            y_new = y * ratio_1[None]

            return x_new, y_new

        elif self.correction == "linear":
            # Linear Model Fit
            x_hat_i = x_hat.flatten().detach().cpu().numpy()
            x_i = x.flatten().detach().cpu().numpy()
            reg = LinearRegression().fit(x_i[:, None], x_hat_i[:, None])

            # parameters of the linear regression
            a = reg.coef_[0][0]
            b = reg.intercept_[0]
            x_new_i = x * a + b
            y_new_i = y * a + b
            return x_new_i, y_new_i


class NoiseModel(torch.nn.Module):
    """
    A class representing a noise model for image degradation.

    Args:
        method (Union[str, torch.device, None]): The method to use for creating noisy 
            images. Can be "simple" or "real".
        device (Optional[str]): The device to use for processing. 

    Attributes:
        noise_matrix (torch.Tensor): The noise matrix used for creating noisy images.
        method (str): The method used for creating noisy images.
        device (str): The device used for processing.

    Methods:
        forward(x: torch.Tensor) -> torch.Tensor:
            Applies the noise model to the input tensor x and returns the noisy tensor.
    """

    def __init__(
        self,
        method: Optional[str] = "simple",
        device: Union[str, torch.device, None] = "cpu",
    ) -> None:
        """
        Initializes a new instance of the NoiseModel class.

        Loads the noise matrix from a file and sets the method and device attributes.

        Args:
            method (str): The method to use for creating noisy images. Can be "simple" or "real".
            device (str): The device to use for processing. Can be "cpu" or "cuda".
        """
        super(NoiseModel, self).__init__()

        file = pkg_resources.resource_filename(
            "opensr_degradation", "models/model_noise.pt"
        )

        # load torchscript model from file
        self.noise_matrix = torch.load(file, map_location=device)
        self.method = method
        self.device = device

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Applies the noise model to the input tensor x and returns the noisy tensor.

        Args:
            x (torch.Tensor): The input tensor to apply the noise model to.

        Returns:
            torch.Tensor: The noisy tensor.
        """
        if self.method == "simple":
            return create_noisy_2(x).to(self.device)
        elif self.method == "real":
            return create_noisy_1(x, self.noise_matrix).to(self.device)
