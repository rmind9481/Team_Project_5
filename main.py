import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QFileDialog, 
    QMessageBox, QTableWidget, QTableWidgetItem
)
import pandas as pd
from web_crawling_Function import make_CSV
from web_company_ver2 import crawl_company_info  # 기업정보 크롤링 함수 추가

class JobSearchApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('채용 공고 검색기')
        self.setGeometry(100, 100, 400, 800)

        # 검색어 입력창
        self.label = QLabel('검색어 입력:', self)
        self.search_input = QLineEdit(self)

        # 검색 버튼
        self.search_btn = QPushButton('검색', self)
        self.search_btn.clicked.connect(self.search_jobs)

        # 파일 열기 버튼
        self.open_file_btn = QPushButton('CSV 파일 열기', self)
        self.open_file_btn.clicked.connect(self.open_csv_file)

         # 기업정보 크롤링 버튼 추가
        self.company_crawl_btn = QPushButton('기업 정보 크롤링', self)
        self.company_crawl_btn.clicked.connect(self.get_company_info)

        # 기업정보 CSV 파일 열기 버튼
        self.open_company_btn = QPushButton('기업정보 CSV 열기', self)
        self.open_company_btn.clicked.connect(self.open_company_csv)

        # 테이블 위젯 추가 (기업 정보 표시용)
        self.table_widget = QTableWidget(self)

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.open_file_btn)
        layout.addWidget(self.company_crawl_btn)  # 기업 크롤링 버튼 추가
        layout.addWidget(self.open_company_btn)
        layout.addWidget(self.table_widget)

        self.setLayout(layout)

    def search_jobs(self):
        search_word = self.search_input.text().strip()
        if search_word:
            make_CSV(search_word)  # 크롤링 함수 실행
            QMessageBox.information(self, '완료', f'{search_word}_채용공고.csv 파일이 생성되었습니다!')
        else:
            QMessageBox.warning(self, '입력 오류', '검색어를 입력해주세요!')

    def open_csv_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'CSV 파일 열기', '', 'CSV Files (*.csv);;All Files (*)')

        if file_name:
            df = pd.read_csv(file_name)
            print(df.head())  # 콘솔에 출력 (GUI에 테이블로 표시 가능)
            QMessageBox.information(self, '파일 로드', f'{file_name} 파일을 열었습니다!')
    
    def get_company_info(self):
        """ 채용공고 CSV를 기반으로 기업 정보 크롤링 """
        output_file = crawl_company_info('./llm_채용공고.csv')  # 기업정보 크롤링 실행
        if output_file:
            QMessageBox.information(self, '완료', f'기업정보가 {output_file}로 저장되었습니다!')

    def open_company_csv(self):
        """ 기업정보 CSV 파일을 선택하고 테이블에 표시 """
        file_name, _ = QFileDialog.getOpenFileName(self, '기업정보 CSV 파일 열기', '', 'CSV Files (*.csv);;All Files (*)')

        if file_name:
            df = pd.read_csv(file_name)
            self.display_data_in_table(df)

            
    def display_data_in_table(self, df):
        """ DataFrame을 PyQt 테이블에 표시하는 함수 """
        self.table_widget.setRowCount(df.shape[0])
        self.table_widget.setColumnCount(df.shape[1])
        self.table_widget.setHorizontalHeaderLabels(df.columns)

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iat[row, col]))
                self.table_widget.setItem(row, col, item)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = JobSearchApp()
    ex.show()
    sys.exit(app.exec())



