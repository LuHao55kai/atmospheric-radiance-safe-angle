# Analytical model and operational query

## 1. Inputs and target quantity

Let $\theta$ be the angle between the solar direction and the target line of
sight as seen by a ground observer, $V$ the meteorological visibility in
kilometers, $b$ the spectral-band label, and $s$ the atmospheric scene. Define
$v=V/(1\ \mathrm{km})$, so the numerical implementation uses $\ln V$ when
$V$ is entered in kilometers.

At fixed $(\theta,V,b,s)$, many solar-zenith, view-zenith, and relative-
azimuth combinations remain possible. The modeled quantity
$L_{\mathrm{env}}$ is a smooth engineering upper-bound curve extracted from
the high radiances over those sampled geometries. It is not a strict
mathematical supremum over every possible atmospheric state.

## 2. Shared mother expression

The central output is

$$
\begin{aligned}
L_{\mathrm{env}}(\theta,V,b,s)
={}&\left[W_{b,s}(V)P_{\mathrm{HG}}(\theta;g_{b,s})
+D_{b,s}(V)\right]T_{\mathrm{base},b,s}(\theta,V)\\
&+S_{b,s}(V)x^{a_{b,s}}
T_{\mathrm{shoulder},b,s}(\theta,V),
\end{aligned}
$$

with

$$
x=\frac{1-\cos\theta}{2},\qquad
y=\frac{1+\cos\theta}{2},
$$

and the Henyey-Greenstein-type angular basis

$$
P_{\mathrm{HG}}(\theta;g)
=\frac{1-g^2}{(1+g^2-2g\cos\theta)^{3/2}}.
$$

The first term represents an effective forward-scattering lobe plus a broad
background pedestal. The second represents an intermediate- and large-angle
shoulder. The HG-type function is a physically motivated basis; fitted $g$ is
an effective curve-shape parameter and must not be reported as an independently
measured aerosol single-scattering asymmetry factor.

## 3. Visibility subformulas

The three radiance amplitudes follow log-power relationships:

$$
\begin{aligned}
W(V)&=\exp(w_0-w_1\ln v),\\
D(V)&=\exp(d_0-d_1\ln v),\\
S(V)&=\exp(s_0-s_1\ln v).
\end{aligned}
$$

The two endpoint tapers share the form

$$
T_j(\theta,V)
=1-\exp\left[-\left(\frac{y}{\tau_j(V)}\right)^p\right],
\qquad j\in\{\mathrm{base},\mathrm{shoulder}\},
$$

where

$$
\tau_j(V)
=\operatorname{clip}\left[
\sigma(t_{j,0}+t_{j,1}\ln v),10^{-4},0.95
\right],
\qquad
\sigma(z)=\frac{1}{1+\exp(-z)}.
$$

$W$, $D$, and $S$ retain the units of band-integrated radiance. The other
parameters are dimensionless effective shape parameters. The nine complete
band-scene rows are packaged in
<code>src/atmospheric_safe_angle/parameters.csv</code>.

## 4. Residual factor and minimum angle

An independently calibrated factor $K_q\ge1$ may account for residual
atmospheric, measurement, and model uncertainty:

$$
L_{\mathrm{safe}}(\theta,V,b,s)
=K_qL_{\mathrm{env}}(\theta,V,b,s).
$$

For a system-supplied admissible atmospheric background radiance
$L_{\mathrm{lim}}$, define

$$
\theta_{\min}
=\inf\left\{\theta_0\ge15^\circ:
L_{\mathrm{safe}}(\theta,V,b,s)\le L_{\mathrm{lim}}
\ \text{for every}\ \theta\ge\theta_0\right\}.
$$

The implementation evaluates a finite angular grid and performs a backward
logical accumulation. This suffix-safe rule avoids declaring an early isolated
crossing safe when a later numerical reversal exceeds the threshold. It
returns <code>None</code> if no grid node satisfies the condition and does not
interpolate between nodes.

$K_q$ is deliberately kept outside the frozen atmospheric mother expression.
Values inferred from the same observations being evaluated are diagnostic,
not independently validated operational factors.

## 5. Symbol table

| Symbol | Meaning | Unit |
|:---|:---|:---|
| $L_{\mathrm{env}}$ | Base atmospheric background-radiance engineering upper bound | $\mathrm{W\,m^{-2}\,sr^{-1}}$ |
| $L_{\mathrm{safe}}$ | Residual-adjusted atmospheric upper bound | $\mathrm{W\,m^{-2}\,sr^{-1}}$ |
| $L_{\mathrm{lim}}$ | System-admissible atmospheric background-radiance threshold | $\mathrm{W\,m^{-2}\,sr^{-1}}$ |
| $\theta$ | Sun-target line-of-sight separation | degree |
| $\theta_{\min}$ | First angle after which all larger sampled angles are admissible | degree |
| $V$ | Meteorological visibility | km |
| $b$ | Discrete band label | VIS, NIR, MWIR |
| $s$ | Discrete scene label | Maritime, desert, rural |
| $K_q$ | Independently calibrated residual factor | dimensionless |
| $g$ | Effective forward-concentration parameter | dimensionless |
| $a$ | Shoulder exponent | dimensionless |
| $\tau_j$ | Endpoint taper scale | dimensionless |
| $p$ | Endpoint taper sharpness | dimensionless |

## 6. Interpretation boundary

This is a physics-informed semi-empirical parameterization, not a new
microscopic scattering law and not a replacement for the radiative-transfer
equation. Its physical meaning lies in the constrained angular components and
their visibility dependence. Individual fitted coefficients, especially
coefficients that reached optimization bounds in MWIR, should not be assigned
unique microscopic interpretations.
