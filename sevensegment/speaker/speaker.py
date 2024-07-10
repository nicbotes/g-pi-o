import RPi.GPIO as GPIO
import time

class Speaker:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 100)
        self.notes = {
            "C": 523.25,  # C5
            "D": 587.33,  # D5
            "E": 659.25,  # E5
            "F": 698.46,  # F5
            "G": 783.99,  # G5
            "A": 880.00,  # A5
            "B": 987.77,  # B5
            "C6": 1046.50 # C6
        }
        self.melodies = {
            "twinkle_twinkle": [
                ("C", 0.5), ("C", 0.5), ("G", 0.5), ("G", 0.5), ("A", 0.5), ("A", 0.5), ("G", 1.0),
                ("F", 0.5), ("F", 0.5), ("E", 0.5), ("E", 0.5), ("D", 0.5), ("D", 0.5), ("C", 1.0)
            ],
            "frere_jacques": [
                ("C", 0.5), ("D", 0.5), ("E", 0.5), ("C", 0.5),
                ("C", 0.5), ("D", 0.5), ("E", 0.5), ("C", 0.5),
                ("E", 0.5), ("F", 0.5), ("G", 1.0),
                ("E", 0.5), ("F", 0.5), ("G", 1.0),
                ("G", 0.25), ("A", 0.25), ("G", 0.25), ("F", 0.25), ("E", 0.5), ("C", 0.5),
                ("G", 0.25), ("A", 0.25), ("G", 0.25), ("F", 0.25), ("E", 0.5), ("C", 0.5)
            ],
            "rock_a_bye_baby": [
                ("E", 0.5), ("C", 0.5), ("E", 0.5), ("G", 1.0),
                ("G", 0.5), ("E", 0.5), ("G", 1.0),
                ("C6", 1.0), ("G", 0.5), ("E", 0.5), ("C", 1.0),
                ("E", 1.0), ("G", 0.5), ("F", 0.5), ("E", 1.0),
                ("E", 0.5), ("D", 0.5), ("C", 0.5), ("G", 0.5),
                ("C", 0.5), (None, 0.5), ("C", 0.5), ("C", 1.0)
            ],
            "exciting_chime": [
                ("C", 0.25), ("E", 0.25), ("G", 0.25), ("C6", 0.25),
                ("C6", 0.25), ("G", 0.25), ("E", 0.25), ("C", 0.25)  # Quick and vibrant pattern
            ],
            "chime_1": [
                ("C", 0.25), ("E", 0.25), ("G", 0.25), ("C6", 0.25),
                ("E", 0.25), ("G", 0.25), ("C6", 0.25), ("E", 0.25)
            ],
            "chime_2": [
                ("C6", 0.25), ("G", 0.25), ("E", 0.25), ("C", 0.25),
                ("C", 0.25), ("E", 0.25), ("G", 0.25), ("C6", 0.25)
            ],
            "chime_3": [
                ("C", 0.25), ("C6", 0.25), ("G", 0.25), ("C6", 0.25),
                ("E", 0.25), ("G", 0.25), ("C6", 0.25), ("G", 0.25)
            ]
        }

    def play_tone(self, frequency, duration):
        self.pwm.ChangeFrequency(frequency)
        self.pwm.start(50)  # 50% duty cycle to generate a tone
        time.sleep(duration)
        self.pwm.stop()

    def play_melody(self, melody_name):
        if melody_name in self.melodies:
            for note, length in self.melodies[melody_name]:
                if note in self.notes:
                    self.play_tone(self.notes[note], length)
                else:
                    time.sleep(length)  # Pause for notes not defined

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

# Example usage
'''
if __name__ == "__main__":
    speaker = Speaker(12)  # Initialize speaker on GPIO 12
    speaker.play_melody("rock_a_bye_baby")
    speaker.play_melody("frere_jacques")
    speaker.play_melody("twinkle_twinkle")
    speaker.cleanup()
'''
