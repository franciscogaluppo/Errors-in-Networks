function newX = validate_prepare_X(X)
% VALIDATE_PREPARE_X checks whether X is a valid design matrix for an A/B test
% This function checks if X is a vector or 2-column matrix such that
% min(X) = 0 and max(X) = 1. It prepends a vector of 1's to X and returns it.
%
% Syntax newX = validate_prepare_X(X)
%
% Author: Fabricio Murai (murai@dcc.ufmg.br)
% Created: Oct 24, 2017
% Last-modified: Oct 24, 2017

    valid = 0;
    if isvector(X)
        X = reshape(X,length(X),1);
	valid = 1;
    elseif ismatrix(X)
        if size(X,2) == 2
	    valid = 1;
        end
    end

    if ~valid
    	error('X must be a vector or a 2-column matrix.')
    end

    minX = min(X(:));
    maxX = max(X(:));
    if (minX ~= 0) || (maxX ~= 1)
        error('min(X) must be 0 and max(X) must be 1.')
    end

    % add column of 1's
    newX = [ones(size(X,1),1) X];
end
