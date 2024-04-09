#!/bin/bash
START=$1      # Initial number of cores
END=$2        # Final number of cores
STEP=$3       # Constant factor with which current number of cores is multiplied at each iteration
N_TILES=$4    # Number of tiles per dimension -> n_tiles * n_tiles total
N_TRAIN=$5    # Number of training samples
N_TEST=$6     # Number of testing samples
N_REG=$7      # Number of delayed input regressors
CHOLESKY=$8   # Choose between right- left- or top-looking tiled Cholesky decomposition
N_LOOP=$9     # Number of iterations to be executed per current number of cores
OUTPUT_FILE=${10}
APEX_FILE="../build/apex.0.csv"
ERROR_FILE="../build/error.csv"

touch $ERROR_FILE
touch $OUTPUT_FILE && echo "Algorithm;Cores;Tiles;N_train;N_test;N_regressor;Total_time;Assemble_time;Cholesky_time;Triangular_time;Predict_time;Error;${N_LOOP}" >> $OUTPUT_FILE

for (( i=$START; i<=$END; i=i*$STEP ))
do
  for (( l=0; l<$N_LOOP; l=l+1 ))
  do
    cd ../build && touch $ERROR_FILE
    ./hpx_cholesky -t$i --n_train $N_TRAIN --n_test $N_TEST --n_regressors $N_REG --n_tiles $N_TILES --cholesky $CHOLESKY
    cd ../benchmark_scripts && ./output_formater.sh $N_TILES $N_TRAIN $N_TEST $N_REG $i $CHOLESKY $APEX_FILE $OUTPUT_FILE $ERROR_FILE
    cd ../build && rm $ERROR_FILE
  done
done
