from PIL import Image

DELIMITER = "#####END#####"  # Unique, unlikely string to appear in the message

def message_to_binary(message):
    return ''.join(format(ord(char), '08b') for char in message)

def binary_to_message(binary_data):
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_message = ''
    for byte in all_bytes:
        decoded_message += chr(int(byte, 2))
    return decoded_message

def encode_message(image_path, message, output_path):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    message += DELIMITER  # Add delimiter to message
    binary_message = message_to_binary(message)

    pixels = list(img.getdata())

    if len(binary_message) > len(pixels) * 3:
        raise ValueError("Message too large to hide in this image.")

    new_pixels = []
    idx = 0

    for pixel in pixels:
        r, g, b = pixel
        if idx < len(binary_message):
            r = (r & ~1) | int(binary_message[idx])
            idx += 1
        if idx < len(binary_message):
            g = (g & ~1) | int(binary_message[idx])
            idx += 1
        if idx < len(binary_message):
            b = (b & ~1) | int(binary_message[idx])
            idx += 1
        new_pixels.append((r, g, b))

    img.putdata(new_pixels)
    img.save(output_path)
    print("Message encoded successfully!")

def decode_message(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())

    binary_data = ''
    for pixel in pixels:
        for value in pixel[:3]:
            binary_data += str(value & 1)

    decoded_message = binary_to_message(binary_data)

    if DELIMITER in decoded_message:
        return decoded_message.split(DELIMITER)[0]
    else:
        return "No hidden message found"
