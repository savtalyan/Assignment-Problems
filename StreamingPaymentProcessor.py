import io

# Create ChecksumBufferedWriter class and its instance.
# Parameter buffer is an instance of io.BufferedWriter(io.BytesIO)

class ChecksumBufferedWriter(io.BufferedWriter):
    def __init__(self, buffer):
        super().__init__(buffer)  # Initialize the parent class
        self.checksum = 0  # Initialize checksum to 0


# Writing bytes to the buffer and updating the checksum. parameter b represents bytes to write to the buffer

    def write(self, b):

        self.checksum += len(b)  # Update checksum with the number of bytes written
        super().write(b)  # Call the parent class's write method to perform the actual writing

# Returning the current checksum of bytes written

    def get_checksum(self):
        return self.checksum


# This is a library function, you can't modify it.
def get_payments_storage():

    return io.BytesIO()


# This is a library function, you can't modify it.

def stream_payments_to_storage(storage):

    for i in range(10):
        storage.write(bytes([1, 2, 3, 4, 5]))

# Processing payments and printing the checksum of bytes written.
def process_payments():
    storage = get_payments_storage()  # Get an instance of the buffer
    buffered_storage = ChecksumBufferedWriter(storage)  # Wrap the buffer in ChecksumBufferedWriter
    stream_payments_to_storage(buffered_storage)  # Stream payments to the custom buffered storage
    print("Checksum of bytes written:", buffered_storage.get_checksum())  # Print the checksum


# Run the function to check the output
process_payments()