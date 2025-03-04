Feature: Tests in the 'Web Tables' sub-section of 'Elements'
    Set of tests on the 'Web Tables' sub-section
    to check the stability, CRUD operations, and filtering.

    Background:
        Given I navigate to DemoQA and "Elements" Page
        When I open the "Web Tables" section

    @webtables @smoke @happy
    Scenario: Verify table loads with default data
        Then I verify the table contains the following rows
            | First Name | Last Name | Email              | Age | Salary | Department |
            | Cierra     | Vega      | cierra@example.com | 39  | 10000  | Insurance  |
            | Alden      | Cantrell  | alden@example.com  | 45  | 12000  | Compliance |
            | Kierra     | Gentry    | kierra@example.com | 29  | 2000   | Legal      |

    @webtables @crud @happy
    Scenario: Add a new entry to the table
        When I create a new entry with the following data
            | First Name | Last Name | Email              | Age | Salary | Department |
            | Ismael     | Sanromán  | ismael@example.com | 33  | 15000  | IT/QA      |
        Then I verify the table contains the following rows
            | First Name | Last Name | Email              | Age | Salary | Department |
            | Ismael     | Sanromán  | ismael@example.com | 33  | 15000  | IT/QA      |

    @webtables @crud @unhappy @TEST
    Scenario: Attempt to add an entry with missing required fields
        When I create a new entry with the following data
            | First Name | Last Name | Email | Age | Salary | Department |
            |            |           |       |     |        |            |
        Then I check that the form alerts me of unfilled fields