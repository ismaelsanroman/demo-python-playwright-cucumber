Feature: Testing on a mocked-up API
    Set of tests on the "Mock API"
    to check stability and functionality.

    Background:
        Given I launch a login request and we get the token

    @api_test
    Scenario: Get all items and verify that they are displayed
        When I launch the petition to obtain all the items
        Then I verify that all items are obtained
            | available | category    | description         | id | name | price | stock |
            |           | Electrónica | tarjeta gráfica RTX |    |      |       |       |
            | true      |             |                     | 4  |      | >100  | >0    |

    @api_test
    Scenario: Create an item and check that it has been created correctly
        When I send a creation request with the following parameters
            | id | name       | description           | category    | price | stock | available |
            | 21 | Nuevo Item | Descripción de prueba | Categoria X | 25.99 | 10    | true      |
        And I confirm that the parameter has been "created" correctly
        Then I delete the created element(s)
        And I confirm that the parameter has been "deleted" correctly