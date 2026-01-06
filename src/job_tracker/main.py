import os

from dotenv import load_dotenv

from job_tracker.utils import FileUtils
from job_tracker.core import JobNormalizer
from job_tracker.services import GeminiClient

def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL")

    file_utils = FileUtils()
    client = GeminiClient(api_key=api_key, model=model)
    job_normalizer = JobNormalizer(client=client)

    file_name = input("Write name for the file :")
    txt_path = file_utils.open_temp_file_for_editing(file_name)

    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()

    json_data = job_normalizer.normalize(content)

    json_file_name = f"{json_data.job.title}_{json_data.company.name}"

    file_utils.save_job_document(doc=json_data, file_name=json_file_name )

if __name__ == "__main__":
    main()