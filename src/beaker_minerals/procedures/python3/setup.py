import IPython
formatter = IPython.get_ipython().display_formatter.formatters['text/plain']
formatter.max_seq_length = 0