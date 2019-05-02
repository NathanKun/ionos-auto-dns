#!/usr/bin/env sh

# Usage: add  _acme-challenge.www.domain.com   "XKrxpRBosdIKFzxW_CT3KLZNf6q0HG9i01zxXp5CPBs"
# Used to add txt record
dns_myapi_add() {
  /home/anaconda3/anaconda3/envs/ionos-auto-dns/bin/python /home/nathankun/ionos-auto-dns/src/script.py addTxt $1 $2
}

# Usage: fulldomain txtvalue
# Used to remove the txt record after validation
dns_myapi_rm() {
  /home/anaconda3/anaconda3/envs/ionos-auto-dns/bin/python /home/nathankun/ionos-auto-dns/src/script.py deleteTxt $1 $2
}
