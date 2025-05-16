import threading
import sys
import os
import traceback
import time
import builtins
sys.path.append(".")
import facialcommunism as fc

class ProcessingStatus:
    def __init__(self):
        self.status = {}
        self.details = {}
        self.progress = {}

    def start_processing(self, filename):
        self.status[filename] = "processing"
        self.details[filename] = "Starting image processing..."
        self.progress[filename] = 0

    def update_progress(self, filename, progress, details):
        self.progress[filename] = progress
        self.details[filename] = details
        builtins.print(f"Processing progress for {filename}: {progress}% - {details}")

    def complete_processing(self, filename, success=True, error_details=None):
        self.status[filename] = "completed" if success else "failed"
        if not success and error_details:
            self.details[filename] = f"Error: {error_details}"
            builtins.print(f"Processing failed for {filename}: {error_details}")
        else:
            self.details[filename] = "Processing completed successfully"
            builtins.print(f"Processing completed for {filename}")

    def get_status(self, filename):
        return self.status.get(filename, "unknown")
    
    def get_details(self, filename):
        return self.details.get(filename, "")

processing_status = ProcessingStatus()

original_print = builtins.print

def custom_print(*args, **kwargs):
    message = " ".join(str(arg) for arg in args)
    original_print(message, **kwargs)
    
    current_filename = getattr(custom_print, 'current_filename', None)
    if current_filename:
        if "faces detected" in message:
            original_print(f"Processing progress for {current_filename}: 20% - {message}")
            processing_status.progress[current_filename] = 20
            processing_status.details[current_filename] = message
        elif "prefix table done" in message:
            original_print(f"Processing progress for {current_filename}: 50% - Processing facial features...")
            processing_status.progress[current_filename] = 50
            processing_status.details[current_filename] = "Processing facial features..."
        elif "computed weights" in message:
            original_print(f"Processing progress for {current_filename}: 80% - Finalizing image...")
            processing_status.progress[current_filename] = 80
            processing_status.details[current_filename] = "Finalizing image..."

def process_image_async(filename):
    """Process an image in a background thread"""
    processing_status.start_processing(filename)
    start_time = time.time()
    
    try:
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            builtins.print(f"Starting processing for {filename}")
            
            custom_print.current_filename = filename
            
            original_builtin_print = builtins.print
            builtins.print = custom_print
            
            try:
                fc.write_image(filename)
                
                builtins.print = original_builtin_print
                
                processing_status.complete_processing(filename, True)
                builtins.print(f"Processing completed in {time.time() - start_time:.2f} seconds")
            except Exception as e:
                builtins.print = original_builtin_print
                raise e
        else:
            error_msg = f"File does not exist or is empty: {filename}"
            builtins.print(error_msg)
            processing_status.complete_processing(filename, False, error_msg)
    except Exception as e:
        error_details = f"{str(e)}\n{traceback.format_exc()}"
        builtins.print(f"Error processing image: {error_details}")
        processing_status.complete_processing(filename, False, error_details)

def start_processing(filename):
    """Start a background thread to process the image"""
    thread = threading.Thread(target=process_image_async, args=(filename,))
    thread.daemon = True
    thread.start()
    return thread
