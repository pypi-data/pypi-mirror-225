from dataclasses import dataclass

@dataclass
class MCT:
    id: int = -1



@dataclass
class Observation(MCT):
    msg_id: str = ""
    sei: bool = False
    serco: bool = False
    white: bool = False
    msg_type: str = ""
    time: int = 0
    date_time: str = ""
    cot_msg: str = ""
    audience: float = 0.0
    observation: float = 0.0
    response: float = 0.0
    question: float = 0.0
    status: float = 0.0
    completion_brief: float = 0.0
    posrep: float = 0.0
    spotrep: float = 0.0
    ticrep: float = 0.0
    backbrief: float = 0.0
    input_text: float = 0.0
    output_text: str = ""
    entity_type: float = 0.0
    callsign: float = 0.0
    latitude: float = 0.0
    longitude: float = 0.0
    chatroom: float = 0.0
    chat_id: float = 0.0
    message_id: float = 0.0
    detection_type: str = ""
    bearing: str = ""
    alert_rate: float = 0.0
    amp_rms: float = 0.0


@dataclass
class Person(MCT):
    height_cm: int = 59
    weight_kg: int = 430
    ssn: str = "ssnnotstr"


@dataclass
class Noise(MCT):
    funding: int = None
    velocity: int = None
