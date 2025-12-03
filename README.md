# ZeusCast B53AII Display Controller

This Python script reads the CPU temperature and displays it on the **Boreas B53AII** display. It supports Celsius and Fahrenheit modes, customizable update intervals, and a debug option.

---

## Requirements

* **Python 3.8+**
* `psutil` Python package
* `hid` Python package
* Access to `/dev/hidraw*` devices (udev rule or sudo)

---

## Installation

1. **Clone or copy the project**:

```bash
cd /path/to/ZeusCast
```

2. **Create a virtual environment (optional but recommended)**:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install required Python packages**:

```bash
pip install --upgrade pip
pip install psutil hid
```

4. **Set device permissions (so Python can access the display without sudo)**:

```bash
sudo bash -c 'cat > /etc/udev/rules.d/99-boreas.rules <<EOF
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="1b80", ATTRS{idProduct}=="b53a", MODE="0666"
EOF'
sudo udevadm control --reload
sudo udevadm trigger
```

---

## Running the Script

From the project root directory:

```bash
source .venv/bin/activate   # if using virtual environment
python ZeusCast.py [OPTIONS]
```

### Available Options

| Option                 | Description                                         | Default  |
|------------------------|-----------------------------------------------------|----------|
| `--mode c`             | Temperature unit: Celsius (`c`) or Fahrenheit (`f`) | `c`      |
| `--interval <seconds>` | Update interval in seconds                          | `0.25`   | 
| `--debug`              | Enable debug logs                                   | Disabled |

Example:

```bash
python ZeusCast.py --mode f --interval 1.0 --debug
```

---

## Running in Background

You can run the script in the background using `nohup` or `&`:

```bash
nohup python ZeusCast.py --mode c --interval 0.25 > zeuscast.log 2>&1 &
```

Check logs:

```bash
tail -f zeuscast.log
```

Stop the process:

```bash
pkill -f ZeusCast.py
```

---

## Notes

* Make sure your user has read/write access to `/dev/hidraw*` (udev rule recommended).
* For systemd integration, make sure the `ExecStart` points to the **absolute path** of the script and that the script is **executable**.

---
## Donate
USDT(Binance Blockchain)
```
0x72F18129A47EA26176B9338E7Dd6A17434aABC8a
```
