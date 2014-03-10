i=0;
for file in Experiences_files/batch$2/*.evo;
    do
        for k in {1..20};
        do
            i=$((i+1));
            echo $i;
            echo $file;
            python Main.py $file &
            if [ $(($i%$1)) == 0 ];
            then
                for job in `jobs -p`
                do
                    echo 'JOB'$job;
                    wait $job;
                done
            fi
        done
    done
