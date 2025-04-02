from sklearn.decomposition import PCA
import numpy as np


def apply_pca(data, n_components):
    """
    Apply PCA to reduce the dimensionality of the input data.
    Parameters:
    - data: np.ndarray of shape (n_samples, n_features)
    - n_components: int, number of output PCA components to retain
    Returns:
    - reduced_data: np.ndarray of shape (n_samples, n_components)
    - pca_model: trained PCA object (can be used for inverse_transform, etc.)
    """
    if not isinstance(data, np.ndarray):
        data = np.array(data)

    assert data.ndim == 2, "Input data must be 2D (n_samples, n_features)"
    assert 1 <= n_components <= data.shape[1], "n_components must be <= input feature dimension"

    pca = PCA(n_components=n_components)
    reduced_data = pca.fit_transform(data)
    return reduced_data, pca