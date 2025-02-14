Feature: Tests in the 'Radio Button' sub-section of 'Elements'
    Set of tests on the 'Radio Button' sub-section
    to check the stability of that section.

    Background:
        Given I navigate to DemoQA and "Elements" Page
        When I open the "Radio Button" section

    @radiobtn @smoke @happy @table_decision
    Scenario Outline: Select the active radio button
        And I select the "<radioButton>" radio button
        Then I verify that radioButton "<radioButton>" is selected

        Examples:
            | radioButton |
            | Yes         |
            | Impressive  |

    @radiobtn @negative @unhappy
    Scenario: Attempt to select the disabled 'No' radio button
        Then I verify that the "No" radio button is disabled

    @radiobtn @boundary @accessibility @state_machine
    Scenario: Switch selection between 'Yes' and 'Impressive'
        When I select the "Yes" radio button
        Then I verify that radioButton "Yes" is selected
        And I verify that "Impressive" is not selected
        And I verify that "No" is not selected
        When I select the "Impressive" radio button
        Then I verify that radioButton "Impressive" is selected
        And I verify that "Yes" is not selected
        And I verify that "No" is not selected

    @radiobtn @pairwise @regression
    Scenario: Verify that only one radio button can be selected at a time
        And I select the "Yes" radio button
        Then I verify that "Impressive" is not selected
        And I verify that "No" is not selected
        When I select the "Impressive" radio button
        Then I verify that "Yes" is not selected
        And I verify that the "No" radio button is disabled

    @radiobtn @boundary @unhappy
    Scenario: Verify selection not persistence after refreshing the page
        And I select the "Yes" radio button
        And I verify that radioButton "Yes" is selected
        And I refresh the page
        Then I verify that "Yes" is not selected