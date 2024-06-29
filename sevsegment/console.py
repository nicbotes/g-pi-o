from sevsegment.display import SevenSegmentDisplay
import time

def main():
    display = SevenSegmentDisplay()
    try:
        while True:
            # Take input from the user
            number = input("Enter a number to display (or 'exit' to quit): ")

            if number.lower() == 'exit':
                break

            # Display the number
            display.display_number(number)
            time.sleep(0.010)
    except KeyboardInterrupt:
        pass
    finally:
        display.cleanup()

if __name__ == "__main__":
    main()
