docker build -t act2 .
docker run --name act2 act2
docker cp act2:/app/emails_d4.txt emails_d4.txt
docker rm act2