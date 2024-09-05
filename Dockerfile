FROM python:3.10.14
# RUN addgroup --system mygroup && adduser --system --ingroup mygroup myuser
RUN mkdir /myapp
WORKDIR /myapp

# Pass build arguments
ARG MONGO_URI
ARG REDIS_URL
ARG MONGO_DB_NAME

# Set environment variables using the build arguments
ENV MONGO_URI=$MONGO_URI
ENV REDIS_URL=$REDIS_URL
ENV MONGO_DB_NAME=$MONGO_DB_NAME

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /myapp

# RUN sudo chown -R myuser:mygroup /myapp
# USER myuser

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["sh", "/entrypoint.sh"]