from docassemble.base.util import CustomDataType, DAObject, get_config, log
import requests

__all__ = ['SpotResult']

api_root = get_config('spot api url', 'https://spot.suffolklitlab.org/v0')

class SpotResult(DAObject):
    @property
    def id(self):
      if self.result is None:
        return None
      if 'id' not in self._full_result['labels'][-1]:
        log('Spot API returned a result but it lacked an id')
        return None
      return self._full_result['labels'][-1]['id']
    @property
    def result(self):
        if hasattr(self, '_active_result') and hasattr(self, '_active_source') and self._active_source == self.source:
            return self._active_result
        if hasattr(self, '_active_result'):
            del self._active_result
        if hasattr(self, '_full_result'):
            del self._full_result
        self._active_source = self.source
        api_key = get_config('spot api key')
        if api_key is None:
            raise Exception("Cannot run Spot api without a 'spot api key' directive in the Configuration.")
        input_data = {
            "text": self._active_source,
            "save-text": 0,
            "cutoff-lower": 0.25,
            "cutoff-pred": 0.5,
            "cutoff-upper": 0.5
        }
        headers = {"Authorization": "Bearer " + api_key, "Content-Type": "application/json", "Accept": "application/json"}
        r = requests.post(api_root + '/entities-nested/', json=input_data, headers=headers)
        success = True
        if r.status_code != 200:
            success = False
            log('Spot API returned non-success status code ' + str(r.status_code) + "\n" + str(r.text))
        if success:
            try:
                self._full_result = r.json()
            except:
                success = False
                log('Spot API did not return valid JSON')
        if success and ('labels' not in self._full_result or len(self._full_result['labels']) == 0):
            success = False
            log('Spot API returned no results')
        if success and 'name' not in self._full_result['labels'][-1]:
            success = False
            log('Spot API returned a result but it lacked a name')
        if success:
            self._active_result = self._full_result['labels'][-1]['name']
        else:
            self._active_result = None
        return self._active_result
    def __str__(self):
        return self.result

class Spot(CustomDataType):
    name = 'spot'
    container_class = 'da-spot-container'
    input_class = 'da-spot'
    is_object = True
    @classmethod
    def transform(cls, item):
        new_item = SpotResult()
        new_item.source = item
        return new_item
    @classmethod
    def default_for(cls, item):
        return item.source