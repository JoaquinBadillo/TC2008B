# Vectores

## Suma

$$\mathbf{v} + \mathbf{u} = \begin{pmatrix}v_{1} + u_{1}\\ \vdots \\v_{n} + u_{n}\end{pmatrix} $$

## Multiplicación por un Escalar

$$\alpha\mathbf{v} = \begin{pmatrix}\alpha v_{1} \\ \vdots \\ \alpha v_{n}\end{pmatrix} $$

## Producto Interno, Escalar o "Punto"

$$\langle \mathbf{v}, \mathbf{u}\rangle = \mathbf{v} \cdot \mathbf{u} = \sum_{k=1}^{N}v_{k}u_{k}$$

## Norma L2 (Magnitud)

$$||\mathbf{v}||_{2} = \sqrt{\sum_{k=1}^{N} v^{2}_{k}}$$

$$||\mathbf{v}||_{2} = \sqrt{\langle\mathbf{v}, \mathbf{v}\rangle}$$

**Ejemplo**

$\mathbf{v_1} = \begin{pmatrix}5\\-7\\3\end{pmatrix}$

$||\mathbf{v_1}|| = \sqrt{\left(5\right)^2 + \left(-7\right)^2 + \left(3\right)^2} = 9.1104...$

## Normalización

$$\hat{\mathbf{v}} = \frac{\mathbf{v}}{||v||}$$

## Producto Vectorial o "Cruz"

Para 2 vectores en $\mathbb{R}^{3}$

$$\mathbf{v} \times \mathbf{u} = \left|\begin{matrix}
\hat{\mathbf{i}} & \hat{\mathbf{j}} & \hat{\mathbf{k}}\\
v_{x} & v_{y} & v_{z}\\
u_{x} & u_{y} & u_{z}\\
\end{matrix}\right| = 
    \hat{\mathbf{i}}\left|\begin{matrix}v_y&v_z\\u_{y}&u_{z}\end{matrix}\right| - 
    \hat{\mathbf{j}}\left|\begin{matrix}v_y&v_z\\u_{y}&u_{z}\end{matrix}\right| +
    \hat{\mathbf{i}}\left|\begin{matrix}v_y&v_z\\u_{y}&u_{z}\end{matrix}\right| 
$$ 
