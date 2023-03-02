#%%
import openai
import yaml


class OpenaiChat():
    def __init__(self, age = 20, gender = 1, hobby = '그림 그리기'):

        with open('conf.yaml', 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        openai.api_key = config.get('api_info').get('api_key')
        openai.organization = config.get('api_info').get('organization')

        self.gender = '남' if gender == 0 else '여'
        self.age = age
        self.hobby = hobby
        self.default_set = [
            {'role':'system','content': f'''
            너는 AI가 아닌 {self.age}살에 {self.gender}성이고 취미는 {self.hobby}인 
            반말을 좋아하는 사람이야,
            모든 대화가 끝날때까지 반드시 이 사실을 잊지 말고 명시적으로 말하지 말아줘'''
            },
        ]
        self.clear_message()

    def send_message(self, message):
        self.history.append({'role':'user','content': message})
        res = openai.ChatCompletion.create(model = 'gpt-3.5-turbo', messages = self.default_set + self.history)

        output = res.choices[0]['message']['content']
        self.history.append({'role':'assistant','content': output})
        return output
    

    def clear_message(self):
        self.history = [{'role':'assistant','content': '안녕!'}]