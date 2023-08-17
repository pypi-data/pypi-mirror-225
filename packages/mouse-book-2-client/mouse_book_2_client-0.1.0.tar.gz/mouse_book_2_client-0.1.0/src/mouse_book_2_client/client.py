import requests

from . import schemas


RECORDS_SEGMENT = '/items'


class Client:

    def __init__(self, api_base: str, api_key: str):
        self.api_base = api_base
        self.api_key = api_key
        self.session = requests.Session()

    def get(self, id: str):
        # return self.session.get(
        #     self.api_base + path,
        #     params=params,
        #     headers={'Authorization': f'Bearer {self.api_key}'})
        return self.session.get(
            self.api_base + RECORDS_SEGMENT + f"/{id}",
        )
    
    def paginated_get(self, exclusive_start_key: str = None):
        params = {}
        if exclusive_start_key:
            params['exclusiveStartKey'] = exclusive_start_key
        # response = self.session.get(
        #     self.api_base + RECORDS_SEGMENT, 
        #     params,
        # )
        for _ in range(10):  # max page requests, hardcoded for dev
            response = self.session.get(
                self.api_base + RECORDS_SEGMENT, 
                json=params,
            )
            data = response.json()
            yield data['items']
            if not 'nextExclusiveStartKey' in data:
                break
            
            params['exclusiveStartKey'] = data['nextExclusiveStartKey']


    def post(self, data: dict = None):
        item = schemas.MouseRecord(**data)
        # return self.session.post(
        #     self.api_base + path,
        #     json=item.dict(),
        #     headers={'Authorization': f'Bearer {self.api_key}'})
        return self.session.post(
            self.api_base + RECORDS_SEGMENT,
            json=item.dict(),
        )
    
    def update(self, id: str, data: dict = None):
        return self.session.put(
            self.api_base + RECORDS_SEGMENT + f"/{id}",
            json=data,
        )

    def delete(self, id: str):
        return self.session.delete(
            self.api_base + RECORDS_SEGMENT + f"/{id}",
        )
