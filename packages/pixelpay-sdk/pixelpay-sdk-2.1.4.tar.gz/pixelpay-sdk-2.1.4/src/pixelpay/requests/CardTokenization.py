from nacl.encoding import Base64Encoder
from ..base.Helpers import Helpers
from ..base.RequestBehaviour import RequestBehaviour
from ..models.Billing import Billing
from ..models.Card import Card
from ..exceptions import FailedEncryptionException


class CardTokenization(RequestBehaviour):
    def __init__(self):
        super().__init__()

        self.number: str = None
        """Card number or PAN"""

        self.cvv2: str = None
        """Card security code"""

        self.expire_month: str = None
        """Card expire month date (MM)"""

        self.expire_year: str = None
        """Card expire year date (YYYY)"""

        self.customer: str = None
        """Tokenized customer identifier (C-* format)"""

        self.cardholder: str = None
        """Cardholder name"""

        self.address: str = None
        """Customer billing address"""

        self.country: str = None
        """Customer billing country alpha-2 code (ISO 3166-1)"""

        self.state: str = None
        """Customer billing state alpha code (ISO 3166-2)"""

        self.city: str = None
        """Customer billing city"""

        self.zip: str = None
        """Customer billing postal code"""

        self.phone: str = None
        """Customer billing phone"""

        self.email: str = None
        """Customer email"""

    def setCard(self, card: Card):
        """Associate and mapping Card model properties to transaction

        Args:
            card (Card): input Card
        """
        self.number = Helpers.cleanString(card.number)
        self.cvv2 = card.cvv2
        self.cardholder = Helpers.trimValue(card.cardholder)

        if card.expire_month != 0:
            self.expire_month = "{:02d}".format(card.expire_month)

        if card.expire_year != 0:
            self.expire_year = str(card.expire_year)

    def setBilling(self, billing: Billing):
        self.address = Helpers.trimValue(billing.address)
        self.country = billing.country
        self.state = billing.state
        self.city = Helpers.trimValue(billing.city)
        self.zip = billing.zip
        self.phone = billing.phone

    def setCustomerToken(self, customer: str):
        """Setup customer token

        Args:
            customer (str): Tokenized customer identifier (C-* format)
        """
        self.customer = customer

    def isEncryptable(self) -> bool:
        """Check if current request needs encryption.

        Returns:
            bool: true if request contains parameters that must be encrypted
        """
        return self.number or self.cvv2 or self.expire_month or self.expire_year

    def withEncryption(self, public_key: str) -> str:
        """Encrypt fields with sensitive data.

        Args:
            public_key (str): merchant public key

        Raises:
            FailedEncryptionException: When public key is empty or encryption fails

        Returns:
            str: SDK public key
        """
        if not public_key:
            raise FailedEncryptionException("Could not process transaction without merchant public key.")

        try:
            key_pair = Helpers.getKeyPair() if not self._sdk_key_pair else self._sdk_key_pair

            number = Helpers.encrypt(self.number, public_key, key_pair)
            cvv2 = Helpers.encrypt(self.cvv2, public_key, key_pair)
            expire_month = Helpers.encrypt(self.expire_month, public_key, key_pair)
            expire_year = Helpers.encrypt(self.expire_year, public_key, key_pair)

            sdk_public_key = key_pair.public_key.encode(encoder=Base64Encoder).decode()

            self.number = number
            self.cvv2 = cvv2
            self.expire_month = expire_month
            self.expire_year = expire_year

            self._sdk_key_pair = key_pair

            return sdk_public_key
        except:
            raise FailedEncryptionException("Encryption process encountered an unexpected error.")
