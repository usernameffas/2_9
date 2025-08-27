import os
import zipfile
from tkinter import Tk, Label
from PIL import Image, ImageTk   # Pillow 라이브러리: 이미지 처리 및 Tkinter 호환 이미지 객체 생성


class MasImageHelper:
    '''
    이미지 폴더를 관리하며,
    현재 이미지 인덱스를 유지하고,
    다음/이전 이미지 경로를 반환하는 헬퍼 클래스
    '''
    def __init__(self, folder_path):
        self.folder_path = folder_path
        # 폴더 내 파일 중 이미지 확장자(.jpg, .jpeg, .png, .gif, .ppm, .pgm)만 필터링
        self.images = sorted([f for f in os.listdir(folder_path)
                              if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.ppm', '.pgm'))])
        self.index = 0                # 현재 인덱스 (첫 번째 이미지를 가리킴)
        self.photo = None             # Tkinter 이미지를 유지(가비지 컬렉션 방지용)


    def get_current_image_path(self):
        '''
        현재 인덱스에 해당하는 이미지 파일 절대경로 반환
        '''
        if self.images:
            return os.path.join(self.folder_path, self.images[self.index])
        return None


    def next_image(self):
        '''
        다음 이미지로 이동하고 이미지 경로 반환
        (끝에 도달하면 처음으로 순환)
        '''
        if self.images:
            self.index = (self.index + 1) % len(self.images)
            return self.get_current_image_path()
        return None


    def prev_image(self):
        '''
        이전 이미지로 이동하고 이미지 경로 반환
        (처음에서 뒤로 가면 마지막 이미지로 순환)
        '''
        if self.images:
            self.index = (self.index - 1) % len(self.images)
            return self.get_current_image_path()
        return None


def extract_zip(zip_path, extract_to):
    '''
    zip 파일을 지정한 폴더로 압축 해제한다.
    이미 폴더가 존재하면 재압축 해제하지 않음.
    예: CCTV.zip → CCTV/ 폴더
    '''
    if not os.path.exists(extract_to):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)


def main():
    zip_path = 'CCTV.zip'        # 압축 파일 이름
    extract_folder = 'CCTV'      # 압축 해제할 폴더 이름


    # ----- (1) 압축 해제 -----
    extract_zip(zip_path, extract_folder)


    # ----- (2) 이미지 폴더 헬퍼 객체 초기화 -----
    img_helper = MasImageHelper(extract_folder)


    # ----- (3) Tkinter 윈도우 설정 -----
    root = Tk()
    root.title('CCTV Image Viewer')     # 프로그램 창 제목
    root.geometry('800x600')            # 초기 창 크기 (800x600 픽셀)


    # Tkinter의 이미지 라벨(이미지 표시 영역 역할)
    label = Label(root)
    label.pack()


    # 이미지 표시 함수 정의
    def show_image(img_path):
        print(f'현재 이미지 표시: {img_path}')   # 콘솔 출력 (디버깅용)
        img = Image.open(img_path)              # PIL로 이미지 열기
        img_helper.photo = ImageTk.PhotoImage(img)  # Tkinter가 사용할 수 있는 객체로 변환
        label.config(image=img_helper.photo)        # 라벨에 이미지 설정


    # 키보드 이벤트 핸들러
    def on_key(event):
        if event.keysym == 'Right':              # 오른쪽 키 누름 → 다음 이미지
            img_path = img_helper.next_image()
            if img_path:
                show_image(img_path)
        elif event.keysym == 'Left':             # 왼쪽 키 누름 → 이전 이미지
            img_path = img_helper.prev_image()
            if img_path:
                show_image(img_path)


    # ----- (4) 키보드 이벤트 등록 -----
    root.bind('<Key>', on_key)   # 모든 키 이벤트를 on_key()로 처리


    # ----- (5) 첫 이미지 표시 -----
    first_img = img_helper.get_current_image_path()
    if first_img:
        show_image(first_img)    # 첫 번째 이미지 보여주기
    else:
        label.config(text='이미지를 찾을 수 없습니다.')   # 폴더가 비었을 때


    # ----- (6) GUI 메인 루프 실행 -----
    root.mainloop()


if __name__ == '__main__':
    main()
