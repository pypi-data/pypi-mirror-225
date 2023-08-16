@tag_name_1 @tag_name_n < optional >
Feature: < descriptive title >

  As a < user >
  I want to < do something | need something >
  So that < I can achieve something >
 
  Contributes to: < name of the artefact|rule to which the value is
contributed >

  Description (optional): < further optional description to understand
the rule, no format defined, the example artefact is only a placeholder >

  Background:
    Given < what is given for all scenarios in this feature file >

  Rule: < points to a specific rule which is valid for the next set of scenarios until the next rule is given >  

  Scenario: < descriptive scenario title >
    Given < precondition >
    When < action >
    Then < expected result >