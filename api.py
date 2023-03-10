#%%
import openai
import yaml








class OpenaiChat():
    def __init__(self, age = 20, gender = 1, hobby = '그림 그리기', prompt = None):

        with open('conf.yaml', 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        openai.api_key = config.get('api_info').get('api_key')
        openai.organization = config.get('api_info').get('organization')

        self.gender = '남' if gender == 0 else '여'
        self.age = age
        self.hobby = hobby

        # 추후 수정 필요
        self.set_prompt(prompt)
        self.clear_message()


    def set_prompt(self, prompt):
        if prompt is None:
            self.default_set = [
                # {'role':'system','content': f'''
                # {self.age}살에 {self.gender}성이고 취미는 {self.hobby}인 사람이야
                # 친구처럼 대답해줘'''
                # },
                # {'role':'system','content': f'''
                # You are a helper that user can ask questions and see the answers
                # '''
                # },
            ]
        else:
            self.default_set = prompt


    def send_message(self, message):
        self.history.append({'role':'user','content': message})
        res = openai.ChatCompletion.create(model = 'gpt-3.5-turbo', messages = self.default_set + self.history)
        output = res.choices[0]['message']['content']
        self.history.append({'role':'assistant','content': output})
        return output
    

    def clear_message(self):
        ''' 
        Clear the history of the conversation
        '''
        self.history = []


    def chat_with_voice(self, file_name):
        text = self._voice_to_text(file_name)
        output = self.send_message(text)
        return output

    def _voice_to_text(self, file_name):
        with open(file_name, 'rb') as f:
            output = openai.Audio.transcribe('whisper-1', f)

        return output['text']



# 임시
def speech_to_text(filename):
    output = OpenaiChat()._voice_to_text(filename)
    return output


# %%



if __name__ == '__main__':
    text = '''
    Q1b.	그 밖에 더 기억나는 광고는 무엇인지 말씀해 주십시오. 
        그 밖에 또 어떤 광고가 기억 나십니까? 그 밖에 기억나는 광고가 더 없습니까?

        제품	상표
        (A)			(B)		 
        (A)			(B)		 
        (A)			(B)		 
        (A)			(B)		 
        (A)			(B)		 

    '''

    output = OpenaiChat().send_message(text)
    # %%
    print(output)
    # %%

    output = OpenaiChat().send_message(text)
    print(output)
    # %%

    model = OpenaiChat()

    # %%
    aa = model.chat_with_voice('goguma.mp3')
    # %%


