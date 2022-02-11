FROM lucasgiu/python-base:latest

# Install OpenJDK-8
RUN apt-get update && \
    apt-get install -y default-jre && \
    apt-get install -y default-jdk && \
    apt-get clean;

# Fix certificate issues
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;

# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN pip install pandas --upgrade
RUN pip install numpy --upgrade --ignore-installed

COPY ./ /giuka_db
WORKDIR /giuka_db

EXPOSE 8050

CMD "python3"
