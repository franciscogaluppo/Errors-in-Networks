cat('Generating data from linear regression model\n')
sigma2 = 1
x = matrix(rnorm(300),100,3)

cat('\nTheoretical MSE:\n')
cat(diag(sigma2*solve(t(x)%*%(x))))

RUNS = 1000

beta = matrix(rnorm(3),3,1)
cat('\nTest 1: beta is\n')
cat(beta)
accum = rep(0,3)
for(r in 1:RUNS) {
y = x %*%  beta + rnorm(100,0,sigma2)
data = data.frame(x,y)
fit <- lm(y~x-1, data=data)
accum = accum + (beta-coef(fit))^2
}
cat('\nMSE is\n')
cat(accum/RUNS)

beta = beta*2
cat('\n\nTest 2: beta is\n')
cat(beta)
accum = rep(0,3)
for(r in 1:RUNS) {
y = x %*%  beta + rnorm(100,0,sigma2)
data = data.frame(x,y)
fit <- lm(y~x-1, data=data)
accum = accum + (beta-coef(fit))^2
}
cat('\nMSE is\n')
cat(accum/RUNS)
