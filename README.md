# saramin-crawler
사람인 채용공고 크롤러 만들어 보겠습니다. with Selenium 

## 개발동기
한남대학교 취업전략팀 근로장학생들은 매주 총 30개의 채용공고를 취합해서 제출해야한다.  
순진하던 2학년 때는 순순히 나의 손목을 혹사 시켰지만 더 이상 후퇴는 없다.  
세상에 치이다보니 어느덧 3학년 3학기! 이제는 파이썬을 활용해 업무 자동화를 꿈꿔본다.

## 개발환경
- Python 3.8.5
- Selenium 3.141.0
- BeautifulSoup4 4.9.1
- ChromeDriver 85.0.4183.83

## 예상동작
1. 프로그램 실행 시 URL 입력
2. URL에 존재하는 채용공고 리스트를 조건에 맞게 필터링
3. 필터링된 리스트를 크롤링
4. 크롤링한 데이터를 엑셀에 저장
5. 부서 선생님께 힘든 척하며 ~~징징대기~~ 생색내기

## 크롤링 조건
1. 지금 마감일이 10일 이상 여유가 있어야한다.
2. 지원 조건이 학사 이하여야 한다.

## 구현 중 어려운 사항 - 채용공고 디테일 페이지가 정형화 되어 있지 않다.
1. 예를들어 어떤 기업은 본문에 자체적인 채용공고 이미지를 업로드한다. (HTML TAG가 존재하지 않는 문제가 있다)  
2. 어떤 기업은 사람인이 제공하는 기본 양식에 맞춰서 성실하게 본문을 작성했다. (HTML TAG 존재)
3. 어떤 기업은 사람인이 제공하는 기본 양식이 아닌 자체적인 기준으로 본문을 작성했다. (HTML TAG 존재 하지만 기업들마다 다른 형태)

## 해결 방안 - 케이스를 나누자
if문과 try-catch문을 활용해서 각 케이스에만 존재하는 특성을 찾아내고 특성에 맞게 크롤링을 진행한다. 

## 예상되는 한계
완벽한 자동화를 꿈꿨으나 수작업을 피할 수는 없을 것 같다. 그래도 80%이상 자동화를 꿈꿔본다. 

## 여담
같이 근로하는 학생 2분이 계신데 모두 여성분이다.  
크롤링 제작을 통해 호의를 배풀고 저 푸른 초원위에 그림 같은 집을 짓고 아들에 손자까지 상상의 나래를 펼치며 **미연시 게임 ON...**
