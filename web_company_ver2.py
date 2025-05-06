from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd
import os

def crawl_company_info(csv_file):
    """ 채용공고 CSV를 기반으로 기업 정보를 크롤링하여 CSV로 저장하는 함수 """

    if not os.path.exists(csv_file):
        print(f"❌ 파일을 찾을 수 없습니다: {csv_file}")
        return None

    company_df = pd.read_csv(csv_file)  # CSV 파일 읽기

    # Selenium WebDriver 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    total_company_data = []

    for idx, row in company_df.iterrows():
        company_name = row['회사명']
        company_url = row['링크']

        driver.get(company_url)  # 기업 상세 페이지 접속
        company_data = [company_name]

        try:
            in_company_url = driver.find_element(By.XPATH, '//*[@id="content"]/div[3]/section[1]/div[1]/div[1]/div[1]/div[1]/a[1]').get_attribute('href')
            driver.get(in_company_url)

            html = urlopen(in_company_url)
            soup = BeautifulSoup(html, 'html.parser')

            # 기업 정보 수집
            업력 = soup.select_one('ul.company_summary strong.company_summary_tit')
            사원수 = soup.select_one('div.company_details_group p')
            업종 = soup.select_one('div.company_details_group dt.tit:contains("업종") + dd')
            사업내용 = soup.select_one('div.company_details_group dt.tit:contains("사업내용") + dd p')

            company_data.extend([
                업력.text.strip() if 업력 else '',
                사원수.text.strip() if 사원수 else '',
                업종.text.strip() if 업종 else '',
                사업내용.text.strip() if 사업내용 else ''
            ])

        except NoSuchElementException:
            print(f"{company_name} 기업 정보 크롤링 실패")
            company_data.extend(['', '', '', ''])

        total_company_data.append(company_data)

    # CSV 저장
    output_file = "기업정보.csv"
    df = pd.DataFrame(total_company_data, columns=['기업명', '업력', '사원수', '업종', '사업내용'])
    df.to_csv(output_file, encoding="utf-8-sig", index=False)

    driver.quit()
    print(f"✅ 기업정보 CSV 저장 완료: {output_file}")
    return output_file
