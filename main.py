import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

# GROQ_API_KEY = "sk_CVSY52o7T1716DIb1CDaWGdyb3FYp3VGkFuq436hNJgPS1QKOCTg"

#ajustar a questão da chave da API, adicionar outros provedores de IA que não sejam pagos para poder testar

TIPOS_ARQUIVOS_VALIDOS = ['Youtube', 'Site', 'Pdf', 'Txt', 'Csv']

CONFIG_MODELOS = {'Groq': {'modelos': ['llama3-70b-8192', 'gemma-2-9b-it'], 'chat': ChatGroq},
'OpenAI': {'modelos': ['gpt-4o-mini', 'gpt-4o'], 'chat': ChatOpenAI}}

MEMORIA = ConversationBufferMemory()
MEMORIA.chat_memory.add_user_message('Olá IA')
MEMORIA.chat_memory.add_ai_message('Olá humano')


def carrega_modelo(provedor, modelo, api_key):
  chat = CONFIG_MODELOS[provedor]['chat'](model=modelo, api_key=api_key)
  st.session_state['chat'] = chat
  return chat


def pag_chat():
  st.header("🤖 Seja bem-vindo ao Oráculo", divider=True)

  chat_model = st.session_state.get('chat')
  memoria = st.session_state.get('memoria', MEMORIA)
  for mensagem in memoria.buffer_as_messages:
    chat = st.chat_message(mensagem.type)
    chat.markdown(mensagem.content)

  input_usuario = st.chat_input("Fale com o Oráculo")
  if input_usuario:
    chat = st.chat_message('human')
    chat.markdown(input_usuario)

    chat = st.chat_message('ai')
    resposta = chat.write_stream(chat_model.stream(input_usuario))

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
    carrega_modelo(provedor, modelo, api_key)




def main():
  pag_chat()
  with st.sidebar:
    side_bar()




if __name__ == "__main__":
  main()



