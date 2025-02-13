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

  @checkbox @boundary @unhappy
  Scenario: Deselect a parent folder and check all children are deselected
    And I select the checkbox for "Documents"
    And I deselect the checkbox for "Documents"
    Then I verify that labels are not selected
      | label     |
      | WorkSpace |
      | Office    |

  @checkbox @pairwise @happy
  Scenario: Select and verify mixed selection state
    And I select the checkbox for "WorkSpace"
    And I deselect the checkbox for "Angular"
    Then I verify that labels are selected
      | label |
      | Veu   |
      | React |
    And I verify that labels are not selected
      | label   |
      | Angular |

  @checkbox @decision_table @unhappy
  Scenario Outline: Select invalid options
    And I select the checkbox for "<invalid_item>"
    Then I verify that labels are not selected
      | label          |
      | <invalid_item> |

    Examples:
      | invalid_item |
      | UnknownFile  |
      | /root        |
      | 1234         |

  @checkbox @state_machine @happy
  Scenario: Navigate through folders and select an item
    And I expand "Documents" section
    And I expand "Office" section
    And I select the checkbox for "Public"
    Then I verify that labels are selected
      | label  |
      | Public |

  @checkbox @caminos_logicos @regression @Test
  Scenario: Validate the selection persistence
    And I select the checkbox for "Downloads"
    And I refresh the page
    Then I verify that labels are not selected
      | label     |
      | Downloads |