FROM cypress/included:cypress-13.10.0-node-20.13.1-chrome-125.0.6422.60-1-ff-126.0-edge-125.0.2535.51-1

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
RUN npm install @faker-js/faker --save-dev


RUN chmod +x setup.sh

ENTRYPOINT ["./setup.sh"]
# ENTRYPOINT ["tail", "-f", "/dev/null"]