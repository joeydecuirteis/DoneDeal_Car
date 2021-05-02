import logging


class DoneDealAd(object):

    def __init__(self, ad: dict):
        self.raw_ad = ad
        self.ID = self.get_id()
        self.price = self.get_price()
        self.dealerType = self.get_dealer_type()
        # These attr names need to be equal to the json tags in the ads
        self.make = None
        self.model = None
        self.mileage = None
        self.year = None
        self.fuelType = None
        self.bodyType = None
        self.engine = None

        # Set instance attrs from displayAttributes
        self.parse_attributes()

    def get_id(self):
        """
        Get ID tag from the ad, should be unique per ad
        :return:
        """
        ID = self.raw_ad.get("id")
        return ID

    def get_price(self):
        """
        Get price tag from the ad, also check currency tag is EUR
        :return:
        """
        price = self.raw_ad.get("price")
        currency = self.raw_ad.get("currency")
        if currency != "EUR":
            logging.error("Unexpected currency found")
        return price


    def get_dealer_type(self):
        """
        Return the dealer type. We prob only want SIMI
        :return:
        """
        dealer_type = self.raw_ad.get("dealer").get("type")
        return dealer_type

    def parse_attributes(self):
        """
        Parse displayAttributes and set instance attrs
        :return:
        """
        # list of dicts
        attrs = self.raw_ad.get("displayAttributes", None)
        if attrs is None:
            print(f"Not able to parse, don't think this is a motor ad: \n{self.raw_ad}")
            return None
        for attr_dict in attrs:
            name = attr_dict.get("name")
            if name in self.__dict__.keys():
                value = attr_dict.get("value")
                logging.debug(f"Setting {value} for {name}")
                self.__dict__[name] = value






