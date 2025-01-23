class RomanNumeral:
    """
    Implementation of Roman numeral system
    Shows both classical and subtractive notation
    """
    ROMAN_NUMS = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]
    
    def __init__(self, number):
        self.number = number
        self.roman = self.to_roman()
        self.classical = self.to_classical_roman()
    
    def to_roman(self):
        """Convert to Roman numerals using subtractive notation"""
        if not isinstance(self.number, int) or self.number < 1:
            raise ValueError("Roman numbers must be positive integers")
            
        result = ""
        num = self.number
        
        for value, symbol in self.ROMAN_NUMS:
            while num >= value:
                result += symbol
                num -= value
                
        return result
    
    def to_classical_roman(self):
        """Convert to classical Roman numerals (no subtractive notation)"""
        classical_map = [(1000, "M"), (500, "D"), (100, "C"),
                        (50, "L"), (10, "X"), (5, "V"), (1, "I")]
        
        num = self.number
        result = ""
        
        for value, symbol in classical_map:
            count = num // value
            result += symbol * count
            num %= value
            
        return result


class MayanNumeral:
    """
    Implementation of Mayan vigesimal (base-20) number system
    Includes dot and bar notation
    """
    def __init__(self, number):
        self.number = number
        self.vigesimal = self.to_vigesimal()
    
    def to_vigesimal(self):
        """Convert decimal to Mayan vigesimal representation"""
        if self.number < 0:
            raise ValueError("Mayan numbers must be positive")
            
        digits = []
        num = self.number
        
        while num > 0:
            digits.append(num % 20)
            num //= 20
            
        return digits[::-1] if digits else [0]
    
    def format_mayan(self):
        """Format number in Mayan style using dots (.) and bars (-)"""
        result = []
        
        for digit in self.vigesimal:
            bars = digit // 5
            dots = digit % 5
            level = "-" * bars + "." * dots
            result.append(level if level else "0")
            
        return " | ".join(result)
    
    def __str__(self):
        return f"{self.number} in Mayan: {self.format_mayan()}"


class ChineseNumeral:
    """
    Implementation of traditional Chinese counting rod numerals
    Demonstrates place value system with vertical and horizontal rod placement
    """
    CHINESE_DIGITS = {
        0: "零", 1: "一", 2: "二", 3: "三", 4: "四",
        5: "五", 6: "六", 7: "七", 8: "八", 9: "九"
    }
    
    PLACES = {
        0: "", 1: "十", 2: "百", 3: "千", 4: "万"
    }
    
    def __init__(self, number):
        self.number = number
        self.chinese = self.to_chinese()
    
    def to_chinese(self):
        """Convert number to traditional Chinese numerals"""
        if not isinstance(self.number, int) or self.number < 0:
            raise ValueError("Number must be a positive integer")
            
        if self.number == 0:
            return self.CHINESE_DIGITS[0]
            
        num = str(self.number)
        length = len(num)
        result = ""
        
        for i, digit in enumerate(num):
            value = int(digit)
            if value != 0:
                result += self.CHINESE_DIGITS[value]
                if length - i - 1 > 0:
                    result += self.PLACES[length - i - 1]
            elif result and result[-1] != self.CHINESE_DIGITS[0]:
                result += self.CHINESE_DIGITS[0]
                
        return result

def demonstrate_number_systems():
    """Demonstrate various ancient number systems"""
    test_numbers = [1994, 2024, 3888]
    
    for num in test_numbers:
        print(f"\nRepresenting {num} in different number systems:")
        print("-" * 50)
        
        # Roman
        roman = RomanNumeral(num)
        print(f"Roman (subtractive): {roman.roman}")
        print(f"Roman (classical):   {roman.classical}")
        
        # Mayan
        mayan = MayanNumeral(num)
        print(f"Mayan: {mayan}")
        
        # Chinese
        chinese = ChineseNumeral(num)
        print(f"Chinese: {chinese.chinese}")

if __name__ == "__main__":
    demonstrate_number_systems()
