import requests
import xml.etree.ElementTree as ET

def get_marine_water_quality_xml():
    # API 엔드포인트 URL
    url = "https://apis.data.go.kr/1192000/OceansWemoObvpRtmInfoService/OceansWemoObvpRtmInfo"
    
    # 쿼리 파라미터 설정 (_type으로 변경)
    params = {
        "serviceKey": "55b9d25730fce5abb690fe93acc581312c7b5faa3d9e93fb9ea21da53a2a6e69",
        "pageNo": "1",          # 페이지 번호
        "numOfRows": "10",      # 한 페이지 결과 수
        "_type": "xml"          # 응답 데이터 형식 지정
    }

    try:
        # GET 요청 보내기
        response = requests.get(url, params=params)
        
        # 응답 코드가 200(성공)인지 확인
        if response.status_code == 200:
            try:
                # XML 데이터 파싱
                root = ET.fromstring(response.content)
                
                # 1. API 자체의 결과 코드 확인 (보통 "00"이 정상)
                result_code = root.find('.//resultCode')
                result_msg = root.find('.//resultMsg')
                
                if result_code is not None and result_code.text == "00":
                    print("데이터 조회 성공!\n")
                    
                    # 2. <item> 태그들을 찾아서 데이터 추출
                    items = root.findall('.//item')
                    
                    if not items:
                        print("조회된 데이터가 없습니다.")
                        return

                    for idx, item in enumerate(items, 1):
                        # 필요한 태그 이름에 맞춰서 가져오기
                        # XML 명세에 따라 rtmWqWtchDtlDt(관측일시), rtmWtchWtem(수온) 등을 추출
                        obs_time = item.findtext('rtmWqWtchDtlDt', default='정보없음')
                        water_temp = item.findtext('rtmWtchWtem', default='정보없음')
                        obs_name = item.findtext('obsrvtNm', default='관측소명 없음') # 관측소명 예시
                        
                        print(f"[{idx}] 관측소: {obs_name} | 관측일시: {obs_time} | 수온: {water_temp}℃")
                else:
                    # API 에러 응답 처리 (예: 인증키 오류, 트래픽 초과 등)
                    msg = result_msg.text if result_msg is not None else "알 수 없는 오류"
                    code = result_code.text if result_code is not None else "코드 없음"
                    print(f"API 응답 오류: {msg} (코드: {code})")
                    print("원본 XML 응답:\n", response.text)
                    
            except ET.ParseError:
                print("XML 파싱 에러. 응답 원본 텍스트:\n", response.text)
        else:
            print(f"API 요청 실패: HTTP 상태 코드 {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"요청 중 통신 오류 발생: {e}")

if __name__ == "__main__":
    get_marine_water_quality_xml()
