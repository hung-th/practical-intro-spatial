# Static figure for Lecture 4: from Poisson to inhomogeneous Poisson to log-Gaussian Cox process.
# Needs numpy and matplotlib. Run from the repository root: python figures/make_L4_cox_figure.py
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
OUT = "figures/"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "savefig.dpi": 200, "savefig.bbox": "tight"})
rng = np.random.default_rng(1855)
G = 60; c = (np.arange(G) + .5) / G; X, Y = np.meshgrid(c, c); cell = 1 / G**2
N = 200                                    # expected number of points in every panel
# Smooth Gaussian random field S(s): squared-exponential covariance, sd 1.1, length scale 0.09
P = np.c_[X.ravel(), Y.ravel()]
D = np.hypot(*(P[:, None, :] - P[None, :, :]).transpose(2, 0, 1))
L = np.linalg.cholesky(1.21 * np.exp(-(D / 0.09) ** 2) + 1e-5 * np.eye(G * G))
def field(): return (L @ rng.standard_normal(G * G)).reshape(G, G)
trend = 1.5 * X                            # covariate effect: intensity rises from west to east
def scale(logl): l = np.exp(logl); return l * N / (l.sum() * cell)
lam = {"hpp": np.full((G, G), float(N)), "ipp": scale(trend)}
S1, S2 = field(), field()
lam["cox1"] = scale(trend + S1); lam["cox2"] = scale(trend + S2)
def points(l):
    k = rng.poisson(l * cell); i, j = np.nonzero(k); r = np.repeat(np.arange(len(i)), k[i, j])
    return np.c_[(j[r] + rng.random(len(r))) / G, (i[r] + rng.random(len(r))) / G]
cols = [("hpp", "Homogeneous Poisson (CSR)", "$\\lambda$ constant"),
        ("ipp", "Inhomogeneous Poisson", "$\\log\\lambda(s)=\\beta_0+\\beta_1c(s)$\nfixed surface"),
        ("cox1", "Log-Gaussian Cox: draw 1", "$\\log\\Lambda(s)=\\beta_0+\\beta_1c(s)+S(s)$\nrandom surface"),
        ("cox2", "Log-Gaussian Cox: draw 2", "same model,\na new random surface")]
fig, ax = plt.subplots(2, 4, figsize=(15, 8), gridspec_kw={"hspace": 0.32, "wspace": 0.08})
norm = LogNorm(vmin=20, vmax=3000)
for k, (key, title, sub) in enumerate(cols):
    a = ax[0, k]; im = a.imshow(np.clip(lam[key], 20, 3000), origin="lower", extent=(0, 1, 0, 1), cmap="magma", norm=norm, interpolation="bilinear")
    a.set_title(title, fontsize=12, loc="left"); a.text(0.03, 0.97, sub, transform=a.transAxes, va="top", fontsize=9.5, color="white")
    pts = points(lam[key]); b = ax[1, k]
    b.scatter(pts[:, 0], pts[:, 1], s=7, color="#18212c"); b.set_xlim(0, 1); b.set_ylim(0, 1); b.set_aspect("equal")
    b.set_title(f"one realisation: n = {len(pts)}", fontsize=10.5, loc="left", color="#5a6573")
    for q in (a, b): q.set_xticks([]); q.set_yticks([])
ax[0, 0].set_ylabel("Step 1: intensity\n(expected points per unit area)", fontsize=11)
ax[1, 0].set_ylabel("Step 2: points drawn\nfrom that intensity", fontsize=11)
fig.colorbar(im, ax=ax.ravel().tolist(), shrink=0.45, anchor=(0, 0.95), pad=0.01, label="intensity (log scale)")
fig.text(0.5, 0.04, "Each intensity surface is scaled to expect 200 points. Only the Cox process draws a new intensity surface each time, so its points form clusters that move between realisations.",
         ha="center", fontsize=10.5, color="#5a6573")
fig.savefig(OUT + "L4_fig_poisson_to_cox.png"); plt.close(fig)
