pkill -f streamlit
nohup streamlit run src/streamlit_dashboard/app.py --server.port 8501 --server.headless true > streamlit.log 2>&1 &
