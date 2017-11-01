#!/bin/bash
for RADIUS in {1..20}
do
	DATA_PATH=$1
		if [ -f $DATA_PATH ]
		then
			echo $RADIUS
		 	python hausdorff_dimension_m2.py -f $DATA_PATH -r $RADIUS
		fi
done
