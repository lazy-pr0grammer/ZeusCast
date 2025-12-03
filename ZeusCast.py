import hid
import time
import psutil
import argparse

ZEUS_VENDOR = 0x1B80
ZEUS_PRODUCT = 0xB53A
PACKET_SIZE = 65
PACKET_HEADER = 0x3AB5
SPACE_CHAR = 0x20
CELSIUS_UNIT = 1
NORMAL_COMMAND = 0x01

def compute_check_value(packet_data):
    return sum(packet_data[:14]) & 0xFF

def prepare_display_digits(temperature):
    scaled_value = int(max(0, min(9999, temperature * 10)))

    digit_values = [
        (scaled_value // 1000) % 10,
        (scaled_value // 100) % 10,
        (scaled_value // 10) % 10,
        scaled_value % 10
    ]

    for position in range(3):
        if digit_values[position] == 0:
            digit_values[position] = SPACE_CHAR
        else:
            break

    return digit_values

def fetch_processor_heat():
    heat_readings = []
    thermal_data = psutil.sensors_temperatures()

    sensor_names = ['coretemp', 'k10temp', 'cpu-thermal', 'acpitz']
    for sensor in sensor_names:
        if sensor in thermal_data:
            for entry in thermal_data[sensor]:
                heat_readings.append(entry.current)

    return max(heat_readings) if heat_readings else 0.0

def convert_temperature_scale(temp_value, scale):
    if scale == "f":
        return temp_value * 9/5 + 32
    return temp_value

def transmit_packet(device, digit_one, digit_two, digit_three, digit_four, verbose=False):
    data_packet = [0] * PACKET_SIZE
    data_packet[0] = 0
    data_packet[1] = PACKET_HEADER >> 8
    data_packet[2] = PACKET_HEADER & 0xFF
    data_packet[3] = NORMAL_COMMAND
    data_packet[4] = digit_one
    data_packet[5] = digit_two
    data_packet[6] = digit_three
    data_packet[7] = digit_four
    data_packet[8] = 0x01
    data_packet[9] = CELSIUS_UNIT
    data_packet[10] = 0x01

    data_packet[13] = compute_check_value(data_packet)

    if verbose:
        print(f"Transmitting: {data_packet[:14]}")

    device.write(data_packet)

def parse_arguments():
    parser = argparse.ArgumentParser(description="ZeusCast Thermal Display Controller")
    parser.add_argument("-d", "--debug", action="store_true", help="Show transmission details")
    parser.add_argument("-i", "--interval", type=float, default=0.25, help="Refresh rate in seconds")
    parser.add_argument("-m", "--mode", type=str, default="c", choices=["c","f"], help="Temperature scale")
    return parser.parse_args()

def main_loop():
    settings = parse_arguments()

    display_device = hid.device()
    display_device.open(ZEUS_VENDOR, ZEUS_PRODUCT)
    display_device.set_nonblocking(False)

    scale_name = "Celsius" if settings.mode == "c" else "Fahrenheit"
    print(f"ZeusCast Display Active | Scale: {scale_name} | Refresh: {settings.interval}s")

    try:
        while True:
            current_temp = fetch_processor_heat()
            scaled_temp = convert_temperature_scale(current_temp, settings.mode)

            display_digits = prepare_display_digits(scaled_temp)
            transmit_packet(display_device, *display_digits, verbose=settings.debug)

            scale_symbol = "°C" if settings.mode == "c" else "°F"
            print(f"\rProcessor: {scaled_temp:.1f}{scale_symbol}", end='', flush=True)

            time.sleep(settings.interval)

    except KeyboardInterrupt:
        print("\nDisplay stopped")
    finally:
        display_device.close()

if __name__ == "__main__":
    main_loop()