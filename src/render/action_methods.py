class ActionMethods:

    # general actions
    @staticmethod
    def assertRequestWasCalledGivenTimes(template, args):
        return template.render(
            alias=args["alias"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def assertStubResponseBodyContains(template, args):
        return template.render(
            alias=args["alias"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def assertStubResponseBodyEquals(template, args):
        return template.render(
            alias=args["alias"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def assertVariableContains(template, args):
        return template.render(
            cy_var=args["var"],
            value=args["value"]
        ) + "\n"
    
    @staticmethod
    def assertVariableEquals(template, args):
        return template.render(
            cy_var=args["var"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def catchExceptions(template):
        return template.render() + "\n"

    @staticmethod
    def cyLog(template, args):
        return template.render(
            value=args["value"]
        ) + "\n"

    @staticmethod
    def interceptRequest(template, args):
        return template.render(
            method=args["method"],
            url=args["url"],
            alias=args["alias"]
        ) + "\n"

    @staticmethod
    def setVariable(template, args):
        return template.render(
            cy_var=args["name"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def stubResponse(template, args):
        return template.render(
            method=args["method"],
            url=args["url"],
            status_code=args["statusCode"],
            body=args["body"],  # maybe add dict(args["body"]) so it encapsulates input into json obj
            alias=args["alias"]
        ) + "\n"

    @staticmethod
    def takeScreenshot(template, args):
        return template.render(
            filename=args["filename"]
        ) + "\n"

    @staticmethod
    def wait(template, args):
        return template.render(
            value=args["value"]
        ) + "\n"

    # web actions
    @staticmethod
    def assertUrlEquals(template, args):
        return template.render(
            value=args["value"]
        ) + "\n"
    
    @staticmethod
    def assertUrlContains(template, args):
        return template.render(
            value=args["value"]
        ) + "\n"
    
    @staticmethod
    def assertPageTitleEquals(template, args):
        return template.render(
            value=args["value"]
        ) + "\n"

    @staticmethod
    def assertPageTitleContains(template, args):
        return template.render(
            value=args["value"]
        ) + "\n"

    @staticmethod
    def assertElementExists(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"]
        ) + "\n"

    @staticmethod
    def assertElementNotExists(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"]
        ) + "\n"

    @staticmethod
    def assertElementIsVisible(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"]
        ) + "\n"

    @staticmethod
    def assertElementIsNotVisible(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"]
        ) + "\n"

    @staticmethod
    def assertElementHasText(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def assertElementIndexHasText(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"],
            index=args["index"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def assertElementContainsText(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def assertElementIndexContainsText(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"],
            index=args["index"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def assertElementHasAttribute(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"],
            attr=args["attribute"]
        ) + "\n"

    @staticmethod
    def assertElementAttributeHasValue(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"],
            attr=args["attribute"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def assertElementAttributeContainsValue(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"],
            attr=args["attribute"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def assertFileContentContainsText(template, args):
        return template.render(
            file=args["filename"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def assertFileContentContainsElementText(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"],
            file=args["filename"]
        ) + "\n"

    @staticmethod
    def assertFileContentEqualsTextElement(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"],
            file=args["filename"]
        ) + "\n"

    @staticmethod
    def clearField(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"]
        ) + "\n"

    @staticmethod
    def clearFieldAndType(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def click(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"]
        ) + "\n"

    @staticmethod
    def clickByIndex(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"],
            index=args["index"]
        ) + "\n"

    @staticmethod
    def forceClick(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"]
        ) + "\n"

    @staticmethod
    def jsScript(template, args):
        return template.render(
            script=args["script"]
        ) + "\n"

    @staticmethod
    def navigateTo(template, args):
        return template.render(
            url=args["url"]
        ) + "\n"

    @staticmethod
    def navigateForward(template):
        return template.render() + "\n"

    @staticmethod
    def navigateBack(template):
        return template.render() + "\n"

    @staticmethod
    def pressKey(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"],
            key=args["key"]
        ) + "\n"

    @staticmethod
    def removeElementTargetAttr(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"]
        ) + "\n"

    @staticmethod
    def selectByIndex(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"],
            index=args["index"]
        ) + "\n"

    @staticmethod
    def selectByText(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"],
            text=args["text"]
        ) + "\n"

    @staticmethod
    def selectByValue(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def setElementTextAsVariable(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"],
            cy_var=args["name"]
        ) + "\n"

    @staticmethod
    def type(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def typeAndPressEnter(template, args):
        return template.render(
            locator_type=args["element"]["type"],
            locator=args["element"]["locator"],
            value=args["value"]
        ) + "\n"

    
    # api actions
    @staticmethod
    def assertResponseStatusCode(template, args):
        return template.render(
            alias=args["alias"],
            statusCode=args["statusCode"]
        ) + "\n"

    @staticmethod
    def assertResponseBodyContains(template, args):
        return template.render(
            alias=args["alias"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def assertResponseBodyHasProperty(template, args):
        return template.render(
            alias=args["alias"],
            property=args["property"]
        ) + "\n"

    @staticmethod
    def assertResponseBodyPropertyHasValue(template, args):
        return template.render(
            alias=args["alias"],
            property=args["property"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def assertResponseBodyHasNestedProperty(template, args):
        return template.render(
            alias=args["alias"],
            nestedProperty=args["nestedProperty"]
        ) + "\n"

    @staticmethod
    def assertResponseBodyNestedPropertyHasValue(template, args):
        return template.render(
            alias=args["alias"],
            nestedProperty=args["nestedProperty"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def assertResponseHeadersContains(template, args):
        return template.render(
            alias=args["alias"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def assertResponseHeadersHasProperty(template, args):
        return template.render(
            alias=args["alias"],
            property=args["property"]
        ) + "\n"

    @staticmethod
    def assertResponseHeadersPropertyHasValue(template, args):
        return template.render(
            alias=args["alias"],
            property=args["property"],
            value=args["value"]
        ) + "\n"

    @staticmethod
    def sendRequest(template, args):
        return template.render(
            method=args["method"],
            url=args["url"],
            alias=args["alias"],
            auth=args["auth"] if args.get("auth") else "",
            body=args["body"] if args.get("body") else {},
            headers=args["headers"] if args.get("headers") else {},
            qs=args["qs"] if args.get("qs") else {},
            log=args["log"] if args.get("log") else "true",
            failOnStatusCode=args["failOnStatusCode"] if args.get("failOnStatusCode") else "true",
            followRedirect=args["followRedirect"] if args.get("followRedirect") else "true",
            form=args["form"] if args.get("form") else "false",
            encoding=args["encoding"] if args.get("encoding") else "utf8",
            retryOnStatusCodeFailure=args["retryOnStatusCodeFailure"] if args.get("retryOnStatusCodeFailure") else "false",
            retryOnNetworkFailure=args["retryOnNetworkFailure"] if args.get("retryOnNetworkFailure") else "true",
            timeout=args["timeout"] if args.get("timeout") else 10000
        ) + "\n"

    @staticmethod
    def sendPostRequestWithPayloadFromFile(template, args):
        return template.render(
            url=args["url"],
            alias=args["alias"],
            body=args["body"],
            auth=args["auth"] if args.get("auth") else "",
            headers=args["headers"] if args.get("headers") else {},
            qs=args["qs"] if args.get("qs") else {},
            log=args["log"] if args.get("log") else "true",
            failOnStatusCode=args["failOnStatusCode"] if args.get("failOnStatusCode") else "true",
            followRedirect=args["followRedirect"] if args.get("followRedirect") else "true",
            form=args["form"] if args.get("form") else "false",
            encoding=args["encoding"] if args.get("encoding") else "utf8",
            retryOnStatusCodeFailure=args["retryOnStatusCodeFailure"] if args.get("retryOnStatusCodeFailure") else "false",
            retryOnNetworkFailure=args["retryOnNetworkFailure"] if args.get("retryOnNetworkFailure") else "true",
            timeout=args["timeout"] if args.get("timeout") else 10000
        ) + "\n"

    @staticmethod
    def sendGraphqlRequest(template, args):
        return template.render(
            url=args["url"],
            alias=args["alias"],
            operationName=args["operationName"] if args.get("operationName") else "",
            query=args["query"],
            variables=args["variables"],
            headers=args["headers"] if args.get("headers") else {},
            log=args["log"] if args.get("log") else "true",
            failOnStatusCode=args["failOnStatusCode"] if args.get("failOnStatusCode") else "true",
            followRedirect=args["followRedirect"] if args.get("followRedirect") else "true",
            retryOnStatusCodeFailure=args["retryOnStatusCodeFailure"] if args.get("retryOnStatusCodeFailure") else "false",
            retryOnNetworkFailure=args["retryOnNetworkFailure"] if args.get("retryOnNetworkFailure") else "true",
            timeout=args["timeout"] if args.get("timeout") else 10000
        ) + "\n"

    @staticmethod
    def setResponseAsVariable(template, args):
        return template.render(
            alias=args["alias"],
            cy_var=args["name"]
        ) + "\n"

    @staticmethod
    def setResponseBodyAsVariable(template, args):
        return template.render(
            alias=args["alias"],
            cy_var=args["name"]
        ) + "\n"

    @staticmethod
    def setResponseBodyPropertyValueAsVariable(template, args):
        return template.render(
            alias=args["alias"],
            cy_var=args["name"],
            path_to_property=args["propertyPath"]
        ) + "\n"

    @staticmethod
    def setResponseHeadersAsVariable(template, args):
        return template.render(
            alias=args["alias"],
            cy_var=args["name"]
        ) + "\n"

    @staticmethod
    def setResponseHeadersPropertyValueAsVariable(template, args):
        return template.render(
            alias=args["alias"],
            cy_var=args["name"],
            path_to_property=args["propertyPath"]
        ) + "\n"