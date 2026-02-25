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
    
    def buscar_empresa(self, nfse: Dict[str, any]) -> Dict[str, any]:
        try:
            empresa = self.db.empresas.find_one(
                {"cnpj": nfse.get("cnpjCpfTomador")}
            )

            if empresa:
                return self.ir.respond(True, "", empresa)
            return self.ir.respond(
                False, f"Empresa com o CNPJ \"{nfse.get('cnpjCpfTomador')}\" não foi encontrada no Motor Fiscal",
                f"Empresa com o CNPJ \"{nfse.get('cnpjCpfTomador')}\" não foi encontrada no Motor Fiscal"
            )
        except Exception as e:
            return self.ir.respond(False, "Erro ao buscar a empresa", {"erro": e})
 
 
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
