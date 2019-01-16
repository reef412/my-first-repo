import boto3

# Retrive list of Service Codes for case category
def createResponse():
    response = client.describe_services(
        serviceCodeList=[
        ],
        language='en'
    )
    return response

# Function to loop for 'customer-account' service code
def getServiceCodes(response, serviceName, codeName):
    for serviceCode in response['services']:
        if serviceCode['code'] == serviceName:
            for categories in serviceCode['categories']:
                if categories['name'] == codeName:
                    return categories['code']

# Function to create new support case
def createCase(client, service_name, severity_code, service_code):
    resp = client.create_case(
        # Subject should be "Please Enroll to Enterprise Support"
        subject='TEST CASE--Please ignore',
        serviceCode=service_name,
        severityCode=severity_code,
        categoryCode=service_code,
        communicationBody="'Hello, I've created new linked account(s) and would like to have Enterprise support enabled. The account(s) IDs are: xxxxxxxxxxxx \
        Thank you.'"
    )

if __name__ == "__main__":
    # Create AWS Support client
    client = boto3.client('support')
    serviceName = 'customer-account'
    codeName = 'Other Account Issues'
    response = createResponse()
    serviceCode = getServiceCodes(response, serviceName, codeName)
    # Severity Level codes: 
    # 'low' - General guidance
    # 'normal' - System impaired
    # 'high' - Production system impaired
    # 'urgent' - Production system down
    createCase(client, serviceName, 'low', serviceCode)