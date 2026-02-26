from pymongo import MongoClient
from os import environ
from typing import Dict, List
from datetime import datetime
from bson import ObjectId
from unidecode import unidecode
import re
import base64
 
class Banco_Mongo():
    db: MongoClient
 
 
    def __init__(self) -> None:
        url = environ.get("URLMONGO").replace("'", "")
        client = MongoClient(url)
        self.db = client[environ.get("BASEMONGO")]
        self.collection = self.db["usuarios"]

    #faço uma consulta na colletion usuario passando o email para pega o id da conta 
    def buscar_id_conta_por_email(self, email: str):
        usuario = self.collection.find_one(
            {"email": email},
            {"configuracao_conta.conta": 1}
        )

        if not usuario:
            return None

        configuracao_conta = usuario.get("configuracao_conta") or {}
        return configuracao_conta.get("conta")
    
    # Apago a conta desse usuario (collection: contas) usando o id da conta
    def apagar_conta_cnpj(self, cnpj: str, id_conta: str) -> bool:
        try:
            result = self.db.contas.delete_one(
                {
                    "_id": ObjectId(id_conta)
                }
            )

            if result.deleted_count > 0:
                return True
            return False
        except Exception as e:
            print(f"Erro ao apagar conta {id_conta} (CNPJ {cnpj}): {e}")
            return False

    # Apago o usuario pelo email (collection: usuarios)
    def apagar_usuario_por_email(self, email: str) -> bool:
        try:
            result = self.collection.delete_one(
                {
                    "email": email
                }
            )

            if result.deleted_count > 0:
                return True
            return False
        except Exception as e:
            print(f"Erro ao apagar usuário com email {email}: {e}")
            return False


    # Apago a conta desse usuario (collection: contas) usando o id da conta
    def apagar_empresa_cnpj(self, cnpj: str) -> bool:
        try:
            result = self.db.empresas.delete_one(
                {
                    "cnpj": cnpj,
                }
            )

            if result.deleted_count > 0:
                return True
            return False
        except Exception as e:
            print(f"Erro ao apagar empresa (CNPJ {cnpj}): {e}")
            return False


    #entra na colletion empresas e consulta cnpj, adicionando servico de robotizacao
    def adicionar_robotizacao_nfse_por_cnpj(self, cnpj: str):
        try:
            result = self.db.empresas.update_one(
                {"cnpj": cnpj},
                {
                    "$push": {
                        "servicos.robotizacao": {
                            "nomeServico": "NFSE_ESCRITURACAO",
                            "ativo": True
                        }
                    }
                }
            )

            if result.modified_count > 0:
                return True
            return False
        except Exception as e:
            print(f"Erro ao adicionar robotização para o CNPJ {cnpj}: {e}")
            return False
        

    #Apagar nota que fez upload 
    def apagar_nota_nfse_do_cnpj(self, cnpj: str):
        try:
            result = self.db.nfses.delete_one(
                {
                    "cnpjCpfTomador": cnpj,
                    "status_escrituracao": "Erro"
                }
            )

            if result.deleted_count > 0:
                return True
            return False
        except Exception as e:
            print(f"Erro ao apagar nota para o CNPJ {cnpj}: {e}")
            return False
   
    
    def salvar_screenshot_nfse(self, id_nfse: ObjectId, screenshot_bytes: bytes) -> Dict[str, any]:

        try:
            screenshot_b64 = base64.b64encode(screenshot_bytes).decode("utf-8")

            result = self.db.nfses.update_one(
                {"_id": id_nfse},
                {
                    "$set": {
                        "screenshot_nota": screenshot_b64,
                        "dt_screenshot": datetime.now()
                    }
                }
            )

            if result.modified_count > 0:
                self.logger.info(f"Screenshot salvo com sucesso - ID: {id_nfse}")
                return self.ir.respond(True, "Screenshot salvo com sucesso.", {})
            elif result.matched_count == 0:
                self.logger.warning(f"Nenhum documento encontrado para ID: {id_nfse}")
                return self.ir.respond(False, "NFSe não encontrada para salvar screenshot.", {})
            else:
                self.logger.info(f"Screenshot já existente ou sem alteração - ID: {id_nfse}")
                return self.ir.respond(True, "Screenshot já existente ou sem alteração.", {})

        except Exception as e:
            self.logger.error(f"Erro ao salvar screenshot da NFSe {id_nfse}: {e}")
            return self.ir.respond(False, "Erro ao salvar screenshot.", {"erro": str(e)})
