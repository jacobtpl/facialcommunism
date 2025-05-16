import threading
import sys
import os
sys.path.append(".")
import facialcommunism as fc

class ProcessingStatus:
    def __init__(self):
        self.status = {}

    def start_processing(self, filename):
        self.status[filename] = "processing"

    def complete_processing(self, filename, success=True):
        self.status[filename] = "completed" if success else "failed"

    def get_status(self, filename):
        return self.status.get(filename, "unknown")

processing_status = ProcessingStatus()

def process_image_async(filename):
    """Process an image in a background thread"""
    processing_status.start_processing(filename)
    try:
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            fc.write_image(filename)
            processing_status.complete_processing(filename, True)
        else:
            processing_status.complete_processing(filename, False)
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        processing_status.complete_processing(filename, False)

def start_processing(filename):
    """Start a background thread to process the image"""
    thread = threading.Thread(target=process_image_async, args=(filename,))
    thread.daemon = True
    thread.start()
    return thread
