function var_est = probit_mse(X, sigma2, params)
% PROBIT_MSE Computes the MSE of the ATE estimator in randomized experiments under a probit model.
% This function computes the Mean Square Error of the Average Treatment Effect estimator assuming
% a network of units under the probit model
%
%   $ P(Y_i=1|Z_i,F_i) = P(\alpha + \beta Z_i + \gamma F_i + U_i > 0)$
%
% where
% $Y_i$ is the response of unit $i$,
% $Z_i$ is the treatment assigned to unit $i$,
% $F_i$ is the fraction/number of $i$'s neighbors assigned to treatment 1,
% * $U_i \sim \textrm{Normal}(0,\sigma^2)$ is the stochastic component
%   associated to $i$,
% $\alpha$, $\beta$ and $\gamma$ are model parameters.
%
% Syntax: est_mse = PROBIT_MSE(X, sigma2, params)
%
% Inputs:
%     X - if X is a vector, it is assumed to be Z, the treatment assignment vector;
%        if X is a 2-column matrix, columns are assumed to be Z and F, respectively.
%     sigma2 - variance of U_i
%     params - vector [alpha beta] or [alpha beta gamma]
%
% Outputs:
%     est_mse - variance of ATE estimator
%
% Author: Fabricio Murai (murai@dcc.ufmg.br)
% Created: Oct 23, 2017
% Last-modified: Oct 25, 2017

    X = validate_prepare_X(X);
    [N, nparams] = size(X);
    params = reshape(params,nparams,1);
    sigma = sqrt(sigma2);


    % use formula to compute Fisher Information Matrix FIM
    %  See Demidenko, Eugene. "Computational aspects of probit model." Mathematical Communications 6.2 (2001): 233-247.
    FIM = zeros(nparams);
    for i=1:N
        si = X(i,:) * params;
        distpdf = normpdf(si, 0, sigma);
        distcdf = normcdf(si, 0, sigma);
        FIM = FIM + distpdf^2/(distcdf * (1-distcdf)) * (X(i,:)' * X(i,:));
    end


    % Variance of estimator computed using Delta method
    % ATE estimator is
    %
    % $h(\alpha,\beta,\gamma)$ = P(U_i < \alpha + \beta + \gamma) - P(U_i < \alpha) $
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
    param_sum_pdf = normpdf(alpha+eta,0,sigma);
    hgrad = [param_sum_pdf - normpdf(alpha,0,sigma)];
    if nparams == 2
        hgrad = [hgrad; param_sum_pdf];
    elseif nparams == 3
        hgrad = [hgrad; param_sum_pdf; param_sum_pdf];
    end
    % var_est = hgrad' * inv(FIM) * hgrad;
    var_est = hgrad' * (FIM\hgrad);

end
