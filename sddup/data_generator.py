from faker import Faker

import random
import base64

class XMLDataGenerator:
    def __init__(self, language: str = "pt-BR", seeded: bool = True):
        self.faker = Faker(language)
        
        # Provides the same results everytime
        if seeded:
            self.__set_seed()

    def __set_seed(self):
        Faker.seed(12345)
        random.seed(12345)

    def generate_data_xml(self):
        data = dict()

        # Graduate data
        data["graduate"] = self.__generate_xml_graduate_data()

        # Course data
        data["course"] = self.__generate_xml_course_data()

        # Issuer data
        data["issuer"] = self.__generate_xml_issuer_data()

        # EncapsulatedTimeStamp data
        data["encapsulated_timestamp"] = self.__generate_encapsulated_timestamp_data()

        # SignatureId data
        data["signature_id"] = self.__generate_signature_id_data()

        # SignatureTimeStamp data
        data["signature_timestamp"] = self.__generate_signature_timestamp_data()

        # SigningTime data
        data["signing_time"] = self.__generate_signing_time_data()

        # SignatureValue data
        data["signature_value"] = self.__generate_signature_value_data()

        return data

    def __generate_xml_graduate_data(self):
        data = dict()
        
        graduate_id = random.randint(10000000, 99999999)
        graduate_name = self.faker.name()
        
        gender = ["M", "F"]
        n = random.randint(0, 1)
        graduate_gender = gender[n]

        graduate_nationality = "Brasileiro"
        graduate_city_code = random.randint(1, 100000000)
        graduate_city_name = self.faker.city()

        # TODO transform in code
        graduate_city_uf = self.faker.state()
        graduate_rg_uf = self.faker.state()
       
        # TODO fix format
        graduate_cpf = random.randint(10000000000, 99999999999)
        graduate_rg = random.randint(1000000, 9999999)

        graduate_birth_date = self.faker.date()

        data["id"] = graduate_id 
        data["name"] = graduate_name
        data["gender"] = graduate_gender
        data["nationality"] = graduate_nationality
        data["city_code"] = graduate_city_code
        data["city_name"] = graduate_city_name
        data["city_uf"] = graduate_city_uf
        data["cpf"] = graduate_cpf
        data["rg"]= graduate_rg
        data["rg_uf"] = graduate_rg_uf
        data["birth_date"] = graduate_birth_date

        return data

    def __generate_xml_course_data(self):
        data = dict()

        # TODO do a generator for this
        course_name = "Ciencias da Computacao"

        course_code = random.randint(1, 99999)

        # TODO give more options
        course_habilitation_name = "Bacharelado em " + course_name
        course_habilitation_date = self.faker.date()

        course_types = ["Presencial", "Semi-presencial", "Remoto"]
        n = random.randint(0, 2)
        course_type = course_types[n]

        course_title = "Bacharel"
        course_degree = "Bacharelado"

        address = self.faker.address().split("\n")
        cep, city_uf = address[2].split(" ", 1)
        city, uf = city_uf.split("/")
        course_address_street = address[0]
        course_address_complement = "Campus Universitario Prof. Joao David Ferreira Lima"
        course_address_district = address[1]
        course_address_city = city.strip()
        course_address_city_code = random.randint(1, 100000000)
        course_address_uf = uf.strip()
        course_address_cep = cep.replace("-", "")

        course_authorization_type = "Parecer"
        course_authorization_number = random.randint(1, 999)
        course_authorization_date = self.faker.date()

        course_recognition_type = "Portaria"
        course_recognition_number = random.randint(1, 999)
        course_recognition_date = self.faker.date()
        course_recognition_publication_date = self.faker.date()

        data["name"] = course_name
        data["code"] = course_code
        data["habilitation_name"] = course_habilitation_name
        data["habilitation_date"] = course_habilitation_date
        data["type"] = course_type
        data["title"] = course_title
        data["degree"] = course_degree
        
        data["address_street"] = course_address_street
        data["address_complement"] = course_address_complement
        data["address_district"] = course_address_district
        data["address_city"] = course_address_city
        data["address_city_code"] = course_address_city_code
        data["address_uf"] = course_address_uf
        data["address_cep"] = course_address_cep

        data["authorization_type"] = course_authorization_type
        data["authorization_number"] = course_authorization_number
        data["authorization_date"] = course_authorization_date

        data["recognition_type"] = course_recognition_type
        data["recognition_number"] = course_recognition_number
        data["recognition_date"] = course_recognition_date
        data["recognition_publication_date"] = course_recognition_publication_date

        return data

    def __generate_xml_issuer_data(self):
        data = dict()

        issuer_name = "UNIVERSIDADE FEDERAL DE SANTA CATARINA"
        issuer_code = random.randint(1, 999)

        # TODO fix format
        issuer_cnpj = random.randint(10000000000000, 99999999999999)

        address = self.faker.address().split("\n")
        cep, city_uf = address[2].split(" ", 1)
        city, uf = city_uf.split("/")
        issuer_address_street = "Campus Universitario"
        issuer_address_number = "s/n"
        issuer_address_district = address[1]
        issuer_address_city_code = random.randint(1, 9999999)
        issuer_address_city = city.strip()
        issuer_address_uf = uf.strip()
        issuer_address_cep = cep.replace("-", "")

        issuer_accreditation_type = "Lei Federal"
        issuer_accreditation_number = random.randint(1, 9999)
        issuer_accreditation_date = self.faker.date()
        issuer_accreditation_publication_date = self.faker.date()
        issuer_accreditation_publication_section = random.randint(1, 9)
        issuer_accreditation_publication_page = random.randint(1, 99)

        issuer_reaccreditation_type = "Portaria"
        issuer_reaccreditation_number = random.randint(1, 9999)
        issuer_reaccreditation_date = self.faker.date()
        issuer_reaccreditation_publication_date = self.faker.date()
        issuer_reaccreditation_publication_section = random.randint(1, 9)
        issuer_reaccreditation_publication_page = random.randint(1, 99)

        issuer_maintainer_name = issuer_name
        issuer_maintainer_cnpj = issuer_cnpj
        issuer_maintainer_address_street = issuer_address_street 
        issuer_maintainer_address_number = issuer_address_number
        issuer_maintainer_address_district = issuer_address_district
        issuer_maintainer_address_city_code = issuer_address_city_code
        issuer_maintainer_address_city = issuer_address_city
        issuer_maintainer_address_uf = issuer_address_uf
        issuer_maintainer_address_cep = issuer_address_cep

        data["name"] = issuer_name
        data["code"] = issuer_code
        data["cnpj"] = issuer_cnpj

        data["address_street"] = issuer_address_street
        data["address_number"] = issuer_address_number
        data["address_district"] = issuer_address_district
        data["address_city_code"] = issuer_address_city_code
        data["address_city"] = issuer_address_city
        data["address_uf"] = issuer_address_uf
        data["address_cep"] = issuer_address_cep

        data["accreditation_type"] = issuer_accreditation_type
        data["accreditation_number"] = issuer_accreditation_number
        data["accreditation_date"] = issuer_accreditation_date
        data["accreditation_publication_date"] = issuer_accreditation_publication_date
        data["accreditation_publication_section"] = issuer_accreditation_publication_section
        data["accreditation_publication_page"] = issuer_accreditation_publication_page

        data["reaccreditation_type"] = issuer_reaccreditation_type
        data["reaccreditation_number"] = issuer_reaccreditation_number
        data["reaccreditation_date"] = issuer_reaccreditation_date
        data["reaccreditation_publication_date"] = issuer_reaccreditation_publication_date
        data["reaccreditation_publication_section"] = issuer_reaccreditation_publication_section
        data["reaccreditation_publication_page"] = issuer_reaccreditation_publication_page

        data["maintainer_name"] = issuer_maintainer_name
        data["maintainer_cnpj"] = issuer_maintainer_cnpj
        data["maintainer_address_street"] = issuer_maintainer_address_street
        data["maintainer_address_number"] = issuer_maintainer_address_number
        data["maintainer_address_district"] = issuer_maintainer_address_district
        data["maintainer_address_city_code"] = issuer_maintainer_address_city_code
        data["maintainer_address_city"] = issuer_maintainer_address_city
        data["maintainer_address_uf"] = issuer_maintainer_address_uf
        data["maintainer_address_cep"] = issuer_maintainer_address_cep
        
        return data

    def __generate_encapsulated_timestamp_data(self):
        data = dict()
        data["id"], data["value"] = list(None for _ in range(13)), list(None for _ in range(13))

        for i in range(13):
            data["id"][i] = "ETS-{}-{}-{}-{}-{}".format(random.randbytes(4).hex(), random.randbytes(2).hex(),
                                                         random.randbytes(2).hex(), random.randbytes(2).hex(),
                                                         random.randbytes(6).hex())
            data["value"][i] = base64.b64encode(random.randbytes(13000))

        return data

    def __generate_signature_id_data(self):
        data = dict()

        for i in range(6):
            data[i] = "id-{}".format(random.randbytes(16).hex())

        return data

    def __generate_signature_timestamp_data(self):
        data = dict()

        for i in range(6):
            data[i] = "TS-{}-{}-{}-{}-{}".format(random.randbytes(4).hex(), random.randbytes(2).hex(),
                                                 random.randbytes(2).hex(), random.randbytes(2).hex(),
                                                 random.randbytes(6).hex())

        return data

    def __generate_signing_time_data(self):
        data = dict()

        for i in range(6):
            time = self.faker.date_time()
            data[i] = time.strftime("%Y-%m-%dT%H:%M:%SZ")

        return data

    def __generate_signature_value_data(self):
        data = dict()
        data["id"], data["value"] = list(None for _ in range(6)), list(None for _ in range(6))

        for i in range(6):
            data["id"][i] = "value-id-{}".format(random.randbytes(16).hex())
            data["value"][i] = base64.b64encode(random.randbytes(258))

        return data\
            
class PDFDataGenerator:
    def __init__(self, language: str = "pt-BR", seeded: bool = True):
        self.faker = Faker(language)
        if seeded:
            self.__set_seed()

    def __set_seed(self):
        Faker.seed(12345)
        random.seed(12345)

    def generate_data_pdf(self):
        data = dict()

        person = self.__generate_person_data()

        father = self.__generate_person_data()
        mother = self.__generate_person_data()

        grandpa_father = self.faker.name_male()
        grandma_father = self.faker.name_female()

        grandpa_mother = self.faker.name_male()
        grandma_mother = self.faker.name_female()

        grandparents = f"{grandpa_father} e {grandma_father}; {grandpa_mother} e {grandma_mother}"

        birth_date = self.__format_date(person["birth_date"])
        birth_city = f"{person['address']['city']} - {person['address']['state']}"
        birth_place = f"Hospital {person['address']['neighborhood']}"

        affiliation = self.__format_affiliation(father, mother)

        declarant = self.faker.name()
        registry_date = self.__format_written_date(person["birth_date"])

        observations = self.__generate_observation(person)

        office_city = f"{person['address']['city']} - {person['address']['state']}"
        office_name = f"Oficio da cidade {person['address']['city']} do Estado de {person['address']['state']}"
        office_address = self.faker.address().replace("\n", " ")

        access_code = base64.b64encode(random.randbytes(6)).decode('UTF-8')

        data["nome"] = person["name"]
        data["matrícula"] = person["registration"]
        data["cpf"] = person["cpf"]

        data["data de nascimento"] = birth_date["written_date"]
        data["dia"] = birth_date["day"]
        data["mês"] = birth_date["month"]
        data["ano"] = birth_date["year"]
        data["hora de nascimento"] = birth_date["hour"]
        data["município de nascimento"] = birth_city
        data["local de nascimento"] = birth_place
        data["município de registro"] = birth_city
        data["sexo"] = person["gender"]

        data["filiação"] = affiliation
        data["avós"] = grandparents

        # TODO random chance to be twins?
        data["nome e matrícula dos gêmeos"] = "Não consta"
        data["gêmeos"] = "Não"

        data["declarante"] = declarant

        data["data do registro"] = registry_date 
        data["dnv"] = "Não consta"

        data["observações"] = observations

        data["município ofício"] = office_city
        data["nome do ofício"] = office_name
        data["endereço"] = office_address

        data["código de acesso"] = access_code

        data["Assinatura do Registrador"] = "foo"

        return data

    def __format_affiliation(self, father: dict, mother: dict):
        data = ""

        states = {"AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas", "BA": "Bahia", "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo", "GO": "Goiás", "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul", "MG": "Minas Gerais", "PA": "Pará", "PB": "Paraíba", "PR": "Paraná", "PE": "Pernambuco", "PI": "Piauí", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte", "RS": "Rio Grande do Sul", "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina", "SP": "São Paulo", "SE": "Sergipe", "TO": "Tocantins"}
  
        father_name = father["name"]
        father_street = father["address"]["street"]
        father_number = father["address"]["number"]
        father_city = father["address"]["city"]
        father_state = father["address"]["state"]
        father_state_full = states[father_state]

        mother_name = mother["name"]
        mother_street = mother["address"]["street"]
        mother_number = mother["address"]["number"]
        mother_city = mother["address"]["city"]
        mother_state = mother["address"]["state"]
        mother_state_full = states[mother_state]
        
        data = f"{father_name}, Natural de Estado de {father_state_full} - {father_state}, residente e domiciliado à(em) rua {father_street}, {father_number}, {father_city}-{father_state} e "
        data += f"{mother_name}, Natural de Estado de {mother_state_full} - {mother_state}, residente e domiciliada à(em) rua {father_street}, {father_number}, {father_city}-{father_state}."

        return data

    def __format_date(self, birth_date):
        data = dict()

        hour = birth_date.strftime("%H:%S")
        day = birth_date.strftime("%d")
        month = birth_date.strftime("%m")
        year = birth_date.strftime("%Y")
        written_date = self.__format_written_date(birth_date)

        data["hour"] = hour
        data["day"] = day
        data["month"] = month
        data["year"] = year
        data["written_date"] = written_date

        return data

    def __format_written_date(self, date):
        days = {1: "Um", 2: "Dois", 3: "Três", 4: "Quatro", 5: "Cinco", 6: "Seis", 7: "Sete", 8: "Oito", 9: "Nove", 10: "Dez",
                11: "Onze", 12: "Doze", 13: "Treze", 14: "Quatorze", 15: "Quinze", 16: "Desesseis", 17: "Dezessete", 18: "Dezoito", 19: "Dezenove", 20: "Vinte",
                21: "Vinte e Um", 22: "Vinte e Dois", 23: "Vinte e Três", 24: "Vinte e Quatro", 25: "Vinte e Cinco", 26: "Vinte e Seis", 27: "Vinte e Sete", 28: "Vinte e Oito", 29: "Vinte e Nove", 30: "Trinta",
                31: "Trinta e Um"}

        months = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho",
                  7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}

        year_thousands = {19: "Mil Novecentos", 20: "Dois Mil"}
        year_tens = {2: "Vinte", 3: "Trinta", 4: "Quarenta", 5: "Cinquenta", 6: "Sessenta", 7: "Setenta", 8: "Oitenta", 9: "Noventa"}

        day = date.strftime("%d")
        month = date.strftime("%m")
        year = date.strftime("%Y")

        day_written = days[int(day)]
        month_written = months[int(month)]

        year_str = str(year)
        year_thousands_str = year_str[:2]
        year_tens_str = year_str[2]
        year_units_str = year_str[3]

        year_thousand = year_thousands[int(year_thousands_str)]

        if year_tens_str == "0" and year_units_str == "0":
            return f"{day_written} de {month_written} de {year_thousand}"

        if year_tens_str == "0" and year_units_str != "0":
            year_unit = days[int(year_units_str)]
            return f"{day_written} de {month_written} de {year_thousand} e {year_unit}"

        if year_tens_str == "1":
            year_unit = days[int(year_tens_str + year_units_str)]
            return f"{day_written} de {month_written} de {year_thousand} e {year_unit}"

        year_ten = year_tens[int(year_tens_str)]
        
        if year_units_str == "0":
            return f"{day_written} de {month_written} de {year_thousand} e {year_ten}"

        year_unit = days[int(year_units_str)]

        return f"{day_written} de {month_written} de {year_thousand} e {year_ten} e {year_unit}"

    def __generate_cpf(self):
        a = random.randint(0, 999)
        b = random.randint(0, 999)
        c = random.randint(0, 999)
        d = random.randint(0, 99)

        cpf = f"{a:03}.{b:03}.{c:03}-{d:02}"
        
        return cpf

    def __generate_registration(self):
        registry_id = random.randint(0, 999999)
        collection_id = random.randint(0, 99)
        rc_service_number = random.randint(0, 99)
        year = random.randint(0, 9999)
        registration_type = random.randint(0, 9)
        book_number = random.randint(0, 99999)
        page_number = random.randint(0, 999)
        term_number = random.randint(0, 9999999)
        verification_number = random.randint(0, 99)

        registration = f"{registry_id:06} {collection_id:02} {rc_service_number:02} {year:04} {registration_type} {book_number:03} {page_number:03} {term_number:07} {verification_number:02}"

        return registration

    def __generate_address(self):
        data = dict()

        address = self.faker.address().split("\n")
        
        street_chunks = address[0].split(",")
        street = street_chunks[0].strip()
        
        if len(street_chunks) > 1:
            number = street_chunks[1].strip()
        else:
            number = "s/n"

        neighborhood = address[1].strip()

        address_chunks = address[2].split(" ", 1)
        city_state = address_chunks[1].split("/")

        cep = address_chunks[0].strip()
        city = city_state[0].strip()
        state = city_state[1].strip()

        data["street"] = street
        data["number"] = number
        data["neighborhood"] = neighborhood
        data["cep"] = cep
        data["city"] = city
        data["state"] = state
        data["cep"] = cep

        return data

    def __generate_observation(self, person: dict):
        date = self.__format_date(self.faker.date_time())
        
        ret = "AVERBAÇÃO: {} ESTÁ INSCRITO(A) NO CPF SOB O Nº {}, AVERBADO(S) NOS TERMOS DO PROVIMENTO Nº 149/2023 DO CNJ. {} - {}, {}/{}/{} ".format(person["name"], person["cpf"], person["address"]["city"], person["address"]["state"], date["day"], date["month"], date["year"])

        return ret

    def __generate_person_data(self):
        data = dict()
        
        name = self.faker.name()
        registration = self.__generate_registration()
        cpf = self.__generate_cpf()

        birth_date = self.faker.date_time()

        address = self.__generate_address()

        gender = ["Masculino", "Feminino"]
        n = random.randint(0, 1)
        gender = gender[n]

        data["name"] = name
        data["registration"] = registration
        data["cpf"] = cpf
        data["birth_date"] = birth_date
        data["address"] = address
        data["gender"] = gender

        return data
