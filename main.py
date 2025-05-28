import streamlit as st

TIPOS_ARQUIVOS_VALIDOS = ['Youtube', 'Site', 'Pdf', 'Txt', 'Csv']

CONFIG_MODELOS = {'Groq': {'modelos': ['llama-3.1-70b-versatile', 'gemma-2-9b-it']},
                  'OpenAI': {'modelos': ['gpt-4o-mini', 'gpt-4o']}
                  }

MENSAGENS_EXEMPLO = [
  ('user', 'olá'),
  ('assistant', 'tudo bem?'),
  ('user', 'tudo ótimo!')
]

def pag_chat():
  st.header("🤖 Seja bem-vindo ao Oráculo", divider=True)

  mensagens = st.session_state.get('mensagens', MENSAGENS_EXEMPLO)
  for mensagem in mensagens:
    chat = st.chat_message(mensagem[0])
    chat.markdown(mensagem[1])

  input_usuario = st.chat_input("Fale com o Oráculo")
  if input_usuario:
    mensagens.append(('user', input_usuario))
    st.session_state['mensagens'] = mensagens
    st.rerun()


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
    
    #commitfuncionaaa

def main():
  pag_chat()
  with st.sidebar:
    side_bar()








if __name__ == "__main__":
  main()



