import asyncio
from bleak import BleakClient, BleakScanner

BOOST_MAC = "YOUR_MAC_ADDRESS_OF_HUB" #Replace with Hub's Mac Address

# UUIDs for LEGO Move Hub (example: motor A)
# Replace these with correct motor characteristic UUIDs for actual control
MOTOR_A_UUID = "00001625-1212-efde-1623-785feabcd123"  

async def move_motor(client):
    """Send simple command to move motor A forward repeatedly."""
    print("🚀 Starting motor A forward...")
    while True:
        try:
            # Dummy command: replace with real motor value
            await client.write_gatt_char(MOTOR_A_UUID, bytearray([100]))
        except Exception as e:
            print(f"⚠️ Motor command failed: {e}")
        await asyncio.sleep(0.5)  # send command every 0.5s

async def try_connect():
    """Scan, connect, and immediately move forward."""
    while True:
        print("🔍 Scanning for Boost hub...")
        devices = await BleakScanner.discover(timeout=5)
        hub_device = next((d for d in devices if d.address.upper() == BOOST_MAC.upper()), None)

        if not hub_device:
            print("❌ Hub not found, retrying in 3s...")
            await asyncio.sleep(3)
            continue

        print(f"✅ Found hub at {hub_device.address}, connecting...")
        try:
            async with BleakClient(hub_device) as client:
                if client.is_connected:
                    print(f"🤝 Connected to {hub_device.address}")
                    # Immediately start motor
                    await move_motor(client)
                else:
                    print("❌ Could not stay connected, retrying...")
        except Exception as e:
            print(f"⚠️ Connection error: {e}")
        print("🔄 Retrying scan in 3s...")
        await asyncio.sleep(3)

asyncio.run(try_connect())
