import uuid


class TrackingIdGenerator:
    '''
    Class to Generate Tracking Id for Azure Resource Management Automation
    '''
    def __init__(self, ):
        self.uuid =  uuid.uuid4()

    def trackingId(self, ):
        return str(self.uuid)