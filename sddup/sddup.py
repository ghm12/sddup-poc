from xml_handler import XMLHandler
from pdf_handler import PDFHandler

import hashlib
import shutil
import os

class SDDup:
    def __init__(self):
        self.xml_handler = XMLHandler()
        self.pdf_handler = PDFHandler()

        self.outputs_path = "./sddup/outputs"

        self.xml_template_path = "./sddup/data/templates/diploma_template.xml"
        self.xml_generated_xml_path = "./sddup/outputs/xml/generated_xmls"
        self.xml_extracted_data_path = "./sddup/outputs/xml/extracted_data"
        self.xml_recreated_xml_path = "./sddup/outputs/xml/recreated_xmls"

        self.pdf_template_path = "./sddup/data/templates/birth_certificate_template.pdf"
        self.pdf_generated_pdf_path = "./sddup/outputs/pdf/generated_pdfs"
        self.pdf_extracted_data_path = "./sddup/outputs/pdf/extracted_data"
        self.pdf_recreated_pdf_path = "./sddup/outputs/pdf/recreated_pdfs"

    def run_experiment(self, experiment_type: str, amount: int = 100):
        if experiment_type == "xml" or experiment_type == "both":
            self.run_experiment_xml(amount)

        if experiment_type == "pdf" or experiment_type == "both":
            self.run_experiment_pdf(amount)

    def run_experiment_xml(self, amount: int = 100):
        experiment_type = "xml"

        print("Starting experiment for XML")
        print()

        print("Cleaning previous experiment (if any)...")
        self.__clean_previous_experiment("xml")
        print("Done.")

        print(f"Creating {amount} XMLs with fake data...")
        self.xml_handler.create_xml(amount)
        print("Done.")

        print("Extracting data from generated XMLs...")
        self.xml_handler.extract_data(amount)
        print("Done.")

        print(f"Recreating {amount} XMLs from extracted data...")
        self.xml_handler.recreate_xml(amount)
        print("Done.")

        print("Comparing hash value of generated XMLs and recreated XMLs...")
        if not self.__check_hash_from_recreated_files(experiment_type, amount):
            print("Hash checking failed, one of the hash values does not match.")
            return
        print("Done. All hashes are OK.")
        
        print("Calculating R and E values...")
        r_value = self.__calculate_R(experiment_type, amount)
        e_value = self.__calculate_E(r_value)
        print(f"R = {r_value:.5%} / E = {e_value:.5%}")
        print()

    def run_experiment_pdf(self, amount: int = 100):
        experiment_type = "pdf"

        print("Starting experiment for PDF")
        print()

        print("Cleaning previous experiment (if any)...")
        self.__clean_previous_experiment("pdf")
        print("Done.")

        print(f"Creating {amount} PDFs with fake data...")
        self.pdf_handler.create_pdf(amount)
        print("Done.")

        print("Extracting data from generated PDFs...")
        self.pdf_handler.extract_data(amount)
        print("Done.")

        print(f"Recreating {amount} PDFs from extracted data...")
        self.pdf_handler.recreate_pdf(amount)
        print("Done.")

        print("Comparing hash value of generated PDFs and recreated PDFs...")
        if not self.__check_hash_from_recreated_files(experiment_type, amount):
            print("Hash checking failed, one of the hash values does not match.")
            return
        print("Done. All hashes are OK.")
        
        print("Calculating R and E values...")
        r_value = self.__calculate_R(experiment_type, amount)
        e_value = self.__calculate_E(r_value)
        print(f"R = {r_value:.5%} / E = {e_value:.5%}")
        print()

    def __check_hash_from_recreated_files(self, experiment_type: str, amount: int = 100):
        if experiment_type == "xml":
            generated_path = f"{self.xml_generated_xml_path}/xml_generated_from_template_" + "{}" + ".xml"
            recreated_path = f"{self.xml_recreated_xml_path}/xml_recreated_from_data_" + "{}" + ".xml"

        if experiment_type == "pdf":
            generated_path = f"{self.pdf_generated_pdf_path}/pdf_generated_from_template_" + "{}" + ".pdf"
            recreated_path = f"{self.pdf_recreated_pdf_path}/pdf_recreated_from_data_" + "{}" + ".pdf"
        
        for i in range(amount):
            generated_xml = open(generated_path.format(i), "rb")
            generated_xml_hash = hashlib.file_digest(generated_xml, "sha256").hexdigest()

            recreated_xml = open(recreated_path.format(i), "rb")
            recreated_xml_hash = hashlib.file_digest(recreated_xml, "sha256").hexdigest()

            if generated_xml_hash != recreated_xml_hash:
                return False

        return True

    def __clean_previous_experiment(self, experiment_type: str):
        path = f"{self.outputs_path}/{experiment_type}"
        if os.path.isdir(path):
            shutil.rmtree(path)

    def __calculate_R(self, experiment_type: str, amount: int):
        if experiment_type == "xml":
            generated_path = self.xml_generated_xml_path
            template_path = self.xml_template_path
            extracted_data_path = self.xml_extracted_data_path

        if experiment_type == "pdf":
            generated_path = self.pdf_generated_pdf_path
            template_path = self.pdf_template_path
            extracted_data_path = self.pdf_extracted_data_path
        
        naive_approach_total_size = self.__get_directory_filesize(generated_path)

        template_size = self.__get_filesize(template_path)
        sddup_approach_total_size = self.__get_directory_filesize(extracted_data_path)

        naive_approach_median_size = naive_approach_total_size/amount
        sddup_approach_median_size = sddup_approach_total_size/amount

        print(f"Naive approach: {naive_approach_total_size} bytes (median: {naive_approach_median_size} bytes)")
        print(f"Template size: {template_size} bytes")
        print(f"SDDup extracted data: {sddup_approach_total_size} bytes (median: {sddup_approach_median_size} bytes)")

        return (template_size + sddup_approach_total_size)/naive_approach_total_size 

    def __calculate_E(self, R: float):
        return 1 - R

    def __get_filesize(self, file_path: str):
        return os.path.getsize(file_path)

    def __get_directory_filesize(self, directory_path: str):
        sum = 0
        for file in os.listdir(directory_path):
            sum += self.__get_filesize(f"{directory_path}/{file}")
        return sum
