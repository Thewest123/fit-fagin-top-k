class Mouse:
    def __init__(self) -> None:
        self.name = None
        self.weight = None
        self.accuracy = None
        self.dpi = None
        self.price = None

        self.name_normalized = None
        self.weight_normalized = None
        self.accuracy_normalized = None
        self.dpi_normalized = None
        self.price_normalized = None

    def assign(self, name, weight, accuracy, dpi, price) -> None:
        self.name = name
        self.weight = weight
        self.accuracy = accuracy
        self.dpi = dpi
        self.price = price

    def assign_normalized(self, name, weight, accuracy, dpi, price) -> None:
        self.name_normalized = name
        self.weight_normalized = weight
        self.accuracy_normalized = accuracy
        self.dpi_normalized = dpi
        self.price_normalized = price

    def __repr__(self) -> str:
        return f"{self.name} | {self.weight:.1f}g | {self.accuracy:.0%} | {self.dpi:.0f} DPI | ${self.price}"

    def __hash__(self) -> int:
        return hash((self.name, self.weight, self.accuracy, self.dpi, self.price))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Mouse):
            return False

        return (
            self.name == other.name
            and self.weight == other.weight
            and self.accuracy == other.accuracy
            and self.dpi == other.dpi
            and self.price == other.price
        )

    def as_list(self) -> list:
        return [self.name, self.weight, self.accuracy, self.dpi, self.price]

    def as_list_normalized(self) -> list:
        return [
            self.name_normalized,
            self.weight_normalized,
            self.accuracy_normalized,
            self.dpi_normalized,
            self.price_normalized,
        ]

    def fields_count(self) -> int:
        return len(self.as_list())
