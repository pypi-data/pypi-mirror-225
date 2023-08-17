import io


def get_mime_type(buffer: io.BufferedReader):
    signature = ""
    if buffer:
        first_bytes = buffer.peek()
        signature = first_bytes.hex()[:8].upper()
    is_png = signature == "89504E47"
    is_jpg = (
        signature == "FFD8FFDB" or signature == "FFD8FFE0" or signature == "FFD8FFE1"
    )
    if is_png:
        return "image/png"
    if is_jpg:
        return "image/jpeg"
    return "application/octet-stream"
