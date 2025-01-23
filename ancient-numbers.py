class EgyptianNumber:
    """
    Implementation of Egyptian number system using hieroglyphic principles
    
    Egyptian numerals were additive, using different symbols for powers of 10:
    1 = | (single stroke)
    10 = ∩ (heel bone)
    100 = ⚪ (coiled rope)
    1000 = 𓂀 (lotus flower)
    10000 = ☝ (pointing finger)
    100000 = 𓆐 (tadpole)
    1000000 = 🙏 (astonished man)
    """
    
    SYMBOLS = {
        1000000: "🙏",
        100000: "𓆐",
        10000: "☝",
        1000: "𓂀",
        100: "⚪",
        10: "∩",
        1: "|"
    }
    
    def __init__(self, number):
        self.number = number
        self.egyptian = self.to_egyptian()
    
    def to_egyptian(self):
        """Convert decimal number to Egyptian representation"""
        if not isinstance(self.number, int) or self.number < 1:
            raise ValueError("Egyptian numbers must be positive integers")
            
        result = []
        remaining = self.number
        
        for value, symbol in sorted(self.SYMBOLS.items(), reverse=True):
            while remaining >= value:
                result.append(symbol)
                remaining -= value
                
        return " ".join(result)
    
    def __str__(self):
        return f"{self.number} in Egyptian numerals: {self.egyptian}"


class BabylonianNumber:
    """
    Implementation of Babylonian sexagesimal (base-60) number system
    
    Babylonians used a positional system with base 60, using wedge (𐎝) and 
    corner (𐎜) symbols in cuneiform writing. Numbers 1-59 were written using
    a combination of symbols for 1 (𐎝) and 10 (𐎜).
    """
    
    def __init__(self, decimal_num):
        self.decimal = decimal_num
        self.sexagesimal = self.to_sexagesimal()
    
    def to_sexagesimal(self):
        """Convert decimal number to sexagesimal representation"""
        if self.decimal < 0:
            raise ValueError("Babylonian numbers must be positive")
            
        quotient = self.decimal
        remainders = []
        
        while quotient > 0:
            quotient, remainder = divmod(quotient, 60)
            remainders.append(remainder)
            
        return remainders[::-1]
    
    def format_sexagesimal(self):
        """Format number in Babylonian style using Unicode wedge and corner symbols"""
        result = []
        
        for value in self.sexagesimal:
            tens, ones = divmod(value, 10)
            number = "𐎜" * tens + "𐎝" * ones
            result.append(number if number else "0")
            
        return ";".join(result)
    
    def __str__(self):
        return f"{self.decimal} in Babylonian sexagesimal: {self.format_sexagesimal()}"


def demonstrate_number_systems():
    """Demonstrate both number systems with examples"""
    # Egyptian examples
    print("Egyptian Number System Examples:")
    egyptian_numbers = [1, 123, 3642]
    for num in egyptian_numbers:
        print(EgyptianNumber(num))
    
    print("\nBabylonian Number System Examples:")
    babylonian_numbers = [60, 121, 3600]
    for num in babylonian_numbers:
        print(BabylonianNumber(num))

if __name__ == "__main__":
    demonstrate_number_systems()
