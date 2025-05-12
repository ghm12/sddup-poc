from data_generator import XMLDataGenerator
from data_cipher import DataCipher

from lxml import etree
import os

import xml.etree.ElementTree as ET

class XMLHandler:
    def __init__(self):
        self.generator = XMLDataGenerator()
        self.data_cipher = DataCipher()
        self.namespaces = {"ns": "http://portal.mec.gov.br/diplomadigital/arquivos-em-xsd",
                           "xades": "http://uri.etsi.org/01903/v1.3.2#",
                           "ds": "http://www.w3.org/2000/09/xmldsig#"}

    def create_xml(self, amount: int = 1, template_path: str = "./sddup/data/templates/diploma_template.xml", output_path: str = "./sddup/outputs/xml/generated_xmls"):
        os.makedirs(output_path, exist_ok=True)

        for i in range(amount):
            data = self.generator.generate_data_xml()
            formatted_data = self.__format_data(data)
            
            template_root = etree.parse(template_path)
            template_root = self.__fill_xml(formatted_data, template_root)

            template_root.write(f"{output_path}/xml_generated_from_template_{i}.xml", doctype='<?xml version="1.0" encoding="UTF-8" standalone="no"?>', encoding="UTF-8")

    def extract_data(self, amount: int = 1, xml_dir_path: str = "./sddup/outputs/xml/generated_xmls", output_path: str = "./sddup/outputs/xml/extracted_data"):
        os.makedirs(output_path, exist_ok=True)

        for i in range(amount):
            data = self.__extract_data_from_xml(f"{xml_dir_path}/xml_generated_from_template_{i}.xml")
            data = self.data_cipher.encrypt_data(data)
            with open(f"{output_path}/extracted_data_{i}.data", "wb") as file:
                file.write(data)

    def recreate_xml(self, amount: int = 1, template_path: str = "./sddup/data/templates/diploma_template.xml", data_path: str = "./sddup/outputs/xml/extracted_data", output_path: str = "./sddup/outputs/xml/recreated_xmls"):
        os.makedirs(output_path, exist_ok=True)

        for i in range(amount):
            with open(f"{data_path}/extracted_data_{i}.data", "rb") as file:
                data = file.read()

            data = self.data_cipher.decrypt_data(data)
            xml_root = etree.parse(template_path)

            xml_root = self.__fill_xml(data, xml_root)
            xml_root.write(f"{output_path}/xml_recreated_from_data_{i}.xml", doctype='<?xml version="1.0" encoding="UTF-8" standalone="no"?>', encoding="UTF-8")

    def __fill_xml(self, data: str, xml_root):
        data_chunks_by_type = data.split("$")

        diploma_data = data_chunks_by_type[0]
        encapsulated_timestamp_data = data_chunks_by_type[1]
        signature_id_data = data_chunks_by_type[2]
        signature_timestamp_data = data_chunks_by_type[3]
        signing_time_data = data_chunks_by_type[4]
        signature_value_data = data_chunks_by_type[5]

        xml_root = self.__fill_diploma_data_xml(diploma_data, xml_root)
        xml_root = self.__fill_encapsulated_timestamp_data_xml(encapsulated_timestamp_data, xml_root)
        xml_root = self.__fill_signature_id_data_xml(signature_id_data, xml_root)
        xml_root = self.__fill_signature_timestamp_data_xml(signature_timestamp_data, xml_root)
        xml_root = self.__fill_signing_time_data_xml(signing_time_data, xml_root)
        xml_root = self.__fill_signature_value_data_xml(signature_value_data, xml_root)
        
        return xml_root

    def __fill_diploma_data_xml(self, data: str, xml_root):
        data_chunks = data.split(";")
        for chunk in data_chunks:
            tag_path, value = chunk.split(":")

            # Formatting tag_path to be used with xpath
            tag_path = ".//ns:" + tag_path.replace("/", "/ns:")
                
            xml_root.xpath(tag_path, namespaces= self.namespaces)[0].text = value

        return xml_root

    def __fill_encapsulated_timestamp_data_xml(self, data: str, xml_root):
        data_chunks = data.split(";")
        tags = xml_root.xpath(".//xades:EncapsulatedTimeStamp", namespaces= self.namespaces)
        for chunk in data_chunks:
            occurence, tag_id, value = chunk.split(":")
            occurence = int(occurence)

            tags[occurence].attrib["Id"] = tag_id
            tags[occurence].text = value

        return xml_root

    def __fill_signature_id_data_xml(self, data: str, xml_root):
        data_chunks = data.split(";")
        tags = xml_root.xpath(".//ds:Signature", namespaces= self.namespaces)
        for chunk in data_chunks:
            occurence, tag_id = chunk.split(":")
            occurence = int(occurence)

            tags[occurence].attrib["Id"] = tag_id

        return xml_root

    def __fill_signature_timestamp_data_xml(self, data: str, xml_root):
        data_chunks = data.split(";")
        tags = xml_root.xpath(".//xades:SignatureTimeStamp", namespaces= self.namespaces)
        for chunk in data_chunks:
            occurence, tag_id = chunk.split(":")
            occurence = int(occurence)

            tags[occurence].attrib["Id"] = tag_id

        return xml_root

    def __fill_signing_time_data_xml(self, data: str, xml_root):
        data_chunks = data.split(";")
        tags = xml_root.xpath(".//xades:SigningTime", namespaces= self.namespaces)
        for chunk in data_chunks:
            occurence, value = chunk.split(":", 1)
            occurence = int(occurence)

            tags[occurence].text = value

        return xml_root

    def __fill_signature_value_data_xml(self, data: str, xml_root):
        data_chunks = data.split(";")
        tags = xml_root.xpath(".//ds:SignatureValue", namespaces= self.namespaces)
        for chunk in data_chunks:
            occurence, tag_id, value = chunk.split(":")
            occurence = int(occurence)

            tags[occurence].attrib["Id"] = tag_id
            tags[occurence].text = value

        return xml_root


    def __extract_data_from_xml(self, xml_path: str):
        xml_root = etree.parse(xml_path)
        data = ""

        data += self.__extract_diploma_data_from_xml(xml_root) + "$"
        data += self.__extract_encapsulated_timestamp_from_xml(xml_root) + "$"
        data += self.__extract_signature_id_from_xml(xml_root) + "$"
        data += self.__extract_signature_timestamp_from_xml(xml_root) + "$"
        data += self.__extract_signing_time_from_xml(xml_root) + "$"
        data += self.__extract_signature_value_from_xml(xml_root)

        return data

    def __extract_diploma_data_from_xml(self, xml_root):
        tags = {"Diplomado": ["ID", "Nome", "Sexo", "Nacionalidade", "Naturalidade/CodigoMunicipio", "Naturalidade/NomeMunicipio", "Naturalidade/UF", "CPF", "RG/Numero", "RG/UF", "DataNascimento"],
                "DadosCurso": ["NomeCurso", "CodigoCursoEMEC", "Habilitacao/NomeHabilitacao", "Habilitacao/DataHabilitacao", "Modalidade", "TituloConferido/Titulo", "GrauConferido",
                               "EnderecoCurso/Logradouro", "EnderecoCurso/Complemento", "EnderecoCurso/Bairro", "EnderecoCurso/CodigoMunicipio", "EnderecoCurso/NomeMunicipio", "EnderecoCurso/UF", "EnderecoCurso/CEP",
                               "Autorizacao/Tipo", "Autorizacao/Numero", "Autorizacao/Data", "Reconhecimento/Tipo", "Reconhecimento/Numero", "Reconhecimento/Data", "Reconhecimento/DataPublicacao"],
                "IesEmissora": ["Nome", "CodigoMEC", "CNPJ", "Endereco/Logradouro", "Endereco/Numero", "Endereco/Bairro", "Endereco/CodigoMunicipio", "Endereco/NomeMunicipio", "Endereco/UF", "Endereco/CEP",
                                "Credenciamento/Tipo", "Credenciamento/Numero", "Credenciamento/Data", "Credenciamento/DataPublicacao", "Credenciamento/SecaoPublicacao", "Credenciamento/PaginaPublicacao",
                                "Recredenciamento/Tipo", "Recredenciamento/Numero", "Recredenciamento/Data", "Recredenciamento/DataPublicacao", "Recredenciamento/SecaoPublicacao", "Recredenciamento/PaginaPublicacao",
                                "Mantenedora/RazaoSocial", "Mantenedora/CNPJ", "Mantenedora/Endereco/Logradouro", "Mantenedora/Endereco/Numero", "Mantenedora/Endereco/Bairro", "Mantenedora/Endereco/CodigoMunicipio",
                                "Mantenedora/Endereco/NomeMunicipio", "Mantenedora/Endereco/UF", "Mantenedora/Endereco/CEP"]}

        data = ""
        
        for path in tags["Diplomado"]:
            tag = "Diplomado/" + path
            tag_xpath = ".//ns:" + tag.replace("/", "/ns:")
            value = xml_root.xpath(tag_xpath, namespaces=self.namespaces)[0].text
            data += f"{tag}:{value};" 

        for path in tags["DadosCurso"]:
            tag = "DadosCurso/" + path
            tag_xpath = ".//ns:" + tag.replace("/", "/ns:")
            value = xml_root.xpath(tag_xpath, namespaces=self.namespaces)[0].text
            data += f"{tag}:{value};" 

        for path in tags["IesEmissora"]:
            tag = "IesEmissora/" + path
            tag_xpath = ".//ns:" + tag.replace("/", "/ns:")
            value = xml_root.xpath(tag_xpath, namespaces=self.namespaces)[0].text
            data += f"{tag}:{value};"

        data = data[:len(data)-1]

        return data

    def __extract_encapsulated_timestamp_from_xml(self, xml_root):
        tags = xml_root.xpath(".//xades:EncapsulatedTimeStamp", namespaces= self.namespaces)
        data = ""

        for i in range(len(tags)):
            tag_attrib = tags[i].attrib.get("Id")
            tag_value = tags[i].text

            data += f"{i}:{tag_attrib}:{tag_value};"

        data = data[:len(data)-1]

        return data

    def __extract_signature_id_from_xml(self, xml_root):
        tags = xml_root.xpath(".//ds:Signature", namespaces= self.namespaces)
        data = ""

        for i in range(len(tags)):
            tag_attrib = tags[i].attrib.get("Id")

            data += f"{i}:{tag_attrib};"

        data = data[:len(data)-1]
        
        return data

    def __extract_signature_timestamp_from_xml(self, xml_root):
        tags = xml_root.xpath(".//xades:SignatureTimeStamp", namespaces= self.namespaces)
        data = ""

        for i in range(len(tags)):
            tag_attrib = tags[i].attrib.get("Id")

            data += f"{i}:{tag_attrib};"

        data = data[:len(data)-1]
        
        return data

    def __extract_signing_time_from_xml(self, xml_root):
        tags = xml_root.xpath(".//xades:SigningTime", namespaces= self.namespaces)
        data = ""

        for i in range(len(tags)):
            tag_value = tags[i].text

            data += f"{i}:{tag_value};"

        data = data[:len(data)-1]
        
        return data

    def __extract_signature_value_from_xml(self, xml_root):
        tags = xml_root.xpath(".//ds:SignatureValue", namespaces= self.namespaces)
        data = ""

        for i in range(len(tags)):
            tag_attrib = tags[i].attrib.get("Id")
            tag_value = tags[i].text

            data += f"{i}:{tag_attrib}:{tag_value};"

        data = data[:len(data)-1]
        
        return data

    def __format_data(self, data):
        # Formatted data follows the following pattern:
        # tag:occurence:value;
        # - tag: tag name
        # - occurence: which occurence of tag to change, if tag appears multiple times (e.g. CPF appears multiple times through the document)
        # - value: tag name
        # - ; acts as a separator of data, can be changed to something else if conflicts happen

        formatted_data = ""

        # Graduate data
        formatted_data += "Diplomado/ID:{};".format(data["graduate"]["id"])
        formatted_data += "Diplomado/Nome:{};".format(data["graduate"]["name"])
        formatted_data += "Diplomado/Sexo:{};".format(data["graduate"]["gender"])
        formatted_data += "Diplomado/Nacionalidade:{};".format(data["graduate"]["nationality"])
        formatted_data += "Diplomado/Naturalidade/CodigoMunicipio:{};".format(data["graduate"]["city_code"])
        formatted_data += "Diplomado/Naturalidade/NomeMunicipio:{};".format(data["graduate"]["city_name"])
        formatted_data += "Diplomado/Naturalidade/UF:{};".format(data["graduate"]["city_uf"])
        formatted_data += "Diplomado/CPF:{};".format(data["graduate"]["cpf"])
        formatted_data += "Diplomado/RG/Numero:{};".format(data["graduate"]["rg"])
        formatted_data += "Diplomado/RG/UF:{};".format(data["graduate"]["rg_uf"])
        formatted_data += "Diplomado/DataNascimento:{};".format(data["graduate"]["birth_date"])
        
        # Course data
        formatted_data += "DadosCurso/NomeCurso:{};".format(data["course"]["name"])
        formatted_data += "DadosCurso/CodigoCursoEMEC:{};".format(data["course"]["code"])
        formatted_data += "DadosCurso/Habilitacao/NomeHabilitacao:{};".format(data["course"]["habilitation_name"])
        formatted_data += "DadosCurso/Habilitacao/DataHabilitacao:{};".format(data["course"]["habilitation_date"])
        formatted_data += "DadosCurso/Modalidade:{};".format(data["course"]["type"])
        formatted_data += "DadosCurso/TituloConferido/Titulo:{};".format(data["course"]["title"])
        formatted_data += "DadosCurso/GrauConferido:{};".format(data["course"]["degree"])

        formatted_data += "DadosCurso/EnderecoCurso/Logradouro:{};".format(data["course"]["address_street"])
        formatted_data += "DadosCurso/EnderecoCurso/Complemento:{};".format(data["course"]["address_complement"])
        formatted_data += "DadosCurso/EnderecoCurso/Bairro:{};".format(data["course"]["address_district"])
        formatted_data += "DadosCurso/EnderecoCurso/CodigoMunicipio:{};".format(data["course"]["address_city_code"])
        formatted_data += "DadosCurso/EnderecoCurso/NomeMunicipio:{};".format(data["course"]["address_city"])
        formatted_data += "DadosCurso/EnderecoCurso/UF:{};".format(data["course"]["address_uf"])
        formatted_data += "DadosCurso/EnderecoCurso/CEP:{};".format(data["course"]["address_cep"])

        formatted_data += "DadosCurso/Autorizacao/Tipo:{};".format(data["course"]["authorization_type"])
        formatted_data += "DadosCurso/Autorizacao/Numero:{};".format(data["course"]["authorization_number"])
        formatted_data += "DadosCurso/Autorizacao/Data:{};".format(data["course"]["authorization_date"])

        formatted_data += "DadosCurso/Reconhecimento/Tipo:{};".format(data["course"]["recognition_type"])
        formatted_data += "DadosCurso/Reconhecimento/Numero:{};".format(data["course"]["recognition_number"])
        formatted_data += "DadosCurso/Reconhecimento/Data:{};".format(data["course"]["recognition_date"])
        formatted_data += "DadosCurso/Reconhecimento/DataPublicacao:{};".format(data["course"]["recognition_publication_date"])

        # Issuer data
        formatted_data += "IesEmissora/Nome:{};".format(data["issuer"]["name"])
        formatted_data += "IesEmissora/CodigoMEC:{};".format(data["issuer"]["code"])
        formatted_data += "IesEmissora/CNPJ:{};".format(data["issuer"]["cnpj"])
        
        formatted_data += "IesEmissora/Endereco/Logradouro:{};".format(data["issuer"]["address_street"])
        formatted_data += "IesEmissora/Endereco/Numero:{};".format(data["issuer"]["address_number"])
        formatted_data += "IesEmissora/Endereco/Bairro:{};".format(data["issuer"]["address_district"])
        formatted_data += "IesEmissora/Endereco/CodigoMunicipio:{};".format(data["issuer"]["address_city_code"])
        formatted_data += "IesEmissora/Endereco/NomeMunicipio:{};".format(data["issuer"]["address_city"])
        formatted_data += "IesEmissora/Endereco/UF:{};".format(data["issuer"]["address_uf"])
        formatted_data += "IesEmissora/Endereco/CEP:{};".format(data["issuer"]["address_cep"])

        formatted_data += "IesEmissora/Credenciamento/Tipo:{};".format(data["issuer"]["accreditation_type"])
        formatted_data += "IesEmissora/Credenciamento/Numero:{};".format(data["issuer"]["accreditation_number"])
        formatted_data += "IesEmissora/Credenciamento/Data:{};".format(data["issuer"]["accreditation_date"])
        formatted_data += "IesEmissora/Credenciamento/DataPublicacao:{};".format(data["issuer"]["accreditation_publication_date"])
        formatted_data += "IesEmissora/Credenciamento/SecaoPublicacao:{};".format(data["issuer"]["accreditation_publication_section"])
        formatted_data += "IesEmissora/Credenciamento/PaginaPublicacao:{};".format(data["issuer"]["accreditation_publication_date"])

        formatted_data += "IesEmissora/Recredenciamento/Tipo:{};".format(data["issuer"]["reaccreditation_type"])
        formatted_data += "IesEmissora/Recredenciamento/Numero:{};".format(data["issuer"]["reaccreditation_number"])
        formatted_data += "IesEmissora/Recredenciamento/Data:{};".format(data["issuer"]["reaccreditation_date"])
        formatted_data += "IesEmissora/Recredenciamento/DataPublicacao:{};".format(data["issuer"]["reaccreditation_publication_date"])
        formatted_data += "IesEmissora/Recredenciamento/SecaoPublicacao:{};".format(data["issuer"]["reaccreditation_publication_section"])
        formatted_data += "IesEmissora/Recredenciamento/PaginaPublicacao:{};".format(data["issuer"]["reaccreditation_publication_date"])


        formatted_data += "IesEmissora/Mantenedora/RazaoSocial:{};".format(data["issuer"]["maintainer_name"])
        formatted_data += "IesEmissora/Mantenedora/CNPJ:{};".format(data["issuer"]["maintainer_cnpj"])
        formatted_data += "IesEmissora/Mantenedora/Endereco/Logradouro:{};".format(data["issuer"]["maintainer_address_street"])
        formatted_data += "IesEmissora/Mantenedora/Endereco/Numero:{};".format(data["issuer"]["maintainer_address_number"])
        formatted_data += "IesEmissora/Mantenedora/Endereco/Bairro:{};".format(data["issuer"]["maintainer_address_district"])
        formatted_data += "IesEmissora/Mantenedora/Endereco/CodigoMunicipio:{};".format(data["issuer"]["maintainer_address_city_code"])
        formatted_data += "IesEmissora/Mantenedora/Endereco/NomeMunicipio:{};".format(data["issuer"]["maintainer_address_city"])
        formatted_data += "IesEmissora/Mantenedora/Endereco/UF:{};".format(data["issuer"]["maintainer_address_uf"])
        formatted_data += "IesEmissora/Mantenedora/Endereco/CEP:{}".format(data["issuer"]["maintainer_address_cep"])

        formatted_data += "$"

        for i in range(len(data["encapsulated_timestamp"]["id"])):
            if i > 0:
                formatted_data += ";"
            tag_id = data["encapsulated_timestamp"]["id"][i]
            tag_value = data["encapsulated_timestamp"]["value"][i]
            formatted_data += f"{i}:{tag_id}:{tag_value}"
        
        formatted_data += "$"

        for i in range(len(data["signature_id"])):
            if i > 0:
                formatted_data += ";"
            signature_id = data["signature_id"][i]
            formatted_data += f"{i}:{signature_id}"
        
        formatted_data += "$"

        for i in range(len(data["signature_timestamp"])):
            if i > 0:
                formatted_data += ";"
            signature_timestamp = data["signature_timestamp"][i]
            formatted_data += f"{i}:{signature_timestamp}"
        
        formatted_data += "$"

        for i in range(len(data["signing_time"])):
            if i > 0:
                formatted_data += ";"
            signing_time = data["signing_time"][i]
            formatted_data += f"{i}:{signing_time}"

        formatted_data += "$"

        for i in range(len(data["signature_value"]["id"])):
            if i > 0:
                formatted_data += ";"
            tag_id = data["signature_value"]["id"][i]
            tag_value = data["signature_value"]["value"][i]
            formatted_data += f"{i}:{tag_id}:{tag_value}"

        return formatted_data

