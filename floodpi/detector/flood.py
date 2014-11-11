
class FloodDetector:

  def __init__(self, range):
    self.range

  def detect(self, level):
    return level <= self.range['minimum'] and level >= self.range['maximum']
