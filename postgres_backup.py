import os

cmd = """docker exec -t vamsiproject-pg_master-1 bash -c "pg_basebackup -h localhost -p 5432 -U vamsi -D /tmp/backup/$(date +%Y%m%d%H%M%S) -Ft -z -Xs -P" """

os.system(cmd)