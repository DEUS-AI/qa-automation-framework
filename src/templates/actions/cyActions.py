def template_actions():
    general = {
        "assertRequestWasCalledGivenTimes": "cy.get('@{{ alias }}.all').then(cont => {expect(cont).to.have.length({{ value }})})",
        "assertStubResponseBodyContains": "cy.wait('@{{ alias }}').then(cont => {expect(JSON.stringify(cont.response.body)).to.include(`{{ value }}`)})",
        "assertStubResponseBodyEquals": "cy.wait('@{{ alias }}').then(cont => {expect(JSON.stringify(cont.response.body)).to.eq(JSON.stringify({{ text }}))})",
        "assertVariableContains": ".then(() => {expect(`{{ cy_var }}`).to.include(`{{ value }}`)})",
        "assertVariableEquals": ".then(() => {expect(`{{ cy_var }}`).to.eq(`{{ value }}`)})",
        "catchExceptions": "Cypress.on('uncaught:exception', (err, runnable) => {return false})",
        # "command": "cy.{{ command_name }}({{ args }})",
        "cyLog": "cy.log(`{{ value }}`)",
        "interceptRequest": "cy.intercept({method:'{{ method }}', url: '{{ url }}'}).as('{{ alias }}')",
        "setVariable": "Cypress.env('{{ cy_var }}', `{{ value }}`)",
        "stubResponse": "cy.intercept({method:'{{ method }}', url: '{{ url }}'}, { statusCode: {{ status_code }}, body: {{ body }} }).as('{{ alias }}')",
        "takeScreenshot": "cy.screenshot(`{{filename}}`)",
        "wait": "cy.wait({{ value }})"
    }

    web = {
        "assertUrlEquals":"cy.url().should('eq', `{{ value }}`)",
        "assertUrlContains":"cy.url().should('include', `{{ value }}`)",
        "assertPageTitleEquals":"cy.title().should('eq', `{{ value }}`)",
        "assertPageTitleContains":"cy.title().should('include', `{{ value }}`)",
        "assertElementExists":"cy.{{ locator_type }}('{{ locator }}').should('exist')",
        "assertElementNotExists":"cy.{{ locator_type }}('{{ locator }}').should('not.exist')",
        "assertElementIsVisible":"cy.{{ locator_type }}('{{ locator }}').should('be.visible')",
        "assertElementIsNotVisible":"cy.{{ locator_type }}('{{ locator }}').should('not.be.visible')",
        "assertElementHasText":"cy.{{ locator_type }}('{{ locator }}').should('have.text', `{{ value }}`)",
        "assertElementIndexHasText":"cy.{{ locator_type }}('{{ locator }}').eq({{ index }}).should('have.text', `{{ value }}`)",
        "assertElementContainsText":"cy.{{ locator_type }}('{{ locator }}').should('include.text', `{{ value }}`)",
        "assertElementIndexContainsText":"cy.{{ locator_type }}('{{ locator }}').eq({{ index }}).should('include.text', `{{ value }}`)",
        "assertElementHasAttribute":"cy.{{ locator_type }}('{{ locator }}').should('have.attr', `{{ attr }}`)",
        "assertElementAttributeHasValue":"cy.{{ locator_type }}('{{ locator }}').should('have.attr', `{{ attr }}`, `{{ value }}`)",
        "assertElementAttributeContainsValue":"cy.{{ locator_type }}('{{ locator }}').should('have.attr', `{{ attr }}`).then(attr => {expect(attr).to.include(`{{ value }}`)})",
        "assertFileContentContainsText": "cy.fixture(`{{ file }}`).then(cont => {expect(JSON.stringify(cont)).to.contain(`{{ value }}`) })",
        "assertFileContentContainsElementText": "cy.fixture(`{{ file }}`).then(cont => { cy.{{ locator_type }}('{{ locator }}').then($el => { expect(JSON.stringify(cont)).to.contain($el.text()) }) })",
        "assertFileContentEqualsTextElement": "cy.fixture(`{{ file }}`).then(cont => {cy.{{ locator_type }}('{{ locator }}').should('have.text', cont)})",
        "clearField": "cy.{{ locator_type }}('{{ locator  }}').clear()",
        "clearFieldAndType": "cy.{{ locator_type }}('{{ locator  }}').clear().type('{{ value }}')",
        "click": "cy.{{ locator_type }}('{{ locator  }}').click()",
        "clickByIndex": "cy.{{ locator_type }}('{{ locator  }}').eq({{ index }}).click()",
        "forceClick": "cy.{{ locator_type }}('{{ locator  }}').click({force: true})",
        "jsScript": "{{ script }}",
        "navigateTo": "cy.visit(`{{ url }}`)",
        "navigateForward":"cy.go('forward')",
        "navigateBack":"cy.go('back')",
        "pressKey": "cy.{{ locator_type }}('{{ locator  }}').type(`{{ key }}`)",
        "removeElementTargetAttr": "cy.{{ locator_type }}('{{ locator  }}').invoke('removeAttr', 'target')",
        "selectByIndex": "cy.{{ locator_type }}('{{ locator }}').select({{ index }})",
        "selectByText": "cy.{{ locator_type }}('{{ locator }}').select('{{ text }}')",
        "selectByValue": "cy.{{ locator_type }}('{{ locator }}').select('{{ value }}')",
        "setElementTextAsVariable": "cy.{{ locator_type }}('{{ locator }}').then($el => {Cypress.env('{{ cy_var }}', $el.text())})",
        "type": "cy.{{ locator_type }}('{{ locator  }}').type(`{{ value }}`)",
        "typeAndPressEnter": "cy.{{ locator_type }}('{{ locator  }}').type(`{{ value }}{enter}`)"
    }

    api = {
        "assertResponseStatusCode":
        """
        cy.get('@{{ alias }}').then( response => {
            expect(response.status).to.eq({{ statusCode }})
        })
        """,

        "assertResponseBodyContains":
        """
        cy.get('@{{ alias }}').then(response => {
            expect(JSON.stringify(response.body)).to.include('{{ value }}') 
        })
        """,

        "assertResponseBodyHasProperty":
        """
        cy.get('@{{ alias }}').its('body').should('have.property', '{{ property }}')
        """,

        "assertResponseBodyPropertyHasValue":
        """
        cy.get('@{{ alias }}').its('body').should('have.property', '{{ property }}', '{{ value }}')
        """,

        "assertResponseBodyHasNestedProperty":
        """
        cy.get('@{{ alias }}').its('body').should('have.nested.property', '{{ nestedProperty }}')
        """,

        "assertResponseBodyNestedPropertyHasValue":
        """
        cy.get('@{{ alias }}').its('body').should('have.nested.property', '{{ nestedProperty }}', '{{ value }}')
        """,

        "assertResponseHeadersContains":
        """
        cy.get('@{{ alias }}').then(response => {
            expect(JSON.stringify(response.headers)).to.include('{{ value }}') 
        })
        """,

        "assertResponseHeadersHasProperty":
        """
        cy.get('@{{ alias }}').its('headers').should('have.property', '{{ property }}')
        """,

        "assertResponseHeadersPropertyHasValue":
        """
        cy.get('@{{ alias }}').its('headers').should('have.property', '{{ property }}', '{{ value }}')
        """,

       "sendRequest": 
        """
        cy.request(
            {
                method: '{{ method }}',
                url: '{{ url }}',
                auth: '{{ auth }}',
                body: {{ body }},
                headers: {{ headers }},
                qs: {{ qs }},
                log: {{ log }},
                failOnStatusCode: {{ failOnStatusCode }},
                followRedirect: {{ followRedirect }},
                form: {{ form }},
                retryOnStatusCodeFailure: {{ retryOnStatusCodeFailure }},
                retryOnNetworkFailure: {{ retryOnNetworkFailure }},
                encoding: '{{ encoding }}',
                timeout: {{ timeout }}
            }).then(res => {
                cy.wrap(res).as('{{ alias }}')
        })
        """,

        "sendPostRequestWithPayloadFromFile": 
        """
        cy.fixture('{{ body }}').then(payload => {        
            cy.request(
                {
                    method: 'POST',
                    url: '{{ url }}',
                    auth: '{{ auth }}',
                    body: payload,
                    headers: {{ headers }},
                    qs: {{ qs }},
                    log: {{ log }},
                    failOnStatusCode: {{ failOnStatusCode }},
                    followRedirect: {{ followRedirect }},
                    form: {{ form }},
                    retryOnStatusCodeFailure: {{ retryOnStatusCodeFailure }},
                    retryOnNetworkFailure: {{ retryOnNetworkFailure }},
                    encoding: '{{ encoding }}',
                    timeout: {{ timeout }}
                }).then(res => {
                    cy.wrap(res).as('{{ alias }}')
            })
        })
        """,
        
        "sendGraphqlRequest": 
        """
        cy.fixture('{{ query }}').then(query => {
            cy.request(
                {
                    method: 'POST',
                    url: '{{ url }}',
                    body: {
                        operationName: '{{ operationName }}',   
                        query: query,   
                        variables: {{ variables }},   
                    },
                    headers: {{ headers }},
                    log: {{ log }},
                    failOnStatusCode: {{ failOnStatusCode }},
                    followRedirect: {{ followRedirect }},
                    retryOnStatusCodeFailure: {{ retryOnStatusCodeFailure }},
                    retryOnNetworkFailure: {{ retryOnNetworkFailure }},
                    timeout: {{ timeout }}
                }).then(res => {
                    cy.wrap(res).as('{{ alias }}')
            })
        })
        """,

        "setResponseAsVariable": """
        cy.get('@{{ alias }}').then( response => {
            Cypress.env('{{ cy_var }}', JSON.stringify(response))
            })
        """,

        "setResponseBodyAsVariable": """
        cy.get('@{{ alias }}').then( response => {
            Cypress.env('{{ cy_var }}', JSON.stringify(response.body))
            })
        """,

        "setResponseBodyPropertyValueAsVariable": """
        cy.get('@{{ alias }}').then( response => {
            Cypress.env('{{ cy_var }}', response.body.{{ path_to_property }})
            })
        """,

        "setResponseHeadersAsVariable": """
        cy.get('@{{ alias }}').then( response => {
            Cypress.env('{{ cy_var }}', JSON.stringify(response.headers))
            })
        """,

        "setResponseHeadersPropertyValueAsVariable": """
        cy.get('@{{ alias }}').then( response => {
            Cypress.env('{{ cy_var }}', response.headers.{{ path_to_property }})
            })
        """
    }



    return general | web | api


if __name__ == "__main__":
    pass