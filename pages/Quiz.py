import streamlit as st
import streamlit_book as stb
import time
import random

with stb.echo("below", "Here is a nice **Hint**"):
    stb.multiple_choice("### Thats your question generated by GPT",
                        {"Das richtige ✅":True,
                         "Falsch 😅":False,
                         "pyspark":False,
                         "vulpix":False}
                       )