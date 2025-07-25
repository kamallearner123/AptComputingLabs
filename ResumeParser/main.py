import logging
import os
import logging
logging.basicConfig(level=logging.INFO)

from bws_extract import parse_resume

# Constants
RESUMES_DIR = "Resumes"


# Main function to parse resumes
if __name__=="__main__":
    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
    RESUMES_PATH = os.path.join(CURRENT_PATH, RESUMES_DIR)
    if not os.path.exists(RESUMES_PATH):
        os.makedirs(RESUMES_PATH)
        logging.info(f"Resumes directory created at: {RESUMES_PATH}")
        logging.info("Please add resumes to the 'Resumes' directory.")
        exit(-1)
    else:
        # Open csv file to write results Candidates.csv with headers Name, Address, Skills
        logging.info("Resumes directory already exists.")
        logging.info("Parsing resumes in the 'Resumes' directory.")

        CsvFilePath = os.path.join(RESUMES_PATH, "Candidates.csv")
        if not os.path.exists(CsvFilePath):
            csv_file = open(CsvFilePath, 'w')   
            csv_file.write("Name,Address,Skills\n")
            logging.info(f"CSV file created at: {CsvFilePath}")
        else:
            logging.info(f"CSV file already exists at: {CsvFilePath}")
            csv_file = open(CsvFilePath, 'a')

        
        logging.info(f"Resumes directory found at: {RESUMES_PATH}")
        for filename in os.listdir(RESUMES_PATH):
            if filename.endswith(".pdf") or filename.endswith(".docx") or filename.endswith(".doc"):
                resume_path = os.path.join(RESUMES_PATH, filename)
                if not os.path.exists(resume_path):
                    logging.error(f"Resume file not found: {resume_path}")
                    continue

                if filename.endswith(".pdf"):
                    logging.info(f"Parsing PDF resume: {filename}")
                    result = parse_resume(resume_path, use_docling_for_pdf=True)
                else:
                    result = parse_resume(resume_path, use_docling_for_pdf=False)

                print("Extracted Resume Details:")
                print(f"Name: {result.get('name', 'Not found')}")
                print(f"Address: {result.get('address', 'Not found')}")
                print(f"Skills: {result.get('skills', 'Not found')}")

                # Write results to CSV file
                csv_file.write(f"{result.get('name', 'Not found')},{result.get('address', 'Not found')},{'; '.join(result.get('skills', []))}\n")
                logging.info(f"Results written to CSV file: {CsvFilePath}")


    


