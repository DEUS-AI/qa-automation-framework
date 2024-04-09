const { defineConfig } = require('cypress');

module.exports = defineConfig({
  reporter: '../../node_modules/cypress-mochawesome-reporter',
  reporterOptions: {
    reportDir: 'cypress/report',
    reportPageTitle: 'Automation Run Report',
    charts: true,
    embeddedScreenshots: true,
    inlineAssets: false,
    saveAllAttempts: false,
    overwrite: false,
  },

  e2e: {
    setupNodeEvents(on, config) {
      require('cypress-failed-log/on')(on)
      const options = {
        printLogsToConsole: 'always'
      };
      require('cypress-terminal-report/src/installLogsPrinter')(on, options);
      on('task', {
        log(message) {
          console.log(message)
          return null
        },
      })
      require('cypress-mochawesome-reporter/plugin')(on)
      require('@cypress/grep/src/plugin')(config);
      return config;
    },
  env: {
      hideCredentials: true,
      hideXhr: true,
      grepFilterSpecs: true,
      grepOmitFiltered: true
    },
    chromeWebSecurity: false,
    experimentalRunAllSpecs: true,
    experimentalMemoryManagement: true,
    specPattern: './cypress/acceptance',
    downloadsFolder: './cypress/downloads',
    screenshotsFolder: "./cypress/results/screenshots",
    videosFolder: "./cypress/results/videos",
    supportFile: './cypress/support/e2e.js',
    video: false,
    retries: {
      runMode: 0,
      openMode: 0,
    }
  }
})