import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import csv
import os
import tkinter

global canvas

# == 아티팩트 함수 ==========================================================================================================================
def memory_dump_func():
    file_name = 'memory_dump.csv'

    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        return list(reader)

def prefetch_func():
    file_name = 'prefetch.csv'

    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        return list(reader)

def NTFS_func():
    return ["항목1", "항목2", "항목3"]


def sys_info_func():
    return []

def regi_hive():
    return ["1232"]

def event_viewer_log_func():
    return 1

def enviornment_func():
    return 1

def patch_list_func():
    return 1

def process_list_info_func():
    return 1

def connection_info_func():
    return 1

def ip_setting_info_func():
    return 1

def ARP_info_func():
    return 1

def NetBIOS_info_func():
    return 1

def open_handle_info_func():
    return 1

def work_schedule_info_func():
    return 1

def sys_logon_info_func():
    return 1

def regi_service_info_func():
    return 1

def recent_act_info_func():
    return 1

def userassist_func():
    return 1

def autorun_func():
    return 1

def registry_func():
    return 1

def browser_info_func():
    return 1

def bin_func():
    return 1

def powershell_log_func():
    return 1

def lnk_files_func():
    return 1



# == 아티팩트 함수 ==========================================================================================================================
artifact_functions = {
    "메모리 덤프": memory_dump_func,
    "Prefetch" : prefetch_func,
    "NTFS 아티팩트" : NTFS_func,
    "시스템 정보" : sys_info_func,
    "레지스트리 하이브" : regi_hive,
    "이벤트 뷰어 로그" : event_viewer_log_func,
    "환경 변수" : enviornment_func,
    "패치 리스트" : patch_list_func,
    "실행 프로세스 목록 정보" : process_list_info_func,
    "연결 정보 (열려진 포트)" : connection_info_func,
    "IP 설정 정보" : ip_setting_info_func,
    "ARP 정보" : ARP_info_func,
    "NetBIOS 정보" : NetBIOS_info_func,
    "열려있는 핸들 정보" : open_handle_info_func,
    "작업 스케줄 정보" : work_schedule_info_func,
    "시스템 로그온 정보" : sys_logon_info_func,
    "등록된 서비스 정보" : regi_service_info_func,
    "최근 활동 정보" : recent_act_info_func,
    "UserAssist" : userassist_func,
    "AutoRun" : autorun_func,
    "레지스트리" : registry_func,
    "브라우저 기록" : browser_info_func,
    "휴지통" : bin_func,
    "파워쉘 로그" : powershell_log_func,
    "최근 LNK 파일" : lnk_files_func
}


# 아티팩트 별 검색 기능
def search_in_treeview(tree, query, header_name, header_map, search_results):
    search_results.clear()

    if header_name == '전체':
        search_columns = range(len(tree['columns']))
    else:
        search_columns = [header_map[header_name]]

    for item in tree.get_children():
        if any(query.lower() in str(tree.item(item, 'values')[col]).lower() for col in search_columns):
            tree.item(item, tags=('found',))
            search_results.append(item)
        else:
            tree.item(item, tags=('not_found',))



def navigate_search_results(tree, search_results, direction):
    if not search_results:
        return

    current_item = tree.focus()
    next_item = None

    if direction == "up":
        previous_items = [item for item in search_results if tree.index(item) < tree.index(current_item)]
        if previous_items:
            next_item = previous_items[-1]

    elif direction == "down":
        next_items = [item for item in search_results if tree.index(item) > tree.index(current_item)]
        if next_items:
            next_item = next_items[0]

    if next_item:
        tree.selection_set(next_item)
        tree.focus(next_item)
        tree.see(next_item)  





# 결과 리스트 토글 기능
def toggle_items(frame):
    frame.pack_forget() if frame.winfo_viewable() else frame.pack(side='top', fill='x', padx=5, pady=5)

# 결과 프레임 출력
def create_result_frame(parent, title, items):
    frame = tk.Frame(parent, relief='solid', borderwidth=2, background='white')
    frame.pack(side='top', fill='x', padx=5, pady=5)

    title_frame = tk.Frame(frame, background='#D6D5CB')
    title_frame.pack(side='top', fill='x')
    title_label = tk.Label(title_frame, text=title, font=('Arial', 10), background='#D6D5CB', anchor='w')
    title_label.pack(side='left', padx=5, pady=5)

    items_frame = tk.Frame(frame, background='white')
    items_frame.pack(side='top', fill='x', padx=5, pady=5)

    if not isinstance(items, list):
        items = [items]

    if len(items) > 0 and all(isinstance(item, list) for item in items):
        search_results = []
        header_map = {name: index for index, name in enumerate(items[0])}
        search_frame = tk.Frame(frame)
        search_frame.pack(side='top', fill='x', padx=5, pady=5)

        header_options = ['전체'] + items[0]
        header_combobox = ttk.Combobox(search_frame, values=header_options, state="readonly")
        header_combobox.current(0)
        header_combobox.pack(side='left', padx=5, pady=5)

        # 검색창 및 검색 버튼
        search_entry = tk.Entry(search_frame)
        search_entry.pack(side='left', padx=5, pady=5)
        search_button = tk.Button(search_frame, text="검색", command=lambda: search_in_treeview(tree, search_entry.get(), header_combobox.get(), header_map))
        search_button.pack(side='left', padx=5, pady=5)

        up_button = tk.Button(search_frame, text="위", command=lambda: navigate_search_results(tree, search_results, "up"))
        up_button.pack(side='left', padx=5, pady=5)

        down_button = tk.Button(search_frame, text="아래", command=lambda: navigate_search_results(tree, search_results, "down"))
        down_button.pack(side='left', padx=5, pady=5)

        # 필터링 버튼 추가
        filter_button = tk.Button(search_frame, text="필터링", command=lambda: show_filter_window(items[0], tree))
        filter_button.pack(side='left', padx=5, pady=5)

        search_button.config(command=lambda: search_in_treeview(tree, search_entry.get(), header_combobox.get(), header_map, search_results))


        # Treeview 위젯 생성 및 설정
        tree = ttk.Treeview(items_frame, columns=[str(i) for i in range(len(items[0]))], show='headings')
        tree.pack(side='left', fill='both', expand=True)

        for i, title in enumerate(items[0]):
            tree.heading(str(i), text=title)
            tree.column(str(i), width=100, minwidth=50, anchor=tk.W)

        for row in items[1:]:
            tree.insert('', 'end', values=row)

        scrollbar = ttk.Scrollbar(items_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)

        tree.tag_configure('found', background='yellow')
        tree.tag_configure('not_found', background='white')

    else:
        for item in items:
            item_label = tk.Label(items_frame, text=item, background='white')
            item_label.pack(side='top', anchor='w', padx=5, pady=2)

    title_frame.bind("<Button-1>", lambda e: toggle_items(items_frame))
    title_label.bind("<Button-1>", lambda e: toggle_items(items_frame))

    return frame







# 필터링 창 생성 및 설정
def show_filter_window(headers, tree):
    filter_window = tk.Toplevel(app)
    filter_window.title("필터 설정")
    filter_window.geometry("330x400")
    filter_window.resizable(False, False)

    filter_frame = tk.Frame(filter_window)
    filter_frame.pack(fill='both', expand=True, padx=5, pady=5)

    button_frame = tk.Frame(filter_window)
    button_frame.pack(side='top', pady=5)

    # 조건추가 버튼
    add_condition_button = tk.Button(filter_window, text="조건추가", command=lambda: add_filter_condition(filter_frame, headers, tree))
    add_condition_button.pack(side='top', pady=5)

    # 필터링 적용 버튼에 트리 뷰 전달
    apply_button = tk.Button(button_frame, text="적용", command=lambda: apply_filters(tree, headers, filter_window))
    apply_button.pack(side='left', padx=5)

    # 필터링 조건 추가 함수를 처음에 한 번 호출하여 초기 조건을 설정합니다.
    add_filter_condition(filter_frame, headers, tree)


filter_conditions = []
def add_filter_condition(filter_frame, headers, tree):
    # 새로운 필터링 조건을 위한 프레임 생성
    condition_frame = tk.Frame(filter_frame)
    condition_frame.pack(fill='x', padx=5, pady=5)

    # 헤더 선택을 위한 콤보박스
    header_options = ["전체"] + headers
    header_combobox = ttk.Combobox(condition_frame, values=header_options, state="readonly", width=10)
    header_combobox.pack(side='left', padx=5)
    header_combobox.current(0)

    # 필터링 내용을 입력할 입력 필드
    filter_entry = ttk.Entry(condition_frame, width=20)
    filter_entry.pack(side='left', padx=5)
    

    # 삭제 버튼 추가
    def delete_condition():
        condition_frame.destroy()

    delete_button = tk.Button(condition_frame, text="X", command=delete_condition)
    delete_button.pack(side='right', padx=5)

    # 필터링 조건 저장을 위한 딕셔너리
    condition = {
        "header_combobox": header_combobox,
        "filter_entry": filter_entry,
    }
    filter_conditions.append(condition)



def apply_filters(tree, headers, filter_window):
    for item in tree.get_children():
        tree.item(item, tags=('default',))

    for item in tree.get_children():
        item_values = tree.item(item, 'values')
        match = True

        for condition in filter_conditions:
            try:
                header = condition["header_combobox"].get()
                value = condition["filter_entry"].get().lower()

                header_index = headers.index(header) if header != "전체" else None

                if header_index is not None:
                    if value not in item_values[header_index].lower():
                        match = False
                        break
                else:
                    if not any(value in str(v).lower() for v in item_values):
                        match = False
                        break
            except tkinter.TclError:
                # 위젯이 더 이상 유효하지 않음
                continue

        if not match:
            tree.item(item, tags=('not_found',))
        else:
            tree.item(item, tags=('found',))

    tree.tag_configure('found', background='white')
    tree.tag_configure('not_found', background='lightgray')
    tree.tag_configure('default', background='white')

    filter_window.destroy()












# 결과 창 스크롤 마우스 휠 연동
def on_mousewheel(event):
    global canvas
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")



def move_to_frame():
    selected_artifact = selected_combobox.get()
    if selected_artifact in artifact_frames:
        y_position = artifact_frames[selected_artifact]
        
        # 캔버스 스크롤 영역의 높이를 가져옴
        scrollregion = canvas.cget("scrollregion").split()
        if scrollregion:
            scrollregion_height = int(scrollregion[3])

            # 프레임의 상대적 위치 계산
            relative_position = y_position / scrollregion_height

            # 캔버스 스크롤
            canvas.yview_moveto(relative_position)



def start_capture():
    global case_ref_label, case_ref_entry, options_frame, output_label, output_entry, browse_button, start_button, artifact_label, canvas, fixed_frame, selected_combobox, artifact_frames
    # 기존 위젯 숨기기
    case_label.grid_forget()
    case_ref_entry.grid_forget()
    options_frame.grid_forget()
    output_label.grid_forget()
    output_entry.grid_forget()
    browse_button.grid_forget()
    start_button.grid_forget()
    artifact_label.grid_forget()



    case_ref = case_ref_entry.get()

    # 고정 콤보박스를 위한 새 프레임 생성
    fixed_frame = tk.Frame(app, background='#f0f0f0')
    fixed_frame.grid(row=0, column=0, columnspan=3, sticky='ew')

    move_button = ttk.Button(fixed_frame, text="이동", command=move_to_frame)
    move_button.grid(row=0, column=1, padx=5, pady=5)

    # 선택된 체크박스 목록 생성
    selected_options = [option for option in options if variables[option].get()]
    
    # 콤보박스 생성 및 설정
    selected_combobox = ttk.Combobox(fixed_frame, values=selected_options, state="readonly")
    selected_combobox.grid(row=0, column=0, padx=5, pady=5)

    # 스크롤 가능한 프레임
    canvas = tk.Canvas(app, borderwidth=0, background="#ffffff", height=550, width=780)
    scrollbar = tk.Scrollbar(app, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=3, column=1, sticky='ns')
    canvas.grid(row=2, column=0, sticky="nsew")
    canvas.bind_all("<MouseWheel>", on_mousewheel)


    # 캔버스 안에 결과 프레임 배치
    result_container = tk.Frame(canvas, background='white')
    canvas.create_window((0, 0), window=result_container, anchor="nw")
    result_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


    case_ref_label = tk.Label(result_container, text="케이스 참조: {}".format(case_ref), font=('Arial', 12), background='white', anchor='w', width=85)
    case_ref_label.pack(side='top', fill='x', padx=5, pady=5)


    artifact_frames = {}
    y_position = 0
    for option in options:
        if variables[option].get() and option in artifact_functions:
            function = artifact_functions[option]
            result_items = function()
            frame = create_result_frame(result_container, option, result_items)
            frame.pack(side='top', fill='x', padx=5, pady=5)

            # Tkinter 윈도우 갱신
            app.update_idletasks()

            # 프레임의 실제 높이 계산
            frame_height = frame.winfo_height()
            artifact_frames[option] = y_position
            y_position += frame_height





# == 시작 페이지 ==================================================================================================================================


# 파일 위치 찾아보기 함수
def browse_output_directory():
    directory = filedialog.askdirectory()
    if directory:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, directory)


# UI 창 구성 / 스타일
app = tk.Tk()
app.title('데이터 수집 도구')
app.geometry("800x600")
app.resizable(False, False)
app['bg'] = '#f0f0f0'
style = ttk.Style()
style.theme_use('clam')



# 사례 참조 섹션
case_label = ttk.Label(app, text="케이스 번호 / 참조:", background='#f0f0f0')
case_label.grid(row=0, column=0, padx=5, pady=10)
case_ref_entry = ttk.Entry(app)
case_ref_entry.grid(row=0, column=1, padx=5, pady=10, columnspan=2, sticky='ew')


# 수집 옵션 섹션
artifact_label = ttk.Label(app, text="탐지할 아티팩트 선택", background='#f0f0f0', font=('Arial', 10))
artifact_label.grid(row=1, column=0, columnspan=1, padx=5, pady=(50, 1))
options_frame = ttk.Frame(app, relief='solid', borderwidth=2)
options_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=1, sticky='ew')


# 모두 선택 함수
def select_all():
    for option in options:
        variables[option].set(select_all_var.get())

# 각 체크박스와 변수 초기화
checkbuttons = {}
variables = {}
options = [
    "메모리 덤프",
    "Prefetch", 
    "NTFS 아티팩트", 
    "시스템 정보",
    "레지스트리 하이브",
    "이벤트 뷰어 로그",
    "SRUM, Hosts 및 서비스",
    "환경 변수",
    "패치 리스트",
    "실행 프로세스 목록 정보",
    "연결 정보 (열려진 포트)",
    "IP 설정 정보",
    "ARP 정보",
    "NetBIOS 정보",
    "열려있는 핸들 정보",
    "작업 스케줄 정보",
    "시스템 로그온 정보",
    "등록된 서비스 정보",
    "최근 활동 정보",
    "UserAssist",
    "AutoRun",
    "레지스트리",
    "브라우저 기록",
    "휴지통",
    "파워쉘 로그",
    "최근 LNK 파일"
    ]
for i, option in enumerate(options):
    variables[option] = tk.BooleanVar()
    checkbuttons[option] = ttk.Checkbutton(options_frame, text=option, variable=variables[option])
    checkbuttons[option].grid(row=i // 5, column=i % 5, padx=3, pady=2, sticky='w')

# 프레임 내의 각 열에 가중치 설정
for i in range(5):
    options_frame.grid_columnconfigure(i, weight=1)

# 모두 선택 기능
select_all_var = tk.BooleanVar()
select_all_checkbox = ttk.Checkbutton(options_frame, text="모두 선택", variable=select_all_var, command=select_all)
select_all_checkbox.grid(row=100, column=4, padx=3, pady=2, sticky='e')



# 출력 저장 위치 설정
output_label = ttk.Label(app, text="출력 저장 위치:", background='#f0f0f0')
output_label.grid(row=1000, column=0, padx=5, pady=100, sticky='e')
output_entry = ttk.Entry(app)
output_entry.grid(row=1000, column=1, padx=5, pady=100, sticky='ew')
browse_button = ttk.Button(app, text="찾아보기", command=browse_output_directory)
browse_button.grid(row=1000, column=2, padx=(5, 30), pady=100)



# 캡처 시작 버튼
start_button = ttk.Button(app, text="캡처 시작", command=start_capture)
start_button.grid(row=1001, column=0, columnspan=3, padx=5, pady=20)



result_label = tk.Label(app, justify=tk.LEFT, anchor='w')
result_label.grid(row=1002, column=0, columnspan=3, padx=5, pady=20)


app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(1, weight=1)
app.mainloop()
