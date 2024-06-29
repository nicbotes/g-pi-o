from sevensegment.display import SevenSegmentDisplay
import time
import threading
import signal
import sys

# Global variable to store the number to display
current_number = '0000'
decimal_points = []
display = None

def display_thread():
    global current_number
    global decimal_points
    global display
    while True:
        display.display_number(current_number, decimal_points)
        time.sleep(0.01)

def signal_handler(sig, frame):
    global current_number
    global decimal_points
    print("\nInterrupt received. Enter a new number to display or 'q' to quit.")
    while True:
        user_input = input("Enter a number (up to 4 digits) to display or 'q' to quit: ")
        if user_input.lower() == 'q':
            display.cleanup()
            sys.exit(0)
        elif user_input.isdigit() and len(user_input) <= 4:
            current_number = user_input.zfill(4)
            dp_input = input("Enter decimal point positions (0-3, separated by space, or 'none'): ")
            if dp_input.lower() == 'none':
                decimal_points = []
            else:
                decimal_points = list(map(int, dp_input.split()))
            break
        else:
            print("Invalid input. Please enter a number up to 4 digits.")

def main():
    global display
    display = SevenSegmentDisplay()

    # Start the display thread
    thread = threading.Thread(target=display_thread)
    thread.daemon = True
    thread.start()

    # Set up signal handler for interrupt signal
    signal.signal(signal.SIGINT, signal_handler)

    # Keep the main thread running
    print("Displaying numbers. Press Ctrl+C to enter a new number.")
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
