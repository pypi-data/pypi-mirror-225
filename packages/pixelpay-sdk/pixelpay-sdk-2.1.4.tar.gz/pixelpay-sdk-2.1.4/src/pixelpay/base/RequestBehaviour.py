import locale
from nacl.public import PrivateKey
from .Helpers import Helpers
from .. import __version__


class RequestBehaviour:
    def __init__(self):
        """Initialize request"""
        [rfc1766, _] = locale.getdefaultlocale()
        lang = None
        if rfc1766:
            lang = rfc1766.split("_")[0]

        if lang != "es" or lang != "en":
            lang = "es"

        self.env: str = None
        """Environment identifier (live|test|sandbox)"""

        self.lang: str = lang
        """Transaction response messages language"""

        self.from_type: str = "sdk-python"
        """SDK identifier type"""

        self.sdk_version: str = __version__
        """SDK version"""

        self._sdk_key_pair: PrivateKey = None
        """For internal use to prevent encrypting same request instance twice"""

    def isEncryptable(self) -> bool:
        """Check if current request needs encryption, must be overriden by inherited classes.

        Returns:
            bool: true if request contains parameters that must be encrypted
        """
        return False

    def withEncryption(self, public_key: str) -> str:
        """Encrypt fields with sensitive data, must be overriden by inherited classes.

        Args:
            public_key (str): merchant public key

        Returns:
            None: this base method always returns None
        """
        return None

    def toJson(self) -> str:
        """Serialize object to JSON string

        Returns:
            str: JSON string
        """

        # because "from" is a reserved keyword,
        # we temporarily change the attribute "from_type" to "from"
        if self.from_type:
            setattr(self, "from", self.from_type)
            delattr(self, "from_type")

        json_output = Helpers.objectToJson(self, ignore=['_sdk_key_pair'])

        # restore the previous changes
        from_attr = getattr(self, "from")
        if from_attr:
            setattr(self, "from_type", from_attr)
            delattr(self, "from")

        return json_output
