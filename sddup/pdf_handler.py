from data_generator import PDFDataGenerator

import os

from fillpdf import fillpdfs

class PDFHandler:
    def __init__(self):
        self.generator = PDFDataGenerator()

        self.form_fields = ['ano', '6176f373', 'cpf', 'código de acesso', 'data de nascimento', 'data do registro', 'declarante', 'dia', 'dnv', 'endereço', '66696c6961e7e36f', 'gêmeos', 'hora de nascimento', 'local de nascimento', 'matrícula', 'município de nascimento', 'município de registro', 'município ofício', '6dea73', 'nome', 'nome do ofício', 'nome e matrícula dos gêmeos', 'observações', 'sexo']


    def create_pdf(self, amount: int = 1, template_path: str = "./sddup/templates/birth_certificate_template.pdf", output_path: str = "./sddup/outputs/pdf/generated_pdfs"):
        os.makedirs(output_path, exist_ok=True)

        for i in range(amount):
            data = self.generator.generate_data_pdf()
            formatted_data = self.__format_data(data)
            
            form_data = self.__fill_form_data(formatted_data)

            output_path = f"{output_path}/pdf_generated_from_template_{i}.pdf"

            fillpdfs.write_fillable_pdf(template_path, output_path, form_data, flatten=True)

    def __fill_form_data(self, formatted_data: str):
        form_data = dict()
        formatted_data = formatted_data.split("#")

        for field, data in zip(self.form_fields, formatted_data):
            form_data[field] = data

        return form_data

    def __format_data(self, data: dict):
        formatted_data = ""  
        for field in sorted(list(data.keys())):
            formatted_data += f"{data[field]}#"

        formatted_data = formatted_data[:len(formatted_data)-1]

        return formatted_data

handler = PDFHandler()
handler.create_pdf()
print(fillpdfs.get_form_fields("./sddup/outputs/pdf/generated_pdfs/pdf_generated_from_template_0.pdf"))
