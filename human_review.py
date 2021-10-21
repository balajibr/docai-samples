# Manually trigger the human review of any document.

# Fill in the PROJECT_ID,  PROCESSOR_ID, FILE_NAME based on the created processor.

project_id= 'PROJECT_ID' 
location = 'us' # Format is 'us' or 'eu'
processor_id = 'PROCESSOR_ID' # Create processor in Cloud Console
file_path = 'FILE_NAME.pdf' # The local file in your current working directory
#file_path = '../resources/procurement/invoices/invoice.pdf'

from google.cloud import documentai_v1beta3 as documentai
from google.cloud import storage

def review_document(
    project_id=project_id, location=location, processor_id=processor_id,  file_path=file_path
):

    # Instantiates a client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processor/processor-id/humanReviewConfig
    # You must create new processors in the Cloud Console first
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}/humanReviewConfig"

    with open(file_path, "rb") as image:
        image_content = image.read()
    
    # Read the file into memory
    document = {"content": image_content, "mime_type": "application/pdf"}

    # Configure the human review (HITL) request
    request = {"human_review_config": name, "document": document}

    # Use the Document AI client to process the sample form
    result = client.review_document(request=request, )

    print(result.operation)
    return result



def get_operation(lro):
    client = documentai.DocumentProcessorServiceClient()
    operation = client._transport.operations_client.get_operation(lro)
    if operation.done:
        print("HITL location: {} ".format(str(operation.response.value)[5:-1]))
    else:
        print('Waiting on human review.')

# Pass the operation name got from the previous call 
#get_operation("projects/xxxxxxxx/locations/us/operations/yyyyyyyyyyy")


result = review_document()

# Check the current state of the operation
get_operation(result.operation.name)