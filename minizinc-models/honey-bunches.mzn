int: N = 21;
array[1..N] of var float: X;

constraint forall (x in X) (x > 0);

include "decreasing.mzn";
constraint decreasing(X);

constraint sum(X) = 1;

constraint X[1] = 0.36;
constraint X[2] = 0.2;
constraint X[4] = 0.087;
constraint X[5] = 0.047;
constraint X[14] = 0.004;

solve maximize X[3];