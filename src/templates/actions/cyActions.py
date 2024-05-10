def template_actions():
    general = {
        "assertRequestWasCalledGivenTimes": ".then(() => {cy.get('@{{ alias }}.all').then(cont => {expect(cont).to.have.length({{ value }})})})",
        "assertStubResponseBodyContains": ".then(() => {cy.wait('@{{ alias }}').then(cont => {expect(JSON.stringify(cont.response.body)).to.include(`{{ value }}`)})})",
        "assertStubResponseBodyEquals": ".then(() => {cy.wait('@{{ alias }}').then(cont => {expect(JSON.stringify(cont.response.body)).to.eq(JSON.stringify({{ text }}))})})",
        "assertVariableContains": ".then(() => {expect(`{{ cy_var }}`).to.include(`{{ value }}`)})",
        "assertVariableEquals": ".then(() => {expect(`{{ cy_var }}`).to.eq(`{{ value }}`)})",
        "catchExceptions": ".then(() => {Cypress.on('uncaught:exception', (err, runnable) => {return false})})",
        "cyLog": ".then(() => {cy.log(`{{ value }}`)})",
        "command": ".then(() => {cy.{{ name }}({{ params }})})",
        "interceptRequest": ".then(() => {cy.intercept({method:'{{ method }}', url: '{{ url }}'}).as('{{ alias }}')})",
        "script": ".then(() => { {{ js }} })",
        "reload": ".then(() => {cy.reload()})",
        "session": """
            .then(() => {
                cy.session(`{{ name }}`, () => {
                    {{ actions }}
                }, {
                    validate() {
                        {{ validate }}
                        },
                    cacheAcrossSpecs: {{ cache }}
                }
            )
        })""",
        "setVariable": ".then(() => {Cypress.env('{{ cy_var }}', `{{ value }}`)})",
        "stubResponse": ".then(() => {cy.intercept({method:'{{ method }}', url: '{{ url }}'}, { statusCode: {{ status_code }}, body: {{ body }} }).as('{{ alias }}')})",
        "stubResponseFromFile": ".then(() => {cy.intercept({method:'{{ method }}', url: '{{ url }}'}, { statusCode: {{ status_code }}, fixture: `{{ file }}` }).as('{{ alias }}')})",
        "takeScreenshot": ".then(() => {cy.screenshot(`{{filename}}`)})",
        "viewport": ".then(() => {cy.viewport({{ width }}, {{ height }})})",
        "wait": ".then(() => {cy.wait({{ value }})})"
    }

    web = {
        "assertUrlEquals": ".then(() => {cy.url({ timeout: {{ timeout }} }).should('eq', `{{ value }}`)})",
        "assertUrlContains": ".then(() => {cy.url({ timeout: {{ timeout }} }).should('include', `{{ value }}`)})",
        "assertPageTitleEquals": ".then(() => {cy.title().should('eq', `{{ value }}`)})",
        "assertPageTitleContains": ".then(() => {cy.title().should('include', `{{ value }}`)})",
        "assertElementExists": ".then(() => {cy.{{ locator_type }}('{{ locator }}', { timeout: {{ timeout }} }).should('exist')})",
        "assertElementNotExists": ".then(() => {cy.{{ locator_type }}('{{ locator }}', { timeout: {{ timeout }} }).should('not.exist')})",
        "assertElementIsVisible": ".then(() => {cy.{{ locator_type }}('{{ locator }}', { timeout: {{ timeout }} }).should('be.visible')})",
        "assertElementIsNotVisible": ".then(() => {cy.{{ locator_type }}('{{ locator }}', { timeout: {{ timeout }} }).should('not.be.visible')})",
        "assertElementHasText": ".then(() => {cy.{{ locator_type }}('{{ locator }}').should('have.text', `{{ value }}`)})",
        "assertElementIndexHasText": ".then(() => {cy.{{ locator_type }}('{{ locator }}').eq({{ index }}).should('have.text', `{{ value }}`)})",
        "assertElementContainsText": ".then(() => {cy.{{ locator_type }}('{{ locator }}').should('include.text', `{{ value }}`)})",
        "assertElementIndexContainsText": ".then(() => {cy.{{ locator_type }}('{{ locator }}').eq({{ index }}).should('include.text', `{{ value }}`)})",
        "assertElementHasAttribute": ".then(() => {cy.{{ locator_type }}('{{ locator }}').should('have.attr', `{{ attr }}`)})",
        "assertElementIndexHasAttribute": ".then(() => {cy.{{ locator_type }}('{{ locator }}').eq({{ index }}).should('have.attr', `{{ attr }}`)})",
        "assertElementAttributeHasValue": ".then(() => {cy.{{ locator_type }}('{{ locator }}').should('have.attr', `{{ attr }}`, `{{ value }}`)})",
        "assertElementIndexAttributeHasValue": ".then(() => {cy.{{ locator_type }}('{{ locator }}').eq({{ index }}).should('have.attr', `{{ attr }}`, `{{ value }}`)})",
        "assertElementAttributeContainsValue": ".then(() => {cy.{{ locator_type }}('{{ locator }}').should('have.attr', `{{ attr }}`).then(attr => {expect(attr).to.include(`{{ value }}`)})})",
        "assertElementIndexAttributeContainsValue": ".then(() => {cy.{{ locator_type }}('{{ locator }}').eq({{ index }}).should('have.attr', `{{ attr }}`).then(attr => {expect(attr).to.include(`{{ value }}`)})})",
        "assertElementLength": ".then(() => {cy.{{ locator_type }}('{{ locator }}').should('have.length{{ option }}', {{ value }})})",
        "assertLocalStorageItemEquals": ".then(() => {cy.getAllLocalStorage().should(() => {expect(localStorage.getItem(`{{ key }}`)).to.eq(`{{ value }}`)})})",
        "assertSessionStorageItemEquals": ".then(() => {cy.getAllSessionStorage().should(() => {expect(sessionStorage.getItem(`{{ key }}`)).to.eq(`{{ value }}`)})})",
        "assertLocalStorageItemIsNull": ".then(() => {cy.getAllLocalStorage().should(() => {expect(localStorage.getItem(`{{ key }}`)).to.be.null})})",
        "assertSessionStorageItemIsNull": ".then(() => {cy.getAllSessionStorage().should(() => {expect(sessionStorage.getItem(`{{ key }}`)).to.be.null})})",
        "assertFileContentContainsText": ".then(() => {cy.fixture(`{{ file }}`).then(cont => {expect(JSON.stringify(cont)).to.contain(`{{ value }}`) })})",
        "assertFileContentContainsElementText": ".then(() => {cy.fixture(`{{ file }}`).then(cont => { cy.{{ locator_type }}('{{ locator }}').then($el => { expect(JSON.stringify(cont)).to.contain($el.text()) }) })})",
        "assertFileContentEqualsTextElement": ".then(() => {cy.fixture(`{{ file }}`).then(cont => {cy.{{ locator_type }}('{{ locator }}').should('have.text', cont)})})",
        "clearAllLocalStorage": ".then(() => {cy.clearAllLocalStorage()})",
        "clearAllSessionStorage": ".then(() => {cy.clearAllSessionStorage()})",
        "clearField": ".then(() => {cy.{{ locator_type }}('{{ locator  }}').clear()})",
        "clearFieldAndType": ".then(() => {cy.{{ locator_type }}('{{ locator  }}').clear().type(`{{ value }}`)})",
        "click": ".then(() => {cy.{{ locator_type }}('{{ locator  }}').click()})",
        "clickByIndex": ".then(() => {cy.{{ locator_type }}('{{ locator  }}').eq({{ index }}).click()})",
        "forceClick": ".then(() => {cy.{{ locator_type }}('{{ locator  }}').click({force: true})})",
        "navigateTo": ".then(() => {cy.visit(`{{ url }}`)})",
        "navigateForward": ".then(() => {cy.go('forward')})",
        "navigateBack": ".then(() => {cy.go('back')})",
        "pressKey": ".then(() => {cy.{{ locator_type }}('{{ locator  }}').type(`{{ key }}`)})",
        "removeElementTargetAttr": ".then(() => {cy.{{ locator_type }}('{{ locator  }}').invoke('removeAttr', 'target')})",
        "selectByIndex": ".then(() => {cy.{{ locator_type }}('{{ locator }}').select({{ index }})})",
        "selectByText": ".then(() => {cy.{{ locator_type }}('{{ locator }}').select('{{ text }}')})",
        "selectByValue": ".then(() => {cy.{{ locator_type }}('{{ locator }}').select('{{ value }}')})",
        "setElementLengthAsVariable": ".then(() => {cy.{{ locator_type }}('{{ locator }}').then($el => {Cypress.env('{{ cy_var }}', $el.length)})})",
        "setElementTextAsVariable": ".then(() => {cy.{{ locator_type }}('{{ locator }}').then($el => {Cypress.env('{{ cy_var }}', $el.text())})})",
        "setLocalStorage": ".then(() => {window.localStorage.setItem(`{{ key }}`, `{{ value }}`) })",
        "setSessionStorage": ".then(() => {window.sessionStorage.setItem(`{{ key }}`, `{{ value }}`) })",
        "scrollIntoView": ".then(() => {cy.{{ locator_type }}('{{ locator }}').scrollIntoView()})",
        "type": ".then(() => {cy.{{ locator_type }}('{{ locator  }}').type(`{{ value }}`, { log: {{ log }} })})",
        "typeAndPressEnter": ".then(() => {cy.{{ locator_type }}('{{ locator  }}').type(`{{ value }}{enter}`)})",
    }

    api = {
        "assertResponseStatusCode":
        """
        .then(() => {
            cy.get('@{{ alias }}').then( response => {
                expect(response.status).to.eq({{ statusCode }})
            })
        })
        """,

        "assertResponseBodyContains":
        """
        .then(() => {
            cy.get('@{{ alias }}').then(response => {
                expect(JSON.stringify(response.body)).to.include(`{{ value }}`) 
            })
        })
        """,

        "assertResponseBodyHasProperty":
        """
        .then(() => {
            cy.get('@{{ alias }}').its('body').should('have.property', `{{ property }}`)
        })
        """,

        "assertResponseBodyPropertyHasValue":
        """
        .then(() => {
            cy.get('@{{ alias }}').its('body').should('have.property', `{{ property }}`, `{{ value }}`)
        })
        """,

        "assertResponseBodyHasNestedProperty":
        """
        .then(() => {
            cy.get('@{{ alias }}').its('body').should('have.nested.property', `{{ nestedProperty }}`)
        })
        """,

        "assertResponseBodyNestedPropertyHasValue":
        """
        .then(() => {
            cy.get('@{{ alias }}').its('body').should('have.nested.property', `{{ nestedProperty }}`, `{{ value }}`)
        })
        """,

        "assertResponseHeadersContains":
        """
        .then(() => {
            cy.get('@{{ alias }}').then(response => {
                expect(JSON.stringify(response.headers)).to.include(`{{ value }}`) 
            })
        })
        """,

        "assertResponseHeadersHasProperty":
        """
        .then(() => {
            cy.get('@{{ alias }}').its('headers').should('have.property', `{{ property }}`)
        })
        """,

        "assertResponseHeadersPropertyHasValue":
        """
        .then(() => {
            cy.get('@{{ alias }}').its('headers').should('have.property', `{{ property }}`, `{{ value }}`)
        })
        """,

       "sendRequest": 
        """
        .then(() => {
            cy.request({
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
        })
        """,

        "sendPostRequestWithPayloadFromFile": 
        """
        .then(() => {
            cy.fixture('{{ body }}').then(payload => {        
                cy.request({
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
        })
        """,

        "sendRequestToUploadFileAsFormData": 
        """
        .then(() => {
            cy.fixture('{{ file }}', 'binary').then(file => {
                
                const formData = new FormData()
                const blob = Cypress.Blob.binaryStringToBlob(file, '{{ file }}')

                formData.append(`{{ fileFieldName }}`, blob, '{{ file }}')
                {% if append_args is defined %}
                    {% for arg_dict in append_args %}
                        {% for key, value in arg_dict.items() %}
                            formData.append('{{ key }}', '{{ value }}');
                        {% endfor %}
                    {% endfor %}
                {% endif %}

                cy.request({
                    method: '{{ method }}',
                    url: '{{ url }}',
                    auth: '{{ auth }}',
                    body: formData,
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
        })
        """,
        
        "sendGraphqlRequest": 
        """
        .then(() => {
            cy.fixture('{{ query }}').then(query => {
                cy.request({
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
        })
        """,

        "setResponseAsVariable": 
        """
        .then(() => {
            cy.get('@{{ alias }}').then( response => {
                Cypress.env('{{ cy_var }}', JSON.stringify(response))
            })
        })
        """,

        "setResponseBodyAsVariable": 
        """
        .then(() => {
            cy.get('@{{ alias }}').then( response => {
                Cypress.env('{{ cy_var }}', JSON.stringify(response.body))
            })
        })
        """,

        "setResponseBodyPropertyValueAsVariable": 
        """
        .then(() => {
            cy.get('@{{ alias }}').then( response => {
                Cypress.env('{{ cy_var }}', response.body{{ path_to_property }})
            })
        })
        """,

        "setResponseHeadersAsVariable": 
        """
        .then(() => {
            cy.get('@{{ alias }}').then( response => {
                Cypress.env('{{ cy_var }}', JSON.stringify(response.headers))
            })
        })
        """,

        "setResponseHeadersPropertyValueAsVariable": 
        """
        .then(() => {
            cy.get('@{{ alias }}').then( response => {
                Cypress.env('{{ cy_var }}', response.headers{{ path_to_property }})
            })
        })
        """
    }



    return general | web | api


if __name__ == "__main__":
    pass