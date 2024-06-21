# Algorithm for Averaging 3D Points with Covariance Matrices

## Introduction

This document describes the algorithm for averaging a set of points in 3D space, considering their uncertainties and covariance matrices. Each point has associated uncertainties represented by a \(3 \times 3\) covariance matrix. The algorithm calculates the weighted average of the points and the combined covariance matrix.

## Input Data

The input consists of:
- A list of points \(\mathbf{p}_i\), where each point \(\mathbf{p}_i\) is a vector \(\begin{pmatrix} x_i \\ y_i \\ z_i \end{pmatrix}\).
- A list of covariance matrices \(\Sigma_i\), where each \(\Sigma_i\) is a \(3 \times 3\) matrix representing the uncertainties of the corresponding point \(\mathbf{p}_i\).

## Algorithm

### Step 1: Inverse Covariance Matrices

For each covariance matrix \(\Sigma_i\), calculate the inverse matrix \(W_i\):
\[ 
W_i = \Sigma_i^{-1}
\]

### Step 2: Combined Covariance Matrix

Calculate the combined covariance matrix \(\Sigma_{\text{combined}}\) using the sum of the inverse covariance matrices:
\[
\Sigma_{\text{combined}} = \left( \sum_{i} W_i \right)^{-1}
\]

### Step 3: Weighted Sum of Points

Calculate the weighted sum of the points:
\[
\mathbf{p}_{\text{weighted\_sum}} = \sum_{i} W_i \mathbf{p}_i
\]

### Step 4: Averaged Point

Calculate the averaged point \(\mathbf{p}_{\text{avg}}\) using the combined covariance matrix and the weighted sum of points:
\[
\mathbf{p}_{\text{avg}} = \Sigma_{\text{combined}} \mathbf{p}_{\text{weighted\_sum}}
\]