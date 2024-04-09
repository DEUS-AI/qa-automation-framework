FROM cypress/included

WORKDIR /app
COPY . .

RUN apt-get update 
RUN apt-get install -y python3 python3-pip vim 
RUN pip install -r requirements.txt
RUN npm install --save-dev cypress cypress-failed-log
RUN npm install --save-dev cypress-terminal-report
RUN npm install --save-dev cypress-plugin-xhr-toggle
RUN npm install --save-dev cypress-xpath
RUN npm install --save-dev cypress-mochawesome-reporter
RUN npm i -D @cypress/grep


RUN chmod +x setup.sh

ENTRYPOINT ["./setup.sh"]
# ENTRYPOINT ["tail", "-f", "/dev/null"]