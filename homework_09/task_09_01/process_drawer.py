from os import listdir, cpu_count
from multiprocessing import Process, Queue
from PIL import Image, ImageDraw
from time import time
from numpy import array_split


class DrawProcess(Process):

    def __init__(self, file_names: str, folder_path: str, queue: Queue):
        super().__init__()
        self.file_names = file_names
        self.folder_path = folder_path
        self.queue = queue

    def run(self):
        for fileName in self.file_names:
            img = Image.open(f'{self.folder_path}/{fileName}')
            draw = ImageDraw.Draw(img)
            draw.rectangle([(0, 0), (img.size[0] - 1, img.size[1] - 1)], outline='black')
            # self.queue.put((fileName, img.size))

            with open(f'flags_plus/{fileName}', 'wb') as out:
                img.save(out, img.format)


def draw_boarders_linear(folder_path: str):
    time_start = time()

    for fileName in listdir(folder_path):
        img = Image.open(f'{folder_path}/{fileName}')
        draw = ImageDraw.Draw(img)
        draw.rectangle([(0, 0), (img.size[0] - 1, img.size[1] - 1)], outline='black')

        with open(f'flags_plus/{fileName}', 'wb') as out:
            img.save(out, img.format)

    time_end = time()

    print(time_end-time_start)


def draw_borders_with_processes(folder_path: str):
    queqe = Queue()
    processes = []
    cpu_amount = cpu_count()
    files = listdir(folder_path)

    files_on_process = array_split(files, cpu_amount)
    time_start = time()

    for i in range(cpu_amount):
        processes.append(
            DrawProcess(files_on_process[i], 'flags/', queqe))

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    time_end = time()

    print(time_end - time_start)


if __name__ == '__main__':
    draw_borders_with_processes('flags/')
    draw_boarders_linear('flags/')
