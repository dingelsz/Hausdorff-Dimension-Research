#!/bin/bash
for nSteps in 10 25 50 75 100 250 500 750 1000 2500 5000 7500 10000 25000 50000 75000 100000 250000 500000 750000 1000000 2500000 5000000 7500000 10000000
do
	for i in {1..30}
	do
		DATA_PATH="data/data_for_${nSteps}_steps_${i}.csv"
		if [ ! -f $DATA_PATH ]
			then
		 		python earthworm.py -n $nSteps -f $DATA_PATH
				echo $DATA_PATH
		fi
	done
done
