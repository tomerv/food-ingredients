int: N = 10;
array[1..N] of var 0.0..1.0: X;

constraint forall (x in X) (x >= 0.000001);

include "decreasing.mzn";
constraint decreasing(X);

constraint sum(X) = 1.0;

constraint X[1] = 0.481;
constraint X[2] = 0.31;
constraint X[4] = 0.058;
constraint X[5] = 0.042;

solve maximize X[3];