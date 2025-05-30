import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_community.llms import HuggingFaceHub
from loaders import *
import tempfile
from langchain.prompts import ChatPromptTemplate
#from langchain_huggingface import HuggingFaceHub

# GROQ_API_KEY = "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"



TIPOS_ARQUIVOS_VALIDOS = ['Youtube', 'Site', 'Pdf', 'Txt', 'Csv']

CONFIG_MODELOS = {
    'Groq': {
        'modelos': ['llama3-70b-8192', 'gemma-2-9b-it'],
        'chat': ChatGroq
    },
    'OpenAI': {
        'modelos': ['gpt-4o-mini', 'gpt-4o'],
        'chat': ChatOpenAI
    },
    'HuggingFace': {
        'modelos': ['meta-llama/Meta-Llama-3-8B-Instruct', 'mistralai/Mixtral-8x7B-Instruct-v0.1'],
        'chat': HuggingFaceHub
    }
}

MEMORIA = ConversationBufferMemory()
MEMORIA.chat_memory.add_user_message('Olá IA')
MEMORIA.chat_memory.add_ai_message('Olá humano')

def carrega_arquivo(tipo_arquivo, arquivo):
  if tipo_arquivo == 'Site':
    documento = carrega_site(arquivo)

  if tipo_arquivo == 'Youtube':
    documento = carrega_video(arquivo)

  if tipo_arquivo == 'Pdf':
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
      temp.write(arquivo.read())
      nome_temp = temp.name
    documento = carrega_pdf(nome_temp)
  
  if tipo_arquivo == 'Csv':
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
      temp.write(arquivo.read())
      nome_temp = temp.name
    documento = carrega_csv(nome_temp)

  if tipo_arquivo == 'Txt':
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp:
      temp.write(arquivo.read())
      nome_temp = temp.name
    documento = carrega_txt(nome_temp)

  return documento


def carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo):

  documento = carrega_arquivo(tipo_arquivo, arquivo)

  system_message = '''Voce é um assistente amigável chamado Oráculo.
  Voce possui acesso às seguintes informações vindas 
  de um documento {}:

  ####
  {}
  ####

  Utilize as informações fornecidas para basear as suas respostas.

  Sempre que houver $ na sua saída, substitua por 5.

  Se a informação do documento for algo como "Just a moment...Enable JavaScript and cookies to continue" sugira ao usuário carregar novamento o Oráculo!

'''.format(tipo_arquivo, documento)

  template = ChatPromptTemplate.from_messages([
    ('system', system_message),
    ('placeholder', '{chat_history}'),
    ('user', '{input}')
  ])



  chat = CONFIG_MODELOS[provedor]['chat'](model=modelo, api_key=api_key)
  chain = template | chat


  st.session_state['chain'] = chain
  


def pag_chat():
  st.header("🤖 Seja bem-vindo ao Oráculo", divider=True)

  chain = st.session_state.get('chain')
  if chain is None:
    st.error('Carregue o Oráculo')
    st.stop()


  memoria = st.session_state.get('memoria', MEMORIA)
  for mensagem in memoria.buffer_as_messages:
    chat = st.chat_message(mensagem.type)
    chat.markdown(mensagem.content)

  input_usuario = st.chat_input("Fale com o Oráculo")
  if input_usuario:
    chat = st.chat_message('human')
    chat.markdown(input_usuario)

    chat = st.chat_message('ai')
    resposta = chat.write_stream(chain.stream({'input': input_usuario, 'chat_history': memoria.buffer_as_messages}))

    memoria.chat_memory.add_user_message(input_usuario)
    memoria.chat_memory.add_ai_message(resposta)
    st.session_state['memoria'] = memoria
    


def side_bar():
  tabs = st.tabs(['Uploads de arquivos', 'Seleção de modelos'])
  with tabs[0]:
    tipo_arquivo = st.selectbox('Selecione o tipo de arquivo', TIPOS_ARQUIVOS_VALIDOS)
    if tipo_arquivo == 'Site':
      arquivo = st.text_input('Digite a URL do site')

    if tipo_arquivo == 'Youtube':
      arquivo = st.text_input('Digite a URL do video')

    if tipo_arquivo == 'Pdf':
      arquivo = st.file_uploader('Faça o upload do arquivo pdf', type=['.pdf'])

    if tipo_arquivo == 'Txt':
      arquivo = st.file_uploader('Faça o upload do arquivo txt', type=['.txt'])

    if tipo_arquivo == 'Csv':
      arquivo = st.file_uploader('Faça o upload do arquivo csv', type=['.csv'])
  
  with tabs[1]:
    provedor = st.selectbox('Selecione o provedor dos modelos', CONFIG_MODELOS.keys())
    modelo = st.selectbox('Selecione o modelo', CONFIG_MODELOS[provedor]['modelos'])
    api_key = st.text_input(f'Ponha a sua API key para o provedor {provedor}', value=st.session_state.get(f'api_key_{provedor}'))

    st.session_state[f'api_key_{provedor}'] = api_key
    
  if st.button('Inicializar Oráculo', use_container_width=True):
    carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo)

  if st.button('Apagar Histórico de conversa', use_container_width=True):
    st.session_state['memoria'] = MEMORIA


def main():
  with st.sidebar:
    side_bar()
  pag_chat()





if __name__ == "__main__":
  main()



