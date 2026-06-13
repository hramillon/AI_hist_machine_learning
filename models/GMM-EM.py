import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from scipy.stats import multivariate_normal

def gmm_em(X, k, max_iter=100, tol=1e-4):
    n_samples, n_features = X.shape
    
    # on intialise nos gaussiennes 
    pi = np.ones(k) / k
    means = X[np.random.choice(n_samples, k, replace=False)]
    covariances = [np.cov(X.T) for _ in range(k)]
    
    responsibilities = np.zeros((n_samples, k))
    
    for iteration in range(max_iter):
        prev_means = means.copy()
        
        # Epectation
        for j in range(k):
            responsibilities[:, j] = pi[j] * multivariate_normal.pdf(X, mean=means[j], cov=covariances[j])
        
        somme_resp = responsibilities.sum(axis=1, keepdims=True)
        responsibilities /= np.where(somme_resp == 0, 1e-10, somme_resp)
        
        # Maximization
        N_k = responsibilities.sum(axis=0)
        # maj des moyennes covariance et poids
        for j in range(k):
            means[j] = np.sum(responsibilities[:, j, np.newaxis] * X, axis=0) / N_k[j]
            
            diff = X - means[j]
            covariances[j] = np.dot(responsibilities[:, j] * diff.T, diff) / N_k[j]
            covariances[j] += np.eye(n_features) * 1e-6
            
            pi[j] = N_k[j] / n_samples
            
        # est ce que ça converge ?
        if np.linalg.norm(means - prev_means) < tol:
            break
            
    return responsibilities, means

iris = load_iris()
X = iris.data[:, [2, 3]]   
y = iris.target
noms_features = [iris.feature_names[2], iris.feature_names[3]]

responsibilities, means = gmm_em(X, k=3)
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].scatter(X[:, 0], X[:, 1], c=y, cmap="viridis", edgecolor="k")
axes[0].set_title("Vraies espèces (y)")
axes[0].set_xlabel(noms_features[0])
axes[0].set_ylabel(noms_features[1])

axes[1].scatter(X[:, 0], X[:, 1], c=responsibilities, edgecolor="k")
axes[1].scatter(means[:, 0], means[:, 1], c="red", marker="X", s=200, label="Moyennes µ")
axes[1].set_title("GMM EM from scratch (Soft Clustering)")
axes[1].set_xlabel(noms_features[0])
axes[1].set_ylabel(noms_features[1])
axes[1].legend()

plt.tight_layout()
plt.savefig("gmm_iris.png", dpi=120)