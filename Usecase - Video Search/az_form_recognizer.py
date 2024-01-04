# pip install azure-ai-formrecognizer==3.3.0

# import libraries
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

class FormRecognizer:
    def __init__(self, endpoint: str, key: str) -> None:
        """Initialize the Form Recognizer client"""
        self.endpoint = endpoint
        self.key = key

    def format_polygon(self, polygon):
        if not polygon:
            return "N/A"
        return ", ".join(["[{}, {}]".format(p.x, p.y) for p in polygon])

    def analyze_general_documents(self, file_path: str) -> str:
        """Analyze a general document and return the content of the document
        
        Args:
            file_path (str): path to the document to analyze
            
            Returns:
                str: content of the document
        """
        # create your `DocumentAnalysisClient` instance and `AzureKeyCredential` variable
        document_analysis_client = DocumentAnalysisClient(
            endpoint = self.endpoint,
            credential = AzureKeyCredential(self.key)
        )

        with open(file_path, "rb") as file:
            poller = document_analysis_client.begin_analyze_document("prebuilt-document", file)
        
        result = poller.result()

        # get the text content as a markdown format        

        content = ""
        print(f"Total Page Count: {len(result.pages)}\n\n")
        for page in result.pages:
            for line in page.lines:
                content += line.content + "\n"

        for table_idx, table in enumerate(result.tables):
            print(f"Table # {table_idx} has {table.row_count} rows and {table.column_count} columns")

            table_data = []
            for row in range(int(table.row_count)):
                table_data.append([])
                for col in range(int(table.column_count)):
                    table_data[row].append(table.cells[row * table.column_count + col].content)

            transposed_table = list(map(list, zip(*table_data)))
            table_content = ""
            for row in transposed_table:
                for col in row:
                    table_content += "|"
                    table_content += col
                    # table_content += "|"
                table_content += "|\n"
            print(table_content)

        return content


if __name__ == "__main__":
    # Define the Form Recognizer endpoint, key, and the form recognizer client
    endpoint = "https://az4formrecognizer.cognitiveservices.azure.com"
    key = "49c48c7cd8c24d358212d52e495e2231"
    form_recognizer = FormRecognizer(endpoint, key)
    file_path = "Sample.pdf"
    content = form_recognizer.analyze_general_documents(file_path)
    # print(content)
