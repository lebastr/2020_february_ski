while true; do
    python estimate_weight_balance.py > log.txt && cat log.txt
    sleep 1
done
