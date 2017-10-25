function var_est = logistic_mse(X, params)
% LOGISTIC_MSE Computes the MSE of the ATE estimator in randomized experiments under a logistic model.
% This function computes the Mean Square Error of the Average Treatment Effect estimator assuming
% a network of units under the logistic model
%
%   $ P(Y_i=1|Z_i,F_i) = \textrm{logit}^{-1}(\alpha + \beta Z_i + \gamma F_i)$
%
% where
% $Y_i$ is the response of unit $i$,
% $Z_i$ is the treatment assigned to unit $i$,
% $F_i$ is the fraction/number of $i$'s neighbors assigned to treatment 1,
% $\alpha$, $\beta$ and $\gamma$ are model parameters.
%
% Syntax: est_mse = LOGISTIC_MSE(X, params)
%
% Inputs:
%     X - if X is a vector, it is assumed to be Z, the treatment assignment vector;
%        if X is a 2-column matrix, columns are assumed to be Z and F, respectively.
%     params - vector [alpha beta] or [alpha beta gamma]
%
% Outputs:
%     est_mse - variance of ATE estimator
%
% Author: Fabricio Murai (murai@dcc.ufmg.br)
% Created: Oct 23, 2017
% Last-modified: Oct 24, 2017

    X = validate_prepare_X(X);
    nparams = size(X,2);
    params = reshape(params,nparams,1);

    % compute diagonal matrix W
    score = exp(X * params);
    W = diag(score ./ ((1+score).^2));

    % use formula for parameter estimation variance
    % See https://stats200.stanford.edu/Lecture26.pdf
    %     cov(\hat{alpha},\hat{beta}) = (X^T W X)^{-1}
    FIM = X' * W * X;

    % Variance of estimator computed using Delta method
    % ATE estimator is
    %
    % $h(\alpha,\beta,\gamma)$ = \frac{\exp(-\alpha) - \exp(-\alpha-\beta-\gamma)}
    %                                 {1+\exp(-\alpha)+\exp(-\alpha-\beta-\gamma)+\exp(-2\alpha-\beta-\gamma)} $
    %
    % Variance of the ATE estimator in the limit when N goes to infinity is
    %
    %   $\nabla h' \times \textrm{Cov} \times \nabla h$
    %
    % where
    % * $\nabla h$ is the gradient of function $h$ and
    % * Cov is the covariance matrix of the parameter estimates.

    alpha = params(1);
    eta = sum(params(2:end));
    exp_sum_plus_one = exp(alpha+eta)+1;
    exp_ratio = exp(alpha+eta)/exp_sum_plus_one^2;
    hgrad = [1/(exp_sum_plus_one) - 1/(exp_sum_plus_one^2) - exp(alpha)/(exp(alpha)+1)^2];
    if nparams == 2
	    hgrad = [hgrad; exp_ratio];
    elseif nparams == 3
	    hgrad = [hgrad; exp_ratio; exp_ratio];
    end
    %var_est = hgrad' * cov_matrix * hgrad;
    var_est = hgrad' * (FIM\hgrad);

    
end
