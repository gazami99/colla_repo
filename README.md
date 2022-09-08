## 깃허브 사용법
### 파이썬 
	
	1. pytest 를 사용한 python test
    2. 테스트하고 싶은 파이썬 파일을 def 로 작성하고 파일 시작이름이 test_*.py 형식으로 하나더 작성함
    3. test_*.py 형식에  테스트하고 싶은 파일을 import 하여 def test 정의하여 저장함 
    4. 그럼 깃허브액션 워크플로우에서 test_ 을 인식하여 def 테스트해줌 (pytest 모듈)
    5. 필요한 모듈은 requirements에 저장해서 의존성 캐싱

### 예시
    
    메인 파이썬

```python

# math.py
def add_numbers(a, b):
    return a + b
```
    
    pull_request를 위한 test 파이썬 파일 def  3개  테스트함 
    
```python

# test_math.py
    
from math import add_numbers
    
def test_add_positive():
    assert add_numbers(1, 2) == 3

def test_add_zero():
    assert add_numbers(1, 0) == 1

def test_add_negative():
    assert add_numbers(4, -100) == -96

```
