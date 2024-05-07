# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import numpy as np
from pymor.models.iosys import LTIModel

from models import gab08
from reductors import IRKACauchyIndexReductor, IRKAWithLineSearchReductor
from tools import plot_combined, plot_fom, plot_rom, settings

settings()

# %% [markdown]
# # FOM

# %%
fom = gab08()

# %%
print(fom)

# %%
w = (1e-2, 1e2)
_ = plot_fom(fom, w)

# %% [markdown]
# # IRKA

# %%
irka = IRKACauchyIndexReductor(fom)
rom0 = LTIModel.from_matrices(np.array([[-0.27]]), np.eye(1), np.eye(1))
rom = irka.reduce(rom0, compute_errors=True, conv_crit='h2')

# %%
_ = plot_rom(fom, rom, w, irka, 'IRKA')

# %%
print((fom - rom).h2_norm() / fom.h2_norm())

# %% [markdown]
# # IRKA with line search

# %%
irka_rgd = IRKAWithLineSearchReductor(fom)
rom_rgd = irka_rgd.reduce(rom0, compute_errors=True, conv_crit='h2')

# %%
_ = plot_rom(fom, rom_rgd, w, irka_rgd, 'RGD-IRKA')

# %%
print((fom - rom_rgd).h2_norm() / fom.h2_norm())

# %%
_ = plot_combined(irka, irka_rgd, 'gab3_r1_c1.pdf')
