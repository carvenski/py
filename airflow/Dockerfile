# Dockerfile to build airflow standalone image for test env use
# MAINTAINER xing.yang@intel.com

FROM python:3.7

WORKDIR /

RUN mkdir airflow

ENV AIRFLOW_HOME /airflow  
ENV AIRFLOW_VERSION 2.4.2  
ENV PYTHON_VERSION 3.7  
ENV CONSTRAINT_URL "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"  

RUN export http_proxy=http://child-prc.intel.com:913 && \
    export https_proxy=http://child-prc.intel.com:913 && \
    pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

VOLUME /airflow

EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/airflow", "standalone"]

# The Standalone command will initialise the database, make a user,
# and start all components for you.

# Visit localhost:8080 in the browser and use the admin account details
# shown on the terminal to login.
# Enable the example_bash_operator dag in the home page
