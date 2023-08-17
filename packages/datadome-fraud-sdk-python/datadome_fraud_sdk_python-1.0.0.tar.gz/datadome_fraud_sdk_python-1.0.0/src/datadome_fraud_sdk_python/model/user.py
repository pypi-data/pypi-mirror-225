from datetime import datetime, timezone
from .address import Address
from enum import Enum


class Title(Enum):
    """ Title
    
    Values:
        EMPTY
        MR
        MRS
        MX
    """
    EMPTY = ""
    MR = "Mr"
    MRS = "Mrs"
    MX = "Mx"
class User:
    """ User information
    to be sent inside the user object
    to the DataDome Fraud API
    
    Attributes:
        id: A unique customer identifier from your system.
        title: Title of the user
        firstName: First name of the user
        lastName: Last name of the user
        createdAt: Creation date of the user, Format ISO 8601 YYYY-MM-DDThh:mm:ssTZD
        email: Email of the user
        address: Address of the user
    """
    def __init__(
        self, id, title=Title.EMPTY, firstName="", lastName="",
        createdAt=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),  # noqa: E501
        phone="",
        email="", address=Address()
    ):
        self.id = id
        self.title = title.value
        self.firstName = firstName
        self.lastName = lastName
        self.createdAt = createdAt
        self.phone = phone
        self.email = email
        self.address = address
        
    def __str__(self):
        return ("User: id=" + self.id
                + "\n title=" + self.title
                + "\n firstName=" + self.firstName  
                + "\n lastName=" + self.lastName
                + "\n createdAt=" + self.createdAt 
                + "\n phone=" + self.phone 
                + "\n email=" + self.email
                + "\n address=" + str(self.address))
        
    
class UserSession:
    """ Session information
    to be sent inside the session object
    to the DataDome Fraud API
    
    Attributes:
        id: A unique session identifier from your system
        createdAt: Creation date of the user, Format ISO 8601 YYYY-MM-DDThh:mm:ssTZD
    """
    def __init__(
        self, id="", 
        createdAt=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),  # noqa: E501

    ):
        self.id = id
        self.createdAt = createdAt
        
    def __str__(self):
        return ("UserSession: id=" + self.id 
                + "\n createdAt=" + self.createdAt)