from datetime import datetime

class MediaData:
    mediaData_id = -1

    def __init__(self):
        self.Type: str = ""            
        if MediaData.mediaData_id == -1:
            MediaData.mediaData_id = self.__get_media_data_id()
        MediaData.Id = MediaData.mediaData_id + 1
        self.Id: int = MediaData.mediaData_id
        self.ZoneId: str = ""
        self.CameraId: str = ""
        self.MotTrackerId: int = None
        self.EdgeFilename: str = ""
        self.MotEdgeFilename: str = ""
        self.MIMEType: str = ""
        self.AltText: str = ""
        self.RawData: str  = ""  # Base64 encoded binary data
        self.DetectedStart_tm: float = 0
        self.DetectedEnd_tm: float = 0

    def __get_media_data_id(self) -> int:
        utcnow = datetime.utcnow()
        beginning_of_year = datetime(utcnow.year, 1, 1)
        time_difference = utcnow - beginning_of_year
        return int(time_difference.total_seconds()*10)