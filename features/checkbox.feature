Feature: Tests in the 'Check Box' sub-section of 'Elements'
  Set of tests on the 'Check Box' sub-section
  to check the stability and correctness of that section.

  Background:
    Given I navigate to DemoQA and "Elements" Page
    When I open the "Check Box" section

  @checkbox @smoke @happy
  Scenario: Select a single file
    And I select the checkbox for "Notes"
    Then I verify that labels are selected
      | label |
      | Notes |

  @checkbox @boundary @unhappy
  Scenario: Select and deselect a single file
    And I select the checkbox for "Commands"
    And I verify that labels are selected
      | label    |
      | Commands |
    And I deselect the checkbox for "Commands"
    Then I verify that labels are not selected
      | label    |
      | Commands |

  @checkbox @boundary @happy
  Scenario: Select a parent folder and check all children are selected
    And I select the checkbox for "Desktop"
    Then I verify that labels are selected
      | label    |
      | Notes    |
      | Commands |
