function est_mse = tau_mse(X, sigma2, tau)
	[N, nparams] = size(X);

	mat = zeros(N, 3);
	for i=1:N
		if (X(i,1) == 0) && (X(i,2) <= (1-tau))
			mat(i,:) = [1, 0, 0];
		elseif (X(i,1) == 0) && (X(i,2) > (1-tau))
			mat(i,:) = [1, 0, X(i,2) - (1-tau)];
		elseif (X(i,1) == 1) && (X(i,2) >= tau)
			mat(i,:) = [1, 1, 0];
		else
			mat(i,:) = [1, 1, X(i,2) - (1-tau)];
		end
	end

	est_mse = [0, 1, 1] * sigma2 * inv(mat.' * mat) * [0, 1, 1].';

end
