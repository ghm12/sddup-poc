from data_generator import PDFDataGenerator

import os
import base64

from fillpdf import fillpdfs

from pyhanko.sign import signers
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter

class PDFHandler:
    def __init__(self):
        self.generator = PDFDataGenerator()

        self.form_fields = ["ano", "avós", "cpf", "código de acesso", "data de nascimento", "data do registro", "declarante", "dia", "dnv", "endereço", "filiação", "gêmeos", "hora de nascimento", "local de nascimento", "matrícula", "município de nascimento", "município de registro", "município ofício", "mês", "nome", "nome do ofício", "nome e matrícula dos gêmeos", "observações", "sexo"]

        self.signature_fields = ["Assinatura do Registrador"]
        
        # Some field names are wrong because of unicode, they are saved as hex values instead
        # so we need to treat them properly so the PDF is correctly filled
        self.special_fields = {"avós": "6176f373", "filiação": "66696c6961e7e36f", "mês": "6dea73"}

    def create_pdf(self, amount: int = 1, template_path: str = "./sddup/data/templates/birth_certificate_template.pdf", output_path: str = "./sddup/outputs/pdf/generated_pdfs", private_key_path: str = "./sddup/data/sddup_private_key.pem", certificate_path: str = "./sddup/data/sddup_certificate.pem"):
        os.makedirs(output_path, exist_ok=True)

        for i in range(amount):
            data = self.generator.generate_data_pdf()
            formatted_data = self.__format_data(data)
            
            form_data, signature_data = self.__fill_pdf_data(formatted_data)

            output_file = f"{output_path}/pdf_generated_from_template_{i}.pdf"
            fillpdfs.write_fillable_pdf(template_path, output_file, form_data, flatten=True)
            self.__sign_pdf(output_file, private_key_path, certificate_path)

    def extract_data(self, amount: int = 1, pdf_path: str = "./sddup/outputs/pdf/generated_pdfs", output_path: str = "./sddup/outputs/pdf/extracted_data"):
        os.makedirs(output_path, exist_ok=True)
        data = ""

        for i in range(amount):
            data = self.__extract_pdf_data(f"{pdf_path}/pdf_generated_from_template_{i}.pdf")
            
            with open(f"{output_path}/extracted_data_{i}.data", "w") as file:
                file.write(data)

    def recreate_pdf(self, amount: int = 1, template_path: str = "./sddup/data/templates/birth_certificate_template.pdf", data_path: str = "./sddup/outputs/pdf/extracted_data", output_path: str = "./sddup/outputs/pdf/recreated_pdfs"):
        os.makedirs(output_path, exist_ok=True)

        for i in range(amount):
            with open(f"{data_path}/extracted_data_{i}.data", "r") as file:
                data = file.read()

            form_data, signature_data = self.__fill_pdf_data(data)

            output_file = f"{output_path}/pdf_recreated_from_template_{i}.pdf"
            fillpdfs.write_fillable_pdf(template_path, output_file, form_data, flatten=True)
            self.__fill_signature_data(output_file, signature_data)

    def __sign_pdf(self, pdf_path: str, private_key_path: str, certificate_path: str):
        cms_signer = signers.SimpleSigner.load(private_key_path, 
                                               certificate_path,
                                               ca_chain_files=[certificate_path])

        with open(pdf_path, "rb") as file:
            pdf = IncrementalPdfFileWriter(file)
            signer = signers.PdfSigner(signers.PdfSignatureMetadata(field_name="sddup signature"),
                                       signer=cms_signer)
            signed_pdf = signer.sign_pdf(pdf)

        with open(pdf_path, "wb") as file:
            file.write(signed_pdf.getbuffer())

    def __extract_pdf_data(self, pdf_path: str):
        data_from_pdf = fillpdfs.get_form_fields(pdf_path)
        data = self.__format_data(data_from_pdf, handle_special_fields= True)
        data += "{}".format(self.__extract_pdf_signature(pdf_path))

        print(data)

        return data

    def __extract_pdf_signature(self, pdf_path: str):
        data = ''.encode("UTF-8")
        pdf = open(pdf_path, "rb")
        
        for line in pdf:
            if line == "%%EOF\n".encode("UTF-8"):
                break

        for line in pdf:
            data += line

        data = data.decode("UTF-8")

        return data

    def __fill_pdf_data(self, formatted_data: str):
        form_data = dict()
        formatted_data = formatted_data.split("#")

        user_data = formatted_data[:len(self.form_fields)]
        signature_data = formatted_data[len(self.form_fields):]

        form_data = self.__fill_form_data(user_data)

        return form_data, signature_data

    def __fill_form_data(self, formatted_data: str):
        form_data = dict()

        for field, data in zip(self.form_fields, formatted_data):
            if field in self.special_fields.keys():
                field = self.special_fields[field]
            form_data[field] = data

        return form_data

    def __fill_signature_data(self, pdf_path: str, signature_data: str):
        pdf = open(pdf_path, "ab")
        signature_byte = "#".join(signature_data).encode("UTF-8")
        pdf.write(signature_byte)

    def __format_data(self, data: dict, handle_special_fields: bool = False):
        formatted_data = ""  
        for field in self.form_fields:
            if handle_special_fields and field in self.special_fields.keys():
                formatted_data += f"{data[self.special_fields[field]]}#"
                continue
            
            formatted_data += f"{data[field]}#"

        return formatted_data

pdf = PDFHandler()
pdf.create_pdf(5)
pdf.extract_data(5)
pdf.recreate_pdf(5)
