function est_mse = linear_mse(X, sigma2)
% LINEAR_MSE Computes the MSE of the ATE estimator in randomized experiments under a linear model.
% This function computes the Mean Square Error of the Average Treatment Effect estimator assuming
% a network of units under the linear model
%
%   $Y_i = \alpha + \beta Z_i + \gamma F_i + U_i$
%
% where
% * $Y_i$ is the response of unit $i$,
% * $Z_i$ is the treatment assigned to unit $i$,
% * $F_i$ is the fraction/number of $i$'s neighbors assigned to treatment 1,
% * $U_i \sim \textrm{Normal}(0,\sigma^2)$ is the stochastic component
%   associated to $i$,
% * $\alpha$, $\beta and $\gamma$ are model parameters.
%
% Syntax: est_mse = LINEAR_MSE(X, sigma2)
%
% Inputs:
%   X - if X is a vector, it is assumed to be Z, the treatment assignment vector;
%        if X is a 2-column matrix, columns are assumed to be Z and F, respectively.
%   sigma2 - variance of U_i
%
% Outputs:
%     est_mse - variance of ATE estimator
%
% Author: Fabricio Murai (murai@dcc.ufmg.br)
% Created: Oct 23, 2017
% Last-modified: Oct 24, 2017

    X = validate_prepare_X(X);
    nparams = size(X,2);

    % use well-known formula for parameter estimation variance
    %     cov(\hat{alpha},\hat{beta}) = sigma^2 * (X^T X)^{-1}
    cov_matrix = sigma2*inv(X' * X);
    % if X is Z, return element associated with beta
    % if X is [Z F], return var(\hat{beta}) + 2*cov(\hat{beta},\hat{gamma}) + var(\hat{gamma})

    if nparams == 2
        est_mse = cov_matrix(2,2);
    else
        est_mse = sum(sum(cov_matrix(2:3,2:3)));
    end
end
