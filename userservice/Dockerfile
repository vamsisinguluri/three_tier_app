FROM centos:7

RUN yum -y update
RUN yum -y install epel-release && yum clean all
RUN yum -y install python3 python3-pip

RUN python3 -m pip install --upgrade pip

ENV APP_HOME=/app
RUN mkdir $APP_HOME
WORKDIR $APP_HOME


COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME

RUN pip install -r requirements.txt

RUN sed -i -e 's/\r$//' entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

