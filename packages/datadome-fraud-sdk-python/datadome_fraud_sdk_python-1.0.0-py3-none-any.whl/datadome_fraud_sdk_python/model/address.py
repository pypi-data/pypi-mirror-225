class Address:
    """ Address of the user
    
    Attributes:
        name: Name of the address
        line1: line 1
        line2: line 2
        city: City
        countryCode: Country code, Format ISO-3166-1-alpha-2
        regionCode: Region code
        zipCode: Zip code
    """
    def __init__(
        self, name ="", line1="", line2="",
        city="", countrycode="", country="",
        regioncode="", zipcode=""
    ):
        self.name = name
        self.line1 = line1
        self.line2 = line2
        self.city = city
        self.countrycode = countrycode
        self.country = country
        self.regioncode = regioncode
        self.zipcode = zipcode
        
    def __str__(self):
        return ("Address: name=" + self.name 
                + "\n line1=" + self.line1  
                + "\n line2=" + self.line2
                + "\n city=" + self.city 
                + "\n countrycode=" + self.countrycode 
                + "\n country=" + self.country
                + "\n regioncode=" + self.regioncode 
                + "\n zipcode=" + self.zipcode)
    
