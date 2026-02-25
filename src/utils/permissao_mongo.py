from db_mongo.banco_mongo import Banco_Mongo

#consulta na colletion usuario passando o email para pega o id da conta 
banco = Banco_Mongo()
id_conta = banco.buscar_id_conta_por_email("motor_teste@gmail.com")
print(id_conta)

#Liberar escrituração
uploard_planilha = Banco_Mongo.adicionar_robotizacao_nfse_por_cnpj("43456133000180")
print(uploard_planilha)