from datetime import datetime
from agora_utils import AgoraTimeStamp
from agora_config import config
from .media_data import MediaData
from .work_flow import WorkFlow
from typing import List

class EventMsg:
    event_id = -1

    def __init__(self):         
        if EventMsg.event_id == -1:
            EventMsg.event_id = self.__get_event_id()
        EventMsg.event_id = EventMsg.event_id + 1
        self.EventId = EventMsg.event_id        
      
        if config["GROUP_ID"] is None or config["GROUP_ID"] == "":
            self.GroupId = ""
        else:
            self.GroupId = config["GROUP_ID"]

        if config["GATEWAY_ID"] is None or config["GATEWAY_ID"] == "":
            self.GatewayId = ""
        else:
            self.GatewayId = config["GATEWAY_ID"]
        
        self.SlaveId = 999
        
        if config["DEVICE_ID"] is None or config["DEVICE_ID"] == "":
            self.ControllerId = ""
        else:
            self.ControllerId = config["DEVICE_ID"]
        
        self.Start_tm = 0
        self.End_tm = 0
        self.DetectedStart_tm = 0
        self.DetectedEnd_tm = 0
        self.Sent_tm = 0
        self.Created_tm = 0
        self.Detected_tm = 0

        #self.mediaData = MediaData()
        self.mediaDataRef: List[MediaData] = []
        self.workFlow = WorkFlow()
        self.Version = "1.0.27"  #schema version...
        

    def __get_event_id(self):
        utcnow = datetime.utcnow()
        beginning_of_year = datetime(utcnow.year, 1, 1)
        time_difference = utcnow - beginning_of_year
        return int(time_difference.total_seconds()*10)