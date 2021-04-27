from setting.card import *
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36",
    "Accept-Language": "ko",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
}
# 학교 당담자 부서, 이름 안내 문구 제공
def search_Parser():
    title = "부서 연락처 안내"
    description = "부서 연락처는 담당자의 \n이름, 부서(소속)로 확인해드릴 수 있어요. \n아래 항목에서 선택해주세요.😀"
    response = insert_card(title,description)
    response = insert_button_text(response,"이름","이름")
    response = insert_button_text(response, "부서(소속)", "부서(소속)")
    return response

# 학교 당담자 이름으로 검색
def search_member_Parser(content):
    content = content['action']['detailParams']['search_name']["value"]
    content = ''.join(str(e) for e in content)
    condition = 'name_kr'
    text = DU_search_Parser(content, condition)
    response = insert_text(text)
    return response

# 학교 당담자 부서로 섬색
def search_buseo_Parser(content):
    content = content['action']['detailParams']['search_name']["value"]
    content = ''.join(str(e) for e in content)
    condition = 'buseo'
    text = DU_search_Parser(content, condition)
    response = insert_text(text)
    return response

#이름 연락처 찾기 파싱
def DU_search_Parser(content,condition):
    try:
        url = 'https://www.daegu.ac.kr/customer/emp/list'
        response = requests.post(url=url, headers=headers, data={
            'searchCondition': condition,
            'searchKeyword': content,
            'noSubmit': ""
        })
        schedule = response.json()
        data = []
        if schedule != []:
            for a in schedule:
                data.append(
                    "이름 : " + a['name_kr'] +
                    "\n부서 : " + a['buseo'] +
                    "\n직책 : " + a['user_upmu'] +
                    "\n전화번호: 053-850-" + a['user_telno']+
                    "\n----------------------------------")

            member_text = '\n'.join(str(e) for e in data)
            text = "입력하신 " + content + " 담당자의\n연락처는 아래와 같습니다. \n\n----------------------------------\n" + member_text
        else:
            text = "입력하신 " + content + " 담당자의\n연락처는 아래와 같습니다. \n\n----------------------------------\n교내 전화번호 조회된 내용이 없습니다."

        return text
    except:
        pass