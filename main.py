import streamlit as st

def pag_chat():
  st.header("🤖 Seja bem-vindo ao Oráculo", divider=True)

  mensagem = st.session_state.get('mensagens', [])

def main():
  pag_chat()


if __name__ == "__main__":
  main()



