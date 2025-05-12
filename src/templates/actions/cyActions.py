def template_actions():
    general = {
        "assertRequestWasCalledGivenTimes": ".then(() => {cy.get('@{{ alias }}.all').then(cont => {expect(cont).to.have.length({{ value }})})})",
        "assertStubResponseBodyContains": ".then(() => {cy.wait(`@{{ alias }}`).then(cont => {expect(JSON.stringify(cont.response.body)).to.include(`{{ value }}`)})})",
        "assertStubResponseBodyEquals": ".then(() => {cy.wait(`@{{ alias }}`).then(cont => {expect(JSON.stringify(cont.response.body)).to.eq(JSON.stringify({{ text }}))})})",
        "assertVariableContains": ".then(() => {expect(`{{ cy_var }}`).to.include(`{{ value }}`)})",
        "assertVariableEquals": ".then(() => {expect(`{{ cy_var }}`).to.eq(`{{ value }}`)})",
        "catchExceptions": ".then(() => {Cypress.on('uncaught:exception', (err, runnable) => {return false})})",
        "cyLog": ".then(() => {cy.log(`{{ value }}`)})",
        "command": ".then(() => {cy.{{ name }}({{ arguments }})})",
        "jsCommand": ".then(() => {cy.{{ name }}({{ arguments }})})",
        "interceptRequest": ".then(() => {cy.intercept({method:'{{ method }}', url: `{{ url }}`}).as('{{ alias }}')})",
        "interceptGqlRequest": """
        .then(() => {
            cy.intercept(
                {
                    method:'POST',
                    url: `{{ url }}`
                },
                (req) => {
                    if (req.body.operationName === `{{ operationName }}`) {
                        req.alias = `{{ alias }}`
                    } else {
                        req.alias = 'noOperationNameRequests'
                    }
                }
            )
        })
        """,
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
        "stubResponse": ".then(() => {cy.intercept({method:'{{ method }}', url: `{{ url }}`}, { statusCode: {{ status_code }}, body: {{ body }} }).as('{{ alias }}')})",
        "stubResponseFromFile": ".then(() => {cy.intercept({method:'{{ method }}', url: `{{ url }}`}, { statusCode: {{ status_code }}, fixture: `{{ file }}` }).as('{{ alias }}')})",
        "stubGqlResponseFromFile": """
        .then(() => {
            cy.intercept(
                {
                    method: 'POST',
                    url: `{{ url }}`
                }, 
                (req) => {
                    if (req.body.operationName === `{{ operationName }}`) {
                        req.reply({ 
                            statusCode: {{ status_code }},
                            fixture: `{{ file }}` 
                        })
                    }
                }
            ).as('{{ alias }}')       
        })""",
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
        "assertElementHasText": ".then(() => {cy.{{ locator_type }}('{{ locator }}', { timeout: {{ timeout }} }).should('have.text', `{{ value }}`)})",
        "assertElementNotHaveText": ".then(() => {cy.{{ locator_type }}('{{ locator }}', { timeout: {{ timeout }} }).should('not.have.text', `{{ value }}`)})",
        "assertEachElementHasText": ".then(() => {cy.{{ locator_type }}('{{ locator }}').as('els')\ncy.get('@els').each($el => {cy.wrap($el).should('have.text', `{{ value }}`)})})",
        "assertElementIndexHasText": ".then(() => {cy.{{ locator_type }}('{{ locator }}', { timeout: {{ timeout }} }).eq({{ index }}).should('have.text', `{{ value }}`)})",
        "assertElementIndexNotHaveText": ".then(() => {cy.{{ locator_type }}('{{ locator }}', { timeout: {{ timeout }} }).eq({{ index }}).should('not.have.text', `{{ value }}`)})",
        "assertElementContainsText": ".then(() => {cy.{{ locator_type }}('{{ locator }}', { timeout: {{ timeout }} }).should('include.text', `{{ value }}`)})",
        "assertEachElementContainsText": ".then(() => {cy.{{ locator_type }}('{{ locator }}').as('els')\ncy.get('@els').each($el => {cy.wrap($el).should('include.text', `{{ value }}`)})})",
        "assertElementIndexContainsText": ".then(() => {cy.{{ locator_type }}('{{ locator }}', { timeout: {{ timeout }} }).eq({{ index }}).should('include.text', `{{ value }}`)})",
        "assertElementHasAttribute": ".then(() => {cy.{{ locator_type }}('{{ locator }}').should('have.attr', `{{ attr }}`)})",
        "assertElementIndexHasAttribute": ".then(() => {cy.{{ locator_type }}('{{ locator }}').eq({{ index }}).should('have.attr', `{{ attr }}`)})",
        "assertElementAttributeHasValue": ".then(() => {cy.{{ locator_type }}('{{ locator }}').should('have.attr', `{{ attr }}`, `{{ value }}`)})",
        "assertElementIndexAttributeHasValue": ".then(() => {cy.{{ locator_type }}('{{ locator }}').eq({{ index }}).should('have.attr', `{{ attr }}`, `{{ value }}`)})",
        "assertElementAttributeContainsValue": ".then(() => {cy.{{ locator_type }}('{{ locator }}').should('have.attr', `{{ attr }}`).then(attr => {expect(attr).to.include(`{{ value }}`)})})",
        "assertElementIndexAttributeContainsValue": ".then(() => {cy.{{ locator_type }}('{{ locator }}').eq({{ index }}).should('have.attr', `{{ attr }}`).then(attr => {expect(attr).to.include(`{{ value }}`)})})",
        "assertElementHasCssProperty": ".then(() => {cy.{{ locator_type }}('{{ locator }}').should('have.css', `{{ property }}`)})",
        "assertElementIndexHasCssProperty": ".then(() => {cy.{{ locator_type }}('{{ locator }}').eq({{ index }}).should('have.css', `{{ property }}`)})",
        "assertElementCssPropertyHasValue": ".then(() => {cy.{{ locator_type }}('{{ locator }}').should('have.css', `{{ property }}`, `{{ value }}`)})",
        "assertElementIndexCssPropertyHasValue": ".then(() => {cy.{{ locator_type }}('{{ locator }}').eq({{ index }}).should('have.css', `{{ property }}`, `{{ value }}`)})",
        "assertElementCssPropertyContainsValue": ".then(() => {cy.{{ locator_type }}('{{ locator }}').should('have.css', `{{ property }}`).then(prop => {expect(prop).to.include(`{{ value }}`)})})",
        "assertElementIndexCssPropertyContainsValue": ".then(() => {cy.{{ locator_type }}('{{ locator }}').eq({{ index }}).should('have.css', `{{ property }}`).then(prop => {expect(prop).to.include(`{{ value }}`)})})",
        "assertElementLength": ".then(() => {cy.{{ locator_type }}('{{ locator }}').should('have.length{{ option }}', {{ value }})})",
        "assertLocalStorageItemEquals": ".then(() => {cy.getAllLocalStorage().should(() => {expect(localStorage.getItem(`{{ key }}`)).to.eq(`{{ value }}`)})})",
        "assertSessionStorageItemEquals": ".then(() => {cy.getAllSessionStorage().should(() => {expect(sessionStorage.getItem(`{{ key }}`)).to.eq(`{{ value }}`)})})",
        "assertLocalStorageItemIsNull": ".then(() => {cy.getAllLocalStorage().should(() => {expect(localStorage.getItem(`{{ key }}`)).to.be.null})})",
        "assertSessionStorageItemIsNull": ".then(() => {cy.getAllSessionStorage().should(() => {expect(sessionStorage.getItem(`{{ key }}`)).to.be.null})})",
        "assertFileContentContainsText": ".then(() => {cy.fixture(`{{ file }}`).then(cont => {expect(JSON.stringify(cont)).to.contain(`{{ value }}`) })})",
        "assertFileContentContainsElementText": ".then(() => {cy.fixture(`{{ file }}`).then(cont => { cy.{{ locator_type }}('{{ locator }}').then($el => { expect(JSON.stringify(cont)).to.contain($el.text()) }) })})",
        "assertFileContentEqualsTextElement": ".then(() => {cy.fixture(`{{ file }}`).then(cont => {cy.{{ locator_type }}('{{ locator }}').should('have.text', cont)})})",
        "assertElementHasPseudoElement": """.then(() => {
            cy.{{ locator_type }}('{{ locator  }}').within(($el) => {
                cy.window().then((win) => {
                const before = win.getComputedStyle($el[0], '{{ pseudo_element }}')
                expect(before === 'undefined').to.not.be.true
                })
            })
        })
        """,
        "assertElementPseudoElementHasProperty": """.then(() => {
            cy.{{ locator_type }}('{{ locator  }}').within(($el) => {
                cy.window().then((win) => {
                const before = win.getComputedStyle($el[0], '{{ pseudo_element }}')
                const prop = before.getPropertyValue('{{ property }}')
                expect(prop === 'undefined').to.not.be.true
                })
            })
        })
        """,
        "assertElementPseudoElementPropertyHasValue": """.then(() => {
            cy.{{ locator_type }}('{{ locator  }}').within(($el) => {
                cy.window().then((win) => {
                const before = win.getComputedStyle($el[0], '{{ pseudo_element }}')
                const prop = before.getPropertyValue('{{ property }}')
                expect(prop).to.equal(`{{ value }}`)
                })
            })
        })
        """,
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
        "rightClick": ".then(() => {cy.{{ locator_type }}('{{ locator }}').rightclick()})",
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
        "uploadFile": ".then(() => {cy.fixture(`{{ file }}`, null).as('myFixture')\n\t\tcy.{{ locator_type }}('{{ locator }}').selectFile('@myFixture', { action: '{{ action }}' ,force: {{ force }}, timeout: {{ timeout }}, waitForAnimations: {{ wait_for_animations }} })})"
    }

    api = {
        "assertResponseStatusCode":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).then( response => {
                expect(response.status).to.eq(Number(`{{ statusCode }}`))
            })
        })
        """,

        "assertResponseBodyContains":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).then(response => {
                expect(JSON.stringify(response.body)).to.include(`{{ value }}`) 
            })
        })
        """,

        "assertResponseBodyHasProperty":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its('body').should('have.property', `{{ property }}`)
        })
        """,

        "assertResponseBodyPropertyHasValue":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its('body').should('have.property', `{{ property }}`, `{{ value }}`)
        })
        """,

        "assertResponseBodyPropertyNotHaveValue":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its('body').should('have.property', `{{ property }}`).and('not.eq', `{{ value }}`)
        })
        """,

        "assertResponseBodyPropertyContainsValue":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).then(res => { expect(res.body{{ property }}).to.include(`{{ value }}`) })
        })
        """,

        "assertResponseBodyPropertyHasNumericValue":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its('body').should('have.property', `{{ property }}`, Number(`{{ value }}`))
        })
        """,

        "assertResponseBodyHasNestedProperty":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its('body').should('have.nested.property', `{{ nestedProperty }}`)
        })
        """,

        "assertResponseBodyNestedPropertyHasValue":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its('body').should('have.nested.property', `{{ nestedProperty }}`, `{{ value }}`)
        })
        """,

        "assertResponseBodyNestedPropertyNotHaveValue":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its('body').should('have.nested.property', `{{ nestedProperty }}`).and('not.eq', `{{ value }}`)
        })
        """,

        "assertResponseBodyNestedPropertyContainsValue":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).then(res => { expect(res.body{{ nestedProperty }}).to.include(`{{ value }}`) })
        })
        """,

        "assertResponseBodyNestedPropertyHasNumericValue":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its('body').should('have.nested.property', `{{ nestedProperty }}`, Number(`{{ value }}`))
        })
        """,

        "assertResponseBodyPropertyValueIsEmpty":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its(`body{{ path_to_property }}`).should('be.empty')
        })
        """,

        "assertResponseBodyPropertyValueIsNotEmpty":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its(`body{{ path_to_property }}`).should('not.be.empty')
        })
        """,

        "assertResponseBodyPropertyValueIsNull":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its(`body{{ path_to_property }}`).should('be.null')
        })
        """,

        "assertResponseBodyPropertyValueIsNotNull":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its(`body{{ path_to_property }}`).should('not.be.null')
        })
        """,

        "assertResponseBodyPropertyValueType":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its(`body{{ path_to_property }}`).should('be.a', `{{ type }}`)
        })
        """,

        "assertResponseBodyPropertyValueIsNotType":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its(`body{{ path_to_property }}`).should('not.be.a', `{{ type }}`)
        })
        """,

        "assertResponseBodyPropertyValueLength":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its(`body{{ path_to_property }}`).should('have.length', `{{ length }}`)
        })
        """,

        "assertResponseBodyPropertyValueIsGreaterThan":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its(`body{{ path_to_property }}`).should('be.greaterThan', {{ nr }})
        })
        """,

        "assertResponseBodyPropertyValueIsAtLeast":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its(`body{{ path_to_property }}`).should('be.at.least', {{ nr }})
        })
        """,

        "assertResponseBodyPropertyValueIsLessThan":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its(`body{{ path_to_property }}`).should('be.lessThan', {{ nr }})
        })
        """,

        "assertResponseBodyPropertyValueIsWithin":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its(`body{{ path_to_property }}`).should('be.within', {{ first_nr }}, {{ second_nr }})
        })
        """,

        "assertResponseBodyPropertyValueIsInstanceOf":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its(`body{{ path_to_property }}`).should('be.instanceOf', {{ array }})
        })
        """,

        "assertResponseBodyPropertyValueIsCloseTo":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its(`body{{ path_to_property }}`).should('be.closeTo', {{ first_nr }}, {{ second_nr }})
        })
        """,

        "assertResponseBodyPropertyValueIsOneOf":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its(`body{{ path_to_property }}`).should('be.oneOf', {{ array }})
        })
        """,

        "assertResponseBodyPropertyValueIsTrue":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its(`body{{ path_to_property }}`).should('be.true')
        })
        """,

        "assertResponseBodyPropertyValueIsFalse":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its(`body{{ path_to_property }}`).should('be.false')
        })
        """,

        "assertResponseBodyPropertyValueIsUndefined":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its(`body{{ path_to_property }}`).should('be.undefined')
        })
        """,

        "assertGqlResponseBodyHasProperty":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its('response.body').should('have.property', `{{ property }}`)
        })
        """,

        "assertGqlResponseBodyNotHaveProperty":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its('response.body').should('not.have.property', `{{ property }}`)
        })
        """,

        "assertGqlResponseBodyPropertyHasValue":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its('response.body').should('have.property', `{{ property }}`, `{{ value }}`)
        })
        """,

        "assertGqlResponseBodyPropertyNotHaveValue":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its('response.body').should('have.property', `{{ property }}`).should('not.eq', `{{ value }}`)
        })
        """,

        "assertGqlResponseBodyHasNestedProperty":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its('response.body').should('have.nested.property', `{{ nestedProperty }}`)
        })
        """,

        "assertGqlResponseBodyNotHaveNestedProperty":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its('response.body').should('not.have.nested.property', `{{ nestedProperty }}`)
        })
        """,

        "assertGqlResponseBodyNestedPropertyHasValue":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its('response.body').should('have.nested.property', `{{ nestedProperty }}`, `{{ value }}`)
        })
        """,

        "assertGqlResponseBodyNestedPropertyNotHaveValue":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its('response.body').should('have.nested.property', `{{ nestedProperty }}`).should('not.eq', `{{ value }}`)
        })
        """,

        "assertResponseHeadersContains":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).then(response => {
                expect(JSON.stringify(response.headers)).to.include(`{{ value }}`) 
            })
        })
        """,

        "assertResponseHeadersHasProperty":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its('headers').should('have.property', `{{ property }}`)
        })
        """,

        "assertResponseHeadersPropertyHasValue":
        """
        .then(() => {
            cy.get(`@{{ alias }}`).its('headers').should('have.property', `{{ property }}`, `{{ value }}`)
        })
        """,

       "sendRequest": 
        """
        .then(() => {
            cy.request({
                method: '{{ method }}',
                url: `{{ url }}`,
                auth: `{{ auth }}`,
                {% if body is defined %}body: {{ body }},{% endif %}
                {% if headers is defined %}headers: {{ headers }},{% endif %}
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

        "sendRequestWithPayloadFromFile": 
        """
        .then(() => {
            cy.fixture('{{ body }}').then(payload => {        
                cy.request({
                    method: '{{ method }}',
                    url: `{{ url }}`,
                    auth: `{{ auth }}`,
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
                    url: `{{ url }}`,
                    auth: `{{ auth }}`,
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
                    url: `{{ url }}`,
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
            cy.get(`@{{ alias }}`).then( response => {
                Cypress.env('{{ cy_var }}', JSON.stringify(response))
            })
        })
        """,

        "setResponseBodyAsVariable": 
        """
        .then(() => {
            cy.get(`@{{ alias }}`).then( response => {
                Cypress.env('{{ cy_var }}', JSON.stringify(response.body))
            })
        })
        """,

        "setResponseBodyPropertyValueAsVariable": 
        """
        .then(() => {
            cy.get(`@{{ alias }}`).then( response => {
                Cypress.env('{{ cy_var }}', response.body{{ path_to_property }})
            })
        })
        """,

        "setResponseHeadersAsVariable": 
        """
        .then(() => {
            cy.get(`@{{ alias }}`).then( response => {
                Cypress.env('{{ cy_var }}', JSON.stringify(response.headers))
            })
        })
        """,

        "setResponseHeadersPropertyValueAsVariable": 
        """
        .then(() => {
            cy.get(`@{{ alias }}`).then( response => {
                Cypress.env('{{ cy_var }}', response.headers{{ path_to_property }})
            })
        })
        """
    }



    return general | web | api


if __name__ == "__main__":
    pass