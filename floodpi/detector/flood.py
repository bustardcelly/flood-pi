
class FloodDetector:

  def __init__(self, range_dict):
    self.range = range_dict

  def detect(self, level):
    return level <= self.range['minimum'] and level >= self.range['maximum']
