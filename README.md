# Github 사용법
## Github Action 사용법 
	
	1. pytest 를 사용한 python test
    2. 테스트하고 싶은 파이썬 파일을 def 로 작성하고 파일 시작이름이 test_*.py 형식으로 하나더 작성함
    3. test_*.py 형식에  테스트하고 싶은 파일을 import 하여 def test 정의하여 저장함 
    4. 그럼 깃허브액션 워크플로우에서 test_ 을 인식하여 def 테스트해줌 (pytest 모듈)
    5. 필요한 모듈은 requirements에 저장해서 의존성 캐싱

### 예시
    
    협업 메인 파이썬 파일 

```python

# mathadd.py
def add_numbers(a, b):
    return a + b
```
    
    pull_request를 위한 test 파이썬 파일 def  3개  테스트함 
    
```python

# test_math.py
    
from mathadd import add_numbers
    
def test_add_positive():
    assert add_numbers(1, 2) == 3

def test_add_zero():
    assert add_numbers(1, 0) == 1

def test_add_negative():
    assert add_numbers(4, -100) == -96

```

  기존파일을 수정하면서   위에처럼 자기가만든 기능은 test에 추가할것을 권장


## main Branch

	1. main 옆에 화살표 눌려서 view all branch 클릭
	2. 그리고 new branch로 자기꺼 branch 만들기
	3. main 을 기준으로만들면 main 파일을 그대로 가져와서 만들어짐
	4. 자기가 만든 기능을 다완성시 pull request 을 눌려서, new pull request 누르고  base: main <- compare: private branch  로 설정
	5. merge 요청시 github action 실행
	6. github action 에러없으면 merge commit 이후 자기 브랜치 제거 
	7. 새로운기능을 만들고자 다시 작업시 1번부터 재반복

궁금한 사항은 Slack
