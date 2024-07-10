from threading import Thread, Lock, Event
import time

class ThreadControl:
    def __init__(self):
        self.current_thread = None
        self.lock = Lock()
        self.stop_event = Event()

    def stop_current_thread(self):
        print('stopping thread.')
        with self.lock:
            if self.current_thread:
                self.stop_event.set()  # Signal the thread to stop
                self.current_thread.join(timeout=1)  # Wait for the thread to finish
                if self.current_thread.is_alive():
                    print("Thread did not stop in time.")
                self.stop_event.clear()  # Reset the stop event for future use

    def play_melody(self, speaker, melody_name):
        print("!!elody_worker")
        with self.lock:
            print("Request to play melody received.")
            self.stop_current_thread()  # Ensure any running thread is stopped before starting a new one
            print("Previous thread stopped, if any.")
            self.current_thread = Thread(target=self.melody_worker, args=(speaker, melody_name))
            self.current_thread.start()
            print("New melody thread started.")

    def melody_worker(self, speaker, melody_name):
        print("Starting melody_worker")
        notes = speaker.get_melody(melody_name)
        for note, duration in notes:
            if self.stop_event.is_set():
                print(" melody_worker")
                break  # Exit the loop if stop event is set
            speaker.play_tone(note, duration)
            print("elody_worker")
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
