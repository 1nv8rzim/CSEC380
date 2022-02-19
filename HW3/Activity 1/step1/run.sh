docker build -t act1ste1 .
docker run --name act1ste1 act1ste1
docker cp act1ste1:/app/classes.csv classes.csv
docker rm act1ste1