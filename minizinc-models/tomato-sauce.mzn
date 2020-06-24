int: N = 8;
array[1..N] of var 0.0..1.0: X;

constraint forall (x in X) (x >= 0.000001);

include "decreasing.mzn";
constraint decreasing(X);

constraint sum(X) = 1.0;

constraint X[1] = 0.72;
constraint X[2] = 0.14;
constraint X[4] = 0.02;  % added to make the minimization more interesting
constraint X[5] = 0.02;

solve minimize X[3];