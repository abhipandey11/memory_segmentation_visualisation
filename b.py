import random
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, ttk

class Segment:
    def __init__(self, name, limit):
        self.name = name
        self.limit = limit
        self.base_address = -1
        self.end_address = -1

    def get_name(self):
        return self.name

    def get_limit(self):
        return self.limit

    def get_base_address(self):
        return self.base_address

    def get_end_address(self):
        return self.end_address

    def set_base_address(self, base_address):
        self.base_address = base_address

    def set_end_address(self, end_address):
        self.end_address = end_address

    def is_overlapping(self, other):
        return (self.base_address < other.get_end_address() and self.end_address > other.get_base_address()) or \
               (other.get_base_address() < self.end_address and other.get_end_address() > self.base_address)

    def is_allocated(self):
        return self.base_address != -1 and self.end_address != -1

    def is_within_memory(self, memory_size):
        return 0 <= self.base_address <= memory_size and 0 <= self.end_address <= memory_size

class MemorySegmentationGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Memory Segmentation")
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.memory_size = None
        self.num_segments = None
        self.segments = []

        self.create_widgets()

    def create_widgets(self):
        memory_label = ttk.Label(self.main_frame, text="Memory Size:")
        memory_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.memory_size_entry = ttk.Entry(self.main_frame)
        self.memory_size_entry.grid(row=0, column=1, padx=5, pady=5)

        segments_label = ttk.Label(self.main_frame, text="Number of Segments:")
        segments_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.num_segments_entry = ttk.Entry(self.main_frame)
        self.num_segments_entry.grid(row=1, column=1, padx=5, pady=5)

        self.segment_entries_frame = ttk.Frame(self.main_frame)
        self.segment_entries_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

        allocate_button = ttk.Button(self.main_frame, text="Allocate Memory", command=self.allocate_memory)
        allocate_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def add_segment_entry(self, index):
        label = ttk.Label(self.segment_entries_frame, text=f"Segment {index + 1} Info:")
        label.grid(row=index, column=0, padx=5, pady=5, sticky=tk.W)
        entry = ttk.Entry(self.segment_entries_frame)
        entry.grid(row=index, column=1, padx=5, pady=5)
        self.segments.append(entry)

    def allocate_memory(self):
        self.memory_size = int(self.memory_size_entry.get())
        self.num_segments = int(self.num_segments_entry.get())
        self.segments.clear()

        # Clear existing segment entries
        for widget in self.segment_entries_frame.winfo_children():
            widget.destroy()

        # Add segment entries
        for i in range(self.num_segments):
            self.add_segment_entry(i)

        # Add button to confirm segment entries
        confirm_button = ttk.Button(self.segment_entries_frame, text="Confirm", command=self.process_segment_entries)
        confirm_button.grid(row=self.num_segments, column=0, columnspan=2, padx=5, pady=5)

    def process_segment_entries(self):
        segments = []
        for entry in self.segments:
            segment_info = entry.get().split()
            segment_name = segment_info[0]
            segment_limit = int(segment_info[1])
            segments.append(Segment(segment_name, segment_limit))

        memory = MemorySegmentation(self.memory_size)
        for segment in segments:
            memory.add_segment(segment)

        memory.allocate_memory_randomly()
        memory.display_memory_layout()
        memory.visualize_memory_allocation()

    def run(self):
        self.root.mainloop()

class MemorySegmentation:
    def __init__(self, main_memory_size):
        self.main_memory_size = main_memory_size
        self.segments = []
        self.random = random.Random()

    def add_segment(self, segment):
        self.segments.append(segment)

    def allocate_memory_randomly(self):
        for segment in self.segments:
            overlapped = True
            attempts = 0
            while overlapped and attempts <= self.main_memory_size - segment.get_limit():
                base_address = self.random.randint(0, self.main_memory_size - segment.get_limit())
                end_address = base_address + segment.get_limit()
                segment.set_base_address(base_address)
                segment.set_end_address(end_address)
                overlapped = False
                for other in self.segments:
                    if other != segment and segment.is_overlapping(other):
                        overlapped = True
                        break
                attempts += 1
            if overlapped:
                self.compact_memory()
                if not self.attempt_memory_allocation(segment):
                    print(f"Error: Cannot allocate segment '{segment.get_name()}' even after compaction.")

    def compact_memory(self):
        base_address = 0
        for segment in self.segments:
            if segment.is_allocated():
                end_address = base_address + segment.get_limit()
                if end_address <= self.main_memory_size:
                    segment.set_base_address(base_address)
                    segment.set_end_address(end_address)
                    base_address = end_address
                else:
                    segment.set_base_address(-1)
                    segment.set_end_address(-1)

    def attempt_memory_allocation(self, segment):
        for existing_segment in self.segments:
            if not existing_segment.is_allocated() and existing_segment.get_limit() >= segment.get_limit():
                new_base_address = segment.get_base_address()
                new_end_address = segment.get_end_address()
                if existing_segment.is_within_memory(self.main_memory_size) and \
                        0 <= new_base_address <= self.main_memory_size and \
                        0 <= new_end_address <= self.main_memory_size:
                    existing_segment.set_base_address(new_base_address)
                    existing_segment.set_end_address(new_end_address)
                    return True
        return segment.is_allocated()

    def display_memory_layout(self):
        print("Memory Segmentation:")
        print("--------------------")
        print("Segment Name\tlimit\tBase Address")
        for segment in self.segments:
            if segment.is_allocated():
                print(f"{segment.get_name()}\t\t{segment.get_limit()}\t\t{segment.get_base_address()}")
            else:
                print(f"{segment.get_name()}\t\tUnallocated\tUnallocated")

    def visualize_memory_allocation(self):
        plt.figure(figsize=(10, 6))
        plt.title("Memory Segmentation")
        plt.xlabel("Memory Address")
        plt.ylabel("Segment Name")

        # Define a list of colors to be used for segments
        colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']

        # Plot memory segments
        color_index = 0  # Index to keep track of the color to be used
        for segment in self.segments:
            if segment.is_allocated():
                plt.barh(segment.get_name(), width=segment.get_end_address() - segment.get_base_address(), left=segment.get_base_address(), height=0.5, color=colors[color_index])
                color_index = (color_index + 1) % len(colors)  # Move to the next color, looping back to the start if necessary

        plt.xlim(0, self.main_memory_size)
        plt.ylim(-0.5, len(self.segments) - 0.5)
        plt.gca().invert_yaxis()
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.show()


def main():
    gui = MemorySegmentationGUI()
    gui.run()

if __name__ == "__main__":
    main()
