class ExtendUtil():
    @staticmethod
    def replace(raw: str, key_value_pairs: dict[str, str]):
        text: str = raw
        for i in key_value_pairs:
            text = text.replace(i, key_value_pairs[i])        
        return text