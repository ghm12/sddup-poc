from xml_handler import XMLHandler

import hashlib
import shutil
import os

class SDDup:
    def __init__(self):
        self.xml_handler = XMLHandler()

        self.outputs_path = "./sddup/outputs"

        self.xml_template_path = "./sddup/templates/diploma_template.xml"
        self.xml_generated_xml_path = "./sddup/outputs/xml/generated_xmls"
        self.xml_extracted_data_path = "./sddup/outputs/xml/extracted_data"
        self.xml_recreated_xml_path = "./sddup/outputs/xml/recreated_xmls"

    def run_experiment(self, amount: int = 100):
        print("Cleaning previous experiment (if any)...")
        self.__clean_previous_experiment()
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
        if not self.__check_hash_from_recreated_files(amount):
            print("Hash checking failed, one of the hash values does not match.")
            return
        print("Done. All hashes are OK.")
        
        print("Calculating R and E values...")
        r_value = self.__calculate_R(amount)
        e_value = self.__calculate_E(r_value)
        print(f"R = {r_value:.5%} / E = {e_value:.5%}")

    def __check_hash_from_recreated_files(self, amount = 100):
        for i in range(amount):
            generated_xml = open(f"{self.xml_generated_xml_path}/xml_generated_from_template_{i}.xml", "rb")
            generated_xml_hash = hashlib.file_digest(generated_xml, "sha256").hexdigest()

            recreated_xml = open(f"{self.xml_recreated_xml_path}/xml_recreated_from_data_{i}.xml", "rb")
            recreated_xml_hash = hashlib.file_digest(recreated_xml, "sha256").hexdigest()

            if generated_xml_hash != recreated_xml_hash:
                return False

        return True

    def __clean_previous_experiment(self):
        shutil.rmtree(self.outputs_path)

    def __calculate_R(self, amount: int):
        naive_approach_total_size = self.__get_directory_filesize(self.xml_generated_xml_path)

        template_size = self.__get_filesize(self.xml_template_path)
        sddup_approach_total_size = self.__get_directory_filesize(self.xml_extracted_data_path)

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
