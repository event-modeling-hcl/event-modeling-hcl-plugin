# Sample audit reports

The model covers a library that lends books.

## Full audit

- 1.1 FAIL. Fine Total Calculated is a calculation (K1 rule 3). Fix: remove the event and add a field "fine total" to the Member Account read model. Part: events, read models.
- 1.2 WARN. Loan Maybe Overdue states a possibility (K1 rule 36). Fix: name the fact, Loan Became Overdue. Part: events.
- 1.3 PASS. No event records a click or a message.
- 1.4 PASS. Book Lent appears on two screens and is one event.
- 2.1 PASS. Book Lent and Book Returned belong to the loan stream only.
- 2.2 PASS. The loan lifecycle starts with Lend Book and ends in Returned or Lost.
- 2.3 PASS. No refusal is recorded as an event.
- 3.1 FAIL. Lend Book has two issuers: the Front Desk screen and the Auto Renewal automation (K1 rule 16). Fix: keep the screen as the issuer and give the automation its own command, Renew Loan. Part: commands.
- 3.2 PASS. Every command names Librarian, Member, or Renewal Robot.
- 3.3 PASS. Lend Book produces Book Lent or rejects when the member has three open loans.
- 3.4 PASS. No command only loads data.
- 3.5 PASS. Lend Book decides from the earlier events of the loan stream.
- 4.1 PASS. Each read model serves one screen.
- 4.2 PASS. No read model names machinery.
- 5.1 PASS. Each slice holds one element.
- 5.2 PASS. Each flow starts with a screen or with an automation.
- 5.3 PASS. The story reads from lending to return.
- 5.4 WARN. No path exists for a lost book after the member pays. Fix: add a compensation path. Part: lifecycles.
- 6.1 WARN. The Return Desk read model takes five events. Under K4 it answers two questions: open loans and fines. Fix: one read model for each question. Part: read models.

Final question 1: yes. The story reads from lending to return in one chapter.
Final question 2: yes. The fine rate lives in a read model.

Verdict: FAIL, because audits 1.1 and 3.1 failed.

## Partial audit on a model with only events

This run is partial. Only the audits on events ran.

- 1.1 PASS. Each event is a captured fact.
- 1.2 WARN. Loan Maybe Overdue states a possibility (K1 rule 36). Fix: name the fact, Loan Became Overdue. Part: events.
- 1.3 PASS. No event records a click or a message.
- 1.4 PASS. No two events mean the same thing.
- 2.1 to 2.3 NOT RUN. The model has no streams and no lifecycles.
- 3.1 to 3.5 NOT RUN. The model has no commands.
- 4.1 to 4.2 NOT RUN. The model has no read models.
- 5.1 to 5.4 NOT RUN. The model has no slices.
- 6.1 NOT RUN. The model has no screens, commands, or read models.

Final question 1: not asked. Final question 2: not asked.

Verdict for audits 1.1 to 1.4: PASS WITH WARNINGS.

## In an .em.hcl model

First run `emhcl validate --profile strict library.em.hcl` and copy its lines unchanged. The lines below only sketch the content. The real form comes from the tool:

```text
Validator
library.em.hcl:41:3: warning EM402: command lend_book has more than one event
library.em.hcl:88:1: error EM406: hotspot fine_rate is open
```

Then the audits. Audit 5.1 reads "covered by the validator". Audit 6.1 judges the EM402 signal: "Lend Book records Book Lent and Loan Limit Reached. Both always happen together when the third loan starts, so the domain explains the count. No finding." The open hotspot is a validator error, so the verdict is FAIL.
