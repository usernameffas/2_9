import os
import zipfile
from tkinter import Tk, Label, PhotoImage

# -----------------------------------
# MasImageHelper 클래스 정의
# -----------------------------------
class MasImageHelper:
    '''
    이미지 파일들이 저장된 폴더를 관리하고,
    다음/이전 이미지 탐색 기능을 제공하는 헬퍼 클래스입니다.

    주요 기능:
    - 폴더에서 지원하는 이미지 파일 목록 생성 및 정렬
    - 현재 탐색중인 이미지 인덱스 유지
    - 다음, 이전 이미지 경로 반환
    '''

    def __init__(self, folder_path):
        '''
        클래스 생성자 (초기화 메서드)
        folder_path: 이미지가 저장된 폴더 경로 (문자열)
        '''

        self.folder_path = folder_path
        # 폴더 내에서 .png, .gif, .ppm, .pgm 확장자 이미지 파일만 리스트화 후 정렬
        self.images = sorted([f for f in os.listdir(folder_path)
                              if f.lower().endswith(('.png', '.gif', '.ppm', '.pgm'))])
        # 현재 보고 있는 이미지 번호(인덱스)를 0으로 초기화 (첫 번째 이미지)
        self.index = 0
        # tkinter PhotoImage 객체를 저장할 변수 (화면 갱신시 필요)
        self.photo = None

    def get_current_image_path(self):
        '''
        현재 인덱스에 해당하는 이미지 파일의 전체 경로를 문자열로 반환
        이미지가 없으면 None 반환
        '''
        if self.images:
            return os.path.join(self.folder_path, self.images[self.index])
        return None

    def next_image(self):
        '''
        현재 이미지 인덱스를 1 증가시킨 후,
        폴더 내 이미지 개수 범위를 초과하면 0으로 순환
        다음 이미지 경로 반환
        '''
        if self.images:
            self.index = (self.index + 1) % len(self.images)
            return self.get_current_image_path()
        return None

    def prev_image(self):
        '''
        현재 이미지 인덱스를 1 감소시킨 후,
        음수가 되면 폴더 내 이미지 개수 -1로 순환
        이전 이미지 경로 반환
        '''
        if self.images:
            self.index = (self.index - 1) % len(self.images)
            return self.get_current_image_path()
        return None

# -----------------------------------
# 압축 파일 해제 함수
# -----------------------------------
def extract_zip(zip_path, extract_to):
    '''
    CCTV.zip과 같이 주어진 경로 zip_path를
    extract_to 폴더로 압축 해제합니다.
    이미 해당 폴더가 있으면 압축 해제를 건너뜁니다.
    '''

    if not os.path.exists(extract_to):
        # zipfile 라이브러리로 zip 파일 열기
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # 모든 파일 extract_to 폴더에 압축 해제
            zip_ref.extractall(extract_to)

# -----------------------------------
# 프로그램 메인 함수
# -----------------------------------
def main():
    # CCTV.zip 파일 경로와 압축 해제될 폴더명 지정
    zip_path = 'CCTV.zip'
    extract_folder = 'CCTV'

    # CCTV.zip 압축 해제 (이미 존재하면 건너뜀)
    extract_zip(zip_path, extract_folder)

    # 이미지 헬퍼 클래스로 폴더 내 이미지 관리 준비
    img_helper = MasImageHelper(extract_folder)

    # Tkinter 윈도우 생성 및 제목 설정
    root = Tk()
    root.title('CCTV Image Viewer')

    # 이미지를 보여주는 라벨(Label) 위젯 생성 및 배치
    label = Label(root)
    label.pack()

    def show_image(img_path):
        '''
        이미지 파일 경로 img_path를 받아
        tkinter PhotoImage 객체로 변환한 후
        라벨에 이미지를 설정하여 화면에 표시함
        '''
        img_helper.photo = PhotoImage(file=img_path)
        label.config(image=img_helper.photo)

    def on_key(event):
        '''
        키보드 방향키 이벤트 처리 함수
        오른쪽 방향키 -> 다음 이미지로 변경
        왼쪽 방향키 -> 이전 이미지로 변경
        '''
        if event.keysym == 'Right':
            img_path = img_helper.next_image()
            if img_path:
                show_image(img_path)
        elif event.keysym == 'Left':
            img_path = img_helper.prev_image()
            if img_path:
                show_image(img_path)

    # 만들어진 윈도우에 키보드 입력 이벤트 핸들러 바인딩
    root.bind('<Key>', on_key)

    # 첫 이미지 화면에 표시 (없으면 안내 메시지 표시)
    first_img = img_helper.get_current_image_path()
    if first_img:
        show_image(first_img)
    else:
        label.config(text='이미지를 찾을 수 없습니다.')

    # tkinter 이벤트 루프 진입: 윈도우가 닫힐 때까지 대기 및 이벤트 처리
    root.mainloop()

# -----------------------------------
# 이 파일이 직접 실행될 때 main 함수 호출
# -----------------------------------
if __name__ == '__main__':
    main()

