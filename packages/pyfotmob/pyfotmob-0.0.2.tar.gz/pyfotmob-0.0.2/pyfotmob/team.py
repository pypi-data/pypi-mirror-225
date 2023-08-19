import requests

from models.team import TeamModel


class Team:
    BASE_URL = "https://www.fotmob.com/api"

    def __init__(self, id_team: int):
        self.id = id_team

    def get(self) -> dict:
        response = requests.get(f"{Team.BASE_URL}/teams?id={self.id}").json()

        # if attr is not None:
        #     return response.get(attr)
        #
        # else:
        #     return TeamModel(**response)

        if response:
            return response
            # if field:
            #     try:
            #         return response[field]
            #     except KeyError:
            #         return {
            #             "details": "no field found"
            #         }
            # else:
            #     return response
        else:
            return {
                "details": "no team found"
            }
