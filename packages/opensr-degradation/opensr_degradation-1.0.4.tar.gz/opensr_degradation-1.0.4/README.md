<p align="center">
  <a href="https://github.com/ESAOpenSR/opensr-test"><img src="https://github.com/ESAOpenSR/opensr-test/assets/16768318/608fce3d-af32-4330-9d1a-096f1e5835e1" alt="header" width="55%"></a>
</p>

<p align="center">
    <em>A python package to degradate NAIP into Sentinel-2 like</em>
</p>

<p align="center">
<a href='https://pypi.python.org/pypi/opensr-degradation'>
    <img src='https://img.shields.io/pypi/v/opensr-degradation.svg' alt='PyPI' />
</a>

<a href="https://opensource.org/licenses/MIT" target="_blank">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
</a>
<a href='https://opensr-degradation.readthedocs.io/en/latest/?badge=main'>
    <img src='https://readthedocs.org/projects/opensr-degradation/badge/?version=main' alt='Documentation Status' />
</a>
<a href="https://github.com/psf/black" target="_blank">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black">
</a>
<a href="https://pycqa.github.io/isort/" target="_blank">
    <img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" alt="isort">
</a>
</p>

---

**GitHub**: [https://github.com/ESAOpenSR/opensr-degradation](https://github.com/ESAOpenSR/opensr-degradation)

**Documentation**: [https://opensr-degradation.readthedocs.io/](https://opensr-degradation.readthedocs.io/)

**PyPI**: [https://pypi.org/project/opensr-degradation/](https://pypi.org/project/opensr-degradation/)

**Paper**: Coming soon!

---

## Overview

In the domain of remote sensing, image super-resolution (ISR) goal is augmenting the ground sampling distance, also known as spatial resolution. Over recent years, numerous research papers have been proposed addressing ISR; however, they invariably suffer from two main issues. Firstly, the majority of these proposed models are tested on synthetic data. As a result, their applicability and performance in real-world scenarios remain unverified. Secondly, the frequently utilized evaluation metrics for these models, such as LPIPS and SSIM, are inherently designed for perceptual image analysis, not specifically for super-resolution.

In response to these challenges, **'opensr-test'** has been introduced as a Python package, designed to provide users with three meticulously curated test datasets. These datasets are tailored to minimize spatial distortions between Low Resolution (LR) and High Resolution (HR) images, while calibrating differences in the spectral domain. Moreover, the **'opensr-test'** package offers five distinct types of metrics aimed at accurately evaluating the performance of ISR algorithms, thus addressing the aforementioned shortcomings of conventional evaluation techniques.
