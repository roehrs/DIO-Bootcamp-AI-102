import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from datetime import datetime

# Configurações do cliente
endpoint = "https://<seu-endpoint>.cognitiveservices.azure.com/"
key = "<sua-chave>"

document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# Caminho para o documento de cartão de crédito
document_path = "caminho/para/seu/cartoes_de_creditos.pdf"

# Função para validar o número do cartão de crédito usando o algoritmo de Luhn
def luhn_check(card_number):
    card_number = card_number.replace(" ", "")
    total = 0
    reverse_digits = card_number[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0

# Função para validar a data de validade do cartão de crédito
def validate_expiry_date(expiry_date):
    try:
        expiry = datetime.strptime(expiry_date, "%m/%y")
        return expiry > datetime.now()
    except ValueError:
        return False

# Função para analisar o documento
def analyze_credit_card(document_path):
    with open(document_path, "rb") as document:
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-creditCard", document
        )
        result = poller.result()

        # Processar os resultados
        for page in result.pages:
            for table in page.tables:
                for cell in table.cells:
                    print(f"Texto: {cell.content}, Confiança: {cell.confidence}")
                    if "Card Number" in cell.content:
                        card_number = cell.content.split(":")[1].strip()
                        if luhn_check(card_number):
                            print("O número do cartão é válido.")
                        else:
                            print("O número do cartão é inválido.")
                    if "Expiry Date" in cell.content:
                        expiry_date = cell.content.split(":")[1].strip()
                        if validate_expiry_date(expiry_date):
                            print("A data de validade do cartão é válida.")
                        else:
                            print("A data de validade do cartão é inválida.")

# Analisar o documento
analyze_credit_card(document_path)
