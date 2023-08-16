class IoPoint:
    def __init__(self,
                 value: float = None,
                 value_str: str = None,
                 quality_code: int = None,
                 timestamp: float = None):
        """
        Args:
            value (int, optional): Value of the IoPoint.
            quality_code (int, optional): 0 if good quality,1 if bad quality.
            timestamp (_type_, optional): AgoraTimeStamp
            value_str (str, optional): Supports sending non numeric value. Defaults to "".
        """
        self.value: float = value
        self.quality_code: int = quality_code
        self.timestamp: float = timestamp
        self.value_str: str = value_str
