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


'''Create detail.py
import: 파일 탐색, 압축 해제, GUI 구성용 모듈을 불러옴.

MasImageHelper 클래스: 이미지 폴더 내 지원 확장자 이미지 파일 목록 생성 및 정렬, 현재 위치 관리, 이미지 경로 반환 기능 제공.

extract_zip 함수: 압축이 이미 풀린 경우 재실행하지 않도록 체크 후 압축 해제.

main 함수: 압축 해제 → 이미지 객체 초기화 → tkinter 윈도우 생성 → 키보드 이벤트 등록 → 첫 이미지 표시 → tkinter 이벤트 루프 실행.

tkinter 역할: Tk()가 프로그램 윈도우, Label이 이미지 출력 담당, bind()를 통해 키 이벤트 처리, mainloop()가 GUI 작동 유지.

키 이벤트 처리: 방향키 오른쪽 누르면 next_image(), 왼쪽 누르면 prev_image() 호출해 인덱스 이동, 이미지를 재표시.'''


'''1. Tkinter란 무엇인가?
Tkinter 는 Python에 내장된 GUI(그래픽 사용자 인터페이스) 라이브러리입니다.

사용자가 마우스, 키보드 등으로 조작할 수 있는 창(window), 버튼, 텍스트, 이미지 등 다양한 UI(사용자 인터페이스) 위젯(widget)을 만들 수 있습니다.

GUI 프로그램의 기본은 이벤트(event) 기반의 반복 루프를 돌면서 사용자의 행동(입력 이벤트)을 처리하는 것입니다.

Tkinter는 Tcl/Tk 툴킷의 Python 바인딩으로 작동하며, Windows, macOS, Linux 등 대부분 OS에서 사용 가능합니다.

2. GUI 프로그램의 기본 구성 요소
2.1 루트 윈도우 (Root Window)
Tk() 클래스를 호출하여 생성합니다.

모든 위젯은 이 루트 윈도우 내에 포함되어 화면에 표시됩니다.

보통 프로그램에서 하나만 만들어 사용합니다.

python
root = Tk()  # GUI 프로그램 창 생성
root.title('윈도우 제목')  # 창의 제목 설정
2.2 위젯 (Widget)
사용자가 볼 수 있는 요소(버튼, 레이블, 입력창, 이미지 등)

생성 후 위치와 크기를 지정해야 보임

대표적으로 Label(텍스트, 이미지 표시), Button(버튼), Entry(입력창) 등이 있음

python
label = Label(root, text='안녕하세요')
label.pack()  # 창에 위젯을 배치(보여주기)
pack(), grid(), place() 등 다양한 방법으로 위젯 위치 지정 가능

간단한 프로그램 대부분 pack() 많이 사용

2.3 이벤트 바인딩 (Event Binding)
사용자의 입력(키보드, 마우스 등) 이벤트에 반응하는 동작을 지정

bind() 함수로 이벤트와 처리할 함수를 연결함

python
def on_key(event):
    print(event.keysym)  # 누른 키보드 키 이름 출력

root.bind('<Key>', on_key)  # 키보드 이벤트 바인딩
3. 예제 프로젝트: CCTV 이미지 뷰어 만들기
3.1 프로젝트 흐름 요약
CCTV.zip 압축 파일을 해제해서 CCTV 폴더를 만듦

CCTV 폴더 내 이미지 파일 목록을 불러와 정렬

Tkinter 윈도우를 띄우고 첫 번째 이미지를 출력

방향키 ←/→ 로 이전, 다음 이미지 보기 기능 구현

3.2 필요한 라이브러리 임포트
python
import os  # 운영체제 파일/폴더 기능 제어
import zipfile  # ZIP 압축 해제 기능 제공
from tkinter import Tk, Label, PhotoImage  # tkinter GUI용 필수 모듈
os: 파일 경로 읽기, 존재 여부 검사, 폴더 리스트 조회 등 운영체제 연동 작업

zipfile: ZIP 압축 파일을 읽고 해제

tkinter: GUI 윈도우 생성, 이미지 위젯 선언을 위한 함수/클래스 제공

3.3 이미지 헬퍼 클래스 (이미지 파일 관리)
python
class MasImageHelper:
    def __init__(self, folder_path):
        # 폴더 내 이미지 파일(확장자 필터 추가)을 정렬해 읽음
        self.folder_path = folder_path
        self.images = sorted([f for f in os.listdir(folder_path)
                              if f.lower().endswith(('.png', '.gif', '.ppm', '.pgm'))])
        self.index = 0  # 현재 이미지 인덱스 초기값 = 0
        self.photo = None  # tkinter에 보일 이미지 객체 저장용 변수

    def get_current_image_path(self):
        # 현재 인덱스의 이미지 전체 경로 반환, 이미지가 없으면 None 반환
        if self.images:
            return os.path.join(self.folder_path, self.images[self.index])
        return None

    def next_image(self):
        # 인덱스를 1 증가시키고 순환하며 다음 이미지 경로 반환
        if self.images:
            self.index = (self.index + 1) % len(self.images)
            return self.get_current_image_path()
        return None

    def prev_image(self):
        # 인덱스를 1 감소시키고 순환하며 이전 이미지 경로 반환
        if self.images:
            self.index = (self.index - 1) % len(self.images)
            return self.get_current_image_path()
        return None
정렬된 이미지 리스트를 만들고,

현재 보여줄 인덱스 값을 유지하며 이동함

이미지 경로만 반환하는 일은 GUI와 분리해 재사용 가능하게 관리하는 좋은 코딩 방법

3.4 ZIP 압축 해제 함수
python
def extract_zip(zip_path, extract_to):
    if not os.path.exists(extract_to):  # 이미 폴더 있으면 재해제 방지
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)  # 압축 해제
초기 실행 시 압축을 풀어 이미지 원본 준비

os.path.exists로 중복해제 방지

3.5 메인 실행 함수 (GUI, 이벤트 처리)
python
def main():
    zip_path = 'CCTV.zip'
    extract_folder = 'CCTV'

    extract_zip(zip_path, extract_folder)  # 압축 풀기

    img_helper = MasImageHelper(extract_folder)  # 이미지 관리 객체 생성

    root = Tk()  # tkinter 윈도우 생성
    root.title('CCTV Image Viewer')  # 윈도우 제목 설정

    label = Label(root)  # 이미지를 띄울 레이블 위젯 생성
    label.pack()  # 위젯 배치 (자동 위치 지정)

    def show_image(img_path):
        # 주어진 이미지 경로로 PhotoImage 객체 만들고 라벨에 적용
        img_helper.photo = PhotoImage(file=img_path)
        label.config(image=img_helper.photo)

    def on_key(event):
        # 키보드 누름 이벤트 함수: 방향키에 따라 이미지 전환
        if event.keysym == 'Right':
            img_path = img_helper.next_image()
            if img_path:
                show_image(img_path)
        elif event.keysym == 'Left':
            img_path = img_helper.prev_image()
            if img_path:
                show_image(img_path)

    root.bind('<Key>', on_key)  # 모든 키 입력 이벤트를 on_key 함수에 연결

    first_img = img_helper.get_current_image_path()  # 첫 이미지 경로
    if first_img:
        show_image(first_img)
    else:
        label.config(text='이미지를 찾을 수 없습니다.')  # 이미지가 없으면 메시지 표시

    root.mainloop()  # GUI 이벤트 루프 진입, 이벤트 대기 및 처리 시작

if __name__ == '__main__':
    main()
4. GUI 핵심 작동 프로세스
Tk() 객체는 GUI 창을 띄우는 가장 상위 컨테이너 역할

Label() 은 이미지나 텍스트를 표시하는 위젯, pack() 메서드로 화면에 배치

PhotoImage 로 이미지 파일을 읽어 GUI에 표시

root.bind('<Key>', on_key) 는 키보드 이벤트가 발생하면 on_key 함수를 호출하도록 연결

mainloop() 는 프로그램이 종료될 때까지 이벤트를 계속 대기 및 수행

5. 이벤트 처리 작동 원리
사용자가 방향키를 누르면 on_key 함수가 실행되어 입력된 키(event.keysym)를 확인

오른쪽 키면 img_helper.next_image() 호출해 이미지 인덱스를 이동시키고 다음 이미지 경로 받아옴

받은 이미지 경로로 show_image 함수 호출해 이미지 객체 생성 및 라벨에 표시

이렇게 키 입력에 의해 화면 속 이미지가 바뀌는 동작을 구현

6. 요약 및 학습 포인트
Python은 기본 라이브러리로 tkinter GUI를 쉽게 만들 수 있다.

GUI는 윈도우(창), 위젯(요소), 이벤트(사용자 입력)로 구성됨을 이해

tkinter는 Tk(), Label(), PhotoImage, bind(), mainloop() 가 핵심 함수/클래스 임

파일 IO와 이미지 관리 기능을 클래스로 분리하여 코드 재사용성 높임

이벤트 바인딩으로 사용자 입력에 실시간 반응 구현 가능

프로그램 진입점인 if __name__ == '__main__' 은 Python 스크립트 실행 관례'''
