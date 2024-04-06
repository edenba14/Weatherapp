FROM python:3.12-slim AS build
SHELL ["/bin/bash","-c"]
WORKDIR /weatherapp
COPY /weatherapp /weatherapp
RUN python3 -m venv venv
RUN source venv/bin/activate
RUN pip install --user -r requirements.txt


FROM python:3.12-slim
WORKDIR /weatherapp
COPY --from=build /weatherapp /weatherapp
COPY --from=build /root/.local /root/.local 
RUN apt-get update && apt-get install -y nginx
COPY weather /etc/nginx/sites-available
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /etc/nginx/sites-available/weather /etc/nginx/sites-enabled
ENV PATH=/root/.local/bin:$PATH
ENV VC_API_KEY=${VC_API_KEY}
ENV API_SEC_KEY=${API_SEC_KEY}
ENV GIT_VAL=${GIT_VAL}
ENV GIT_KEY=${GIT_KEY}
CMD service nginx start & gunicorn --bind unix:/weatherapp/weather.sock -m 000 weather_service:app
