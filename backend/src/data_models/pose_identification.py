from pydantic import BaseModel


class PoseIdentificationResponse(BaseModel):
    pose_name: str 
    alternate_names: list[str]
    related_poses: list[str]