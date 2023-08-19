from os.path import dirname, join, realpath

import numpy as np
import pytest

from ssspy.bss.fdica import AuxLaplaceFDICA, GradLaplaceFDICA, NaturalGradLaplaceFDICA

ssspy_tests_dir = dirname(dirname(dirname(realpath(__file__))))


from dummy.utils.dataset import load_regression_data

fdica_root = join(ssspy_tests_dir, "mock", "regression", "fdica")
n_sources = 2

parameters_is_holonomic = [True, False]
parameters_spatial_algorithm = ["IP1", "IP2"]


@pytest.mark.parametrize("is_holonomic", parameters_is_holonomic)
def test_grad_laplace_fdica(is_holonomic: bool):
    if is_holonomic:
        root = join(fdica_root, "grad_laplace_fdica", "holonomic")
    else:
        root = join(fdica_root, "grad_laplace_fdica", "nonholonomic")

    npz_input, npz_target = load_regression_data(root=root)
    spectrogram_mix = npz_input["spectrogram"]
    spectrogram_trg = npz_target["spectrogram"]
    n_iter = npz_target["n_iter"].item()

    assert npz_target["is_holonomic"].item() == is_holonomic

    fdica = GradLaplaceFDICA(is_holonomic=is_holonomic)
    spectrogram_est = fdica(spectrogram_mix, n_iter=n_iter)

    assert np.allclose(spectrogram_est, spectrogram_trg)


@pytest.mark.parametrize("is_holonomic", parameters_is_holonomic)
def test_natural_grad_laplace_fdica(is_holonomic: bool):
    if is_holonomic:
        root = join(fdica_root, "natural_grad_laplace_fdica", "holonomic")
    else:
        root = join(fdica_root, "natural_grad_laplace_fdica", "nonholonomic")

    npz_input, npz_target = load_regression_data(root=root)
    spectrogram_mix = npz_input["spectrogram"]
    spectrogram_trg = npz_target["spectrogram"]
    n_iter = npz_target["n_iter"].item()

    assert npz_target["is_holonomic"].item() == is_holonomic

    fdica = NaturalGradLaplaceFDICA(is_holonomic=is_holonomic)
    spectrogram_est = fdica(spectrogram_mix, n_iter=n_iter)

    assert np.allclose(spectrogram_est, spectrogram_trg)


@pytest.mark.parametrize("spatial_algorithm", parameters_spatial_algorithm)
def test_aux_laplace_fdica(spatial_algorithm: str):
    root = join(fdica_root, "aux_laplace_fdica", spatial_algorithm)
    npz_input, npz_target = load_regression_data(root=root)
    spectrogram_mix = npz_input["spectrogram"]
    spectrogram_trg = npz_target["spectrogram"]
    n_iter = npz_target["n_iter"].item()

    assert npz_target["spatial_algorithm"].item() == spatial_algorithm

    fdica = AuxLaplaceFDICA(spatial_algorithm=spatial_algorithm)
    spectrogram_est = fdica(spectrogram_mix, n_iter=n_iter)

    assert np.allclose(spectrogram_est, spectrogram_trg)
