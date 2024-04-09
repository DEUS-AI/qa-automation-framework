import 'cypress-plugin-xhr-toggle'
import 'cypress-xpath'
require('cypress-failed-log')
import "cypress-failed-log"
const options = {
    // Log console output only
    collectTypes: ['cons:log', 'cons:error', 'cy:log', 'cy:request', 'cy:intercept', 'cy:command'],
  };
require('cypress-terminal-report/src/installLogsCollector')(options);

import registerCypressGrep from '@cypress/grep'
registerCypressGrep()

import 'cypress-mochawesome-reporter/register'

Cypress.on('test:after:run', (test, runnable) => {
  if (Cypress.config('results/screenshots')) {
    const imgFile = `../results/screenshots/${Cypress.spec.name}/${filename}`
    if (Cypress.Mochawesome) {
      Cypress.Mochawesome.context.push(imgFile)
    }
  }
})