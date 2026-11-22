# waitpub.sh COMP T L : ждать DONE COMP в q.log, затем pub1
until grep -qE "(DONE|FAIL) $1\$" /tmp/q.log; do sleep 15; done; grep -E " $1\$" /tmp/q.log|tail -1; cd /home/claude && bash tools/pub1.sh $2 $3 2>&1 | tail -4
