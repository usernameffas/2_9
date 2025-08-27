import os
import zipfile
from tkinter import Tk, Label, PhotoImage

class MasImageHelper:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.images = sorted([f for f in os.listdir(folder_path)
                              if f.lower().endswith(('.png', '.gif', '.ppm', '.pgm'))])
        self.index = 0
        self.photo = None

    def get_current_image_path(self):
        if self.images:
            return os.path.join(self.folder_path, self.images[self.index])
        return None

    def next_image(self):
        if self.images:
            self.index = (self.index + 1) % len(self.images)
            return self.get_current_image_path()
        return None

    def prev_image(self):
        if self.images:
            self.index = (self.index - 1) % len(self.images)
            return self.get_current_image_path()
        return None

def extract_zip(zip_path, extract_to):
    if not os.path.exists(extract_to):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

def main():
    zip_path = 'CCTV.zip'
    extract_folder = 'CCTV'

    # 압축 해제
    extract_zip(zip_path, extract_folder)

    # 이미지 헬퍼 초기화
    img_helper = MasImageHelper(extract_folder)

    # Tkinter 윈도우 생성
    root = Tk()
    root.title('CCTV Image Viewer')

    label = Label(root)
    label.pack()

    def show_image(img_path):
        img_helper.photo = PhotoImage(file=img_path)
        label.config(image=img_helper.photo)

    def on_key(event):
        if event.keysym == 'Right':
            img_path = img_helper.next_image()
            if img_path:
                show_image(img_path)
        elif event.keysym == 'Left':
            img_path = img_helper.prev_image()
            if img_path:
                show_image(img_path)

    root.bind('<Key>', on_key)

    # 첫번째 이미지 보여주기
    first_img = img_helper.get_current_image_path()
    if first_img:
        show_image(first_img)
    else:
        label.config(text='No images found')

    root.mainloop()

if __name__ == '__main__':
    main()
