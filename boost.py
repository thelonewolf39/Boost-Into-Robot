import asyncio
from bleak import BleakClient, BleakScanner

#Replace with real Boost Mac id
BOOST_MAC = "1A:2B:3C:4D:5E:6F"
#Replace with real motor UUID
MOTOR_CHAR_UUID = "8db79ce7-76f9-490e-93af-a4d617894121"

def motor_command(power):
    if power < 0:
        power = 256 + power
    return bytearray([power])

async def move(client, left_power, right_power, duration=2):
    try:
        await client.write_gatt_char(MOTOR_CHAR_UUID, motor_command(left_power))
        await client.write_gatt_char(MOTOR_CHAR_UUID, motor_command(right_power))
        await asyncio.sleep(duration)
        # stop motors
        await client.write_gatt_char(MOTOR_CHAR_UUID, motor_command(0))
        await client.write_gatt_char(MOTOR_CHAR_UUID, motor_command(0))
    except:
        pass  # ignore errors

async def patrol_loop(client):
    while True:
        await move(client, 50, 50, 3)    # forward
        print("Moved Forward!")
        await move(client, 50, -50, 1)   # turn right
        print("Moved Right!")
        await move(client, 50, 50, 3)    # forward
        print("Moved Forward!")
        await move(client, -50, 50, 1)   # turn left
        print("Moved Left!")

async def wait_and_connect():
    while True:
        print("🔍 Scanning for Hub...")
        devices = await BleakScanner.discover(timeout=5)
        hub = next((d for d in devices if d.address.upper() == BOOST_MAC.upper()), None)

        if hub is None:
            print("❌ Hub not found, retrying in 3s...")
            await asyncio.sleep(3)
            continue

        print(f"✅ Found hub at {hub.address}, connecting...")
        try:
            async with BleakClient(hub) as client:
                if client.is_connected:
                    print("🤝 Connected! Starting patrol...")
                    await patrol_loop(client)
                else:
                    print("❌ Could not stay connected, retrying...")
        except:
            print("⚠️ Connection failed, retrying in 3s...")
            await asyncio.sleep(3)

asyncio.run(wait_and_connect())
