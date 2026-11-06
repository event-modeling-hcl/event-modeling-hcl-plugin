# Worked example: a bike-sharing tender

The source is a 60-page tender from a city. The perspective is the bidder. The source does not say this, so the certainty is assumed.

## Part of the ledger table in the reply

| Id | Kind | Statement | Location | Certainty | Record |
| --- | --- | --- | --- | --- | --- |
| F01 | actor | City transport office issues the tender | tender.pdf, section 1.1, page 2 | stated | request concerning roles |
| F02 | event | Tender published | tender.pdf, section 1.3, page 2 | stated | evidence on the event Tender Published |
| F03 | deadline | Offers close on 30 April at 12:00 | tender.pdf, section 2.4, page 5 | stated | request concerning automations |
| F04 | rule | An offer after the closing time is not considered | tender.pdf, section 2.4, page 5 | stated | request concerning command scenarios |
| F05 | rule | Fleet of at least 400 bikes in year one | tender.pdf, section 4.2, page 18 | stated | request concerning command scenarios |
| F07 | unknown | Offer validity period not given | tender.pdf, section 2 | stated | open question |
| F08 | unknown | Start of service is 1 June on page 3 and 1 July on page 41 | tender.pdf, pages 3 and 41 | stated | open question |
| F09 | data | General legal terms | tender.pdf, section 9 | stated | left out: boilerplate |
| F10 | process | Lot 2, cargo bikes | tender.pdf, section 7 | stated | left out: out of focus, the person asked for lot 1 only |

F08 names both locations. The skill does not choose one date.

## Scenario requests from the rules

- F04: an offer before 30 April 12:00 passes. An offer after that time is refused with "the offer period is over".
- F05: an offer with 400 bikes passes. An offer with 399 bikes is refused.

## In an .em.hcl model

```hcl
evidence_source "tender_pdf" {
  kind     = "document"
  location = "tender.pdf"
}

evidence "tender_published_f02" {
  certainty = "stated"
  source    = evidence_source.tender_pdf
  location  = "section 1.3, page 2"
  on        = event.tendering.tender_published
}

hotspot "fleet_size_rule" {
  kind     = "request"
  concerns = "scenario"
  question = "Can Hand In Offer get two scenarios: 400 bikes passes, 399 bikes is refused (tender.pdf, section 4.2, page 18)?"
  on       = command.hand_in_offer.hand_in_offer
}

hotspot "start_of_service" {
  question = "Service starts on 1 June (page 3) or on 1 July (page 41). Which date applies?"
  options  = ["1 June", "1 July", "Leave it"]
}

decision "legal_terms_left_out" {
  statement = "tender.pdf, section 9, general legal terms stay out of the model."
  reason    = "boilerplate with no business decision"
}
```
