
class FloodDetector:

  def __init__(self, range_min, range_max):
    self.minimum = range_min
    self.maximum = range_max

  def detect(self, level):
    return level <= self.minimum and level >= self.maximum
