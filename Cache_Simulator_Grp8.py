from collections import deque
import random
import tkinter as tk
from tkinter import ttk
from tkinter import font

class Set:
    def __init__(self, n_way):
        self.n_way = n_way
        self.blocks = deque(maxlen=n_way)
        self.block_ages = {}

    def check(self, block_addr):
        if block_addr in self.blocks:
            self.update(block_addr)
            return True
        else:
            self.replace_lru(block_addr)
            return False

    def update(self, most_recent):
        self.block_ages[most_recent] = 0

        for block in self.blocks:
            if block != most_recent:
                self.block_ages[block] += 1

    def replace_lru(self, addr):
        if addr not in self.blocks and len(self.blocks) == self.n_way:
            oldest = self.blocks.popleft()
            del self.block_ages[oldest]

        if addr not in self.blocks:
            self.blocks.append(addr)
            self.block_ages[addr] = 0

        for block in self.blocks:
            if block != addr:
                self.block_ages[block] += 1

    def to_string(self):
        return ", ".join(str(block) + " (Age: " + str(self.block_ages[block]) + ")" for block in self.blocks)

class Cache:
    def __init__(self, num_sets, n_way):
        self.sets = [Set(n_way) for i in range(num_sets)]
        self.hit_count = 0  # Added hit_count attribute

    def access_block(self, block_addr):
        set_index = block_addr % len(self.sets)
        set_to_check = self.sets[set_index]
        is_hit = set_to_check.check(block_addr)
        if is_hit:
            self.hit_count += 1
        print("\nAccessing block address: [ " + str(block_addr) + " ] - " + ("HIT" if is_hit else "MISS"))
        self.print_cache()
        return is_hit

    def print_cache(self):
        print("Cache Memory:")
        for i, s in enumerate(self.sets):
            print("Set " + str(i) + ": " + s.to_string())

    def ret_cache(self):
        return self.sets

def sequential_sequence(num_blocks):
    if num_blocks > 32:
        num_blocks = 32
    sequence = list(range(2 * num_blocks))
    return sequence * 4

def random_sequence(num_blocks):
    sequence = random.sample(range(4 * num_blocks), 4 * num_blocks)
    return sequence

def mid_repeat_blocks(num_blocks):
    sequence = [0] + (list(range(1, num_blocks-1)) * 2) + list(range(num_blocks-1, 2 * num_blocks))
    return sequence * 4

def finalCache(set0, set1):
    for col in range(8):
        label = tk.Label(frame, text=f"Block {col}", bg = '#3A3845', fg='white')
        label.config(font=("Courier", 11))
        label.grid(row=0, column=col + 1, padx=5, pady=5)
        
            # Create labels for set numbers and cache contents
    
    for r in range(2):
                # Set labels
        set_label = tk.Label(frame, text=f"Set {r}",  bg = '#3A3845', fg='white', font = font.Font(weight='bold'))
        set_label.config(font=("Courier", 11))
        set_label.grid(row=(r*2) + 1, column=0, pady=5)

        if r == 0:
            dispSet = set0
        else:
            dispSet = set1
                # Cache content labels
        for col in range(len(dispSet.blocks)):
            content_label = tk.Label(frame, text=dispSet.blocks[col], bg = '#3A3845', fg='white', width=7)
            content_label.config(font=("Courier", 11))
            content_label.grid(row=(r*2) + 1, column=col + 1, padx=1)

            age_label = tk.Label(frame, text=f"Age: {dispSet.block_ages[dispSet.blocks[col]]}", bg = '#3A3845', fg='white', width=7)
            age_label.config(font=("Courier", 11))
            age_label.grid(row=(r*2) + 2, column=col + 1, padx=1)
            


def step_by_stepCache(set0, set1):

    for col in range(8):
        label = tk.Label(frame, text=f"Block {col}", bg='#3A3845', fg='white')
        label.config(font=("Courier", 11))
        label.grid(row=0, column=col + 1, padx=5, pady=5)

    for r in range(2):
        set_label = tk.Label(frame, text=f"Set {r}", bg='#3A3845', fg='white', font=font.Font(weight='bold'))
        set_label.config(font=("Courier", 11))
        set_label.grid(row=(r*2) + 1, column=0, pady=5)

        if r == 0:
            dispSet = set0
        else:
            dispSet = set1

        for col in range(len(dispSet.blocks)):
            content_label = tk.Label(frame, text=dispSet.blocks[col], bg='#3A3845', fg='white', width=7)
            content_label.config(font=("Courier", 11))
            content_label.grid(row=(r*2) + 1, column=col + 1, padx=1)

            age_label = tk.Label(frame, text=f"Age: {dispSet.block_ages[dispSet.blocks[col]]}", bg='#3A3845', fg='white', width=7)
            age_label.config(font=("Courier", 11))
            age_label.grid(row=(r*2) + 2, column=col + 1, padx=1)




def simulate_step_by_step(cache, block_sequence, index, result_labels):
    if index >= len(block_sequence):
        return
    
    
    for label in result_labels.values():
        label.pack(pady=2)

    block_addr = block_sequence[index]
    is_hit = cache.access_block(block_addr)

    last_set1 = cache.sets[-1]
    last_set0 = cache.sets[-2]

    step_by_stepCache(last_set0, last_set1)

    total_accesses = index + 1
    hit_rate = (cache.hit_count / total_accesses) * 100
    miss_rate = 100 - hit_rate
    miss_count = total_accesses - cache.hit_count
    miss_penalty = 1 + (10 + ((10 * total_accesses) / 2))
    avg_time = (cache.hit_count / total_accesses) * 1 + (1 - (cache.hit_count / total_accesses)) * miss_penalty
    total_time = (cache.hit_count * (total_accesses * 1)) + (miss_count * (1 + (total_accesses * 10)))

    result_labels['total_accesses'].config(text="Memory Access Count: " + str(total_accesses))
    result_labels['hit_count'].config(text="Cache Hit Count: " + str(cache.hit_count))
    result_labels['miss_count'].config(text="Cache Miss Count: " + str(miss_count))
    result_labels['hit_rate'].config(text="Cache Hit Rate: " + str(hit_rate) + "%")
    result_labels['miss_rate'].config(text="Cache Miss Rate: " + str(miss_rate) + "%")
    result_labels['avg_time'].config(text="Average Memory Access Time: " + str(avg_time) + " ns")
    result_labels['total_time'].config(text="Total Memory Access Time: " + str(total_time) + " ns")

    index += 1

    window.after(1000, simulate_step_by_step, cache, block_sequence, index, result_labels)

def StartSimulation(block_sequence):
    clear_frame(frame)
    print(block_sequence)

    def test_case_check():
        
        test_case = optiontext_entry.get() 
        num_sets = 2
        n_way = 8
        num_cache = 16

        cache = Cache(num_sets, n_way)
        cache.hit_count = 0
        index = 0



        result_labels = {
            'total_accesses': tk.Label(frame3, text="Memory Access Count: ", font=("Courier", 11)),
            'hit_count': tk.Label(frame3, text="Cache Hit Count: ", font=("Courier", 11)),
            'miss_count': tk.Label(frame3, text="Cache Miss Count: ", font=("Courier", 11)),
            'hit_rate': tk.Label(frame3, text="Cache Hit Rate: ", font=("Courier", 11)),
            'miss_rate': tk.Label(frame3, text="Cache Miss Rate: ", font=("Courier", 11)),
            'avg_time': tk.Label(frame3, text="Average Memory Access Time: ", font=("Courier", 11)),
            'total_time': tk.Label(frame3, text="Total Memory Access Time: ", font=("Courier", 11))
        }
        
        if test_case == 'a':
            clear_frame(frame)
            window.after(0, simulate_step_by_step, cache, block_sequence, index, result_labels)
        elif test_case == 'b':
            clear_frame(frame)
            hit_count = 0
            for block_addr in block_sequence:
                if cache.access_block(block_addr):
                    hit_count += 1
            last_set1 = cache.sets[-1]
            last_set0 = cache.sets[-2]
            total_accesses = len(block_sequence)
            hit_rate = (hit_count / total_accesses * 100) 
            miss_rate = 100 - hit_rate
            miss_count = total_accesses - hit_count
            miss_penalty =  1 + ( 10 + ((10*len(block_sequence)))/2 )
            avg_time = (hit_count / total_accesses)*1 + (1- (hit_count / total_accesses))*miss_penalty
            total_time = (hit_count * (len(block_sequence)*1)) + (miss_count * ( 1 + (len(block_sequence)*10)))

            result_labels['total_accesses'].config(text="Memory Access Count: " + str(total_accesses))
            result_labels['hit_count'].config(text="Cache Hit Count: " + str(hit_count))
            result_labels['miss_count'].config(text="Cache Miss Count: " + str(miss_count))
            result_labels['hit_rate'].config(text="Cache Hit Rate: " + str(hit_rate) + "%")
            result_labels['miss_rate'].config(text="Cache Miss Rate: " + str(miss_rate) + "%")
            result_labels['avg_time'].config(text="Average Memory Access Time: " + str(avg_time) + " ns")
            result_labels['total_time'].config(text="Total Memory Access Time: " + str(total_time) + " ns")
                    
            for label in result_labels.values():
                label.pack()
            finalCache(last_set0, last_set1)
        else:
            return
    
    option_label = tk.Label(frame, text="Please choose one\n a.) Step by step process \n b.) Proceed to the final output", bg="#D3D3D3")
    option_label.pack()
    option_label.config(font=("Courier", 15))
    optiontext_entry = tk.Entry(frame)
    optiontext_entry.pack(pady=8)
    optiontext_entry.config(font=("Courier", 15))
    option_button = tk.Button(frame, text='Enter', bg="#D3D3D3", command=test_case_check)
    option_button.config(font=('Courier', 15))
    option_button.pack()



    

def main():
    number = int(memBlocktext_entry.get())

    if number <= 0:
        clear_frame(frame2)
        error_label = tk.Label(frame2, text="Invalid number of blocks. Please input a new one.")
        error_label.pack()
        return

    menu(number)

def menu(num_blocks):
    clear_frame(frame2)
    clear_frame(frame)
    clear_frame(frame3)

    def test_case_check():
        test_case = optiontext_entry.get()



        print("option: " + test_case)
        block_sequence = []
        if test_case == 'a':
            block_sequence = sequential_sequence(num_blocks)
            StartSimulation(block_sequence)
        elif test_case == 'b':
            block_sequence = random_sequence(num_blocks)
            StartSimulation(block_sequence)
        elif test_case == 'c':
            block_sequence = mid_repeat_blocks(num_blocks)
            StartSimulation(block_sequence)
        else:
            print("Invalid!")
            return


    option_label = tk.Label(frame, text="Select test case:\na) Sequential\nb) Random\nc) Mid-repeat blocks", bg="#D3D3D3")
    option_label.pack()
    option_label.config(font=("Courier", 15))
    optiontext_entry = tk.Entry(frame)
    optiontext_entry.pack(pady=8)
    optiontext_entry.config(font=("Courier", 15))
    option_button = tk.Button(frame, text='Enter', bg="#D3D3D3", command=test_case_check)
    option_button.config(font=('Courier', 15))
    option_button.pack()

def clear_frame(frame):
    for widgets in frame.winfo_children():
        if widgets.winfo_exists():
            widgets.destroy()

if __name__ == '__main__':
    window = tk.Tk()
    window.title("8 - Way BSA + LRU Cache Memory")
    window.geometry('700x500')
    window.configure(bg="#D3D3D3")

    frame2 = tk.Frame(window)
    frame2.pack()
    frame = tk.Frame(window, bg="#D3D3D3")
    frame.pack(pady=60)
    frame3 = tk.Frame(window)
    frame3.pack()

    memBlock_label = tk.Label(frame, text="Please Enter Number of Memory Block", bg="#D3D3D3")
    memBlock_label.config(font=("Courier", 15))
    memBlock_label.pack()
    memBlocktext_entry = tk.Entry(frame)
    memBlocktext_entry.config(font=("Courier", 15))
    memBlocktext_entry.pack(pady=10)
    memBlock_button = tk.Button(frame, text='Enter', command=main)
    memBlock_button.config(font=("Courier", 15))
    memBlock_button.pack()

    window.mainloop()
