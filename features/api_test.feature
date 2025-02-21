# features/api_test.feature
Feature: Testing on a mocked-up API
  Set of tests on the "Mock API" to check stability and functionality.

  Background:
    Given I launch a login request and we get the token

  @api_test @happy
  Scenario: Get all items and verify that they are displayed
    When I launch the request to obtain all items
    Then I verify that all items are retrieved
      | available | category    | description         | id | name | price | stock |
      |           | Electrónica | tarjeta gráfica RTX |    |      |       |       |
      | true      |             |                     | 4  |      | >100  | >0    |

  @api_test @happy
  Scenario: Create an item and check that it has been created correctly
    When I send a creation request with the following parameters
      | id | name       | description           | category    | price | stock | available |
      | 21 | Nuevo Item | Descripción de prueba | Categoria X | 25.99 | 10    | true      |
    And I confirm that the item has been "created" correctly
    Then I delete the created elements
    And I confirm that the item has been "deleted" correctly

  @api_test @unhappy
  Scenario: Create an item with missing required fields and verify failure
    When I send a creation request with the following parameters
      | id | name | description | category | price | stock | available |
      | 22 |      |             |          |       |       |           |
    Then I verify that the item creation fails with an error message

  @api_test @unhappy
  Scenario: Create an item with a duplicate ID and verify failure
    Given An item with ID 21 already exists
    When I send a creation request with the following parameters
      | id | name      | description    | category    | price | stock | available |
      | 21 | Duplicate | Duplicate item | Categoria Y | 30.00 | 5     | true      |
    Then I verify that the item creation fails due to duplicate ID

  @api_test @unhappy
  Scenario: Get a non-existing item and verify response
    When I launch the request to obtain an item with ID 9999
    Then I verify that the response indicates "Item not found"

  @api_test @security
  Scenario: Request items without a valid token and verify unauthorized access
    When I launch the request to obtain all items without a token
    Then I verify that the response returns an error for a missing or invalid token
