import os
import json
import logging
from typing import Dict, List
from pydantic import BaseModel, Field, ValidationError
from groq import Groq, GroqError
from dotenv import load_dotenv

# Configuração de logging profissional
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("GeradorQuiz")

load_dotenv()


class ParPerguntaResposta(BaseModel):
    pergunta: str = Field(..., description="Uma pergunta clara e desafiadora estilo prova universitária.")
    resposta: str = Field(..., description="A resposta detalhada, didática e correta para a pergunta.")


class QuizSchema(BaseModel):
    """Garante que a IA retorne uma lista exata de perguntas e respostas estruturadas."""
    questoes: List[ParPerguntaResposta] = Field(..., description="Lista contendo exatamente as questões solicitadas.")


class Gerador:
    """Gerador de quiz inteligente utilizando Groq e validação estricta com Pydantic."""

    def __init__(self, modelo: str = "llama-3.3-70b-versatile") -> None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("A chave GROQ_API_KEY não foi encontrada nas variáveis de ambiente.")
        
        self.client = Groq(api_key=api_key)
        self.model = modelo

    def _construir_prompt(self, tema: str, quantidade: int) -> str:
        return f"""
        Você é um professor universitário sênior e especialista no tema: {tema}.
        Seu objetivo é criar material de estudo de alta qualidade para estudantes universitários.

        Gere exatamente {quantidade} perguntas e respostas didáticas sobre o tema: {tema}.
        As perguntas devem exigir raciocínio crítico, parecendo questões de provas acadêmicas reais.

        FORMATO DE SAÍDA OBRIGATÓRIO (JSON):
        O JSON deve seguir estritamente este formato de lista de objetos:
        {{
          "questoes": [
            {{
              "pergunta": "Texto da pergunta aqui?",
              "resposta": "Explicação detalhada da resposta aqui."
            }}
          ]
        }}
        """

    def gerar_perguntas(self, tema: str, quantidade: int = 10, tentativas_maximas: int = 3) -> Dict[str, str]:
        """Gera e valida as perguntas, retornando um dicionário limpo no formato {pergunta: resposta}."""
        prompt = self._construir_prompt(tema, quantidade)

        for tentativa in range(1, tentativas_maximas + 1):
            try:
                logger.info(f"Tentativa {tentativa}/{tentativas_maximas} gerando quiz para o tema: '{tema}'...")

                resposta = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )

                conteudo_bruto = resposta.choices[0].message.content
                dados_json = json.loads(conteudo_bruto)

                # Valida o formato usando Pydantic
                quiz_validado = QuizSchema(**dados_json)

                # Transforma a lista validada no dicionário clássico {pergunta: resposta}
                quiz_dict = {q.pergunta: q.resposta for q in quiz_validado.questoes}

                logger.info("Quiz gerado e validado com sucesso!")
                return quiz_dict

            except (GroqError, json.JSONDecodeError, ValidationError) as e:
                logger.warning(f"Falha na tentativa {tentativa}: {e}. Tentando novamente...")
        
        logger.error("Todas as tentativas de geração falharam.")
        return {}

    @staticmethod
    def salvar_json(dados: Dict[str, str], caminho: str = "quiz_estudo.json") -> None:
        """Salva o dicionário final formatado em um arquivo JSON."""
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
            logger.info(f"Arquivo salvo com sucesso em: {caminho}")
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo: {e}")
