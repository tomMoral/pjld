i=0;
mkdir Experiences_files;

for s in {100..300..20}; 
	do 
		echo $s; 
		echo $i; 
		for ad in `seq 0.7 0.1 1.5`; 
			do 
				echo $ad; i=$((i+1)); 
				sed 's/AdCost.*/AdCost\t'$ad'/' Evolife.evo |\
				sed 's/WDGrid.*/WDGridSize\t'$s'/' |\
				sed 's/,/./'|\
				sed 's/ResultDir.*/ResultDir\t.\/___Results\/'$i'/' >Experiences_files/Exp$i.evo; 					mkdir ./___Results/$i; 
			done;  
	done
