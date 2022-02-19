docker build -t act1ste2 .
docker run --name act1ste2 act1ste2
docker cp act1ste2:/app/images/ images/
docker rm act1ste2