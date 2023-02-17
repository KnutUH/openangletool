# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import math
import numpy as np
# %%
class Calc:
    def __init__(self, dw, lp, beta, ds, dj, o, hc):
        self.solved = False
        self.dw = dw
        self.lp = lp
        self.beta = beta / 180.0 * math.pi
        self.ds = ds
        self.dj = dj
        self.o = o
        self.hc = hc

        self.solve()

    def rad(self, d):
        return d / 180 * math.pi

    def deg(self, r):
        return r * 180 / math.pi

    def solve(self):
        a = 45.0 / 180.0 * math.pi
        b = math.pi
        xa = self.x(a)
        xb = self.x(b)
        eps = 1e-5

        print("solve: a=", self.deg(a), ", b=", self.deg(b), ", xa=", self.deg(xa), ", xb=", self.deg(xb))

        self.solved = False
        while (np.sign(xa) != np.sign(xb)) and (b - a) > eps:
            m = 0.5 * (a + b)
            xm = self.x(m)
            if np.sign(xa) == np.sign(xm):
                a = m
                xa = xm
            else:
                b = m
                xb = xm
            print(
                "solve: a=",
                self.deg(a),
                ", b=",
                self.deg(b),
                ", xa=",
                self.deg(xa),
                ", xb=",
                self.deg(xb),
            )
            self.solved = True

        if not self.solved:
            return

        self.alpha = 0.5 * (a + b)

        self.h = 0.5 * (
            self.ds * math.cos(self.alpha + self.beta)
            - 2 * self.lp * math.cos(self.alpha + self.beta)
            + self.dw * math.sin(self.alpha)
            - self.dj * math.sin(self.alpha + self.beta)
            - self.ds * math.sin(self.alpha + self.beta)
        )

        self.hr = (
            math.sqrt(self.o * self.o + self.h * self.h) + 0.5 * self.ds - 0.5 * self.dw
        )
        self.hn = self.h + 0.5 * self.ds - self.hc
        return

    def x(self, alpha):
        return (
            -self.o
            + 0.5 * self.dw * math.cos(alpha)
            - 0.5 * (self.dj + self.ds) * math.cos(alpha + self.beta)
            + (-0.5 * self.ds + self.lp) * math.sin(alpha + self.beta)
        )

    def get(self):
        if self.solved:
            return {
                "alpha": self.deg(self.alpha),
                "h": self.h,
                "hr": self.hr,
                "hn": self.hn,
            }
        return {"alpha": "-", "h": "-", "hr": "-", "hn": "-"}


# %%
calc = Calc(250, 139, 15, 12, 12, 50, 29)
calc.get()

# %%

# %%
