from dataclasses import dataclass


@dataclass
class KeyTiming:
    max_keystroke_time: float = 0.7
    keystroke_time_scale: float = 0.32
    time_to_think: float = 1
    time_at_end: float = 5
    time_to_read_one_char: float = 0.005

    def filter(self, times):
        for t in times:
            t *= self.keystroke_time_scale
            if t <= self.max_keystroke_time:
                yield t

    def read_text(self, chars):
        return self.time_to_think + chars * self.time_to_read_one_char
