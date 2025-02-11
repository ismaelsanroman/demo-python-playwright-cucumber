Feature: Tests in the 'Text Box' sub-section of 'Elements'
  Set of tests on the 'Text Box' sub-section 
  to check the stability of that section.

  @textbox @smoke @happy
  Scenario: Fill text box with valid data
    Given I navigate to DemoQA and "Elements" Page
    When I open the "Text Box" section
    Then I fill in the form with the following data
      | name            | email                    | current_address | permanent_address |
      | Ismael Sanromán | IsmaelSanroman@gmail.com |     123 Main St |    456 Another St |
    And I verify the form with the following data

  @textbox @boundary @unhappy 
  Scenario: Submit form with all fields empty
    Given I navigate to DemoQA and "Elements" Page
    When I open the "Text Box" section
    Then I fill in the form with the following data
      | name | email | current_address | permanent_address |
      | ""   | ""    | ""              | ""                |
    And I verify the form fails

  @textbox @negative @unhappy
  Scenario Outline: Submit form with invalid email
    Given I navigate to DemoQA and "Elements" Page
    When I open the "Text Box" section
    Then I fill in the form with the following data
      | name        | email         | current_address | permanent_address |
      | Ismael SDET | <email_value> | Address line    | Another line      |
    And I verify the form fails

    Examples:
      | email_value                                            |
      | a@b                                                    |
      | not_an_email                                           |
      |Jöhn#1!!@example.org |
      | testEmailWithoutAtSymbol                               |
      | extremelylongemail1234567890@verylongdomainexample.com |

  @textbox @boundary @unhappy
  Scenario: Submit form with extra-long name
    Given I navigate to DemoQA and "Elements" Page
    When I open the "Text Box" section
    Then I fill in the form with the following data
      | name                                                                                                                                   | email                | current_address | permanent_address |
      | AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA | longName@example.com | Some address    | Another address   |
    And I verify the form with the following data

  @textbox @special_chars
  Scenario Outline: Submit form with special characters
    Given I navigate to DemoQA and "Elements" Page
    When I open the "Text Box" section
    Then I fill in the form with the following data
      | name         | email         | current_address     | permanent_address    |
      | <name_value> | <email_value> | <cur_address_value> | <perm_address_value> |
    And I verify the form with the following data

    Examples:
      | name_value | email_value          | cur_address_value | perm_address_value |
      | Jöhn #1!!  | John@example.org | £¥€©Jöhn #1!!     | £¥€©Jöhn #1!!      |
      | 😀🚀      | John@example.org | 😀🚀              | 😀🚀              |

  @textbox @security @script_injection 
  Scenario: Submit form with script injection in name
    Given I navigate to DemoQA and "Elements" Page
    When I open the "Text Box" section
    Then I fill in the form with the following data
      | name                         | email             | current_address | permanent_address   |
      | <script>alert('Hi')</script> | script@attack.com | Test injection  | Test injection perm |
    And I verify the form with the following data

  @textbox @boundary @unhappy @partial 
  Scenario: Submit form with partial fields filled
    Given I navigate to DemoQA and "Elements" Page
    When I open the "Text Box" section
    Then I fill in the form with the following data
      | name         | email  | current_address | permanent_address |
      | Partial Name | "@.com | ""              | Address only      |
    And I verify the form fails
