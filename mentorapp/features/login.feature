Feature: User Login

    Scenario: Successful Login
    Given the login page is displayed
    When the user enters valid credentials 
    Then the user should be redirected to the dashboard
