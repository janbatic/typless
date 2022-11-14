run 

sudo docker run -p 7777:8000 -d amazon/dynamodb-local

then when container is running  run

python dynamodb_migrate.py


We have 3 api's:\
create will create documents in a batch\
delete will delete documents in batch\
edit will first delete gotten documents and then create in a batch
