## Otimizando o consumo de imagens com API REST em Python - Na prática !

'Monografia de conclusão de curso, Sistema de Informação - Fametro'

- Execução do projeto completo:
    1. Subindo os contêiners `docker-compose up -d --build` 
    2. Checar saúde dos contêiner `docker logs -f --tail 100 'containers_id'`
    3. Abra o navegador e digite `localhost:5555` APIRESTful
    4. Mongo express `localhost:8081` gerenciador do MongoDB

- Para executar o projeto python local sem o docker:
    https://github.com/Deyveson/Project-Article/tree/master/ws-img

## Execute esses comandos como admin (Mongo Example persistence)
- Subindo apenas o mongo
    1. Subindo contêiner `docker-compose up -d --build mongo` 
    2. Terminal contêiner `docker exec -it 'name_container' bash`
    3. Para iniciar o cliente no Terminal do MongoDB `mongo`
    4. Bancos de dados existentes `show dbs`
    5. Criando o banco `use baseImages`
    * Para criar o banco efetivamente, você precisa fazer um insert
    6. Para inserir os dados `db.produtos.save({"_id": 1, "Name": "Coca", "Img": "asdasd"})`
    7. Podemos consultar dados usando algo como o seguinte `db.produtos.find({nome: "Deyveson"})`
