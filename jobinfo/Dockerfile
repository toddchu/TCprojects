FROM python:3
ADD  jobinfo.py /
ADD  jobgui.py /
RUN pip install --upgrade pip
RUN pip install pathlib2
RUN pip install wxPython
CMD ["python", "./jobgui.py"]
