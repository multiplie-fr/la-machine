"""
La Machine DIY - MicroPython for ESP32-C3
Waits for switch S3, then moves the servo arm while playing a sound.
"""

import machine
import time
from machine import Pin, PWM, I2S

# --- Pin definitions (from La Machine PCBA v1.8) ---
BUTTON_PIN = 3          # Switch S3, active high
SERVO_PWM_PIN = 10      # Servo signal
SERVO_BOOST_PIN = 4     # Servo boost enable (powers the servo)
AMP_SD_MODE_PIN = 1     # MAX98357A amplifier enable (high = on)
I2S_BCLK_PIN = 8        # I2S bit clock
I2S_LRC_PIN = 7         # I2S word select / LR clock
I2S_DIN_PIN = 6         # I2S data out to amplifier

# --- Servo parameters ---
SERVO_FREQ = 50         # 50 Hz standard servo
# Pulse widths in nanoseconds (from the Erlang calibration)
SERVO_CLOSED_NS = 1_889_000   # ~1889us - lid closed
SERVO_OPEN_NS = 833_000       # ~833us  - lid open (arm out)
SERVO_MOVE_TIME_MS = 800      # Time to allow for servo movement

# --- Audio parameters ---
AUDIO_FILE = "sound.wav"       # Place a 16-bit mono WAV file (44100 or 48000 Hz) on the filesystem
I2S_SAMPLE_RATE = 44100
I2S_BITS = 16
I2S_BUF_SIZE = 4096


def setup_button():
    """Configure the button pin with pull-down (switch pulls high when activated)."""
    return Pin(BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)


def setup_servo():
    """Configure servo PWM at 50Hz, initially in closed position."""
    pwm = PWM(Pin(SERVO_PWM_PIN), freq=SERVO_FREQ, duty_u16=0)
    pwm.duty_ns(SERVO_CLOSED_NS)
    return pwm


def setup_servo_boost():
    """Servo boost enable pin - controls power to the servo."""
    boost = Pin(SERVO_BOOST_PIN, Pin.OUT)
    boost.value(0)  # Off initially
    return boost


def setup_amp():
    """MAX98357A amplifier SD_MODE pin - high to enable."""
    amp = Pin(AMP_SD_MODE_PIN, Pin.OUT)
    amp.value(0)  # Off initially
    return amp


def setup_i2s():
    """Configure I2S output for audio playback."""
    audio_out = I2S(
        0,
        sck=Pin(I2S_BCLK_PIN),
        ws=Pin(I2S_LRC_PIN),
        sd=Pin(I2S_DIN_PIN),
        mode=I2S.TX,
        bits=I2S_BITS,
        format=I2S.MONO,
        rate=I2S_SAMPLE_RATE,
        ibuf=I2S_BUF_SIZE,
    )
    return audio_out


def servo_move(pwm, duty_ns):
    """Move servo to a position specified by pulse width in nanoseconds."""
    pwm.duty_ns(duty_ns)


def play_sound(audio_out, amp):
    """Play WAV file through I2S. Skips the 44-byte WAV header."""
    try:
        f = open(AUDIO_FILE, "rb")
    except OSError:
        print("Sound file '{}' not found - skipping audio".format(AUDIO_FILE))
        return

    amp.value(1)  # Enable amplifier
    time.sleep_ms(10)  # Let amp stabilize

    # Skip WAV header (standard 44 bytes)
    f.read(44)

    buf = bytearray(I2S_BUF_SIZE)
    while True:
        n = f.readinto(buf)
        if n is None or n == 0:
            break
        audio_out.write(buf[:n])

    f.close()
    time.sleep_ms(50)  # Let last samples play out
    amp.value(0)  # Disable amplifier


def run_action(servo, boost, audio_out, amp):
    """The main action: open lid (move servo) while playing sound, then close."""
    # Power on servo
    boost.value(1)
    time.sleep_ms(20)

    # Move servo to open position
    servo_move(servo, SERVO_OPEN_NS)

    # Play sound (blocking - servo stays open during playback)
    play_sound(audio_out, amp)

    # Wait a bit with lid open if sound was short
    time.sleep_ms(200)

    # Close lid
    servo_move(servo, SERVO_CLOSED_NS)
    time.sleep_ms(SERVO_MOVE_TIME_MS)

    # Power off servo
    boost.value(0)


def main():
    print("La Machine DIY - starting")

    button = setup_button()
    servo = setup_servo()
    boost = setup_servo_boost()
    amp = setup_amp()
    audio_out = setup_i2s()

    print("Ready - waiting for button press...")

    button_was_pressed = False

    while True:
        if button.value() == 1:
            if not button_was_pressed:
                button_was_pressed = True
                print("Button pressed! Running action...")
                run_action(servo, boost, audio_out, amp)
                print("Action complete. Waiting for next press...")
        else:
            button_was_pressed = False

        time.sleep_ms(20)  # Debounce / polling interval


main()
