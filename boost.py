import asyncio
from bleak import BleakClient, BleakScanner

BOOST_MAC = "1A:2B:3C:4D:5E:6" #Replace with Mac id of Boost Hub

# LEGO Move Hub motor UUIDs
# These are the GATT characteristics for controlling motors
MOTOR_A_UUID = "00001625-1212-efde-1623-785feabcd123"  # left motor (replace with real motor a uuid)
MOTOR_B_UUID = "00001626-1212-efde-1623-785feabcd123"  # right motor (replace with real motor b uuid

# Helper to send motor command
def motor_command(power):
    """
    LEGO Boost expects signed 8-bit power (-100 → 100)
    packed into a 1-byte array. For simplicity here.
    """
    if power < 0:
        power = 256 + power  # convert to unsigned byte
    return bytearray([power])

async def move(client, left_power, right_power, duration=2):
    """Move motors A & B with given power for duration in seconds."""
    try:
        await client.write_gatt_char(MOTOR_A_UUID, motor_command(left_power))
        await client.write_gatt_char(MOTOR_B_UUID, motor_command(right_power))
        print(f"➡️ Moving: left={left_power}, right={right_power}")
        await asyncio.sleep(duration)
        # Stop motors after duration
        await client.write_gatt_char(MOTOR_A_UUID, motor_command(0))
        await client.write_gatt_char(MOTOR_B_UUID, motor_command(0))
    except Exception as e:
        print(f"⚠️ Motor command failed: {e}")

async def patrol_loop(client):
    """Simple patrol pattern: forward → turn → forward"""
    while True:
        await move(client, 50, 50, 3)   # Forward
        await move(client, 50, -50, 1)  # Turn right
        await move(client, 50, 50, 3)   # Forward
        await move(client, -50, 50, 1)  # Turn left

async def try_connect():
    while True:
        print("🔍 Scanning for Boost hub...")
        devices = await BleakScanner.discover(timeout=5)
        hub = next((d for d in devices if d.address.upper() == BOOST_MAC.upper()), None)

        if not hub:
            print("❌ Hub not found, retrying in 3s...")
            await asyncio.sleep(3)
            continue

        print(f"✅ Found hub at {hub.address}, connecting...")
        try:
            async with BleakClient(hub) as client:
                if client.is_connected:
                    print(f"🤝 Connected to {hub.address}, starting patrol")
                    await patrol_loop(client)
                else:
                    print("❌ Could not stay connected, retrying...")
        except Exception as e:
            print(f"⚠️ Connection error: {e}")
        print("🔄 Retrying scan in 3s...")
        await asyncio.sleep(3)

asyncio.run(try_connect())
