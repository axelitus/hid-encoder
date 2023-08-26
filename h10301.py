class H10301:
    """
    Creates an HID card type H10301 that uses the Wiegand protocol (https://en.wikipedia.org/wiki/Wiegand_interface).
    """

    DATA_LENGTH: int = 6
    FACILITY_MIN_VALUE: int = 0
    FACILITY_MAX_VALUE: int = 255
    FACILITY_BITS: int = 8
    CARD_MIN_VALUE: int = 0
    CARD_MAX_VALUE: int = 65535
    CARD_BITS: int = 16
    BIT_COUNT_FOR_PARITY = 12

    def __init__(self, facility: int, card: int):
        assert(self.__validate_facility(facility))
        assert(self.__validate_card(card))

        self.facility = facility
        self.card = card

    def data(self) -> int:
        return (self.facility << self.CARD_BITS) + self.card

    def bin(self) -> str:
        return bin(self.data())[2:]

    def bits(self) -> list[int]:
        return [int(bit) for bit in self.bin()]

    def hex(self) -> str:
        return hex(self.data())[2:].zfill(self.DATA_LENGTH)

    def hex_flipper(self) -> str:
        chunks = [self.hex().upper()[i:i+2] for i in range(0, self.DATA_LENGTH, 2)]
        return ' '.join(chunks)

    def parity_even(self):
        return self.__parity(self.bits()[:self.BIT_COUNT_FOR_PARITY + 1], False)

    def parity_odd(self):
        return self.__parity(self.bits()[self.BIT_COUNT_FOR_PARITY:], True)

    def flipper(self):
        return """Filetype: Flipper RFID key
Version: 1
Key type: H10301
Data: %s
""" % (self.hex_flipper())

    def __validate_facility(self, data: int) -> bool:
        if data < self.FACILITY_MIN_VALUE or data > self.FACILITY_MAX_VALUE:
            return False
        return True

    def __validate_card(self, data: int) -> bool:
        if data < self.CARD_MIN_VALUE or data > self.CARD_MAX_VALUE:
            return False
        return True

    @staticmethod
    def __parity(data: list[int], odd: bool):
        return ((sum(data) % 2) + odd) % 2

