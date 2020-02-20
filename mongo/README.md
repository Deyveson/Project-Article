
## Execute esses comandos como admin 

1. Subindo contêiner `docker-compose up -d` 
2. Terminal contêiner `docker exec -it mongo_mongo_1 bash`
3. Para iniciar o cliente no Terminal do MongoDB `mongo`
4. Bancos de dados existentes `show dbs`
5. Criando o banco `use baseImages`
* Para criar o banco efetivamente, você precisa fazer um insert
6. Para inserir os dados `db.produtos.save({"_id": 1, "Name": "Coca", "Img": "asdasd"})`
7. Podemos consultar dados usando algo como o seguinte `db.produtos.find({nome: "Deyveson"})`
