import torch

from torch import Tensor


def sigmoid(x: Tensor, b: float, c: float) -> Tensor:
    """
    Compute the sigmoid function.

    Args:
        x (Tensor): The input tensor.
        b (float): The shift parameter of the sigmoid function.
        c (float): The scaling parameter of the sigmoid function.

    Returns:
        Tensor: The output tensor with values computed using the sigmoid function.

    """
    # print is the device is cuda
    return 1.0 / (1.0 + torch.exp(-c * (x - b)))


def sigmoid2D(
    b1: float, c1: float, window_size: int, batch_size: int, device: torch.device
) -> Tensor:
    """
    Compute the difference between two sigmoid functions and normalize the result.

    Args:
        b1 (float): The shift parameter of the first sigmoid function.
        c1 (float): The scaling parameter of the first sigmoid function.
        window_size (int): The size of the window.
        batch_size (int): The size of the batch.

    Returns:
        Tensor: The output tensor with values computed by subtracting the two sigmoid functions and normalizing the result.

    """

    # meshgrid
    x = (torch.arange(window_size) - window_size // 2).expand(batch_size, -1)[
        0
    ] / window_size
    x = x.to(device)
    if window_size % 2 == 0:
        x = x + 0.5
    coordx, coordy = torch.meshgrid(x, x)
    radius = torch.sqrt(coordx ** 2 + coordy ** 2)

    # compute sigmoid
    model = sigmoid(-radius, b1, c1)

    return model / model.sum()


def bellshaped(x: Tensor, a: float, b: float, c: float):
    """
    Compute the generalized bell-shaped membership function

    Args:
        x (Tensor): The input tensor.
        a (float): The shape parameter 'a' of the generalized bell-shaped membership function.
        b (float): The shape parameter 'b' of the generalized bell-shaped membership function.
        c (float): The center parameter 'c' of the generalized bell-shaped membership function.

    Returns:
        Tensor: The output tensor with values computed by evaluating the generalized bell-shaped
        membership function and normalizing the result.        
    """
    return 1.0 / (1.0 + torch.abs((x - c) / a) ** (2 * b))


def bellshaped2D(
    a: float, b: float, window_size: int, batch_size: int, device: torch.device
) -> Tensor:
    """
    Compute the generalized bell-shaped membership function

    Args:
        x (Tensor): The input tensor.
        a (float): The shape parameter 'a' of the generalized bell-shaped membership function.
        b (float): The shape parameter 'b' of the generalized bell-shaped membership function.        
        window_size (int): The size of the window.
        batch_size (int): The size of the batch.

    Returns:
        Tensor: The output tensor with values computed by evaluating the generalized bell-shaped
        membership function and normalizing the result.
    """

    # meshgrid
    x = (torch.arange(window_size) - window_size // 2).expand(batch_size, -1)[
        0
    ] / window_size
    x = x.to(device)
    if window_size % 2 == 0:
        x = x + 0.5
    coordx, coordy = torch.meshgrid(x, x)
    radius = torch.sqrt(coordx ** 2 + coordy ** 2)

    # compute bellshaped
    model = bellshaped(-radius, a, b, 0)

    return model / model.sum()


def gaussian(x, sigma: float = 2.5):
    """
    Returns a 1D Gaussian distribution tensor.

    Args:
        x (Tensor): input tensor.
        sigma (float, optional): standard deviation of the Gaussian distribution. Default is 2.5.

    Returns:
        Tensor: 1D Gaussian distribution tensor.
    """
    gauss = torch.exp(-x.pow(2.0) / (2 * sigma.pow(2.0)))
    return gauss / gauss.sum(-1, keepdim=True)


def gaussian2D(sigma: Tensor, window_size: int = 33):
    """
    Returns a 2D Gaussian distribution tensor.

    Args:
        sigma (Tensor): standard deviation of the Gaussian distribution.
        window_size (int, optional): size of the window to apply the Gaussian
            distribution. Default is 33.
        batch_size (int, optional): size of the batch. Default is 1.

    Returns:
        Tensor: 2D Gaussian distribution tensor.
    """
    # kernel 1D
    ky = gaussian(torch.linspace(-1, 1, window_size), sigma=sigma)
    kx = gaussian(torch.linspace(-1, 1, window_size), sigma=sigma)

    kernel = kx.unsqueeze(1) * ky.unsqueeze(0)

    return kernel


class GaussianBlur(torch.nn.Module):
    def __init__(self, kernel_size=65, params=[2.5], device=torch.device("cpu")):
        super(GaussianBlur, self).__init__()
        self.kernel_size = kernel_size
        self.sigma = torch.nn.Parameter(torch.tensor(params[0]))
        # if type is str
        if isinstance(device, str):
            self.device = torch.device(device)
        else:
            self.device = device
        self.kernel = gaussian2D(self.sigma, self.kernel_size)
        self.kernel = self.kernel.to(self.device)

    def forward(self, x):
        return torch.nn.functional.conv2d(
            x, self.kernel, groups=x.shape[0], padding=self.kernel_size // 2
        )


class BellBlur(torch.nn.Module):
    def __init__(self, kernel_size=65, params=[1, 1], device=torch.device("cpu")):
        super(BellBlur, self).__init__()
        self.kernel_size = kernel_size

        # if type is str
        if isinstance(device, str):
            self.device = torch.device(device)
        else:
            self.device = device

        # Create a variable (parameters)
        self.a = torch.nn.Parameter(torch.tensor(float(params[0])))
        self.b = torch.nn.Parameter(torch.tensor(float(params[1])))

        self.kernel = bellshaped2D(self.a, self.b, self.kernel_size, 1, self.device)
        self.kernel = self.kernel.to(self.device)

    def forward(self, x):
        return torch.nn.functional.conv2d(
            x, self.kernel, groups=x.shape[0], padding=self.kernel_size // 2
        )


class SigmoidBlur(torch.nn.Module):
    def __init__(self, kernel_size=65, params=[0, 1], device=torch.device("cpu")):
        super(SigmoidBlur, self).__init__()
        self.kernel_size = kernel_size

        # if type is str
        if isinstance(device, str):
            self.device = torch.device(device)
        else:
            self.device = device

        # Create a variable (parameters)
        self.b = torch.nn.Parameter(torch.tensor(float(params[0])))
        self.c = torch.nn.Parameter(torch.tensor(float(params[1])))

        self.kernel = sigmoid2D(self.b, self.c, self.kernel_size, 1, self.device)

    def forward(self, x):
        return torch.nn.functional.conv2d(
            x, self.kernel, groups=x.shape[0], padding=self.kernel_size // 2
        )
