from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QApplication, QWidget,
        QHBoxLayout, QVBoxLayout,
        QGroupBox, QButtonGroup, QRadioButton,
        QPushButton, QLabel, QStackedWidget)
from random import shuffle


class Question():
    '''contains a question, a correct answer and three incorrect ones'''
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3


# ===================== DAFTAR SOAL =====================
# Tambah/kurangi soal di sini — jumlah soal akan menyesuaikan otomatis
questions_list = []
questions_list.append(Question('Perintah looping dengan parameter adalah?', 'for', 'while', 'if', 'def'))
questions_list.append(Question('Tipe data logika disebut?', 'Boolean', 'Float', 'String', 'Set'))
questions_list.append(Question('Variabel suatu object class disebut?', 'Property', 'Method', 'Function', 'List'))
# ========================================================


app = QApplication([])

# ── Halaman 1: Quiz ──────────────────────────────────────────────────────────

btn_OK = QPushButton('Jawab')
lb_Question = QLabel('Memuat soal...')
lb_Question.setWordWrap(True)
lb_Question.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

lb_Progress = QLabel('')  # nomor soal, mis. "Soal 1 / 3"
lb_Progress.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

RadioGroupBox = QGroupBox("Pilihan Jawaban")

rbtn_1 = QRadioButton('Opsi 1')
rbtn_2 = QRadioButton('Opsi 2')
rbtn_3 = QRadioButton('Opsi 3')
rbtn_4 = QRadioButton('Opsi 4')

RadioGroup = QButtonGroup()
RadioGroup.addButton(rbtn_1)
RadioGroup.addButton(rbtn_2)
RadioGroup.addButton(rbtn_3)
RadioGroup.addButton(rbtn_4)

layout_ans1 = QHBoxLayout()
layout_ans2 = QVBoxLayout()
layout_ans3 = QVBoxLayout()
layout_ans2.addWidget(rbtn_1)
layout_ans2.addWidget(rbtn_2)
layout_ans3.addWidget(rbtn_3)
layout_ans3.addWidget(rbtn_4)
layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3)
RadioGroupBox.setLayout(layout_ans1)

AnsGroupBox = QGroupBox("Hasil")
lb_Result = QLabel('')
lb_Correct = QLabel('')
lb_Correct.setAlignment(Qt.AlignHCenter)

layout_res = QVBoxLayout()
layout_res.addWidget(lb_Result, alignment=(Qt.AlignLeft | Qt.AlignTop))
layout_res.addWidget(lb_Correct, alignment=Qt.AlignHCenter, stretch=2)
AnsGroupBox.setLayout(layout_res)

layout_line0 = QHBoxLayout()   # progress label (paling atas, kiri)
layout_line1 = QHBoxLayout()   # pertanyaan
layout_line2 = QHBoxLayout()   # pilihan / hasil
layout_line3 = QHBoxLayout()   # tombol

layout_line0.addWidget(lb_Progress)
layout_line0.addStretch(1)

layout_line1.addWidget(lb_Question)

layout_line2.addWidget(RadioGroupBox)
layout_line2.addWidget(AnsGroupBox)
AnsGroupBox.hide()

layout_line3.addStretch(1)
layout_line3.addWidget(btn_OK, stretch=2)
layout_line3.addStretch(1)

quiz_widget = QWidget()
layout_quiz = QVBoxLayout()
layout_quiz.addLayout(layout_line0, stretch=1)
layout_quiz.addLayout(layout_line1, stretch=2)
layout_quiz.addLayout(layout_line2, stretch=8)
layout_quiz.addStretch(1)
layout_quiz.addLayout(layout_line3, stretch=1)
layout_quiz.addStretch(1)
layout_quiz.setSpacing(5)
quiz_widget.setLayout(layout_quiz)

# ── Halaman 2: Finish ────────────────────────────────────────────────────────

finish_widget = QWidget()
layout_finish = QVBoxLayout()
layout_finish.setAlignment(Qt.AlignCenter)

lb_finish_title = QLabel('🎉 Kuis Selesai!')
lb_finish_title.setAlignment(Qt.AlignCenter)
lb_finish_title.setStyleSheet('font-size: 22px; font-weight: bold; margin-bottom: 8px;')

lb_finish_score = QLabel('')
lb_finish_score.setAlignment(Qt.AlignCenter)
lb_finish_score.setStyleSheet('font-size: 18px; margin-bottom: 4px;')

lb_finish_pct = QLabel('')
lb_finish_pct.setAlignment(Qt.AlignCenter)
lb_finish_pct.setStyleSheet('font-size: 14px; color: gray;')

lb_finish_grade = QLabel('')
lb_finish_grade.setAlignment(Qt.AlignCenter)
lb_finish_grade.setStyleSheet('font-size: 15px; margin-top: 8px;')

btn_restart = QPushButton('Ulangi Kuis')
btn_restart.setFixedWidth(160)

layout_finish.addStretch(2)
layout_finish.addWidget(lb_finish_title)
layout_finish.addWidget(lb_finish_score)
layout_finish.addWidget(lb_finish_pct)
layout_finish.addWidget(lb_finish_grade)
layout_finish.addSpacing(16)
layout_finish.addWidget(btn_restart, alignment=Qt.AlignHCenter)
layout_finish.addStretch(3)
finish_widget.setLayout(layout_finish)

# ── Stack: gabungkan dua halaman ─────────────────────────────────────────────

stack = QStackedWidget()
stack.addWidget(quiz_widget)    # index 0 → quiz
stack.addWidget(finish_widget)  # index 1 → finish

# ── State ─────────────────────────────────────────────────────────────────────

answers = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]

state = {
    'score': 0,
    'current_index': 0,        # indeks dalam shuffled_questions
    'shuffled_questions': [],
    'awaiting_next': False,    # True = sudah jawab, menunggu "Lanjut"
}


# ── Helper ────────────────────────────────────────────────────────────────────

def reset_radio():
    RadioGroup.setExclusive(False)
    for btn in [rbtn_1, rbtn_2, rbtn_3, rbtn_4]:
        btn.setChecked(False)
    RadioGroup.setExclusive(True)


def show_quiz_panel():
    RadioGroupBox.show()
    AnsGroupBox.hide()
    btn_OK.setText('Jawab')


def show_result_panel(result_text):
    RadioGroupBox.hide()
    AnsGroupBox.show()
    btn_OK.setText('Lanjut')
    lb_Result.setText(result_text)


def show_finish():
    total = len(state['shuffled_questions'])
    score = state['score']
    pct = score / total * 100 if total else 0

    if pct == 100:
        grade = '⭐ Sempurna! Luar biasa!'
    elif pct >= 80:
        grade = '👍 Bagus sekali!'
    elif pct >= 60:
        grade = '😊 Cukup baik, terus belajar!'
    elif pct >= 40:
        grade = '😅 Perlu lebih banyak latihan.'
    else:
        grade = '💪 Jangan menyerah, coba lagi!'

    lb_finish_score.setText(f'Skor: {score} / {total}')
    lb_finish_pct.setText(f'({pct:.0f}%)')
    lb_finish_grade.setText(grade)
    stack.setCurrentIndex(1)


def load_question(idx):
    q = state['shuffled_questions'][idx]
    total = len(state['shuffled_questions'])
    lb_Progress.setText(f'Soal {idx + 1}/{total}  ')

    shuffle(answers)
    answers[0].setText(q.right_answer)
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)

    lb_Question.setText(q.question)
    lb_Correct.setText(f'Jawaban benar: {q.right_answer}')

    reset_radio()
    show_quiz_panel()
    state['awaiting_next'] = False


def start_quiz():
    shuffled = questions_list[:]
    shuffle(shuffled)
    state['shuffled_questions'] = shuffled
    state['score'] = 0
    state['current_index'] = 0
    state['awaiting_next'] = False
    stack.setCurrentIndex(0)
    load_question(0)


def click_OK():
    if not state['awaiting_next']:
        # --- fase jawab ---
        checked = next((b for b in answers if b.isChecked()), None)
        if checked is None:
            lb_Result.setText('⚠ Pilih salah satu jawaban!')
            AnsGroupBox.show()
            RadioGroupBox.show()   # biarkan pilihan tetap terlihat
            btn_OK.setText('Jawab')
            return

        if answers[0].isChecked():
            state['score'] += 1
            show_result_panel('✅ Benar!')
        else:
            show_result_panel('❌ Salah!')

        state['awaiting_next'] = True

    else:
        # --- fase lanjut ---
        next_idx = state['current_index'] + 1
        if next_idx < len(state['shuffled_questions']):
            state['current_index'] = next_idx
            load_question(next_idx)
        else:
            show_finish()


btn_OK.clicked.connect(click_OK)
btn_restart.clicked.connect(start_quiz)

# ── Window ────────────────────────────────────────────────────────────────────

window = QWidget()
main_layout = QVBoxLayout()
main_layout.setContentsMargins(0, 0, 0, 0)
main_layout.addWidget(stack)
window.setLayout(main_layout)
window.setWindowTitle('Memo Card')
window.resize(420, 300)

start_quiz()
window.show()
app.exec()