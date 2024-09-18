from enum import Enum
from typing import Tuple
import re

class FruitQuality(Enum):
    EXTRA_CLASS = "Extra Class".lower()
    CLASS_I = "Class I".lower()
    CLASS_II = "Class II".lower()
    CLASS_III = "Class III".lower()
    BELOW_STANDARD = "Below Standard".lower()

class FruitQualityAgent:
    def __init__(self):
        self.quality_map = {
            FruitQuality.EXTRA_CLASS: (0, "7-10 days"),
            FruitQuality.CLASS_I: (10, "5-7 days"),
            FruitQuality.CLASS_II: (20, "3-5 days"),
            FruitQuality.CLASS_III: (30, "1-2 days"),
            FruitQuality.BELOW_STANDARD: (None, "Reject")
        }

    def process_fruit_quality(self, quality: str) -> Tuple[int, str, str]:
        try:
            fruit_quality = FruitQuality(quality)
        except ValueError:
            return None, "Invalid input", "Please provide a valid fruit quality"

        discount, shelf_life = self.quality_map[fruit_quality]

        if fruit_quality == FruitQuality.BELOW_STANDARD:
            return None, "Reject", "Fruit is below standard and should be discarded"

        recommendation = self._generate_recommendation(fruit_quality, discount, shelf_life)
        return discount, shelf_life, recommendation

    def _generate_recommendation(self, quality: FruitQuality, discount: int, shelf_life: str) -> str:
        if quality == FruitQuality.EXTRA_CLASS:
            return f"Premium quality fruit. No discount needed. Display prominently. Shelf life: {shelf_life}"
        elif quality == FruitQuality.CLASS_I:
            return f"Good quality fruit. Apply {discount}% discount. Regular display. Shelf life: {shelf_life}"
        elif quality == FruitQuality.CLASS_II:
            return f"Standard quality fruit. Apply {discount}% discount. Consider for quick sale promotions. Shelf life: {shelf_life}"
        elif quality == FruitQuality.CLASS_III:
            return f"Lower quality fruit. Apply {discount}% discount. Use for immediate sale or processing. Shelf life: {shelf_life}"

def fix_json(json_str):
    # Remove any trailing commas
    json_str = re.sub(r',\s*}', '}', json_str)
    json_str = re.sub(r',\s*]', ']', json_str)
    
    # Attempt to fix unescaped quotes within strings
    json_str = re.sub(r'(?<!\\)"(?=(?:(?<!\\)(?:\\\\)*")*(?<!\\)(?:\\\\)*$)', r'\"', json_str)
    
    # Remove any non-printable characters
    json_str = ''.join(char for char in json_str if ord(char) > 31 or ord(char) == 9)
    json_str = json_str.replace('```', '').replace('\\', '')
    return json_str
