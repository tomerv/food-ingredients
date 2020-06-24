int: N = 20;
array[1..N] of var 0.0..1.0: X;

constraint forall (x in X) (x >= 0.000001);

include "decreasing.mzn";
constraint decreasing(X);

constraint sum(X) = 1.0;

constraint X[1] = 0.59;
constraint X[3] = 0.065;
constraint X[5] = 0.05;
constraint X[10] = 0.02;

solve maximize X[2];