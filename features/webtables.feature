Feature: Tests in the 'Web Tables' sub-section of 'Elements'
    Set of tests on the 'Web Tables' sub-section
    to check the stability, CRUD operations, and filtering.

    Background:
        Given I navigate to DemoQA and "Elements" Page
        When I open the "Web Tables" section

    @webtables @smoke @happy
    Scenario: Verify table loads with default data
        Then I verify the table contains the following rows
            | First Name | Last Name | Age | Email              | Salary | Department |
            | Cierra     | Vega      | 39  | cierra@example.com | 10000  | Insurance  |
            | Alden      | Cantrell  | 45  | alden@example.com  | 12000  | Compliance |
            | Kierra     | Gentry    | 29  | kierra@example.com | 2000   | Legal      |