FROM python:3.12-slim AS build
WORKDIR /weatherapp
COPY /weatherapp .
RUN pip install --prefix=/install -r requirements.txt

FROM python:3.12-alpine
WORKDIR /weatherapp
COPY --from=build /weatherapp/ .
COPY --from=build /install /usr/local
ENV VC_API_KEY=${VC_API_KEY}
ENV API_SEC_KEY=${API_SEC_KEY}
ENV GIT_VAL=${GIT_VAL}
ENV GIT_KEY=${GIT_KEY}
CMD gunicorn --bind 0.0.0.0:80 weather_service:app
