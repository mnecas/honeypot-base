
curl -X POST https://server/api/data
   -H 'Content-Type: application/json'
   -d '{"type":"'+$HOSTNAME+'","data":"'+$DATA+',"ip":"'+$IP+'"}'