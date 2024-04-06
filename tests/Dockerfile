FROM joyzoursky/python-chromedriver:3.9-alpine
RUN pip install selenium
RUN pip install requests
RUN pip install pytest
WORKDIR /
COPY tests.py .
CMD python3 tests.py
