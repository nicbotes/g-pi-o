from threading import Thread, Lock, Event
import time

class ThreadControl:
    def __init__(self):
        self.current_thread = None
        self.lock = Lock()
        self.stop_event = Event()

    def stop_current_thread(self):
        with self.lock:
            if self.current_thread:
                self.stop_event.set()  # Signal the thread to stop
                self.current_thread.join()  # Wait for the thread to finish
                self.stop_event.clear()  # Reset the stop event for future use

    def play_melody(self, speaker, melody_name):
        with self.lock:
            self.stop_current_thread()  # Ensure any running thread is stopped before starting a new one
            self.current_thread = Thread(target=self.melody_worker, args=(speaker, melody_name))
            self.current_thread.start()

    def melody_worker(self, speaker, melody_name):
        notes = speaker.get_melody(melody_name)
        for note, duration in notes:
            if self.stop_event.is_set():
                break  # Exit the loop if stop event is set
            speaker.play_tone(note, duration)
            time.sleep(duration)  # Simulate the duration of the note

    def play_wheel_effect(self, ws2812):
        with self.lock:
            self.stop_current_thread()
            self.current_thread = Thread(target=self.wheel_worker, args=(ws2812,))
            self.current_thread.start()

    def wheel_worker(self, ws2812):
        for i in range(256):
            if self.stop_event.is_set():
                break
            for j in range(ws2812.strip.numPixels()):
                ws2812.strip.setPixelColor(j, ws2812.wheel((i+j) % 255))
            ws2812.strip.show()
            time.sleep(0.01)  # control the speed of the wheel effect
