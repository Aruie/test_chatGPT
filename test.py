#%%
import markdown
from api import OpenaiChat

content = '```import numpy as np```'
markdown.markdown(content)


# %%
prompt = [
        # {'role':'system','content': 'You are a helper that input the survey and output the yaml format'},
        {'role':'system','content': '''You are a helper that input the survey text and output the yaml format
type is one of the (multi, yn, free)
        
input like this

Q2. 	귀하나 귀하의 가족 중 다음의 산업에 종사하시는 분이 계십니까?
광고대행사 	1  
시장조사 	2
언론/TV/라디오 	3	→ 중단하시오

Q3. 
...

output like this

data:
  - no: Q2
    question: 귀하의 가족 중 다음의 산업에 종사하시는 분이 계십니까?
    type: multi
    answer:
      - 광고대행사
      - 시장조사
      - 언론/TV/라디오 

  -  no: Q3 
    ...

if type yn or free then remove answer
'''},
]


text = '''
    [쇼카드S2]
    S2. 	귀하나 귀하의 가족 중 다음의 산업에 종사하시는 분이 계십니까?
        광고대행사 	1  
        시장조사 	2
        언론/TV/라디오 	3	→ 중단하시오
        PR/프로모션 	4

    Q3. 	귀하께서는 지난 6개월 동안 광고관련 설문 조사에 응답한 경험이 있으십니까?
        예 	1	→ 중단하시오. 
        아니오 	2 	

    Dummy 질문을 통해 테스트 광고의 제품/서비스를 사용여부 판단(쿼다 확인)
    S5.	귀하께서는 oooo를 사용해 보신 적이 있으십니까? 
        
        예	1 	 쿼타 확인 
        아니오	2	 쿼타 확인

    S7.    	귀하께서는 은행 자주 방문하는 편이십니까? 
        예	1 	Dummy 질문 
        아니오	2

    '''


model = OpenaiChat(prompt = prompt)
output = model.send_message(text)
print(output)
# %%
